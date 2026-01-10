# testing for supabase
import os

from typing import Final
from supabase import create_client, Client, PostgrestAPIError
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
url: Final[str] = os.getenv('SUPABASE_URL')
pub_key: Final[str] = os.getenv('SUPABASE_PUBLISHABLE_KEY')
supabase: Client = create_client(url, pub_key)

class DuplicateNameException(Exception):
    pass

class BadDateTimeException(Exception):
    pass


def show_tasks():
    response = supabase.table('tasks').select("*").execute()
    tasks = response.data
    return tasks

def insert_task(user_input, timestamp):
    data = (user_input.split(" ", 1)[1]).split("|")
    print(data)
    if len(data) == 1:
        data.append(None)
    payload = {
        "name" : data[0],
        "creation_date" : str(timestamp),
        "due_date" : normalize_time(data[1]),
        "complete" : False,
    }
    print(payload)
    try:
        supabase.table('tasks').insert(payload).execute()
    except Exception as e:
        error_dict = e.__dict__
        error_code = int(error_dict['code'])
        print(e)
        if error_code == 23505:
            raise DuplicateNameException
        elif error_code == 22008:
            raise BadDateTimeException

    return

def normalize_time(time):
    if time == None:
        return None
    else: 
        try:
            time = str(datetime.strptime(time.strip(), "%d-%m-%Y %H:%M"))
        except:
            time == None
        return time

