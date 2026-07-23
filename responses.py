from database import *
from datetime import datetime


def get_response(context):

    print("now in responses.py")
    print(context)
    # probably should put this part in its own function
    context["user_msg"] = context["user_msg"].lower()
    data = context["user_msg"].split(maxsplit=1)
    print(data)
    command = data[0]

    if len(data) != 1:
        task_info = data[1].split("|")
        task_info[0] = " ".join(task_info[0].strip().split())
        if len(task_info) == 1:
            task_info.append(None)
        try:
            task_info[1] = normalize_time(task_info[1])
        except Exception:
            print("bad time")
            return("A date or time is malformated (DD-MM-YYYY H:M)")

    match command:
        case "!view":
            try:
                data =format_result(show_tasks())
                return data
            except: 
                return text_wrapper(("No tasks present :)"))
        case "!insert":
            try:
                insert_task(task_info, datetime.now())
            except DuplicateNameException:
                return text_wrapper(("A task with that name is already present"))
            return text_wrapper(("Task was inserted successfully"))
        case "!remove":
            return text_wrapper(remove_task(task_info[0]))
        case "!complete":
            return text_wrapper(mark_complete(task_info[0]))
        case "!incomplete":
            return text_wrapper(mark_incomplete(task_info[0]))
        case "!cleardone":
            return text_wrapper(clear_done())
        case "!help":
            helptext = "```"+"""
            Taskman - Commands
            !view - view all tasks (ordered by due date)

            !insert - create a new task [ !insert TASKNAME | OPTIONAL: TIMESTAMP DD-MM-YYYY H:M ]
            Example - !insert buy milk | 20-02-2026 12:30, !insert buy bread
            Note that only one task of a specific name may exist at a time

            !remove - remove a specified task from a table
            Example - !remove do dishes

            !complete - mark a specified task as complete
            Example - !complete take out rubbish

            !incomplete - Mark a specified task as incomplete
            Example - !incomplete rebuild engine again

            !cleardone - remove all completed tasks
            """ + "```"
            return helptext
        case _ if command.startswith("!"):
            return ("Unkown command, try !help for details")
        case _:
            return None


def format_result(tasks):
    task_list = []
    for task in tasks:
        status = " V " if task['complete'] else " X "
        try:
            due_date = format_time(datetime.fromisoformat(
                str(task['due_date'])).replace(microsecond=0, tzinfo=None))
        except:
            due_date = "No date given"

        line = f"[{status}] {task['name']} (Due: {due_date})"
        task_list.append(line)
        msg = "\n".join(task_list)
    return "```" + msg + "```"


def format_time(timestamp):
    return timestamp.strftime("%d-%m-%Y %H:%M")

def normalize_time(time):
    if time == None:
        return None
    else:
        time = time.strip()
        try:
            time = datetime.strptime(time, "%d-%m-%Y %H:%M")
            return str(time)
        except Exception:
            raise Exception
        
def text_wrapper(msg): 
    return "```" + msg + "```"
