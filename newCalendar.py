from CNF import to_cnf
from toCalendar import to_calendar

import sys
import os

os.system('make rs -C ./glucose-syrup-4.1/simp')
tname = to_cnf(sys.argv[1])
print(tname)
os.system(f'./glucose-syrup-4.1/simp/glucose_static SAT_{tname}.txt SOL_{tname}.txt')
to_calendar(sys.argv[1], f'SOL_{tname}.txt')
