from LightCycles.Racer import Racer


class TestRacer(Racer):
    direction = 0
    directions = [
        (0, 1),
        (1, 0),
        (0, -1),
        (-1, 0)
    ]

    def __init__(self, start_row, start_col, grid_width):
        super().__init__(start_row, start_col, grid_width)

    def get_next_move(self, racer_positions, _map):
        r, c = self.get_pos()

        for i in range(4):
            nr, nc = (r, c)
            dr, dc = self.directions[self.direction]
            nr += dr
            nc += dc

            gw = self.grid_width
            if nr >= gw or nr < 0 or nc >= gw or nc < 0 or _map[nr][nc]:
                self.direction += 1
                self.direction %= 4
            else:
                return self.directions[self.direction]

        return [0, 0]
