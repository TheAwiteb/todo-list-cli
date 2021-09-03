
import os
import json
from datetime import datetime
from pytz import timezone, UnknownTimeZoneError
from math import ceil
from rich.console import Console
from rich.columns import Columns
from rich.panel import Panel
from rich.prompt import Confirm, Prompt, IntPrompt
from rich.traceback import install
from __init__ import VERSION, JSON_FILE, MAX_TODO

console = Console()
install()

def get_json():
    with open(JSON_FILE, 'r') as f:
        return json.load(f)


def add_json(dct):
    with open(JSON_FILE, 'w') as f:
        json.dump(dct, f, indent=4)


def add_new_todo(title: str):
    data = get_json()
    new_id = len(data['todoList']) + 1
    dct = {
        "id":new_id,
        "title":title,
        "timestamp": datetime.now().timestamp()
    }
    data["todoList"].append(dct)
    add_json(data)

def format_todo(todo: dict):
    title = todo['title']
    date_format = "%b %d %Y %I:%M %p"
    date = datetime.fromtimestamp(todo['timestamp'], tz=TZ).strftime(date_format)
    return f"[b]{title}[/b]\n[yellow]{date}"

def get_page(page_number: int):
    todo_list = get_json()['todoList']
    len_todo = len(todo_list)
    pages = ceil(len_todo / MAX_TODO)
    start, end = (page_number-1) * MAX_TODO, page_number * 10
    title = f"[b yellow]TODO LIST[/]\n[b]{page_number if pages else 0}[/]/{pages} Pages\nTotal: [b]{len_todo}[/] Todo\n[i b yellow blink]{VERSION}v[/]"
    if pages > 0:
        if page_number > pages or page_number < 1:
            raise Exception("incorrect page number maximum is %d and page number must be bigger than 0" % pages)
        else:
            todo_renderables = [Panel(format_todo(todo), expand=True, title=f"id={id_}") for todo, id_ in zip(todo_list, [t['id'] for t in todo_list])]
            console.print(Columns(todo_renderables[start:end], expand=True, title=title))
    else:
        console.print(title)
def add_todo():
    while True:
        title = Prompt.ask("[b]Enter Todo[/] [cyan](must be at least 100 characters)")
        if len(title) <= 100:
            console.print(f"\n[i b cyan]the Todo is [/]\n\n{title}\n")
            if Confirm.ask("[b]continue?[/]"):
                break
            else:
                pass
        else:
            console.print("[prompt.invalid]Todo must short than 100")
    add_new_todo(title=title)
    console.clear()
    console.print("[b]added successfully.[/b]")

def done_todo():
    json = get_json()
    todo_list = json["todoList"]
    ids = list(map(lambda todo: todo["id"], todo_list))
    while True:
        id_ = IntPrompt.ask("[b]Enter id of Todo[/]")
        if id_ in ids:
            break
        else:
            console.print(f"[prompt.invalid] {id_} not in list")
    json["todoList"] = list(filter(lambda todo: todo["id"] != id_, todo_list))
    add_json(json)
    console.clear()
    console.print("[b]deleted successfully.[/b]")


def homepage(page_number: int):
    make_description = lambda dct: "[b]{}[/b]-[b]{}[/b]: [i]{}[/i]".format(*dct.values())
    choices = {
        "add" : "Add new todo to list.",
        "done": "Delete todo fron list.",
        "next": "Go next page.",
        "back": "Go back page.",
        "exit": "Exit.",
        }
    try:
        get_page(page_number)
    except Exception as err:
        console.print(f"[prompt.invalid]{err}")
        return
    console.print('\n'+'\n'.join(map(make_description, [{"count": count, "command":tup[0], "description":tup[1]} 
                                                            for count, tup in enumerate(choices.items(), 1)])), end="\n\n")
    user_input = Prompt.ask("[b]Choose from above[/]", choices=choices.keys())
    return user_input

if os.path.lexists(JSON_FILE):
    TZ = timezone(get_json()['tz'])
else:
    while True:
        console.print("[i cyan]You can find TimeZone in[/] [i b u blue link https://www.zeitverschiebung.net/en]zeitverschiebung.net[/]")
        TZ = Prompt.ask("[b]Enter TimeZone[/b]", default="Asia/Riyadh")
        try:
            timezone(TZ)
            break
        except UnknownTimeZoneError:
            console.print(f":x:[prompt.invalid] incorrect TimeZone '{TZ}' not found")
    first_line = {
        "tz":TZ,
        "todoList":[]
        }
    TZ = timezone(TZ)
    with open(JSON_FILE, 'w') as f:
        json.dump(first_line, f)

def main():
    page = 1
    last_command = ''
    while True:
        user_input = homepage(page)
        if user_input:
            last_command = user_input
            if user_input == "add":
                add_todo()
            elif user_input == "done":
                done_todo()
            elif user_input == "next":
                page += 1
            elif user_input == "back":
                page -= 1
            elif user_input == "exit":
                break
        else:
            if last_command == "next":
                page -= 1
            elif last_command == "back":
                page += 1
            else:
                break
        if user_input and user_input not in ["add", "done"]:
            console.clear()
        else:
            pass

if __name__ == "__main__":
    main()

t = "jdsjdsk hfbuhrorgnor pjwa;ibshlbygb ufuhhfihvfhn 8934yu37fnu3 89hfsjnc 893yru3hj 89hfoujdn ueh89rfh ed 97egheibhksnkjs 78 e fkb bdkbkdbfkfdb 87 3bkebfkbdhdbfkdbh heiuhfi kbfdb ".split()