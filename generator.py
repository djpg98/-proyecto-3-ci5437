from hashlib import new
import sys
from random import seed, randint, randrange, choice
from time import time
from datetime import date, timedelta

newline = "\n"
tournaments = [
    "Copa Kirin", "Juegos Olimpicos", "Mundial", "Mundial de LoL", "Copa Mundial Femenina"
]
participants = [
    "Afganistan", "Alemania", "Andorra", "Brasil", "Bulgaria", "Bolivia", "Canada", "Camerun", "Catar", "Dinamarca", "Dominica", "Ecuador", "Egipto", "Espanna", "Estados Unidos",
    "Filipinas", "Finlandia", "Francia", "Georgia", "Grecia", "Guyana", "Haiti", "Honduras", "Hungria", "India", "Italia", "Irlanda", "Jamaica", "Japon", "Jordania", "Kazajistan",
    "Kenia", "Kuwait", "Laos", "Libia", "Liechtenstein", "Madagascar", "Malasia", "Maldivas", "Namibia", "Nepal", "Nueva Zelanda", "Oman", "Paises Bajos", "Palestina", "Paraguay",
    "Reino Unido", "Rusia", "Rumania", "Samoa", "Santa Lucia", "Singapur", "Suiza", "Suecia", "Tonga", "Turquia", "Tuvalu", "Uganda", "Uruguay", "Vanuatu", "Venezuela", "Vietnam",
    "Yemen", "Yibuti", "Zimbabue"
]
seed(int(round(time(), 0)))

def generate(n_cases, n_participants, tight):
    
    for i in range(n_cases):
        n_matches = n_participants * (n_participants-1)
        n_hours = n_matches * 2

        hours_per_day = randint(3, 12) * 2
        start_time = randint(0, 24-hours_per_day)
        end_time = start_time + hours_per_day
        
        min_interval_dates = int(round(n_hours/hours_per_day, 0))
        if tight == 2:
            if hours_per_day > 16:
                interval_dates = min_interval_dates
            elif hours_per_day <= 16 and hours_per_day > 5:
                interval_dates = randint(min_interval_dates, min_interval_dates+1)
            elif hours_per_day <= 5:
                interval_dates = randint(min_interval_dates, min_interval_dates+2)
                
        elif tight == 1:
            if hours_per_day > 16:
                interval_dates = randint(min_interval_dates+3, min_interval_dates+8)
            elif hours_per_day <= 16 and hours_per_day > 5:
                interval_dates = randint(min_interval_dates+3, min_interval_dates+9)
            elif hours_per_day <= 5:
                interval_dates = randint(min_interval_dates+3, min_interval_dates+10)
        
        elif tight == 0:
            if hours_per_day > 16:
                interval_dates = randint(min_interval_dates+7, min_interval_dates+14)
            elif hours_per_day <= 16 and hours_per_day > 5:
                interval_dates = randint(min_interval_dates+7, min_interval_dates+16)
            elif hours_per_day <= 5:
                interval_dates = randint(min_interval_dates+7, min_interval_dates+18)
        
        tmp_start_date = date(2021, 1, 1)
        tmp_end_date = date(2025, 1, 1)
        time_between_dates = tmp_end_date - tmp_start_date
        start_date = tmp_start_date + timedelta(days=randrange(time_between_dates.days))
        end_date = start_date + timedelta(days=interval_dates-1)
            
        with open(f'CasosDePrueba/{n_participants}_case_{i}.json', 'w') as case_file:

            case_file.write("{" + newline)
            case_file.write('\t"tournament_name": "' + tournaments[randint(0, len(tournaments)-1)] + '",' + newline)
            case_file.write('\t"start_date": "' + str(start_date) + '",' + newline)
            case_file.write('\t"end_date": "' + str(end_date) + '",' + newline)
            if start_time < 10:
                case_file.write('\t"start_time": "0' + str(start_time) + ':00",' + newline)
            else:
                case_file.write('\t"start_time": "' + str(start_time) + ':00",' + newline)
            if end_time < 10:
                case_file.write('\t"end_time": "0' + str(end_time) + ':00",' + newline)
            else:
                case_file.write('\t"end_time": "' + str(end_time) + ':00",' + newline)

            case_file.write('\t"participants": [' + newline)

            tmp = participants[:]
            for i in range(n_participants):
                rnd_choice = choice(tmp)
                tmp.remove(rnd_choice)
                if (i == n_participants-1):
                    case_file.write('\t\t"' + rnd_choice + '"' + newline)
                else:
                    case_file.write('\t\t"' + rnd_choice + '",' + newline)
            
            case_file.write('\t]' + newline + '}')

            case_file.close()

try:
    # Error Handling
    if int(sys.argv[1]) <= 0:
        sys.exit(" Error: El número de casos debe ser mayor que 0")
    if int(sys.argv[2]) <= 1:
        sys.exit(" Error: El número de participantes debe ser mayor que 1")
    if int(sys.argv[3]) < 0 or int(sys.argv[3]) > 2:
        sys.exit(" Error: Solo se pueden colocar tres modalidades de ajustado: 0- Relajado, 1- Normal, 2- Ajustado")

    generate(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))
    print(f" Los archivo con los casos de prueba se han generado en la carpeta Casos de Prueba")

except IndexError:
    print(" Error: El comando para correr el archivo debe seguir la siguiente forma: generator.py <# de casos> <# de participantes>")