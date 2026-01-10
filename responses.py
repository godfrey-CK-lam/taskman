from sbtest import show_tasks, insert_task, DuplicateNameException, BadDateTimeException
from datetime import datetime
import json 

def get_response(user_input: str, timestamp):
    user_input = user_input.lower()

    if "!addtask" in user_input:
        return("Hello!")
    elif user_input == 'bye':
        return(user_input)
    elif user_input == 'view':
        data = format_result(show_tasks())
        return data
    
    elif "!insert" in user_input:

        try:
            insert_task(user_input, datetime.now())
        except BadDateTimeException: 
            print("bad dt")
            return("A date or time is malformatted, the task was not added")
        except DuplicateNameException:
            print("bad name")
            return("A task with that name is already present")
        
        print("task added")
        return("Task was inserted successfully")

    
    else:
        return(user_input)
    
def format_result(tasks):
    task_list = []
    for task in tasks:
        status = " V " if task['complete'] else " X "

        try:
            due_date = format_time(datetime.fromisoformat(str(task['due_date'])).replace(microsecond=0, tzinfo=None))
        except:
            due_date = "No date given"

        line = f"[{status}] {task['name']} (Due: {due_date})"
        task_list.append(line)
        msg = "\n".join(task_list)
    return msg

def format_time(timestamp):
    return timestamp.strftime("%d-%m-%Y %H:%M")


