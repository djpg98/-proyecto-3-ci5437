from datetime import datetime

import json
import sys

"""
NO OLVIDAR:
Los números de los equipos van de 0 a teams - 1
Los número de fecha/hora van de 1 hasta fecha/hora
"""

teams = 0
days = 0
daily_games = 0
#for match/day to N function
coef1 = 0
#for match/time to N function
coef2 = 0
max_d2n = 0
all_matches = []
newline = '\n'

def round_up(stime):
    if stime[3:5] == '00':
        return stime
    else:
        return str(int(stime[0:2]) + 1) + ':00' 

def round_down(stime):
    if stime[3:5] == '00':
        return stime
    else:
        return stime[0:3] + '00'

def day_to_n(local, visitor, matchday):
    return coef1 * local + days * visitor + matchday

def time_to_n(local, visitor, time):
    return coef2 * local + daily_games * visitor + time + max_d2n


""" t: equipos
    d: días
    h: horas
"""

#This is completely wrong, fix later
def number_of_clauses_v1(t, d, h):

    factor1 = t * (t - 1)

    factor2Num = sum([
        d * (d + 1),
        h * (h + 1),
        ((t * (t - 1))-1)*(d*(d-1))*(h*(h-1)),
        5*(t-2),
        1
    ])

    factor2 = 2 + factor2Num//2

    return factor1 * factor2

def at_least_once(cnf_file):
    counter = 0
    for i,j in all_matches:
        clause_days = []
        for k in range(1, days + 1):
            clause_days.append(str(day_to_n(i, j, k)))

        clause_days.append("0")
        cnf_file.write(" ".join(clause_days) + newline)
        counter += 1

        clause_hours = []
        for m in range(1, daily_games + 1):
            clause_hours.append(str(time_to_n(i, j, m)))

        clause_hours.append("0")
        cnf_file.write(" ".join(clause_hours) + newline)
        counter += 1

    assert(counter == 2 * teams * (teams - 1))

def at_most_once(cnf_file):
    counter = 0
    for i,j in all_matches:
        for k1 in range(1, days + 1):
            for k2 in range(k1 + 1, days + 1):
                current_clause = [str(-1 * day_to_n(i, j, k1)), str(-1 * day_to_n(i, j, k2)), '0']
                cnf_file.write(" ".join(current_clause) + newline)
                counter += 1

        for m1 in range(1, daily_games + 1):
            for m2 in range(m1 + 1, days + 1):
                current_clause = [str(-1 * time_to_n(i, j, m11)), str(-1 * time_to_n(i, j, m2)), '0']
                cnf_file.write(" ".join(current_clause) + newline)
                counter += 1

    correct_total_clauses = ((days * (days - 1) + daily_games * (daily_games - 1))//2) * (teams * (teams - 1))
    assert(counter == correct_total_clauses)

def no_simultaneous_match(cnf_file):
    counter = 0
    current_match = 0
    for i,j in all_matches:
        for a,b in all_matches[current_match+1:]
            for k in range(1, days + 1):
                for m in range(1, daily_games + 1):
                    c_vars = [day_to_n(i, j, k), day_to_n(a, b, k), time_to_n(i, j, m), time_to_n(a, b, m)]
                    current_clause = list(map(str, map(lambda x: -1 * x, c_vars))) + ['0']
                    cnf_file.write(" ".join(current_clause) + newline)
                    counter += 1

        current_match += 1

    matches = teams * (teams -1)
    correct_total_clauses = (matches * (matches - 1) // 2) * days * daily_games

    assert(counter == correct_total_clauses)

def one_match_per_team_per_day(cnf_file):
    counter = 0
    for i in range(teams):
        for j in range(i + 1, teams):
            for k in range(j + 1, teams):
                for m in range(1, days + 1):
                    current_clause = [str(-1 * day_to_n(i, j, m)), str(-1 * day_to_n(i, k, m)), '0']
                    cnf_file.write(" ".join(current_clause) + newline)
                    counter += 1

                    second_clause = [str(-1 * day_to_n(i, j, m)), str(-1 * day_to_n(k, i, m)), '0']
                    cnf_file.write(" ".join(current_clause) + newline)
                    counter += 1

                    third_clause = [str(-1 * day_to_n(j, i, m)), str(-1 * day_to_n(k, i, m)), '0']
                    cnf_file.write(" ".join(current_clause) + newline)
                    counter += 1

            for m in range(1, days + 1):
                current_clause = [str(-1 * day_to_n(i, j, m)), str(-1 * day_to_n(j, i, m)), '0']
                cnf_file.write(" ".join(current_clause) + newline)
                counter += 1

    

            


def generate_cnf_file_v1(data):

    teams = len(data['participants'])
    print("Number of teams: " + str(teams))
    start = datetime.strptime(data['start_date'], '%Y-%m-%d')
    end = datetime.strptime(data['end_date'], '%Y-%m-%d')
    delta = end - start
    days = delta.days
    print("Number of days: " + str(days))
    first_hour = datetime.strptime(round_up(data['start_time']), '%H:%M')
    last_hour = datetime.strptime(round_down(data['end_time']), '%H:%M')
    delta = last_hour - first_hour
    #Esta línea depende de si end_time es la última hora a la que puede empezar un partido o terminar
    daily_games = (delta.seconds // 3600) - 1
    print("Max. games in a day: " + str(daily_games))

    #Pre-calculations
    expected_clauses = number_of_clauses_v1(teams, days, daily_games)
    expected_var = teams * (teams - 1) * (days + daily_games)

    coef1 = (teams - 1) * days + days
    max_d2n = day_to_n(teams - 1, teams - 1, days)
    coef2 = (teams - 1) * daily_games + daily_games

    for i in range(teams):
        for j in range(teams):
            if i == j:
                break

            all_matches.append((i, j))
    
    with open('prueba.txt', 'w') as cnf_file:
        print("Writing file")
        at_least_once(cnf_file)
        print("Finished the at least one of each match restriction set")
        at_most_once(cnf_file)
        print("Finished the at most one of each match restriction set")
        no_simultaneous_match(cnf_file)
        print("Finished the no simultaneous match restriction set")



def to_cnf(file_name):

    with open(file_name, 'r') as datafile:

        data = json.load(datafile)

        datafile.close()

    generate_cnf_file_v1(data)

to_cnf(sys.argv[1])