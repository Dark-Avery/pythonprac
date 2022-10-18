s = input().lower()
print(len({s[i:i+2]:0 for i in range(len(s)-1) if (s[i].isalpha() & s[i+1].isalpha())}))