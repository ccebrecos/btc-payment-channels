import argparse
import ast
from .constants import LOG_DEFAULT, LOGS


# helping methods
def evalTF(string):
    return ast.literal_eval(string.title())


# Default parser
DEFAULT_PARSER = argparse.ArgumentParser(
    # prog = 'iec.py'
    # usage = (generated by default)
    description="""<Description>""",
    epilog="<> with ♥",
    add_help=True,
    allow_abbrev=True
)
DEFAULT_PARSER.add_argument(
    "-v", "--version",
    action="version",
    version="<Program name> 0.0"
)
DEFAULT_PARSER.add_argument(
    "-l", "--log-level",
    metavar="level",
    action="store",
    help="""specifies the level of events to log. Events upper from that level
    will be displayed. Default is %s""" % (LOG_DEFAULT),
    type=str,
    choices=LOGS,
    default=LOG_DEFAULT
)
