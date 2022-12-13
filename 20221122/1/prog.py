import sys

buf = sys.stdin.buffer.read()
count = buf[:1]
buf = buf[1:]

ans = []
for i in range(count[0]):
    list = buf[i*len(buf)//count[0]:(i+1)*len(buf)//count[0]]
    if list:
        ans.append(list)


sys.stdout.buffer.write(count + b"".join(sorted(ans)))
