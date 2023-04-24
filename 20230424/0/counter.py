import gettext, os, sys

popath = os.path.join(os.path.dirname(__file__), 'po')
tranlation = gettext.translation("counter", popath, fallback=True)
_, ngettext = tranlation.gettext, tranlation.ngettext

while s := sys.stdin.readline().split():
    print(ngettext('{} word entered', '{} words entered', len(s)).format(len(s)))