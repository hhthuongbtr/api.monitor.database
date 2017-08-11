import os, sys
import time

#mysql -u root -p -e "show engine innodb status\G;" | grep 10.0.200.30 > dl.txt 
def read_file(file_path):
    f = open(file_path, 'r')
    lines=f.read()
    f.close()
    return lines

def get_process_id(str):
    process_id = str[str.find('id')+3 : str.find(',')]
    return process_id

def kill_death_clock(process_id):
    cmd = """ mysql -uroot -p'password' -h localhost -e 'kill %s;' """%(process_id)
    os.system(cmd)

if __name__ == '__main__':
# Check if file provied as argument and exists
    if len(sys.argv) != 2:
        print("One file should be provided as argument")
        sys.exit(1)
    file_path = sys.argv[1]

    input_string = read_file(file_path)
    for line in input_string.split('\n'):
        process_id = get_process_id(line)
        if process_id.isdigit():
            kill_death_clock(process_id)
