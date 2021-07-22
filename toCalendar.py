from icalendar import Calendar, Event
from datetime import datetime, timedelta
import sys
import json

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

class MatchFacts:

    def __init__(self, date, time=None):
        self.date = date
        self.time = time

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

def n_to_triple(number, coef, teams, fterm):
    if number % coef == 0:
        local = (number // coef) - 1
        return local, teams - 1, fterm
    else:
        local = number // coef
        rest = number % coef
        if rest % fterm == 0:
            visitor = (rest // fterm) - 1
            return local, visitor, fterm
        else:
            visitor = rest // fterm
            return local, visitor, rest % fterm

def get_info_from_number(number, schedule):
    global teams
    global days
    global daily_games
    global coef1
    global coef2
    global max_d2n

    if number <= max_d2n:
        local, visitor, matchday = n_to_triple(number, coef1, teams, days)
        if local == visitor:
            return
        schedule[(local, visitor)] = MatchFacts(matchday)
    else:
        local, visitor, time = n_to_triple(number - max_d2n, coef2, teams, daily_games)
        if local == visitor:
            return
        schedule[(local, visitor)].time = time



def generate_icalendar(sat_solution, data):

    global teams
    global days
    global daily_games
    global coef1
    global coef2
    global max_d2n

    teams = len(data['participants'])
    start = datetime.strptime(data['start_date'], '%Y-%m-%d')
    end = datetime.strptime(data['end_date'], '%Y-%m-%d')
    delta = end - start
    days = delta.days
    first_hour = datetime.strptime(round_up(data['start_time']), '%H:%M')
    last_hour = datetime.strptime(round_down(data['end_time']), '%H:%M')
    delta = last_hour - first_hour
    #Esta línea depende de si end_time es la última hora a la que puede empezar un partido o terminar
    daily_games = ((delta.seconds // 3600)) // 2

    #Pre-calculations

    #print(teams - 1)
    #print(days)
    coef1 = (teams - 1) * days + days
    max_d2n = day_to_n(teams - 1, teams - 1, days)
    coef2 = (teams - 1) * daily_games + daily_games

    schedule = {}

    with open(sat_solution, 'r') as solution:

        for line in solution:

            variables = line.split(" ")

            for var in variables:

                if var[0] == "0":
                    break

                if var[0] != "-":
                    get_info_from_number(int(var), schedule)

        solution.close()

    cal = Calendar()

    assert(len(schedule) == teams * (teams - 1))
    for match in schedule:

        """print("SCHEDULED MATCH")
        print(data['participants'][match[0]])
        print(data['participants'][match[1]])
        print(schedule[match].date)
        print(schedule[match].time)
        print("\n")"""


        event = Event()
        local = data['participants'][match[0]]
        visitor = data['participants'][match[1]]
        matchdate = start + timedelta(days=schedule[match].date - 1)
        matchtime = first_hour + timedelta(hours=(schedule[match].time - 1)*2)
        matchend = matchtime + timedelta(hours=2)
        event['dtstart'] = matchdate.strftime('%Y%m%dT') + matchtime.strftime('%H%M00Z')
        event['dtend'] = matchdate.strftime('%Y%m%dT') + matchend.strftime('%H%M00Z')
        event['summary'] = f'{local} (H) vs {visitor} (A)'
        cal.add_component(event)
        
        #print(event)
        #print("\n")

    name = data['tournament_name']
    with open(f'{name}.ics', 'wb') as tournament_calendar:
        tournament_calendar.write(cal.to_ical())
        tournament_calendar.close()


def to_calendar(file_name, sat_solution):

    with open(file_name, 'r') as datafile:

        data = json.load(datafile)

        datafile.close()

    data['start_time'] = round_up(data['start_time'])
    data['end_time'] = round_down(data['end_time'])

    generate_icalendar(sat_solution, data)

if __name__ == "__main__":
    to_calendar(sys.argv[1], sys.argv[2])

