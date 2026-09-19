"""Everything it says, in each language it says it in.

Reading this reads every language, which is how they come to be in the
table: each one registers itself at the foot of its own file.  A language
left out of this line is a language nothing ever reads.
"""
from . import lookup                                     # noqa: F401
from . import de, en, es, fr                             # noqa: F401
