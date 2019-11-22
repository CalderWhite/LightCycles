from LightCycles.Racer import Racer


class ScaredyCat(Racer):
    direction = 0
    directions = [
        (0, 1),
        (1, 0),
        (0, -1),
        (-1, 0)
    ]

    def __init__(self, start_row, start_col, grid_width):
        super().__init__(start_row, start_col, grid_width)

    @staticmethod
    def dist_squared(x1, y1,  x2, y2):
        return (x1-x2)**2 + (y1-y2)**2

    def get_next_move(self, racer_positions, get_map_at):
        gw = self.grid_width
        r, c = self.get_pos()

        dirs = self.directions.copy()
        pos = [(r, c)]*4

        dist = []
        good_bois = []
        while len(dirs) > 0:
            for i in range(len(dirs)-1, -1, -1):
                nr, nc = pos[i]
                nr += dirs[i][0]
                nc += dirs[i][1]

                if nr >= gw or nr < 0 or nc >= gw or nc < 0 or get_map_at(nr, nc):
                    good_bois.append(dirs[i])
                    dirs.pop(i)
                    pos.pop(i)
                    d = self.dist_squared(r, c, nr, nc)
                    dist.append(d)
                else:
                    pos[i] = (nr, nc)

        return good_bois[dist.index(max(dist))]
