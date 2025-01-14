import shutil
import os
from pathlib import Path

class EventCalendar:
    def __init__(self, config, data):
        self.config = config
        self.data = data
        self.events_dir = self.data["last_events_dir"]
        events_folder = Path(self.config["folder"]) / self.events_dir
        if not events_folder.exists():
            events_folder.mkdir(parents=True)
    
    def make_calendar(self):
        name = input('Enter calendar name: ')
        calendar_path = Path(self.config['folder']) / f"{name}_events"
        if not calendar_path.exists():
            os.mkdir(calendar_path)
        self.events_dir = f"{name}_events"
        print(f"Calendar '{name}' created and set as current calendar.")

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
        if not event_dir.exists():
            os.mkdir(event_dir)
        
        with open(event_dir / "info.txt", 'w') as f:
            f.write(f"Event Name: {name}\n")
            f.write("Event Information:\n")
            f.write(input("Enter information about the event: ") + "\n")
        
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
        if name == "Default Calendar":
            self.events_dir = "events"
        else:
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

    def list_calendars(self):
        print("Default Calendar")
        directory = Path(self.config["folder"])
        for item in os.listdir(directory):
            if item.endswith("_events"):
                print(item.removesuffix('_events'))
        print("")

    def show_participants(self):
        event = input("Enter the event you want to show participants for: ")
        participants_file = Path(self.config["folder"]) / self.events_dir / event / "participants.txt"
        if participants_file.exists():
            with open(participants_file, "r") as f:
                for line in f:
                    print(line)
        else:
            print(f"No participants found for event '{event}'.")

    def delete_calendar(self):
        calendar_name = input("Enter the calendar you want to delete: ")
        if calendar_name == "Default Calendar":
            calendar_dir = Path(self.config['folder']) / "events"
        else:
            calendar_dir = Path(self.config['folder']) / f"{calendar_name}_events"
        if calendar_dir.exists():
            shutil.rmtree(calendar_dir)
            print(f"Calendar {calendar_name} removed successfully!")
        else:
            print(f"Calendar {calendar_name} does not exist.")

    def run(self) -> dict:
        dictionary = {"switchMode": False}
        while True:
            print('Podium Organizer')
            print('1. Add new event')
            print('2. Show all events')
            print('3. Remove event')
            print('4. Make new calendar')
            print('5. Load calendar')
            print('6: List Calendars')
            print('7: Delete Calendar')
            print('8: Show Participants')
            print('9: Switch Mode')
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
            elif choice == '6':
                self.list_calendars()
            elif choice == '7':
                self.delete_calendar()
            elif choice == '8':
                self.show_participants()
            elif choice == '9':
                dictionary["switchMode"] = True
                break
            elif choice.lower() in ["q", "e", "exit", "quit"]:
                print('Exiting the program.')
                break
            else:
                print('Invalid choice. Please try again.')
        return dictionary
