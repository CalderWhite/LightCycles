class Racer(object):
    def __init__(self, start_row, start_col, grid_width):
        self.row = start_row
        self.col = start_col
        self.grid_width = grid_width
        self.color = "black"
        self.index = 0

    def update_pos(self, row, col):
        self.row = row
        self.col = col

    def get_pos(self):
        return self.row, self.col

    def get_color(self):
        return self.color

    def set_color(self, color):
        self.color = color

    def get_index(self):
        return self.index

    def set_index(self, index):
        self.index = index
