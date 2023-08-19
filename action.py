from __future__ import annotations
"""
Grid actions.
Should be used in replay and undo features.
"""

from dataclasses import dataclass, field
from layer_util import Layer
from grid import Grid

@dataclass
class PaintStep:

    affected_grid_square: tuple[int, int]
    affected_layer: Layer

    def undo_apply(self, grid: Grid):
        sq = grid[self.affected_grid_square[0]][self.affected_grid_square[1]]
        sq.erase(self.affected_layer)

    def redo_apply(self, grid: Grid):
        sq = grid[self.affected_grid_square[0]][self.affected_grid_square[1]]
        sq.add(self.affected_layer)


@dataclass
class PaintAction:

    steps: list[PaintStep] = field(default_factory=list)
    is_special: bool = False

    def undo_apply(self, grid: Grid):
        if self.is_special:
            grid.special()
            return
        for step in self.steps:
            step.undo_apply(grid)

    def redo_apply(self, grid: Grid):
        if self.is_special:
            grid.special()
            return
        for step in self.steps:
            step.redo_apply(grid)

    def add_step(self, step: PaintStep):
        self.steps.append(step)
