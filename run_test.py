import subprocess
import csv

def read_output():
    with open('test.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        s = 0
        for row in csv_reader:
            s = s + float(row[1])
        return s/3


def run(flags):
    try:
        subprocess.run(['./test.sh', flags])
        return read_output()
    except:
        return 0
