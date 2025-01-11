from pathlib import Path
import os


class PodiumToDoApp:
    def __init__(self, config, data):
        self.config = config
        self.data = data
        self.camel_case_records = self.data["camel_case_records"]
        self.toDoList = self.data["last_todo_list"]
        if not (Path(self.config["folder"]) / "ToDo" / f"{self.toDoList}.txt").exists():
            with open(Path(self.config["folder"]) / "ToDo" / f"{self.toDoList}.txt", "w") as f:
                f.write("To Do List\n\n")

    def printAll(self):
        with open(Path(self.config["folder"]) / "ToDo" / f"{self.toDoList}.txt", "r") as f:
            for line in f:
                print(line.strip())

    
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
            print(all_lines[0].strip())
            for line in f:
                if line.startswith("Done: "):
                    print(line.strip())

    def addTask(self):
        task = input("Enter the task to add: ")
        with open(Path(self.config["folder"]) / "ToDo" / f"{self.toDoList}.txt", "a") as f:
            f.write("Not Done: " + task + "\n")
        print(f"Task \"{task}\" added to the list.")

    def removeTask(self):
        task_to_remove = input("Enter the task to remove: ")
        lines = []
        with open(Path(self.config["folder"]) / "ToDo" / f"{self.toDoList}.txt", "r") as f:
            lines = f.readlines()
        with open(Path(self.config["folder"]) / "ToDo" / f"{self.toDoList}.txt", "w") as f:
            for line in lines:
                if f"Done: {line.removeprefix('Done: ').strip()}" != task_to_remove and f"Not done: {line.removeprefix('Not done: ').strip()}" != task_to_remove:
                    f.write(line)
        print(f"Task \"{task_to_remove}\" removed from the list.")


    def add_prefix(self, prefix, original_string):
        return prefix + original_string




    def listLists(self):
        for file in os.listdir(Path(self.config["folder"]) / "ToDo"):
            if file.endswith(".txt"):
                print(self.camel_case_records[file.removesuffix(".txt")])

    

    def addList(self):
        name = input("What do you want the name of the task list to be: ")
        camel_cased = self.to_camel_case(name, record=True)
        with open(Path(self.config["folder"]) / "ToDo" / f"{camel_cased}.txt", "w") as f:
            f.write(f"{name}\n\n")
        self.toDoList = camel_cased

    def removeList(self):
        list_to_remove = input("Enter the name of the list to remove: ")
        camel_cased = self.to_camel_case(list_to_remove)
        file_path = Path(self.config["folder"]) / "ToDo" / f"{camel_cased}.txt"
        if file_path.exists():
            os.remove(file_path)
            self.camel_case_records.pop(camel_cased, None)
            print(f"List \"{list_to_remove}\" removed.")
        else:
            print(f"List \"{list_to_remove}\" does not exist.")


    def complete_task(self):
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
    def makeIncomplete(self):                 
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

    def changeToDoList(self):
        toDoList = self.to_camel_case(input("What to do list do ou want to change to? "))
        self.toDoList = toDoList
    
    def run(self) -> dict:
        dictionary = {"switchMode": False}
        print("Podium Organizer")
        print("1. Add task")
        print("2. Remove Task")
        print("3. Print all tasks")
        print("4. Show Completed Tasks")
        print("5. Remove a List")
        print("6. Complete a Task")
        print("7. Change ToDo List")
        print("8. Make Incomplete")
        print("9. List All ToDo Lists")
        print("10. Add List")
        print("11. Switch Mode")
        print("q, e, exit, quit - Exit the program")
        
        while True:
            userInput = input("Enter your choice: ")
            if userInput in ["q", "e", "exit", "quit"]:
                break
            elif userInput == "1":
                self.addTask()
            elif userInput == "2":
                self.removeTask()
            elif userInput == "3":
                self.printAll()
            elif userInput == "4":
                self.printCompleted()
            elif userInput == "5":
                self.removeList()
            elif userInput == "6":
                self.complete_task()
            elif userInput == "7":
                self.changeToDoList()
            elif userInput == "8":
                self.makeIncomplete()
            elif userInput == "9":
                self.listLists()
            elif userInput == "10":
                self.addList()
            elif userInput == "11":
                dictionary["switchMode"] = True
                break
            else:
                print("Invalid choice. Please try again.")
        
        return dictionary