import curses
import random
import time
from curses import wrapper


def init_pairs():
    # color pairs, second color is background
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_RED)


def display_welcome_text(stdscr):
    stdscr.clear()
    stdscr.addstr("Hello, if you want to start the game, press any button (Esc to terminate)")
    stdscr.getkey()


def getRandomSentence():
    file = open('randomTexts.txt', 'r')
    lines = file.readlines()
    return random.choice(lines).strip()


def init_text(stdscr):
    text = getRandomSentence()
    stdscr.clear()
    stdscr.addstr(text, curses.color_pair(1))
    stdscr.addstr(2, 0, f"WPM: 0")
    return text


def process(stdscr, text, curr_text):
    stdscr.clear()
    stdscr.addstr(text, curses.color_pair(3))
    for i in range(len(curr_text)):
        color = curses.color_pair(2)
        char = curr_text[i]
        if text[i] != curr_text[i]:
            color = curses.color_pair(1)
            char = text[i]
            if char == ' ':
                color = curses.color_pair(4)
        stdscr.addstr(0, i, char, color)


def monkey_type(stdscr):
    text = init_text(stdscr)
    curr_text = []
    start_time = time.time()
    # to not wait for key press and display WPM every second
    stdscr.nodelay(True)

    while True:
        # 1 is needed to not get division by zero
        time_elapsed = max(time.time() - start_time, 1)
        wpm = round((len(curr_text) / (time_elapsed / 60)) / 5)
        stdscr.addstr(2, 0, f"WPM: {wpm}")
        try:
            curr_char = stdscr.getkey()
        except:
            continue
        if ord(curr_char) == 27:
            break
            # backspaces on different platforms
        if curr_char in ("KEY_BACKSOACE", '\b', "\x7f"):
            if len(curr_text) > 0:
                curr_text.pop()
        else:
            curr_text.append(curr_char)
        process(stdscr, text, curr_text)
        if "".join(curr_text) == text:
            stdscr.nodelay(False)
            break


def main(stdscr):
    init_pairs()
    display_welcome_text(stdscr)
    while True:
        monkey_type(stdscr)
        stdscr.addstr(3, 0, "Great job! You completed the text! Press any key to continue (Esc to terminate)",
                      curses.color_pair(3))
        key = stdscr.getkey()
        if ord(key) == 27:
            break


wrapper(main)
