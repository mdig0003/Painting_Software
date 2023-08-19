from __future__ import annotations
from action import PaintAction 
from grid import Grid
from data_structures.stack_adt import ArrayStack

class UndoTracker:
    def __init__(self) -> None:
        self.stack_tracker = ArrayStack(10000)
        self.placeholder_stack = ArrayStack(10000)

    def add_action(self, action: PaintAction) -> None:
        """
        Adds an action to the undo tracker.

        If your collection is already full,
        feel free to exit early and not add the action.
        """
        if not self.stack_tracker.is_full():
            self.stack_tracker.push(action)

        
    def undo(self, grid: Grid) -> PaintAction|None:
        """
        Undo an operation, and apply the relevant action to the grid.
        If there are no actions to undo, simply do nothing.

        :return: The action that was undone, or None.
        """
        
        if not self.stack_tracker.is_empty():
            action_undo = self.stack_tracker.pop()
            action_undo.undo_apply(grid)
            self.placeholder_stack.push(action_undo)
            return action_undo

    def redo(self, grid: Grid) -> PaintAction|None:
        """
        Redo an operation that was previously undone.
        If there are no actions to redo, simply do nothing.

        :return: The action that was redone, or None.
        """
        if not self.stack_tracker.is_empty():
            action_redo = self.placeholder_stack.pop()
            action_redo.redo_apply(action_redo, grid)
            self.stack_tracker.push(action_redo)
            return action_redo
            

