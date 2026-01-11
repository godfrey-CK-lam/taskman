from sbtest import *
from datetime import datetime


def get_response(user_input: str):

    user_input = user_input.lower()
    command = user_input.split(maxsplit=1)[0]

    match command:
        case "!view":
            data = "```" + format_result(show_tasks()) + "```"
            return data
        case "!insert":
            try:
                insert_task(user_input, datetime.now())
            except BadDateTimeException:
                return ("A date or time is malformatted, the task was not added")
            except DuplicateNameException:
                return ("A task with that name is already present")
            return ("Task was inserted successfully")
        case "!remove":
            raise NotImplementedError
        case "!complete":
            raise NotImplementedError
        case "!incomplete":
            raise NotImplementedError
        case "!cleardone":
            raise NotImplementedError
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

            raise NotImplementedError
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
    return msg


def format_time(timestamp):
    return timestamp.strftime("%d-%m-%Y %H:%M")
