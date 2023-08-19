from __future__ import annotations
from layer_store import SetLayerStore,AdditiveLayerStore , SequenceLayerStore
from data_structures.referential_array import ArrayR
class Grid:
    DRAW_STYLE_SET = "SET"
    DRAW_STYLE_ADD = "ADD"
    DRAW_STYLE_SEQUENCE = "SEQUENCE"
    DRAW_STYLE_OPTIONS = (
        DRAW_STYLE_SET,
        DRAW_STYLE_ADD,
        DRAW_STYLE_SEQUENCE
    )

    DEFAULT_BRUSH_SIZE = 2
    MAX_BRUSH = 5
    MIN_BRUSH = 0

    def __init__(self, draw_style, x, y) -> None: 
        self.y = y # intialising y var for grid
        self.x = x # initialising x var for grid
        self.draw_style = draw_style # initialise draw style
        self.d = self.DEFAULT_BRUSH_SIZE # initial size of brush 
        self.grid = ArrayR(y)
        for row in range(y):
            self.grid.__setitem__(row,ArrayR(x)) # setting the second array in the for loop 
            for col in range(x): # second for loop 

                if self.draw_style == self.DRAW_STYLE_SET:
                    self.grid[row][col] = SetLayerStore() # setting my item to each of the coordinates
                elif self.draw_style == self.DRAW_STYLE_ADD:
                    self.grid[row][col] = AdditiveLayerStore()
                elif self.draw_style == self.DRAW_STYLE_SEQUENCE:
                    self.grid[row][col]= SequenceLayerStore()


    def __getitem__(self,item):
        return self.grid[item]

    def increase_brush_size(self):
        if self.d <= self.MAX_BRUSH:
            self.d += 1
        # check if brush size is equal to max brush size
        # if true return max brush size 
        # if false return current brush size+1

        
    def decrease_brush_size(self):
        if self.d >= self.MIN_BRUSH: 
            self.d -= 1

        # check if brush size is equal to min brush size
        # if true return min brush size 
        # if false return current brush size-1 

    def special(self):
        for row in range(self.y):
            for col in range(self.x):
                self.grid[row][col].special()
        """
        Activate the special affect on all grid squares.
        """

    def painting(self, px , py, layer):
         for i in range(px-self.d , px+self.d+1): 
            for j in range(py-self.d, py+self.d+1):
                if i >= 0 and j >=0 and i< self.x and j < self.y:
                    self.grid[i][j+1].add(layer)
                if px - i >= 0 and py - j >= 0:
                    self.grid[i-1][j].add(layer)
                if px + i <= self.y and py + j <= self.x:
                    self.grid[i][j].add(layer)
            
