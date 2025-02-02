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
    
    def _get_input(self, prompt):
        return input(prompt)

    def printLine(self, text, end=False):
        print(text)
        if end:
            input("Press Enter to continue...")

    def make_calendar(self):
        name = self._get_input('Enter calendar name: ')
        calendar_path = Path(self.config['folder']) / f"{name}_events"
        if not calendar_path.exists():
            os.mkdir(calendar_path)
        self.events_dir = f"{name}_events"
        self.printLine(f"Calendar '{name}' created and set as current calendar.", end=True)

    def remove_event(self):
        event_name = self._get_input("Enter the name of the event to remove: ")
        event_dir = Path(self.config['folder']) / self.events_dir / event_name
        if event_dir.exists():
            shutil.rmtree(event_dir)
            self.printLine(f"Event {event_name} removed successfully!", end=True)
        else:
            self.printLine(f"Event {event_name} does not exist.", end=True)

    def add_event(self):
        name = self._get_input('Enter event name: ')
        event_dir = Path(self.config['folder']) / self.events_dir / name
        if not event_dir.exists():
            os.mkdir(event_dir)
        
        with open(event_dir / "info.txt", 'w') as f:
            f.write(f"Event Name: {name}\n")
            f.write("Event Information:\n")
            f.write(self._get_input("Enter information about the event: ") + "\n")
        
        with open(event_dir / "participants.txt", 'w') as f:
            f.write("Participants:\n")
            while True:
                participant = self._get_input("Enter participant name (or type 'done' to finish): ")
                if participant.lower() == 'done':
                    break
                else:
                    f.write(participant + "\n")
        
        with open(event_dir / "schedule.txt", 'w') as f:
            f.write("Schedule:\n")
            f.write(f"Date: {self._get_input('Enter the date: ')}\n")
            f.write(f"Time: {self._get_input('Enter time (can be all-day): ')}\n")
            if self._get_input("Does this event repeat? (y/n): ").lower() == 'y':
                f.write(f"Repeat Frequency: {self._get_input('Enter repeat frequency (e.g., daily, weekly, monthly, yearly): ')}")
            else:
                f.write("Repeat Frequency: never")
        
        self.printLine(f"Event {name} added successfully!", end=True)

    def load_calendar(self):
        name = self._get_input('Enter calendar name: ')
        if name == "Default Calendar":
            self.events_dir = "events"
        else:
            self.events_dir = f"{name}_events"
        events_dir = Path(self.config["folder"]) / self.events_dir
        if not events_dir.exists():
            self.printLine(f"Calendar {name} does not exist.", end=True)
        else:
            self.printLine(f"Calendar {name} loaded successfully!", end=True)

    def show_events(self):
        events_dir = Path(self.config["folder"]) / self.events_dir
        events = list(events_dir.iterdir())
        if not events:
            self.printLine("No events found.", end=True)
        else:
            for event in events:
                with open(event / "schedule.txt", 'r') as f:
                    lines = f.readlines()
                    date = next((line for line in lines if "Date" in line), "").split(": ")[1].strip()
                    time = next((line for line in lines if "Time" in line), "").split(": ")[1].strip()
                    repeat = next((line for line in lines if "Repeat Frequency" in line), "").split(": ")[1].strip()
                    datetime = f"{date} at {time}"
                self.printLine(f"{event.name} on {datetime} and repeats {repeat}", end=True)

    def list_calendars(self):
        self.printLine("Default Calendar")
        directory = Path(self.config["folder"])
        for item in os.listdir(directory):
            if item.endswith("_events"):
                self.printLine(item.removesuffix('_events'))
        self.printLine("", end=True)

    def show_participants(self):
        event = self._get_input("Enter the event you want to show participants for: ")
        participants_file = Path(self.config["folder"]) / self.events_dir / event / "participants.txt"
        if participants_file.exists():
            with open(participants_file, "r") as f:
                for line in f:
                    self.printLine(line)
        else:
            self.printLine(f"No participants found for event '{event}'.", end=True)

    def delete_calendar(self):
        calendar_name = self._get_input("Enter the calendar you want to delete: ")
        if calendar_name == "Default Calendar":
            calendar_dir = Path(self.config['folder']) / "events"
        else:
            calendar_dir = Path(self.config['folder']) / f"{calendar_name}_events"
        if calendar_dir.exists():
            shutil.rmtree(calendar_dir)
            self.printLine(f"Calendar {calendar_name} removed successfully!", end=True)
        else:
            self.printLine(f"Calendar {calendar_name} does not exist.", end=True)

    def run(self):
        dictionary = {"switchMode": False}
        current_row = 0
        menu = [
            'Add new event',
            'Show all events',
            'Remove event',
            'Make new calendar',
            'Load calendar',
            'List Calendars',
            'Delete Calendar',
            'Show Participants',
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
                    self.add_event()
                elif current_row == 1:
                    self.show_events()
                elif current_row == 2:
                    self.remove_event()
                elif current_row == 3:
                    self.make_calendar()
                elif current_row == 4:
                    self.load_calendar()
                elif current_row == 5:
                    self.list_calendars()
                elif current_row == 6:
                    self.delete_calendar()
                elif current_row == 7:
                    self.show_participants()
                elif current_row == 8:
                    dictionary["switchMode"] = True
                    break
                elif current_row == 9:
                    print('Exiting the program.')
                    break
            print_menu(current_row)
        return dictionary
