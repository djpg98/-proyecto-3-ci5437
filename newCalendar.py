from CNF import to_cnf
from toCalendar import to_calendar

import sys
import os
import time

newline = '\n'

os.system('make rs -C ./glucose-syrup-4.1/simp')
tname = to_cnf(sys.argv[1])
if (len(sys.argv) > 2 and sys.argv[2] == '-a'):
    result = os.system(f'timeout 10m ./glucose-syrup-4.1/simp/glucose_static SAT_{tname}.txt SOL_{tname}.txt > SATInfo.txt')
    if os.WIFEXITED(result):
        if os.WEXITSTATUS(result) == 124:
            with open('solverResults.csv', 'a') as solverResults:
                solverResults.write(f'TIMEOUT,-1,-1,600' + newline)
                solverResults.close()
            with open('calResults.csv', 'a') as calResults:
                calResults.write(f'-1' + newline)
                calResults.close()
            
            sys.exit()  


    solverstatus = 'SAT'
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
            if ('unsat' in line) or ('UNSAT' in line):
                solverstatus = 'UNSAT'

        info.close()

    with open('solverResults.csv', 'a') as solverResults:
        solverResults.write(f'{solverstatus},{sconflicts},{sdecisions},{stime}' + newline)
        solverResults.close()

    if solverstatus == 'SAT':
        time1 = time.process_time()
        to_calendar(sys.argv[1], f'SOL_{tname}.txt')
        time2 = time.process_time()

        with open('calResults.csv', 'a') as calResults:
            calResults.write(f'{time2 - time1}' + newline)
            calResults.close()
    else:
        with open('calResults.csv', 'a') as calResults:
            calResults.write(f'-1' + newline)
            calResults.close()      

else:
    os.system(f'./glucose-syrup-4.1/simp/glucose_static SAT_{tname}.txt SOL_{tname}.txt')
    to_calendar(sys.argv[1], f'SOL_{tname}.txt')
