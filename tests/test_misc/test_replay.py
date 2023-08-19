import unittest
from ed_utils.decorators import number

from action import PaintAction, PaintStep
from replay import ReplayTracker
from layers import blue, green, red, invert
from grid import Grid

class TestReplay(unittest.TestCase):

    @number("5.1")
    def test_basic(self):
        grid = Grid(Grid.DRAW_STYLE_SET, 10, 10)
        control_grid = Grid(Grid.DRAW_STYLE_SET, 10, 10)

        steps1 = [PaintStep((4, 4), green), PaintStep((4, 5), green), PaintStep((5, 4), green)]
        steps2 = [PaintStep((5, 5), red), PaintStep((4, 4), red)]

        replay = ReplayTracker()
        replay.add_action(PaintAction(steps1[:]))
        replay.add_action(PaintAction(steps2[:]))
        # Do the replay
        replay.start_replay()
        v1 = replay.play_next_action(grid)
        v2 = replay.play_next_action(grid)
        v3 = replay.play_next_action(grid)
        self.assertEqual((v1, v2, v3), (False, False, True), "Wrong value returned from play_next_action")
        # Manually do
        for step in steps1 + steps2:
            step.redo_apply(control_grid)

        self.assertGridEqual(grid, control_grid)

    @number("5.2")
    def test_advanced(self):
        grid = Grid(Grid.DRAW_STYLE_SEQUENCE, 10, 10)
        control_grid = Grid(Grid.DRAW_STYLE_SEQUENCE, 10, 10)

        steps1 = [PaintStep((4, 4), green), PaintStep((4, 5), green), PaintStep((5, 4), green)]
        steps2 = [PaintStep((5, 5), red), PaintStep((4, 4), red)]
        action3 = PaintAction([], is_special=True)
        steps4 = [PaintStep((5, 5), blue)]

        replay = ReplayTracker()
        replay.add_action(PaintAction(steps1[:]))
        replay.add_action(PaintAction(steps2[:]))
        replay.add_action(action3)
        replay.add_action(action3, is_undo=True) # Undo the special.
        replay.add_action(PaintAction(steps4[:]))
        # Do the replay
        replay.start_replay()

        # Normal
        v1 = replay.play_next_action(grid)
        v2 = replay.play_next_action(grid)
        for step in steps1 + steps2:
            step.redo_apply(control_grid)
        self.assertGridEqual(grid, control_grid)

        # Special
        v3 = replay.play_next_action(grid)
        action3.redo_apply(control_grid)
        self.assertGridEqual(grid, control_grid)

        # Undo Special
        v4 = replay.play_next_action(grid)
        action3.undo_apply(control_grid)
        self.assertGridEqual(grid, control_grid)

        # Final step
        v5 = replay.play_next_action(grid)
        for step in steps4:
            step.redo_apply(control_grid)
        self.assertGridEqual(grid, control_grid)

        v6 = replay.play_next_action(grid)
        self.assertEqual((v1, v2, v3, v4, v5, v6), (False, False, False, False, False, True), "Wrong value returned from play_next_action")

    @number("5.3")
    def test_multiple_replays(self):
        grid = Grid(Grid.DRAW_STYLE_ADD, 10, 10)
        control_grid = Grid(Grid.DRAW_STYLE_ADD, 10, 10)

        steps = [PaintStep((4, 4), green), PaintStep((4, 5), green), PaintStep((5, 4), green)]
        replay = ReplayTracker()

        # Add action and play.
        replay.add_action(PaintAction(steps[:]))
        replay.start_replay()
        replay.play_next_action(grid)
        for step in steps:
            step.redo_apply(control_grid)
        self.assertGridEqual(grid, control_grid)
        self.assertEqual(replay.play_next_action(grid), True) # Finished.

        # And repeat process.
        replay.add_action(PaintAction(steps[:]))
        replay.start_replay()
        replay.play_next_action(grid)
        for step in steps:
            step.redo_apply(control_grid)
        self.assertGridEqual(grid, control_grid)
        self.assertEqual(replay.play_next_action(grid), True) # Finished.

    def assertGridEqual(self, grid1: Grid, grid2: Grid):
        for x in range(len(grid1.grid)):
            for y in range(len(grid1[x])):
                sq1 = grid1[x][y]
                sq2 = grid2[x][y]
                self.assertEqual(
                    sq1.get_color((0, 0, 0), 0, x, y),
                    sq2.get_color((0, 0, 0), 0, x, y),
                    "Grid not the same after apply has been made."
                )

