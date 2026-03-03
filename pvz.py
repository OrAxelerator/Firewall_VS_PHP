import curses
from curses import wrapper
import time
import random
from bruitage import play_sound


PARAMETRE = {
    "zombie_speed":8, # vitesse zombie
    "soleil":35, # power de départ
    "app_zombie":40, # vitesse d'apparition
    "bruitage":True, 
    "bonus":25 # combien de power par calcule

}



def new_calc():
    a = random.randint(1, 9)
    b = random.randint(1, 9)
    if random.choice([True, False]):
        return f"{a} + {b}", a + b
    else:
        return f"{a} x {b}", a * b


def draw_map(stdscr, rows, cols, grid):
    for y in range(rows):
        for x in range(cols):
            char = grid[y][x] if grid[y][x] != " " else "_"
            stdscr.addstr(y, x*2 + 3, char)

BITCOIN = 1
FIREWALL = 2
REQUETE = 3

def game(stdscr):
    curses.init_pair(BITCOIN, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(FIREWALL, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(REQUETE, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.timeout(80)
    rows, cols = 5, 8
    grid = [[" " for _ in range(cols)] for _ in range(rows)]
    zombies = []
    stdscr.clear()
    tick = 0
    zombie_speed = PARAMETRE["zombie_speed"]
    soleil = PARAMETRE["soleil"]
    app_zombie = PARAMETRE["app_zombie"]
    expr, result = new_calc()
    answer = ""

    
    special_map = {
        ord('a'): 0,
        ord('z'): 1,
        ord('e'): 2,
        ord('r'): 3,
        ord('t'): 4
    }
    letters = ["a", "z", "e", "r", "t"]
    for i in range(len(letters)):
        stdscr.addstr(i, 0, f"{letters[i]} |")
    draw_map(stdscr, rows, cols, grid)
    stdscr.refresh()

    play_sound("in.mp3", PARAMETRE["bruitage"])

    while True:

        #apparition zombie
        if tick % app_zombie == 0:
            zy = random.randint(0, rows-1)
            zombies.append([zy, cols-1])

        # avancement
        if tick % zombie_speed == 0:
            new_zombies = []
            for z in zombies:
                y, x = z

                if x > 0 and grid[y][x-1] == "P":
                    grid[y][x-1] = " "
                    play_sound("died.mp3", PARAMETRE["bruitage"])
                    stdscr.addstr(y, (x-1)*2 + 3, "_")
                    stdscr.addstr(y, (x)*2 + 3, "_")
                    continue

                if x > 0:
                    new_zombies.append([y, x-1])
                else:
                    play_sound("end.mp3", PARAMETRE["bruitage"])
                    play_sound("end2.mp3", PARAMETRE["bruitage"])
                    stdscr.addstr(rows + 4, 0, "GAME OVER", curses.color_pair(FIREWALL))
                    stdscr.addstr(rows + 5, 0, "Le serveur c'est fait DDOS et a incendié tout le batiment de l'entreprise", curses.color_pair(FIREWALL))
                    
                    stdscr.refresh()
                    stdscr.nodelay(False)

                    stdscr.getch()
                    return

                stdscr.addstr(y, x*2 + 3, "_")

            zombies = new_zombies

        for y, x in zombies:
            if x >= 0:
                stdscr.addstr(y, x*2 + 3, "Z", curses.color_pair(REQUETE))

        key = stdscr.getch()


        if key in special_map and soleil >= 50:
            play_sound("click.mp3", PARAMETRE["bruitage"])
            row = special_map[key]
            for x in range(cols):
                if grid[row][x] != "P":
                    grid[row][x] = "P"
                    soleil -= 50
                    stdscr.addstr(row, x*2 + 3, "P", curses.color_pair(FIREWALL))
                    break
        if ord('0') <= key <= ord('9'):
            if len(answer) < 2:
                answer += chr(key)

        if key == 10:
            if answer == str(result):
                soleil += PARAMETRE["bonus"]
                
            answer = ""
            expr, result = new_calc()

        stdscr.addstr(rows + 1, 0, f"Firewall Power : {soleil}   ", curses.color_pair(BITCOIN))
        stdscr.addstr(rows + 2, 0, f"{expr} = {answer}   ")

        stdscr.refresh()
        tick += 1
        time.sleep(0.05)

def main():
    wrapper(game)