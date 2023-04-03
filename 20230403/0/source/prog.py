import calendar

cal = calendar.month(2023, 4).split('\n')
output = 'Calendar\n========\n\n'
output += '+' + len(cal[2])*'-' + "+" + '\n'
output += '|' + cal[0] + (len(cal[2]) - len(cal[0])) * ' ' +  '|' + '\n'
output += '+--'*7 + '+\n'
for i in range(1, len(cal)-1):
    output += '|' + cal[i].replace(' ', '|') + '|\n'
    output += '+--'*7 + '+\n'
output = output.replace('|||', '|  ')
output = output.replace('||', '| ')
print(output)
