#!/usr/bin/env python3
#-*- coding = utf-8 -*-
 
import curses
 
def main(stdscr):
    # Color Pair
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_WHITE,  curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_CYAN,   curses.COLOR_BLACK)
 
    # Print
    stdscr.addstr(0, 0, "타잔이 ", curses.color_pair(1) | curses.A_BOLD)
    stdscr.addstr("10원", curses.color_pair(2) | curses.A_BOLD)
    stdscr.addstr("짜리 팬티를 입고", curses.color_pair(1) | curses.A_BOLD)
 
    stdscr.addstr(1, 0, "20원", curses.color_pair(2) | curses.A_BOLD)
    stdscr.addstr("짜리 칼을 차고 노래를 한다. ", curses.color_pair(1) | curses.A_BOLD)
    stdscr.addstr("아아아~", curses.color_pair(3) | curses.A_BOLD)
 
    stdscr.addstr(3, 0, "Press enter key...")
    stdscr.refresh()
 
    while True:
        try:
            k = stdscr.getkey()
            if k == "\n": break
        except KeyboardInterrupt:
            break
 
if __name__ == "__main__":
    curses.wrapper(main)

