import shlex
import sys
from pyreadline3 import Readline


print(shlex.join(shlex.split(sys.argv[1])))