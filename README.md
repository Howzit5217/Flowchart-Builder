# Flowchart Builder

Paste textbook-style pseudocode, get a flowchart. Color it in, then save it
as an SVG or a PNG.

This folder is the whole website. It is three files and no server: the page,
the Python that draws the charts, and this readme. The page loads Python
into your browser (Pyodide) and imports `flowchart_builder.py`, so the same
code that runs on a computer runs in the browser, and nothing you type is
sent anywhere.

## Putting it online with GitHub Pages

1. Make a repository on GitHub -- the free kind is fine.
2. Put these files in it. Either drag them onto the web page GitHub shows
   for an empty repository, or, in this folder:

       git init
       git add .
       git commit -m "Flowchart builder"
       git branch -M main
       git remote add origin https://github.com/<you>/<repo>.git
       git push -u origin main

3. On GitHub: **Settings -> Pages**. Under *Build and deployment*, set
   *Source* to **Deploy from a branch**, pick branch **main** and folder
   **/ (root)**, and press Save.
4. Wait a minute, then open `https://<you>.github.io/<repo>/`.

If you keep the files in a `docs/` folder inside a bigger repository, pick
**/docs** as the folder in step 3 instead.

Any other static host works the same way -- Netlify, Cloudflare Pages,
GitLab Pages, or a folder on a school web server. There is nothing to
install and nothing to run.

## Running it on your own computer

    python "Flowchart Builder.py"

opens the same studio, served from your machine. Give it a file instead and
it writes the .svg and .html straight out:

    python "Flowchart Builder.py" mycode.txt -t "My chart"

`--help` lists the rest: the shape to aim at, the language, the seed, and so
on.
