from datetime import datetime

import json
import sys
import time

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
    global coef1
    global days
    return coef1 * local + days * visitor + matchday

def time_to_n(local, visitor, time):
    global coef2
    global daily_games
    global max_d2n
    return coef2 * local + daily_games * visitor + time + max_d2n


""" t: equipos
    d: días
    h: horas
"""

#This is completely wrong, fix later
def number_of_clauses_v1(t, d, h):
    global teams
    global days
    global daily_games
    matches = teams * (teams -1)

    clauses = [
        2 * matches,
        ((days * (days - 1) + daily_games * (daily_games - 1))//2) * matches,
        (matches * (matches - 1) // 2) * days * daily_games,
        (matches//2) * days * (4*(teams - 2) + 1),
        2* matches * (teams - 2) * (days - 1)
    ]

    print(clauses)

    return sum(clauses)

def at_least_once(cnf_file):
    global teams
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

    assert(counter == (2 * teams * (teams - 1)))

def at_most_once(cnf_file):
    global teams
    global days
    global daily_games
    counter = 0
    for i,j in all_matches:
        for k1 in range(1, days + 1):
            for k2 in range(k1 + 1, days + 1):
                current_clause = [str(-1 * day_to_n(i, j, k1)), str(-1 * day_to_n(i, j, k2)), '0']
                cnf_file.write(" ".join(current_clause) + newline)
                counter += 1

        for m1 in range(1, daily_games + 1):
            for m2 in range(m1 + 1, daily_games + 1):
                current_clause = [str(-1 * time_to_n(i, j, m1)), str(-1 * time_to_n(i, j, m2)), '0']
                cnf_file.write(" ".join(current_clause) + newline)
                counter += 1

    correct_total_clauses = ((days * (days - 1) + daily_games * (daily_games - 1))//2) * (teams * (teams - 1))
    assert(counter == correct_total_clauses)

def no_simultaneous_match(cnf_file):
    global teams
    global days
    global daily_games
    counter = 0
    current_match = 0
    dates = []

    for k in range(1, days + 1):
        for m in range(1, daily_games + 1):
            dates.append((k, m))

    for i,j in all_matches:
        for a,b in all_matches[(current_match+1):]:
            for k, m in dates:
                c_vars = [day_to_n(i, j, k), day_to_n(a, b, k), time_to_n(i, j, m), time_to_n(a, b, m)]
                current_clause = list(map(str, map(lambda x: -1 * x, c_vars))) + ['0']
                cnf_file.write(" ".join(current_clause) + newline)
                counter += 1

        current_match += 1

    matches = teams * (teams -1)
    correct_total_clauses = (matches * (matches - 1) // 2) * days * daily_games
    assert(counter == correct_total_clauses)

def one_match_per_team_per_day(cnf_file):
    global teams
    global days
    global daily_games
    counter = 0
    

    for i in range(teams):
        for j in range(teams):
            if i == j:
                continue
            for k in range(j + 1, teams):
                if k == i:
                    continue
                for m in range(1, days + 1):
                    current_clause = [str(-1 * day_to_n(i, j, m)), str(-1 * day_to_n(i, k, m)), '0']
                    cnf_file.write(" ".join(current_clause) + newline)
                    counter += 1

                    current_clause = [str(-1 * day_to_n(i, j, m)), str(-1 * day_to_n(k, i, m)), '0']
                    cnf_file.write(" ".join(current_clause) + newline)
                    counter += 1

                    current_clause = [str(-1 * day_to_n(j, i, m)), str(-1 * day_to_n(i, k, m)), '0']
                    cnf_file.write(" ".join(current_clause) + newline)
                    counter += 1

                    current_clause = [str(-1 * day_to_n(j, i, m)), str(-1 * day_to_n(k, i, m)), '0']
                    cnf_file.write(" ".join(current_clause) + newline)
                    counter += 1

        for j in range(i + 1, teams):
            for m in range(1, days + 1):
                current_clause = [str(-1 * day_to_n(i, j, m)), str(-1 * day_to_n(j, i, m)), '0']
                cnf_file.write(" ".join(current_clause) + newline)
                counter += 1

    matches = teams * (teams - 1)
    correct_total_clauses = (matches//2) * days * (4*(teams - 2) + 1)
    assert(counter == correct_total_clauses)

def consecutive_days(cnf_file):
    global teams
    global days
    global daily_games
    counter = 0
    print("HEY OH HEY OH")
    print(teams)
    print(days)
    print(daily_games)

    for i in range(teams):
        for j in range(teams):
            if i == j:
                continue
            for k in range(j + 1, teams):
                if k == i:
                    continue
                for m in range(1, days):
                    current_clause = [str(-1 *  day_to_n(i, j, m)), str(-1 * day_to_n(i, k, m + 1)), "0"]
                    cnf_file.write(" ".join(current_clause) + newline)
                    counter += 1

                    current_clause = [str(-1 *  day_to_n(i, k, m)), str(-1 * day_to_n(i, j, m + 1)), "0"]
                    cnf_file.write(" ".join(current_clause) + newline)
                    counter += 1

                    current_clause = [str(-1 *  day_to_n(j, i, m)), str(-1 * day_to_n(k, i, m + 1)), "0"]
                    cnf_file.write(" ".join(current_clause) + newline)
                    counter += 1

                    current_clause = [str(-1 *  day_to_n(k, i, m)), str(-1 * day_to_n(j, i, m + 1)), "0"]
                    cnf_file.write(" ".join(current_clause) + newline)
                    counter += 1

    correct_total_clauses = 2 * teams * (teams - 1) * (teams - 2) * (days - 1)
    assert(counter == correct_total_clauses)


def generate_cnf_file_v1(data):
    global teams
    global days
    global daily_games
    global coef1
    global coef2
    global max_d2n
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
    daily_games = ((delta.seconds // 3600) - 1) // 2
    print("Max. games in a day: " + str(daily_games))

    #Pre-calculations
    time1 = time.process_time()
    expected_clauses = number_of_clauses_v1(teams, days, daily_games)

    coef1 = (teams - 1) * days + days
    print(coef1)
    max_d2n = day_to_n(teams - 1, teams - 1, days)
    coef2 = (teams - 1) * daily_games + daily_games

    expected_var = time_to_n(teams - 1, teams - 2, daily_games)

    for i in range(teams):
        for j in range(teams):
            if i == j:
                continue

            all_matches.append((i, j))

    time2 = time.process_time()

    tname = data['tournament_name']
    with open(f'SAT_{tname}.txt', 'w') as cnf_file:
        cnf_file.write('p cnf ' + str(expected_var) + " " + str(expected_clauses) + newline)
        print("Writing file")
        time3 = time.process_time()
        at_least_once(cnf_file)
        time4 = time.process_time()
        print("Finished the at least one of each match restriction set")
        time5 = time.process_time()
        at_most_once(cnf_file)
        time6 = time.process_time()
        print("Finished the at most one of each match restriction set")
        time7 = time.process_time()
        no_simultaneous_match(cnf_file)
        time8 = time.process_time()
        print("Finished the no simultaneous match restriction set")
        time9 = time.process_time()
        one_match_per_team_per_day(cnf_file)
        time10 = time.process_time()
        print("Finished the one match per team per day restriction set")
        time11 = time.process_time()
        consecutive_days(cnf_file)
        time12 = time.process_time()
        print("Finished consecutive days restriction set")
        print("Finished writing")

        cnf_file.close()

    #time report section
    if (len(sys.argv) > 2 and sys.argv[2] == "-a"):
        with open('redResults.csv', 'a') as reduction:
            reduction.write(f'{time2 - time1},{time4 - time3},{time6 - time5},{time8 - time7},{time10 - time9},{time12 - time11}, {time12 - time1}' + newline)
            reduction.close()
    
    return tname




def to_cnf(file_name):

    with open(file_name, 'r') as datafile:

        data = json.load(datafile)

        datafile.close()

    return generate_cnf_file_v1(data)

if __name__ == "__main__":
    to_cnf(sys.argv[1])