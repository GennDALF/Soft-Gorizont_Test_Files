
import locale
from time import sleep
from os.path import getmtime, isfile
from csv import reader as csv_read, writer as csv_write
from datetime import datetime as dt

locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')
# refresh once in 10 seconds: feel free to edit
CHECK_INPUT_RATE = 10


# this reads from input files and writes output
def update_files():
    input_data = []
    for i in range(1, 6):
        with open(f'in\\{str(i)}.csv', encoding='utf-8', newline='') as f_in:
            for row in csv_read(f_in):
                row.insert(0, companies[i])
                input_data.append(row)
    # generating output data
    output_data = {1: [], 2: [], 3: []}
    for line in input_data:
        if 'производитель 1' in line:
            output_data[1].append(line[:3] + line[4:])
        elif 'производитель 3' in line:
            output_data[2].append(line[:3] + line[4:])
        if 'яблоки' in line:
            output_data[3].append(line[:1] + line[2:])
    for i in range(1, 4):
        with open(f'out\\{str(i)}.csv', 'w', encoding='utf-8', newline='') as f_out:
            csv_write(f_out).writerows(output_data[i])
    return None


# our retailers: feel free to edit strings
companies = {1: 'фирма 1',
             2: 'фирма 2',
             3: 'фирма 3',
             4: 'фирма 4',
             5: 'фирма 5'}
try:
    # checks if directory '.\in' exists
    #   and notes time of directory last modification
    last_mod = getmtime('.\\in')
    # initial run
    update_files()
    print(dt.now().strftime('%X %x') + " – Выходные файлы обновлены")
    # as not having a task to set up any interface,
    #   we'll keep main loop stupid but simple
    while True:
        # checks if input files (still) exist
        if all([isfile(f'.\\in\\{str(i)}.csv') for i in range(1, 6)]):
            # writes to list all files' last modification time
            mod_times = [getmtime(f'.\\in\\{str(i)}.csv') for i in range(1, 6)]
            # if just one time from that list differ from last_mod
            #   then update all
            if any([time - last_mod > 0 for time in mod_times]):
                last_mod = max(mod_times)
                update_files()
                print(dt.now().strftime('%X %x') + " – Выходные файлы обновлены")
        else:
            print("Где мои входные файлы?")
            break
        sleep(CHECK_INPUT_RATE)

except OSError:
    print("Где моя входная директория?")
