from sbtest import show_tasks
import json 

def get_response(user_input: str):
    user_input = user_input.lower()

    if user_input == 'hello':
        return("Hello!")
    elif user_input == 'bye':
        return("Goodbye!")
    elif user_input == 'view':
        data = show_tasks()[0]
        values = data['taskname'] + " - " + data['taskdesc'] + " - " + data['creationdate'] + " - " + data['duedate']
        return values
    else:
        return("peck!")

