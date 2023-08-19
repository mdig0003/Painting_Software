import unittest
from ed_utils.decorators import number

from action import PaintAction, PaintStep
from undo import UndoTracker
from layers import green, red, blue
from grid import Grid

class TestUndo(unittest.TestCase):

    @number("4.1")
    def test_basic(self):
        grid = Grid(Grid.DRAW_STYLE_SET, 10, 10)
        control_grid = Grid(Grid.DRAW_STYLE_SET, 10, 10)

        steps1 = [PaintStep((4, 4), green), PaintStep((4, 5), green), PaintStep((5, 4), green)]
        steps2 = [PaintStep((5, 5), red), PaintStep((4, 4), red)]
        steps3 = [PaintStep((5, 5), blue), PaintStep((4, 5), blue), PaintStep((6, 6), blue)]

        undo = UndoTracker()

        undo.add_action(PaintAction(
            steps1[:],
            False
        ))
        undo.add_action(PaintAction(
            steps2[:],
            False
        ))
        for step in steps1 + steps2:
            step.redo_apply(grid)
            step.redo_apply(control_grid)
        self.assertGridEqual(grid, control_grid)

        action = undo.undo(grid)
        self.assertNotEqual(action, None, "Wrong return value")
        self.assertEqual(action.steps, steps2, "Wrong steps undone")
        for step in steps2:
            step.undo_apply(control_grid)
        self.assertGridEqual(grid, control_grid)

        undo.add_action(PaintAction(
            steps3[:],
            False
        ))
        for step in steps3:
            step.redo_apply(grid)
            step.redo_apply(control_grid)
        self.assertGridEqual(grid, control_grid)

        action = undo.undo(grid)
        self.assertNotEqual(action, None, "Wrong return value")
        self.assertEqual(action.steps, steps3, "Wrong steps undone")
        for step in steps3:
            step.undo_apply(control_grid)
        self.assertGridEqual(grid, control_grid)

        action = undo.undo(grid)
        self.assertNotEqual(action, None, "Wrong return value")
        self.assertEqual(action.steps, steps1, "Wrong steps undone")
        for step in steps1:
            step.undo_apply(control_grid)
        self.assertGridEqual(grid, control_grid)

        action = undo.undo(grid)
        self.assertEqual(action, None)

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

