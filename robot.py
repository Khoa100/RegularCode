from map import Map
from Point import Point
from Constants import MIDDLE_TRACK, GOOD_NUM_TEST_RUNS


class OptimizedRobot:
    def __init__(self):
        # start at location (row=0, col=0)
        self.start = Point(0, 0)
        self.track = [self.start]

        self.loc = self.start   # current location
        self.vert_dir = 1       # signifies going 'down'
        self.pos = 'left'       # on edge of 3-lane 'track'
        self.map = None         # the map of dirty locations

    # changes robots vertical direction from up to down or vice-versa
    def change_vert_direction(self):
        # python ternary operator
        self.vert_dir = 1 if self.vert_dir == -1 else -1

    # if the robot is in a center track (track of width 3)
    def is_centered(self):
        return self.loc.col in MIDDLE_TRACK

    # if we're on the upper row bound of the grid
    def is_on_upper_bound(self):
        return self.loc.row == 0

    # if we're on the lower row bound of the grid
    def is_on_lower_bound(self):
        return self.loc.row == self.map.get_upper_bound()

    # used for changing tracks
    def right_shift(self, shift_amt):
        for i in range(shift_amt):
            self.loc = self.loc.mid_right()  # move right
            if self.map.is_dirty(self.loc):
                self.map.clean(self.loc)
            self.track.append(self.loc)  # update track

    # Optimize cleaning when on the left
    def optimize_side(self, side, is_digonal_dirty):
        if side == 'left':
            self.loc = self.loc.mid_left()  # move left
            self.map.clean(self.loc)  # and clean
            self.track.append(self.loc)  # update track
            self.pos = 'left'
        else:
            self.loc = self.loc.mid_right()  # move right
            self.map.clean(self.loc)  # and clean
            self.track.append(self.loc)  # update track
            self.pos = 'right'
        if is_digonal_dirty:
            self.loc = self.loc.vert_center(self.vert_dir)  # move down
            self.map.clean(self.loc)  # and clean
            self.track.append(self.loc)  # update track
            self.recenter()
        elif side == 'left':
            self.loc = self.loc.vert_right(self.vert_dir)  # move diagonally to the center
            self.track.append(self.loc)  # update track
        else:
            self.loc = self.loc.vert_left(self.vert_dir)  # move diagonally to the center
            self.track.append(self.loc)  # update track

    def display_state(self):
        print('\n\n--------------Map-------------')
        self.map.show()
        print('---------Robot Status---------')
        print('\tMoves: %d' % (len(self.track) - 1))
        print('\tLocation: ', self.loc)
        print('\tOn vertical boundary?: ', (self.is_on_upper_bound() or self.is_on_lower_bound()), '\n')

    def recenter(self):
        if self.pos == 'left':
            self.loc = self.loc.mid_right()
            self.track.append(self.loc)
        elif self.pos == 'right':
            self.loc = self.loc.mid_left()
            self.track.append(self.loc)

    # iterates over the map and cleans dirty locations
    def clean(self, task: Map):
        # set the map as a class variable
        self.map = task

        # should be able to simplify this logic into just a while
        # can't think that well right now though
        while self.loc.col <= MIDDLE_TRACK[-1]+1:
            # check if it's on the last iteration, naive. group later
            if (
                self.loc.col == MIDDLE_TRACK[-1] and
                self.is_on_upper_bound()
            ):
                if self.map.is_dirty(self.loc.mid_left()):
                    self.loc = self.loc.mid_left()
                    self.map.clean(self.loc)
                    self.track.append(self.loc)
                    self.loc = self.loc.mid_right()
                    self.track.append(self.loc)
                break

          #  self.display_state()

            if self.map.is_dirty(self.loc):
                self.map.clean(self.loc)

            # check if we should switch to the next track
            # note that we are going left to right

            # on bottom moving down or on top moving up
            # (note that when we shift to a new track, we'll be on the bottom row.
            #  we wouldn't want to shift again, because now we have to go up
            if (
                    self.is_on_lower_bound() and self.vert_dir == 1 or
                    self.is_on_upper_bound() and self.vert_dir == -1
            ):
                if not self.is_centered() and self.pos == 'right':
                    self.right_shift(2)
                    self.change_vert_direction()
                    continue
                # if we're in the center and the row is clean
                elif (
                        self.is_centered() and
                        not self.map.is_dirty(self.loc.mid_left()) and
                        not self.map.is_dirty(self.loc.mid_right())
                ):
                    self.right_shift(3)
                    self.change_vert_direction()
                    continue

            if not self.is_centered():
                if self.pos == 'left':
                    self.loc = self.loc.mid_right()
                    self.track.append(self.loc)
                    continue
                elif self.pos == 'right':
                    self.loc = self.loc.mid_left()
                    self.track.append(self.loc)
                    continue

            # check if a side is dirty
            if self.map.is_dirty(self.loc.mid_left()):
                if self.map.is_dirty(self.loc.mid_right()) or self.is_on_lower_bound() or self.is_on_upper_bound():
                    self.loc = self.loc.mid_left()   # move left
                    self.map.clean(self.loc)         # and clean
                    self.track.append(self.loc)      # update track
                    self.pos = 'left'
                else:
                    self.optimize_side('left', self.map.is_dirty(self.loc.vert_left(self.vert_dir)))
            elif self.map.is_dirty(self.loc.mid_right()):
                if self.map.is_dirty(self.loc.mid_left()) or self.is_on_lower_bound() or self.is_on_upper_bound():
                    self.loc = self.loc.mid_right()  # move right
                    self.map.clean(self.loc)         # and clean
                    self.track.append(self.loc)      # update track
                    self.pos = 'right'
                else:
                    self.optimize_side('right', self.map.is_dirty(self.loc.vert_right(self.vert_dir)))

            # left diagonal is dirty
            elif self.map.is_dirty(self.loc.vert_left(self.vert_dir)):
                self.loc = self.loc.vert_left(self.vert_dir)
                self.track.append(self.loc)
                self.map.clean(self.loc)

                self.loc = self.loc.mid_right()  # return to center
                self.track.append(self.loc)

            # right diagonal is dirty
            elif self.map.is_dirty(self.loc.vert_right(self.vert_dir)):
                self.loc = self.loc.vert_right(self.vert_dir)
                self.track.append(self.loc)
                self.map.clean(self.loc)

                self.loc = self.loc.mid_left()  # return to center
                self.track.append(self.loc)

            # center is dirty, and diagonals aren't
            elif self.map.is_dirty(self.loc.vert_center(self.vert_dir)):
                self.loc = self.loc.vert_center(self.vert_dir)
                self.map.clean(self.loc)
                self.track.append(self.loc)

            # if nothing is dirty, but we're not on an edge
            # we'll get stuck otherwise!
            # 0 0 0
            # 0 0 0
            # 1 1 1
            elif (
                ((not self.is_on_upper_bound()) and self.vert_dir == -1) or
                ((not self.is_on_lower_bound()) and self.vert_dir == 1)
            ):
                if self.is_centered():
                    self.loc = self.loc.vert_center(self.vert_dir)
                    self.track.append(self.loc)
                elif self.pos == 'left':
                    self.loc = self.loc.mid_right(self.vert_dir)
                    self.track.append(self.loc)
                elif self.pos == 'right':
                    self.loc = self.loc.mid_left(self.vert_dir)
                    self.track.append(self.loc)

            # need to check if row is clean first

            # just recenter for simplicity
            if not self.is_centered():
                self.recenter()

            if self.map.is_dirty(self.loc):
                self.map.clean(self.loc)

        # clean the last column
        if self.is_centered():
            self.right_shift(2)
        elif self.pos == 'left':
            self.right_shift(3)
        elif self.pos == 'right':
            self.right_shift(1)

        # we're moving down the last column now
        self.change_vert_direction()

        while not self.is_on_lower_bound():
            if self.map.is_dirty(self.loc):  # if it's dirty
                self.map.clean(self.loc)     # clean it
            self.loc = self.loc.vert_center(self.vert_dir)
            self.track.append(self.loc)
        #    self.display_state()

        # clean the very last square if it's dirty
        if self.map.is_dirty(self.loc):  # if it's dirty
            self.map.clean(self.loc)

    def show(self):
        print('Number of steps: ', len(self.track) - 1)

        # requirement of the assignment
        assert len(self.track) < self.map.get_map_size()


def record_run(avg):
    # open file for reading and writing
    with open('history.txt', 'r') as f:
        best_run = f.readline()

    if avg < int(best_run):
        print('you beat your record, nice optimization!')
        with open('history.txt', 'w') as f:
            f.write(str(avg))
    else:
        print('nice try, optimization didn\'t work though')
        print('best avg. run: ', best_run)


def run_many_optimized(num_runs):
    track_len = 0
    for _ in range(num_runs):
        m = Map(19, 19)
        a = OptimizedRobot()
        a.clean(m)
        track_len += len(a.track)
        assert m.is_clean()
    avg = round(track_len / num_runs)
    record_run(avg)
    print('Avg. track length: ', avg)


if __name__ == '__main__':
    # home = Map(19, 19)
    # agent = OptimizedRobot()
    # agent.clean(home)
    # agent.show()
    # home.show()

    run_many_optimized(GOOD_NUM_TEST_RUNS)
