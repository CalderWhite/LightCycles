import time
import tkinter

from LightCycles.Engine import Engine
from LightCycles.TestRacer import TestRacer

WIDTH = 100
SCREEN_WIDTH = 1000
FPS_MAX = 60
TARGET_DURATION = 1/FPS_MAX
running = True


def keydown(event):
    global running
    if event.keycode == 9:
        running = False


def main():
    root = tkinter.Tk()

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

    # add our game objects
    e = Engine(WIDTH, SCREEN_WIDTH, s)
    a = TestRacer(0, 0, WIDTH)
    e.add_racer(a)
    b = TestRacer(WIDTH-1, WIDTH-1, WIDTH)
    b.direction = 2
    e.add_racer(b)

    # perf_counter() is perferred to time() as of 3.smth
    t1 = time.perf_counter()
    t2 = None
    fps_text = s.create_text(10, 10, text="", font="ansifixed", anchor="w", fill="white")

    # the engine has to render the first frame seperately as all other rendering
    # is done after an update has been made to the game state
    e.draw_first()

    # using tk.mainloop() is preferred to using a while True loop for reasons you
    # can google. The way it works is a little weird so I can restructure this tmrw
    # since i've done it b4.
    while running:
        e.update()

        # calculate extra time left in cycle and sit idle for it
        t2 = time.perf_counter()
        tdiff = t2-t1
        delay = TARGET_DURATION-tdiff
        if delay > 0:
            time.sleep(delay)

        # display fps, no int calls pls
        fps = 1/(tdiff)
        s.itemconfig(fps_text, text=str(fps)[:4])

        t1 = t2

    root.destroy()


if __name__ == "__main__":
    main()
