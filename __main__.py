import shutil
import json
import os
from pathlib import Path

class Podium_Organizer:
    def __init__(self):
        self.data = {}
        self.config = {}
        self.file_path = Path(f"{os.path.expanduser('~')}/.podium-organizer/config/config.json")
        self._load_or_create_config()
        self.events_dir = self.data["last_events_dir"]

    def make_calendar(self):
        name = input('Enter calendar name: ')
        calendar_path = Path(self.config['folder']) / f"{name}_events"
        os.makedirs(calendar_path, exist_ok=True)
        self.events_dir = f"{name}_events"
        print(f"Calendar '{name}' created and set as current calendar.")


    def _save_data(self):
        with open(self.file_path.parent / "data.json", "w") as f:
            json.dump(self.data, f, indent=4)
    def _load_or_create_config(self):
        config_dir = self.file_path.parent.parent
        if not config_dir.exists():
            os.makedirs(config_dir, exist_ok=True)
            self.config = {"folder": f"{os.path.expanduser('~')}/.podium-organizer/Files", "last_events_dir": "events"}
            self._save_config()
        else:
            if self.file_path.exists() and self.file_path.stat().st_size > 0:
                with open(self.file_path, 'r') as f:
                    try:
                        self.config = json.load(f)
                    except json.JSONDecodeError:
                        print("Error: Config file is not in valid JSON format. Creating a new one.")
                        self.config = {"folder": f"{os.path.expanduser('~')}/.podium-organizer/Files"}
                        self._save_config()
            else:
                self.config = {"folder": f"{os.path.expanduser('~')}/.podium-organizer/Files"}
                self._save_config()
            if Path(f"{os.path.expanduser('~')}/.podium_organizer/config/data.json").exists() and Path(f"{os.path.expanduser('~')}/.podium_organizer/config/data.json").stat().st_size > 0:
                with open(Path(f"{os.path.expanduser('~')}/.podium_organizer/config/data.json"), 'r') as f:
                    try:
                        self.data = json.load(f)
                    except json.JSONDecodeError:
                        print("Error: Data file is not in valid JSON format. Creating a new one.")
                        self.data = {}
                        self._save_data()
            else:
                self.data = {"last_events_dir": "events"}
                self._save_data()
                
        events_dir = Path(self.config["folder"]) / "events"
        if not events_dir.exists():
            os.makedirs(events_dir, exist_ok=True)

    def _save_config(self):
        os.makedirs(self.file_path.parent, exist_ok=True)
        with open(self.file_path, "w") as f:
            json.dump(self.config, f, indent=4)

    def remove_event(self):
        event_name = input("Enter the name of the event to remove: ")
        event_dir = Path(self.config['folder']) / self.events_dir / event_name
        if event_dir.exists():
            shutil.rmtree(event_dir)
            print(f"Event {event_name} removed successfully!")
        else:
            print(f"Event {event_name} does not exist.")

    def add_event(self):
        name = input('Enter event name: ')
        event_dir = Path(self.config['folder']) / self.events_dir / name
        os.makedirs(event_dir, exist_ok=True)
        
        with open(event_dir / "info.txt", 'w') as f:
            f.write(f"Event Name: {name}\n")
            f.write("Event Information:\n")
            f.write(input("Enter information about the event:") + "\n")
        
        with open(event_dir / "participants.txt", 'w') as f:
            f.write("Participants:\n")
            while True:
                participant = input("Enter participant name (or type 'done' to finish): ")
                if participant.lower() == 'done':
                    break
                else:
                    f.write(participant + "\n")
        
        with open(event_dir / "schedule.txt", 'w') as f:
            f.write("Schedule:\n")
            f.write(f"Date: {input('Enter the date: ')}\n")
            f.write(f"Time: {input('Enter time (can be all-day): ')}\n")
            if input("Does this event repeat? (y/n): ").lower() == 'y':
                f.write(f"Repeat Frequency: {input('Enter repeat frequency (e.g., daily, weekly, monthly, yearly): ')}")
            else:
                f.write("Repeat Frequency: never")
        
        print(f"Event {name} added successfully!")

    def load_calendar(self):
        name = input('Enter calendar name: ')
        self.events_dir = f"{name}_events"
        events_dir = Path(self.config["folder"]) / self.events_dir
        if not events_dir.exists():
            print(f"Calendar {name} does not exist.")
        else:
            print(f"Calendar {name} loaded successfully!")

    def show_events(self):
        events_dir = Path(self.config["folder"]) / self.events_dir
        events = list(events_dir.iterdir())
        if not events:
            print("No events found.")
        else:
            for event in events:
                with open(event / "schedule.txt", 'r') as f:
                    lines = f.readlines()
                    date = next((line for line in lines if "Date" in line), "").split(": ")[1].strip()
                    time = next((line for line in lines if "Time" in line), "").split(": ")[1].strip()
                    repeat = next((line for line in lines if "Repeat Frequency" in line), "").split(": ")[1].strip()
                    datetime = f"{date} at {time}"
                print(f"{event.name} on {datetime} and repeats {repeat}")

    def run(self):
        while True:
            print('Podium Organizer')
            print('1. Add new event')
            print('2. Show all events')
            print('3. Remove event')
            print('4. Make new calendar')
            print('5. Load calendar')
            print("q, e, exit, or quit to exit")
            choice = input('Enter your choice: ')
            if choice == '1':
                self.add_event()
            elif choice == '2':
                self.show_events()
            elif choice == '3':
                self.remove_event()
            elif choice == '4':
                self.make_calendar()
            elif choice == '5':
                self.load_calendar()
            elif choice.lower() in ["q", "e", "exit", "quit"]:
                print('Exiting the program.')
                self.config["last_events_dir"] = self.events_dir
                self._save_config()
                break
            else:
                print('Invalid choice. Please try again.')

if __name__ == '__main__':
    organizer = Podium_Organizer()
    organizer.run()
