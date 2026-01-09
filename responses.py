from sbtest import show_tasks
from datetime import datetime
import json 

def get_response(user_input: str):
    user_input = user_input.lower()

    if user_input == 'hello':
        return("Hello!")
    elif user_input == 'bye':
        return("Goodbye!")
    elif user_input == 'view':
        data = format_result(show_tasks())
        return data
    else:
        return("peck!")
    
def format_result(tasks):
    task_list = []
    for task in tasks:
        status = " V " if task['completed'] else " X "
        due_date = datetime.fromisoformat(task['duedate']).replace(microsecond=0, tzinfo=None)
        line = f"[{status}] {task['name']} (Due: {due_date})"
        task_list.append(line)
        msg = "\n".join(task_list)
    return msg

print(get_response("view"))