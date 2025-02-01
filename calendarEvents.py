import shutil
import os
from pathlib import Path
import curses
import sys

class EventCalendar:
    def __init__(self, config, data):
        self.config = config
        self.data = data
        self.events_dir = self.data["last_events_dir"]
        events_folder = Path(self.config["folder"]) / self.events_dir
        if not events_folder.exists():
            events_folder.mkdir(parents=True)
    
    def endWin(self):
        curses.endwin()

    def startWin(self):
        input()
        sys.stdout.write('\r')
        sys.stdout.flush()
        curses.doupdate()

    
        

    def make_calendar(self):
        self.endWin()
        name = input('Enter calendar name: ', end='')
        calendar_path = Path(self.config['folder']) / f"{name}_events"
        if not calendar_path.exists():
            os.mkdir(calendar_path)
        self.events_dir = f"{name}_events"
        print(f"Calendar '{name}' created and set as current calendar.")

    def remove_event(self):
        self.endWin()
        event_name = input("Enter the name of the event to remove: ")
        event_dir = Path(self.config['folder']) / self.events_dir / event_name
        if event_dir.exists():
            shutil.rmtree(event_dir)
            print(f"Event {event_name} removed successfully!")
        else:
            print(f"Event {event_name} does not exist.")

    def add_event(self):
        self.endWin()
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
        self.startWin()


    def load_calendar(self):
        self.endWin()
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
        self.startWin()

    def show_events(self):
        self.endWin()
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
        self.startWin()

    def list_calendars(self):
        self.endWin()
        print("Default Calendar")
        directory = Path(self.config["folder"])
        for item in os.listdir(directory):
            if item.endswith("_events"):
                print(item.removesuffix('_events'))
        self.startWin()

    def show_participants(self):
        self.endWin()
        event = input("Enter the event you want to show participants for: ")
        participants_file = Path(self.config["folder"]) / self.events_dir / event / "participants.txt"
        if participants_file.exists():
            with open(participants_file, "r") as f:
                for line in f:
                    print(line)
        else:
            print(f"No participants found for event '{event}'.")
        self.startWin()


    def delete_calendar(self):
        self.endWin()
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
        self.startWin()
    def run(self, stdscr) -> dict:
        dictionary = {"switchMode": False}
        curses.curs_set(0)
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
                    self.endWin()
                    print('Exiting the program.')
                    break
            print_menu(stdscr, current_row)
        return dictionary
