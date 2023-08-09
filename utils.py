import datetime
from pathlib import Path


def check_today_date_in_file(file_path):
    
    today_date = datetime.datetime.now().date()

    with open(file_path, 'r') as file:
        dates_list = [line.strip() for line in file]

    if str(today_date) in dates_list:
        return True
    
    else:
        return False
    

def write_dates_to_file(date, file_path):
    with open(file_path, 'w') as file:
        date_str = date.strftime('%Y-%m-%d')
        file.write(date_str + '\n')


def create_empty_text_file(file_path):
    path = Path(file_path)
    path.touch()
