from calendarEvents import EventCalendar
from todoapp import PodiumToDoApp
import json
import os
from pathlib import Path

class Podium_Organizer:
    def __init__(self):
        self.data = {}
        self.config = {}
        self.file_path = Path(f"{os.path.expanduser('~')}/.podium_organizer/config/config.json")
        self._load_or_create_config()
        self.mode = self.data["last_mode"]
        if not Path(self.config["folder"]).exists():
            Path(self.config["folder"]).mkdir(parents=True)
        if not (Path(self.config["folder"]) / "events").exists():
            (Path(self.config["folder"]) / "events").mkdir()
        if not (Path(self.config["folder"]) / "ToDo").exists():
            (Path(self.config["folder"]) / "ToDo").mkdir()

    def _save_config(self):
        parent_dir = self.file_path.parent
        if not parent_dir.exists():
            os.mkdir(parent_dir)
        with open(self.file_path, "w") as f:
            json.dump(self.config, f, indent=4)
    
    def _save_data(self):
        with open(self.file_path.parent / "data.json", "w") as f:
            json.dump(self.data, f, indent=4)
    
    def _load_or_create_config(self):
        config_dir = self.file_path.parent.parent
        if not config_dir.exists():
            os.mkdir(config_dir)
            os.mkdir(config_dir / "config")
            self.config = {"folder": f"{os.path.expanduser('~')}/.podium_organizer/Files"}
            self._save_config()
        else:
            if self.file_path.exists() and self.file_path.stat().st_size > 0:
                with open(self.file_path, 'r') as f:
                    try:
                        self.config = json.load(f)
                    except json.JSONDecodeError:
                        print("Error: Config file is not in valid JSON format. Creating a new one.")
                        self.config = {"folder": f"{os.path.expanduser('~')}/.podium_organizer/Files"}
                        self._save_config()
            else:
                self.config = {"folder": f"{os.path.expanduser('~')}/.podium_organizer/Files"}
                self._save_config()
            data_file = Path(f"{os.path.expanduser('~')}/.podium_organizer/config/data.json")
            if data_file.exists() and data_file.stat().st_size > 0:
                with open(data_file, 'r') as f:
                    try:
                        self.data = json.load(f)
                    except json.JSONDecodeError:
                        print("Error: Data file is not in valid JSON format. Creating a new one.")
                        self.data = {"last_events_dir": "events", "last_mode": "calendar", "last_todo_list": "toDoList", "camel_case_records": {"toDoList": "To Do List"}}
                        self._save_data()
            else:
                self.data = {"last_events_dir": "events", "last_mode": "calendar", "last_todo_list": "toDoList", "camel_case_records": {"toDoList": "To Do List"}}
                self._save_data()
    
    def run(self):
        out = {"switchMode": False}
        if self.mode == "calendar":
            calendar = EventCalendar(self.config, self.data)
            out = calendar.run()
            self.data["last_events_dir"] = calendar.events_dir
        if self.mode == "todo":
            todoApp = PodiumToDoApp(self.config, self.data)
            out = todoApp.run()
            self.data["last_todo_list"] = todoApp.toDoList
        self.data["last_mode"] = self.mode
        
        self._save_config()
        self._save_data()
        return out
