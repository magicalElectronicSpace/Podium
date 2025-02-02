from pathlib import Path
import os

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

    def _get_input(self, prompt):
        return input(prompt)

    def printLine(self, text, end=False):
        print(text)
        if end:
            input("Press Enter to continue...")

    def printAll(self):
        with open(Path(self.config["folder"]) / "ToDo" / f"{self.toDoList}.txt", "r") as f:
            for line in f:
                self.printLine(line.strip())
        self.printLine("", end=True)

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
        with open(Path(self.config["folder"]) / "ToDo" / f"{self.toDoList}.txt", "r") as f:
            all_lines = f.readlines()
            self.printLine(all_lines[0].strip())
            for line in f:
                if line.startswith("Done: "):
                    self.printLine(line.strip())
        self.printLine("", end=True)

    def addTask(self):
        task = self._get_input("Enter the task to add: ")
        with open(Path(self.config["folder"]) / "ToDo" / f"{self.toDoList}.txt", "a") as f:
            f.write("Not Done: " + task + "\n")
        self.printLine(f"Task \"{task}\" added to the list.", end=True)

    def removeTask(self):
        task_to_remove = self._get_input("Enter the task to remove: ")
        lines = []
        with open(Path(self.config["folder"]) / "ToDo" / f"{self.toDoList}.txt", "r") as f:
            lines = f.readlines()
        with open(Path(self.config["folder"]) / "ToDo" / f"{self.toDoList}.txt", "w") as f:
            for line in lines:
                if f"Done: {line.removeprefix('Done: ').strip()}" != task_to_remove and f"Not done: {line.removeprefix('Not done: ').strip()}" != task_to_remove:
                    f.write(line)
        self.printLine(f"Task \"{task_to_remove}\" removed from the list.", end=True)

    def add_prefix(self, prefix, original_string):
        return prefix + original_string

    def listLists(self):
        for file in os.listdir(Path(self.config["folder"]) / "ToDo"):
            if file.endswith(".txt"):
                self.printLine(self.camel_case_records[file.removesuffix(".txt")])
        self.printLine("", end=True)

    def addList(self):
        name = self._get_input("What do you want the name of the task list to be: ")
        camel_cased = self.to_camel_case(name, record=True)
        with open(Path(self.config["folder"]) / "ToDo" / f"{camel_cased}.txt", "w") as f:
            f.write(f"{name}\n\n")
        self.toDoList = camel_cased

    def removeList(self):
        list_to_remove = self._get_input("Enter the name of the list to remove: ")
        camel_cased = self.to_camel_case(list_to_remove)
        file_path = Path(self.config["folder"]) / "ToDo" / f"{camel_cased}.txt"
        if file_path.exists():
            os.remove(file_path)
            self.camel_case_records.pop(camel_cased, None)
            self.printLine(f"List \"{list_to_remove}\" removed.", end=True)
        else:
            self.printLine(f"List \"{list_to_remove}\" does not exist.", end=True)

    def complete_task(self):
        i = self._get_input("What task do you want to complete? ")
        with open(Path(self.config["folder"]) / "ToDo" / f"{self.toDoList}.txt", "r") as f:
            lines = f.readlines()
        with open(Path(self.config["folder"]) / "ToDo" / f"{self.toDoList}.txt", "w") as f:
            for line in lines:
                if line.startswith("Not Done: "):
                    if line.removeprefix("Not Done: ").strip() == i:
                        f.write(self.add_prefix("Done: ", line.removeprefix("Not Done: ")))
                        self.printLine(f"Task \"{i}\" completed successfully!", end=True)
                    else:
                        f.write(line)
                elif line.startswith("Done: "):
                    if line.removeprefix("Done: ").strip() == i:
                        self.printLine(f"Task \"{i}\" is already completed.", end=True)
                    else:
                        f.write(line)
                else:
                    f.write(line)

    def makeIncomplete(self):                 
        i = self._get_input("What task do you want to make incomplete? ")
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
                        self.printLine(f"Task \"{i}\" is already not completed.", end=True)
                    else:
                        f.write(line)
                else:
                    f.write(line)

    def changeToDoList(self):
        toDoList = self.to_camel_case(self._get_input("What to do list do you want to change to? "))
        self.toDoList = toDoList
    
    def run(self):
        dictionary = {"switchMode": False}
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

        def print_menu(selected_row_idx):
            os.system('cls' if os.name == 'nt' else 'clear')
            print('Podium Organizer\n')
            for idx, row in enumerate(menu):
                if idx == selected_row_idx:
                    print(f"> {row}")
                else:
                    print(f"  {row}")

        print_menu(current_row)

        while True:
            key = ord(msvcrt.getch())

            if key == 224:  # Special keys (arrows, f keys, ins, del, etc.)
                key = ord(msvcrt.getch())
                if key == 72 and current_row > 0:  # Up arrow
                    current_row -= 1
                elif key == 80 and current_row < len(menu) - 1:  # Down arrow
                    current_row += 1
            elif key == 13:  # Enter key
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
                    print('Exiting the program.')
                    break
            print_menu(current_row)
        return dictionary
