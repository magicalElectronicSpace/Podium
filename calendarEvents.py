import shutil
import os
from pathlib import Path
import curses

class EventCalendar:
    def __init__(self, config, data, stdscr):
        self.config = config
        self.data = data
        self.stdscr = stdscr
        self.events_dir = self.data["last_events_dir"]
        events_folder = Path(self.config["folder"]) / self.events_dir
        if not events_folder.exists():
            events_folder.mkdir(parents=True)
    
    def _get_input(self, prompt):
        curses.echo()
        self.stdscr.addstr(prompt)
        self.stdscr.refresh()
        input_str = self.stdscr.getstr().decode('utf-8')
        curses.noecho()
        self.stdscr.clear()
        return input_str

    def make_calendar(self):
        name = self._get_input('Enter calendar name: ')
        calendar_path = Path(self.config['folder']) / f"{name}_events"
        if not calendar_path.exists():
            os.mkdir(calendar_path)
        self.events_dir = f"{name}_events"
        self.stdscr.addstr(f"Calendar '{name}' created and set as current calendar.\n")
        self.stdscr.refresh()

    def remove_event(self):
        event_name = self._get_input("Enter the name of the event to remove: ")
        event_dir = Path(self.config['folder']) / self.events_dir / event_name
        if event_dir.exists():
            shutil.rmtree(event_dir)
            self.stdscr.addstr(f"Event {event_name} removed successfully!\n")
        else:
            self.stdscr.addstr(f"Event {event_name} does not exist.\n")
        self.stdscr.refresh()

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
        
        self.stdscr.addstr(f"Event {name} added successfully!\n")
        self.stdscr.refresh()

    def load_calendar(self):
        name = self._get_input('Enter calendar name: ')
        if name == "Default Calendar":
            self.events_dir = "events"
        else:
            self.events_dir = f"{name}_events"
        events_dir = Path(self.config["folder"]) / self.events_dir
        if not events_dir.exists():
            self.stdscr.addstr(f"Calendar {name} does not exist.\n")
        else:
            self.stdscr.addstr(f"Calendar {name} loaded successfully!\n")
        self.stdscr.refresh()

    def show_events(self):
        events_dir = Path(self.config["folder"]) / self.events_dir
        events = list(events_dir.iterdir())
        if not events:
            self.stdscr.addstr("No events found.\n")
        else:
            for event in events:
                with open(event / "schedule.txt", 'r') as f:
                    lines = f.readlines()
                    date = next((line for line in lines if "Date" in line), "").split(": ")[1].strip()
                    time = next((line for line in lines if "Time" in line), "").split(": ")[1].strip()
                    repeat = next((line for line in lines if "Repeat Frequency" in line), "").split(": ")[1].strip()
                    datetime = f"{date} at {time}"
                self.stdscr.addstr(f"{event.name} on {datetime} and repeats {repeat}\n")
        self.stdscr.refresh()

    def list_calendars(self):
        self.stdscr.addstr("Default Calendar\n")
        directory = Path(self.config["folder"])
        for item in os.listdir(directory):
            if item.endswith("_events"):
                self.stdscr.addstr(item.removesuffix('_events') + "\n")
        self.stdscr.addstr("\n")
        self.stdscr.refresh()

    def show_participants(self):
        event = self._get_input("Enter the event you want to show participants for: ")
        participants_file = Path(self.config["folder"]) / self.events_dir / event / "participants.txt"
        if participants_file.exists():
            with open(participants_file, "r") as f:
                for line in f:
                    self.stdscr.addstr(line)
        else:
            self.stdscr.addstr(f"No participants found for event '{event}'.\n")
        self.stdscr.refresh()

    def delete_calendar(self):
        calendar_name = self._get_input("Enter the calendar you want to delete: ")
        if calendar_name == "Default Calendar":
            calendar_dir = Path(self.config['folder']) / "events"
        else:
            calendar_dir = Path(self.config['folder']) / f"{calendar_name}_events"
        if calendar_dir.exists():
            shutil.rmtree(calendar_dir)
            self.stdscr.addstr(f"Calendar {calendar_name} removed successfully!\n")
        else:
            self.stdscr.addstr(f"Calendar {calendar_name} does not exist.\n")
        self.stdscr.refresh()

    def run(self) -> dict:
        dictionary = {"switchMode": False}
        while True:
            self.stdscr.addstr('Podium Organizer\n')
            self.stdscr.addstr('1. Add new event\n')
            self.stdscr.addstr('2. Show all events\n')
            self.stdscr.addstr('3. Remove event\n')
            self.stdscr.addstr('4. Make new calendar\n')
            self.stdscr.addstr('5. Load calendar\n')
            self.stdscr.addstr('6: List Calendars\n')
            self.stdscr.addstr('7: Delete Calendar\n')
            self.stdscr.addstr('8: Show Participants\n')
            self.stdscr.addstr('9: Switch Mode\n')
            self.stdscr.addstr("q, e, exit, or quit to exit\n")
            choice = self._get_input('Enter your choice: ')
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
                self.stdscr.addstr('Exiting the program.\n')
                self.stdscr.refresh()
                break
            else:
                self.stdscr.addstr('Invalid choice. Please try again.\n')
                self.stdscr.refresh()
        return dictionary
