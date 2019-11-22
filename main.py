import time
import tkinter
import random

from LightCycles.Engine import Engine
from LightCycles.TestRacer import TestRacer

from Racers.ScaredyCat import ScaredyCat

WIDTH = 100
SCREEN_WIDTH = 1000
FPS_MAX = 10
TARGET_DURATION = 1/FPS_MAX
running = True
root = tkinter.Tk()


def keydown(event):
    global running
    if event.keycode in [9, 24]:
        running = False
        root.destroy()


def main():
    global running

    # center the window when it pops up
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()
    x = (ws/2) - (SCREEN_WIDTH/2)
    y = (hs/2) - (SCREEN_WIDTH/2)
    root.geometry('%dx%d+%d+%d' % (SCREEN_WIDTH, SCREEN_WIDTH, x, y))

    s = tkinter.Canvas(root, width=SCREEN_WIDTH, height=SCREEN_WIDTH,
                       background="black", bd=0, highlightthickness=0)
    s.pack()
    s.focus_set()

    s.bind("<KeyPress>", keydown)

    e = Engine(WIDTH, SCREEN_WIDTH, s)

    # add our game objects
    """
    a = ScaredyCat(0, 0, WIDTH)
    e.add_racer(a)
    """

    for i in range(2):
        a = ScaredyCat(random.randint(0, WIDTH-1), random.randint(0, WIDTH-1), WIDTH)
        a.direction = random.randint(0, 3)
        e.add_racer(a)

    fps_text = s.create_text(10, 10, text="", font="ansifixed", anchor="w", fill="white")

    # the engine has to render the first frame seperately as all other rendering
    # is done after an update has been made to the game state
    e.draw_first()

    while running:
        t1 = time.perf_counter()
        e.update()
        running = not e.has_winner()

        # calculate extra time left in cycle and sit idle for it
        t2 = time.perf_counter()
        tdiff = t2-t1
        delay = TARGET_DURATION-tdiff

        if delay > 0:
            time.sleep(delay)

        # recalc fps to include the delay
        t2 = time.perf_counter()
        fps = 1/(t2-t1)

        s.itemconfig(fps_text, text=str(fps)[:4])

    winner = e.get_winner()
    if winner:
        print(winner.get_color(), "wins")
    else:
        print("Tie.")

    root.mainloop()


if __name__ == "__main__":
    main()
