from data import Podium_Organizer
import curses

def switch_mode_menu(stdscr):
    modes = ["calendar", "todo"]
    current_row = 0

    def print_menu(stdscr, selected_row_idx):
        stdscr.clear()
        h, w = stdscr.getmaxyx()
        x = w // 2 - max(len(row) for row in modes) // 2
        y = h // 2 - len(modes) // 2
        stdscr.addstr(y - 2, x, 'Select Mode', curses.A_BOLD)
        for idx, row in enumerate(modes):
            if idx == selected_row_idx:
                stdscr.addstr(y + idx, x, row, curses.color_pair(1))
            else:
                stdscr.addstr(y + idx, x, row)
        stdscr.refresh()

    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    print_menu(stdscr, current_row)

    while True:
        key = stdscr.getch()
        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(modes) - 1:
            current_row += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            return modes[current_row]
        print_menu(stdscr, current_row)

if __name__ == '__main__':
    organizer = Podium_Organizer()
    while True:
        out = organizer.run()
        if out["switchMode"] == True:
            curses.wrapper(lambda stdscr: setattr(organizer, 'mode', switch_mode_menu(stdscr)))
        else:
            break
