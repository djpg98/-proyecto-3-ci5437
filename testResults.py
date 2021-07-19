import sys
import os

#Argv[1] es el nombre del directorio con los casos

newline = '\n'
rootdir = sys.argv[1]
directory = os.fsencode(rootdir)

with open('redResults.csv', 'w') as reduction:
    reduction.write("Precalc, rest. 1, rest. 2, rest. 3, rest. 4, rest. 5, total" + newline)
    reduction.close()

with open('solverResults.csv', 'w') as solver:
    solver.write('conflicts, decisions, time' + newline)
    solver.close()

with open('calResults.csv', 'w') as cal:
    cal.write('time' + newline)
    cal.close()

for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if filename.endswith('.json'):
        os.system('python3.6 newCalendar.py ' + filename + ' -a')

