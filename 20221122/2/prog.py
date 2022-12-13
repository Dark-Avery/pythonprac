import sys


buf = sys.stdin.buffer.read()
buf = buf.decode("UTF-8").encode("latin1",
                                 errors="replace").decode("cp1251",
                                                          errors="replace")
sys.stdout.buffer.write(buf.encode("UTF-8"))
