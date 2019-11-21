from .Racer import Racer


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

    def get_next_move(self, racer_positions, get_map_at):
        dr, dc = self.directions[self.direction]

        nr, nc = self.get_pos()
        nr += dr
        nc += dc

        gw = self.grid_width
        if nr >= gw or nr < 0 or nc >= gw or nc < 0 or get_map_at(nr, nc):
            self.direction += 1
            self.direction %= 4

        return self.directions[self.direction]
