"""The little web server behind --serve."""
import socketserver
import webbrowser

from .. import settings
from ..page import empty_chart, to_page
from ..studio.drawing import draw_for_studio
from ..words.lookup import apply_language, word


def serve(port, text="", title=None, author=None):
    """Run the whole thing as a small website, here on this computer.

    Paste pseudocode in the panel, press the button, and the same code that
    writes the .svg draws it and hands it back.  Nothing leaves the machine:
    the server listens on localhost, and the page it serves is the same one
    that gets written beside an .svg, with the pseudocode panel added.
    """
    import http.server
    import json as _json
    import socketserver

    state = {"code": text, "title": title, "author": author, "shape": settings.SHAPE}

    class Studio(http.server.BaseHTTPRequestHandler):
        server_version = "FlowchartStudio"
        protocol_version = "HTTP/1.1"       # every reply says how long it is

        def log_message(self, *args):
            pass                                # keep the terminal quiet

        def reply(self, body, kind="text/html; charset=utf-8", code=200):
            data = body.encode("utf-8") if isinstance(body, str) else body
            self.send_response(code)
            self.send_header("Content-Type", kind)
            self.send_header("Content-Length", str(len(data)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(data)

        def do_GET(self):
            path, _, query = self.path.partition("?")
            if path not in ("/", "/index.html"):
                self.reply("Nothing here.", "text/plain; charset=utf-8", 404)
                return
            for bit in query.split("&"):        # ?lang=es, from the picker
                if bit.startswith("lang="):
                    apply_language(bit[5:])
            try:
                drawn = draw_for_studio({"text": state["code"],
                                         "title": state["title"],
                                         "author": state["author"],
                                         "shape": state["shape"], "grid": True})
                svg, seed = drawn["svg"], drawn["seed"]
                shown = drawn["title"]
                name = drawn["name"]
            except Exception:                   # an empty start is fine
                svg, seed = empty_chart(), None
                shown, name = word("flowchart"), "flowchart"
            self.reply(to_page(svg, shown, name, source=state, seed=seed))

        def do_POST(self):
            if self.path.split("?")[0] != "/build":
                self.reply("Nothing here.", "text/plain; charset=utf-8", 404)
                return
            try:
                size = int(self.headers.get("Content-Length") or 0)
                ask = _json.loads(self.rfile.read(size).decode("utf-8"))
                if ask.get("lang"):
                    apply_language(ask["lang"])
                out = draw_for_studio(ask)
                state.update(code=ask.get("text", ""), title=ask.get("title"),
                             author=ask.get("author"), shape=ask.get("shape"))
            except Exception as exc:
                out = {"ok": False, "error": str(exc) or exc.__class__.__name__}
            self.reply(_json.dumps(out), "application/json; charset=utf-8")

    # One connection at a time is not enough.  A browser keeps a spare
    # connection open that it has not sent anything on yet, in case it needs
    # it -- and a server that answers one at a time will sit on that spare
    # waiting for a request that never comes, while every real request behind
    # it fails with nothing more useful than "failed to fetch".  It shows up
    # as the thing working with a short program and breaking with a long one,
    # because the longer the drawing takes the likelier the collision, which
    # is a miserable thing to be told to debug.  A thread per connection costs
    # nothing here and the problem cannot happen.
    class Threaded(socketserver.ThreadingMixIn, http.server.HTTPServer):
        daemon_threads = True               # Ctrl+C does not wait for spares

    house = Threaded(("127.0.0.1", port), Studio)
    where = "http://127.0.0.1:%d/" % house.server_address[1]
    print(word("studio_at", url=where))
    print(word("leave_open"))
    webbrowser.open(where)
    try:
        house.serve_forever()
    except KeyboardInterrupt:
        print("\n" + word("stopped"))
    finally:
        house.server_close()
