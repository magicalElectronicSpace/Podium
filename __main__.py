from data import Podium_Organizer


if __name__ == '__main__':
    organizer = Podium_Organizer()
    while True:
        out = organizer.run()
        if out["switchMode"] == True:
            print("Podium Organizer Modes:")
            print("calendar - The default mode where you schedule events. The default is called Default Calendar.")
            print("todo - Another mode: Create new ToDo lists and the default is called To Do List.")
            organizer.mode = input("Enter the mode you want to enter: ")
        else:
            break
