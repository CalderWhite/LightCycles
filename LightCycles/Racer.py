class Racer(object):
    def __init__(self, start_row, start_col, grid_width):
        self.row = start_row
        self.col = start_col
        self.grid_width = grid_width

        # None so that an error is thrown if the renderer tries to render an object
        # that has not been initialized by the Engine
        self.color = None
        self.tracer_color = None
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

    def get_tracer_color(self):
        return self.tracer_color

    def set_tracer_color(self, tracer_color):
        self.tracer_color = tracer_color

    def get_index(self):
        return self.index

    def set_index(self, index):
        self.index = index
