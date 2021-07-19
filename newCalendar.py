from CNF import to_cnf
from toCalendar import to_calendar

import sys
import os
import time

newline = '\n'

os.system('make rs -C ./glucose-syrup-4.1/simp')
tname = to_cnf(sys.argv[1])
if (len(sys.argv) > 2 and sys.argv[2] == '-a'):
    os.system(f'./glucose-syrup-4.1/simp/glucose_static SAT_{tname}.txt SOL_{tname}.txt > SATInfo.txt')
    with open('SATInfo.txt', 'r') as info:
        for line in info:
            if line.startswith('c conflicts'):
                sconflicts = line.split()[3]
                continue
            if line.startswith('c decisions'):
                sdecisions = line.split()[3]
                continue
            if line.startswith('c CPU time'):
                stime = line.split()[4]

        info.close()

    with open('solverResults.csv', 'a') as solverResults:
        solverResults.write(f'{sconflicts},{sdecisions},{stime}' + newline)
        solverResults.close()

    time1 = time.process_time()
    to_calendar(sys.argv[1], f'SOL_{tname}.txt')
    time2 = time.process_time()

    with open('calResults.csv', 'a') as calResults:
        calResults.write(f'{time2 - time1}' + newline)
        calResults.close()

else:
    os.system(f'./glucose-syrup-4.1/simp/glucose_static SAT_{tname}.txt SOL_{tname}.txt')
    to_calendar(sys.argv[1], f'SOL_{tname}.txt')
