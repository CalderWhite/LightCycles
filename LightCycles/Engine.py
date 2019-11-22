class Engine(object):
    racers = []
    colors = ['black', 'red', '#39FF14', 'blue', '#FA8072', '#D2691E',
              '#9966CC', 'white', '#F4A460', '#DDA0DD']

    def __init__(self, width, screen_width, screen):
        self.width = width
        self.screen_width = screen_width
        self.scaling_factor = screen_width / width
        sf = self.scaling_factor
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

    def add_racer(self, racer):
        self.racers.append(racer)
        racer.set_color(self.colors[len(self.racers)])
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
        for racer in self.racers:
            rp = racer_positions.copy()
            del rp[self.racers.index(racer)]
            ro, co = racer.get_next_move(racer_positions, self.get_map_at)

            r, c = racer.get_pos()

            moves.append([r + ro, c + co])

        for i in range(len(self.racers)-1, -1, -1):
            racer = self.racers[i]
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

            if killed:
                del self.racers[i]
            else:
                self.screen.itemconfig(self.rects[nr][nc], fill=racer.get_color())

        self.screen.update()

    def has_winner(self):
        return len(self.racers) < 2

    def get_winner(self):
        if len(self.racers) == 0:
            return None
        else:
            return self.racers[0]
