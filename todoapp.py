from pathlib import Path
import os
import curses
import sys


class PodiumToDoApp:
    def __init__(self, config, data):
        self.config = config
        self.data = data
        self.camel_case_records = self.data["camel_case_records"]
        self.toDoList = self.data["last_todo_list"]
        todo_folder = Path(self.config["folder"]) / "ToDo"
        if not todo_folder.exists():
            todo_folder.mkdir(parents=True)
        if not (todo_folder / f"{self.toDoList}.txt").exists():
            with open(todo_folder / f"{self.toDoList}.txt", "w") as f:
                f.write("To Do List\n\n")

    def endWin(self):
        curses.endwin()

    def startWin(self, pressEnter=True):
        if pressEnter:
            input()
            sys.stdout.write('\r')
            sys.stdout.flush()
        curses.doupdate()

    
    
  

    def printAll(self):
        self.endWin()
        with open(Path(self.config["folder"]) / "ToDo" / f"{self.toDoList}.txt", "r") as f:
            for line in f:
                print(line.strip())
        self.startWin()


    def to_camel_case(self, s, record=False):
        # Split the string into words
        words = s.split()
        
        # Convert the first word to lowercase
        camel_case = words[0].lower()
        
        # Capitalize the first letter of subsequent words and add to camel_case
        for word in words[1:]:
            camel_case += word.capitalize()

        if record == True:
            self.camel_case_records[camel_case] = s
        
        return camel_case

    def printCompleted(self):
        self.endWin()
        with open(Path(self.config["folder"]) / "ToDo" / f"{self.toDoList}.txt", "r") as f:
            all_lines = f.readlines()
            print(all_lines[0].strip())
            for line in f:
                if line.startswith("Done: "):
                    print(line.strip())
        self.startWin()

    def addTask(self):
        self.endWin()
        task = input("Enter the task to add: ")
        with open(Path(self.config["folder"]) / "ToDo" / f"{self.toDoList}.txt", "a") as f:
            f.write("Not Done: " + task + "\n")
        print(f"Task \"{task}\" added to the list.")
        self.startWin()

    def removeTask(self):
        self.endWin()
        task_to_remove = input("Enter the task to remove: ")
        lines = []
        with open(Path(self.config["folder"]) / "ToDo" / f"{self.toDoList}.txt", "r") as f:
            lines = f.readlines()
        with open(Path(self.config["folder"]) / "ToDo" / f"{self.toDoList}.txt", "w") as f:
            for line in lines:
                if f"Done: {line.removeprefix('Done: ').strip()}" != task_to_remove and f"Not done: {line.removeprefix('Not done: ').strip()}" != task_to_remove:
                    f.write(line)
        print(f"Task \"{task_to_remove}\" removed from the list.")
        self.startWin()

    
    def add_prefix(self, prefix, original_string):
        return prefix + original_string

    def listLists(self):
        self.endWin()
        for file in os.listdir(Path(self.config["folder"]) / "ToDo"):
            if file.endswith(".txt"):
                print(self.camel_case_records[file.removesuffix(".txt")])
        self.startWin()

    def addList(self):
        self.endWin()
        name = input("What do you want the name of the task list to be: ")
        camel_cased = self.to_camel_case(name, record=True)
        with open(Path(self.config["folder"]) / "ToDo" / f"{camel_cased}.txt", "w") as f:
            f.write(f"{name}\n\n")
        self.toDoList = camel_cased
        self.startWin(pressEnter=False)

    def removeList(self):
        self.endWin()
        list_to_remove = input("Enter the name of the list to remove: ")
        camel_cased = self.to_camel_case(list_to_remove)
        file_path = Path(self.config["folder"]) / "ToDo" / f"{camel_cased}.txt"
        if file_path.exists():
            os.remove(file_path)
            self.camel_case_records.pop(camel_cased, None)
            print(f"List \"{list_to_remove}\" removed.")
        else:
            print(f"List \"{list_to_remove}\" does not exist.")
        self.startWin()

    
    def complete_task(self):
        self.endWin()
        i = input("What task do you want to complete? ")
        with open(Path(self.config["folder"]) / "ToDo" / f"{self.toDoList}.txt", "r") as f:
            lines = f.readlines()
        with open(Path(self.config["folder"]) / "ToDo" / f"{self.toDoList}.txt", "w") as f:
            for line in lines:
                if line.startswith("Not Done: "):
                    if line.removeprefix("Not Done: ").strip() == i:
                        f.write(self.add_prefix("Done: ", line.removeprefix("Not Done: ")))
                        print(f"Task \"{i}\" completed successfully!")
                    else:
                        f.write(line)
                elif line.startswith("Done: "):
                    if line.removeprefix("Done: ").strip() == i:
                        print(f"Task \"{i}\" is already completed.")
                    else:
                        f.write(line)
                else:
                    f.write(line)
        self.startWin()

    def makeIncomplete(self):
        self.endWin()                 
        i = input("What task do you want to make incomplete? ")
        with open(Path(self.config["folder"]) / "ToDo" / f"{self.toDoList}.txt", "r") as f:
            lines = f.readlines()
        with open(Path(self.config["folder"]) / "ToDo" / f"{self.toDoList}.txt", "w") as f:
            for line in lines:
                if line.startswith("Done"):
                    if line.removeprefix("Done: ").strip() == i:
                        f.write(self.add_prefix("Not Done: ", line.removeprefix("Done: ")))
                    else:
                        f.write(line)
                elif line.startswith("Not Done"):
                    if line.removeprefix("Not Done: ").strip() == i:
                        print(f"Task \"{i}\" is already not completed.")
                    else:
                        f.write(line)
                else:
                    f.write(line)
        self.startWin()



    def changeToDoList(self):
        self.endWin()
        toDoList = self.to_camel_case(input("What to do list do you want to change to? "))
        self.toDoList = toDoList
        self.startWin()
    
    def run(self, stdscr) -> dict:
        dictionary = {"switchMode": False}
        curses.curs_set(0)
        current_row = 0
        menu = [
            'Add task',
            'Remove Task',
            'Print all tasks',
            'Show Completed Tasks',
            'Remove a List',
            'Complete a Task',
            'Change ToDo List',
            'Make Incomplete',
            'List All ToDo Lists',
            'Add List',
            'Switch Mode',
            'Exit'
        ]

        def print_menu(stdscr, selected_row_idx):
            stdscr.clear()
            stdscr.addstr('Podium Organizer\n', curses.A_BOLD)
            for idx, row in enumerate(menu):
                if idx == selected_row_idx:
                    stdscr.addstr(f"{row}\n", curses.color_pair(1))
                else:
                    stdscr.addstr(f"{row}\n")
            stdscr.refresh()

        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
        print_menu(stdscr, current_row)

        while True:
            key = stdscr.getch()

            if key == curses.KEY_UP and current_row > 0:
                current_row -= 1
            elif key == curses.KEY_DOWN and current_row < len(menu) - 1:
                current_row += 1
            elif key == curses.KEY_ENTER or key in [10, 13]:
                if current_row == 0:
                    self.addTask()
                elif current_row == 1:
                    self.removeTask()
                elif current_row == 2:
                    self.printAll()
                elif current_row == 3:
                    self.printCompleted()
                elif current_row == 4:
                    self.removeList()
                elif current_row == 5:
                    self.complete_task()
                elif current_row == 6:
                    self.changeToDoList()
                elif current_row == 7:
                    self.makeIncomplete()
                elif current_row == 8:
                    self.listLists()
                elif current_row == 9:
                    self.addList()
                elif current_row == 10:
                    dictionary["switchMode"] = True
                    break
                elif current_row == 11:
                    self.endWin()
                    print('Exiting the program.')
                    break
            print_menu(stdscr, current_row)
        return dictionary