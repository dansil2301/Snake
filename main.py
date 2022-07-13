import curses
from curses import wrapper
from curses.textpad import rectangle
from time import sleep
from random import randrange


def main(stdscr):
    curses.resize_term(130, 60)
    #stdscr.refresh()

    # Цвета необходимые для игры
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    GREEN_AND_BLACK = curses.color_pair(1)
    RED_AND_BLACK = curses.color_pair(2)
    YELLOW_AND_BLACK = curses.color_pair(3)

    # элементы для нахождения центра консоли
    lines = curses.LINES - 1
    col = curses.COLS - 1
    center = (int((lines + 1) / 2), int((col + 1) / 2))

    # Вывод инструкций для пользователя и окон с данными
    HEAD = 'Console snake'

    stdscr.addstr(center[0] - 10, center[1] - int(len(HEAD) / 2), HEAD, GREEN_AND_BLACK | curses.A_UNDERLINE)

    rectangle(stdscr, center[0] - 5, center[1] - 10, center[0] + 5, center[1] + 10)
    map = curses.newwin(9, 19, center[0] - 4, center[1] - 9)

    ACTION = 'Press space bar to start or to stop'
    stdscr.addstr(center[0] - 9, center[1] - int(len(ACTION) / 2), ACTION, GREEN_AND_BLACK)

    stdscr.addstr(center[0], center[1] - 32, 'score: ')

    stdscr.refresh()

    score = curses.newwin(1, 10, center[0], center[1] - 25)
    score_counter = 0
    score.addstr(str(score_counter))
    score.refresh()

    # Проверка для начала работы
    start = ''
    while start != ' ':
        start = stdscr.getkey()

    stdscr.nodelay(True)

    # 9, 19 -> center 4, 9
    # основные параметры
    y, x = 4, 9
    coords = [(y, x)]
    color = GREEN_AND_BLACK
    map.addstr(coords[0][0], coords[0][1], '0', color)
    rand_food = [randrange(1, 9), randrange(1, 19)]
    map.addstr(rand_food[0], rand_food[1], '1')
    map.refresh()
    bar = 0

    no_key = 'KEY_RIGHT'

    # вся змейка тут
    while True:

        try:
            key = stdscr.getkey()
            no_key = key
        except:
            key = no_key

        if key == 'KEY_LEFT':
            x -= 1
        elif key == 'KEY_RIGHT':
            x += 1
        elif key == 'KEY_UP':
            y -= 1
        elif key == 'KEY_DOWN':
            y += 1
        elif key == ' ':
            bar = 1
            break

        map.clear()
        map.addstr(rand_food[0], rand_food[1], '1')

        # нарушение правил
        if (y, x) in coords:
            break

        # для движения змейки
        coords.append((y, x))

        correct_snake_color = len(coords)

        for i in range(1, len(coords)):
            if i == len(coords) - 1:
                color = GREEN_AND_BLACK
            elif correct_snake_color % 2 == 0:
                color = RED_AND_BLACK
            else:
                color = YELLOW_AND_BLACK
            correct_snake_color -= 1

            # нарушение правил
            try:
                map.addstr(coords[i][0], coords[i][1], '0', color)
            except:
                correct_snake_color = -1
                break

        if correct_snake_color == -1:
            break

        if y != rand_food[0] or x != rand_food[1]:
            coords.pop(0)
        else:
            score.clear()
            score_counter += 1
            score.addstr(str(score_counter))
            score.refresh()
            rand_food = [randrange(1, 9), randrange(1, 19)]
            map.addstr(rand_food[0], rand_food[1], '1')

        map.refresh()
        if key == 'KEY_LEFT' or key == 'KEY_RIGHT':
            sleep(0.3)
        else:
            sleep(0.5)

    stdscr.nodelay(False)
    map.clear()
    if bar != 1:
        map.addstr(4, 9 - int(len('Loss') / 2), 'Loss', RED_AND_BLACK)
    else:
        map.addstr(4, 9 - int(len('Stopped manually') / 2), 'Stopped manually', RED_AND_BLACK)
    map.addstr(5, 9 - int(len('Press any key') / 2), 'Press any key', RED_AND_BLACK)
    map.refresh()
    #stdscr.refresh()
    stdscr.getch()


wrapper(main)
