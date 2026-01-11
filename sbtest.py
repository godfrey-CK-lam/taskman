# testing for supabase
import os

from typing import Final
from supabase import create_client, Client
from datetime import datetime
from dotenv import load_dotenv


load_dotenv()
url: Final[str] = os.getenv("SUPABASE_URL")
pub_key: Final[str] = os.getenv("SUPABASE_PUBLISHABLE_KEY")
supabase: Client = create_client(url, pub_key)


class DuplicateNameException(Exception):
    pass

def show_tasks():
    response = supabase.table("tasks").select("*").order("due_date").execute()
    tasks = response.data
    return tasks

def insert_task(task_info, timestamp):
  
    print("inserting task with values: " + str(task_info) + " timestamp: " + str(timestamp))

    payload = {
        "name": task_info[0],
        "creation_date": str(timestamp),
        "due_date": task_info[1],
        "complete": False,
    }
    print(payload)
    try:
        supabase.table("tasks").insert(payload).execute()
    except Exception as e:
        error_dict = e.__dict__
        error_code = int(error_dict["code"])
        print(e)
        if error_code == 23505:
            raise DuplicateNameException
    return

def remove_task(task_info):

    print("removing task:" + task_info[0])

    try:
        supabase.table("tasks").delete().eq("name",task_info).execute()
    except Exception as e:
        print(e)
    
    print(task_info + " removed")
    return("Task - " + task_info + " removed successfully")

def mark_incomplete(task_info):
    print("marking incomplete: " + task_info) 

    try:
        supabase.table("tasks").update({"complete": False}).eq("name",task_info).execute()
    except Exception as e:
        print(e)
    
    print(task_info + " marked as complete")
    return("Task - " +  task_info + " marked as complete ")
    
def mark_complete(task_info):
    print("marking complete: " + task_info) 

    try:
        supabase.table("tasks").update({"complete": True}).eq("name",task_info).execute()
    except Exception as e:
        print(e)
    
    print( task_info + " marked as complete")
    return("Task - " + task_info + "Task marked as complete ")

def clear_done():
    pass

