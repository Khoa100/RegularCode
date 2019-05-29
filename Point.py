class Point:
    def __init__(self, row_init, col_init):
        self.row = row_init
        self.col = col_init

    def mid_left(self):
        return Point(self.row, self.col-1)

    def mid_right(self):
        return Point(self.row, self.col+1)

    def vert_left(self, vert_dir):
        return Point(self.row+vert_dir, self.col-1)

    def vert_center(self, vert_dir):
        return Point(self.row+vert_dir, self.col)

    def vert_right(self, vert_dir):
        return Point(self.row+vert_dir, self.col+1)

    def __repr__(self):
        return ''.join(["[", str(self.row), ",", str(self.col), "]"])

    # equality checker
    def __eq__(self, other):
        return self.row == other.row and self.col == other.col
