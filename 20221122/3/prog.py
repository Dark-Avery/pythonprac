import sys
import struct


wav = sys.stdin.buffer.read()
if len(wav) < 44 or struct.unpack("4s", wav[8:12])[0] != b"WAVE":
    print("NO")
else:
    print(f"Size={struct.unpack('i', wav[4:8])[0]}, \
Type={struct.unpack('h', wav[20:22])[0]}, \
Channels={struct.unpack('h', wav[22:24])[0]}, \
Rate={struct.unpack('i', wav[24:28])[0]}, \
Bits={struct.unpack('h', wav[34:36])[0]}, \
Data size={struct.unpack('i', wav[40:44])[0]}")
