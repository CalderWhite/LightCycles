from LightCycles.Racer import Racer


class FieldFinder(Racer):
    direction = 0
    directions = [
        (0, 1),
        (1, 0),
        (0, -1),
        (-1, 0)
    ]

    def __init__(self, start_row, start_col, grid_width, use_dist=False):
        super().__init__(start_row, start_col, grid_width)
        self.use_dist = use_dist

    @staticmethod
    def dist_squared(x1, y1,  x2, y2):
        x = x1-x2
        y = y1-y2
        return x*x + y*y

    def get_dir_dists_sqrd(self, pos, get_map_at):
        gw = self.grid_width
        r, c = pos

        dirs = self.directions.copy()
        # never consider going backwards
        pos = [(r, c)]*4

        dist = []
        good_bois = []
        good_pos = []
        while len(dirs) > 0:
            for i in range(len(dirs)-1, -1, -1):
                nr, nc = pos[i]
                nr += dirs[i][0]
                nc += dirs[i][1]

                if nr >= gw or nr < 0 or nc >= gw or nc < 0 or get_map_at(nr, nc):
                    good_bois.append(dirs[i])
                    # append the position instead of the new one, since the new one
                    # gets you killed
                    good_pos.append(pos[i])
                    dirs.pop(i)
                    pos.pop(i)
                    d = self.dist_squared(r, c, nr, nc)
                    dist.append(d)
                else:
                    pos[i] = (nr, nc)

        return dist, good_bois, good_pos

    def get_areas(self, dir, dists, dirs, positions, get_map_at):
        # do not consider going backwards
        dir_inv = (-dir[0], -dir[1])
        dir_inv_i = dirs.index(dir_inv)
        dists.pop(dir_inv_i)
        dirs.pop(dir_inv_i)
        positions.pop(dir_inv_i)

        good_dirs = []
        areas = []
        good_pos = []

        for i in range(len(dirs)):
            _d = dists[i]
            # if the dist is 1 that means it is an instant death move
            if _d == 1:
                continue
            _dir = dirs[i]
            _pos = positions[i]

            _ds, _dr, _ps = self.get_dir_dists_sqrd(_pos, get_map_at)

            # do not consider going backwards
            # otherwise the area would be deceptively large
            _dir_inv = (-_dir[0], -_dir[1])
            _dir_inv_i = _dr.index(_dir_inv)
            _ds.pop(_dir_inv_i)
            _dr.pop(_dir_inv_i)
            _ps.pop(_dir_inv_i)

            fwd_i = _dr.index(_dir)
            _dr.pop(fwd_i)
            _ps.pop(fwd_i)

            # this has no matching pair as backwards is not feasible
            fwd_dist = _ds.pop(fwd_i)

            # the remaining distances create the perpendicular width
            side_dist = sum(_ds)

            area = fwd_dist * side_dist
            areas.append(area)
            good_dirs.append(_dir)
            good_pos.append(_pos)

        return areas, good_dirs, good_pos


    def get_next_move(self, racer_positions, get_map_at):
        dists, dirs, positions = self.get_dir_dists_sqrd(self.get_pos(), get_map_at)

        # area based choice
        if self.use_dist:
            return dirs[dists.index(max(dists))]

        dir = self.directions[self.direction]
        areas, good_dirs, good_pos = self.get_areas(dir, dists, dirs, positions, get_map_at)

        """
        for i in range(3):
            for j in range(len(good_dirs)):
                _dr = good_dirs[j]
                _ps = good_pos[j]

                _ps[0] -= _dr[0]
                _ps[1] -= _dr[1]
        """

        choice = [0, 0]
        if len(areas) > 0:
            choice = good_dirs[areas.index(max(areas))]
            self.direction = self.directions.index(choice)

        return choice
