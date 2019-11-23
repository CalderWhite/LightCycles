import multiprocessing as mp


def get_next_move(inp):
    racer_get_next_move, racer_positions, Map, i = inp
    return racer_get_next_move(racer_positions, Map), i


class Engine(object):
    racers = []
    colors = ['black', 'red', '#39FF14', 'blue', '#FA8072', '#D2691E']
    tracer_colors = ['black', '#FF8888', '#B9FFAB', '#4A4AFF', '#FFB6AD', '#E69053']

    def __init__(self, width, screen_width, screen, render=True):
        self.width = width
        self.screen_width = screen_width
        self.scaling_factor = screen_width / width
        sf = self.scaling_factor
        self.render = render
        self.screen = screen
        self.map = [[0]*width for i in range(width)]
        self.rects = [
            [
                screen.create_rectangle(c*sf, r*sf, c*sf + sf, r*sf + sf,
                                        outline="")
                for c in range(width)
            ]
            for r in range(width)
        ]
        self.pool = mp.Pool(mp.cpu_count())

    def add_racer(self, racer):
        self.racers.append(racer)
        print(len(self.racers))
        racer.set_color(self.colors[len(self.racers)])
        racer.set_tracer_color(self.tracer_colors[len(self.racers)])
        racer.set_index(len(self.racers))
        r, c = racer.get_pos()
        self.map[r][c] = len(self.racers)

    def get_map_at(self, r, c):
        val = 0
        try:
            val = self.map[r][c]
        except IndexError:
            pass

        return val

    def draw_first(self):
        for racer in self.racers:
            r, c = racer.get_pos()
            self.screen.itemconfig(self.rects[r][c], fill=racer.get_color())

    def update(self):
        racer_positions = [i.get_pos() for i in self.racers]
        moves = []

        # first get all the moves to prevent an unfair advantage
        directions = self.pool.map(get_next_move,
                                   [[self.racers[i].get_next_move,
                                     racer_positions, self.map, i]
                                    for i in range(len(self.racers))])
        directions.sort(key=lambda x: x[1])

        for i in range(len(self.racers)):
            rp = racer_positions.copy()
            del rp[self.racers.index(self.racers[i])]
            ro, co = directions[i][0]

            r, c = self.racers[i].get_pos()

            moves.append([r + ro, c + co])

        for i in range(len(self.racers)-1, -1, -1):
            racer = self.racers[i]
            r, c = racer.get_pos()
            nr, nc = moves[i]

            killed = True if moves.count([nr, nc]) > 1 else False

            try:
                if not self.map[nr][nc]:
                    self.map[nr][nc] = racer.get_index()
                    racer.update_pos(nr, nc)
                else:
                    killed = True
            except IndexError:
                killed = True

            if self.render:
                self.screen.itemconfig(self.rects[nr][nc], fill=racer.get_tracer_color())

            if killed:
                del self.racers[i]
            else:
                if self.render:
                    self.screen.itemconfig(self.rects[r][c], fill=racer.get_color())

        if self.render:
            self.screen.update()

    def has_winner(self):
        return len(self.racers) < 2

    def get_winner(self):
        if len(self.racers) == 0:
            return None
        else:
            return self.racers[0]
