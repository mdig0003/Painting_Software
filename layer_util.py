"""
Layer Util functions & definition.

No need to edit unless adding new features.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from data_structures.referential_array import ArrayR

LAYERS: ArrayR[Layer] = ArrayR(20)
cur_layer_index = 0

@dataclass
class Layer:

    index: int
    apply: function
    name: str = field(init=False)
    bg: tuple[int, int, int] | None = None

    def __post_init__(self):
        if hasattr(self.apply, "__bg__"):
            self.bg = self.apply.__bg__
        self.name = self.apply.__name__

class background(object):
    """Simple decorator to add a __bg__ property to a layer

    Usage:  @register
            @background(200, 0, 120)
            def my_special_layer(...):
    """
    def __init__(self, r, g, b):
        self.val = (r, g, b)

    def __call__(self, layer: function|Layer):
        # This could be applied before or after registration
        if isinstance(layer, Layer):
            func = layer.apply
        else:
            func = layer
        func.__bg__ = self.val
        return layer

def register(func):
    """
    Layer register function.

    Usage:  @register
            def my_special_layer(...):

    In order to actually confirm this registration,
    you'll need to import the file containing the layer definition
    """
    global cur_layer_index
    LAYERS[cur_layer_index] = Layer(cur_layer_index, func)
    cur_layer_index += 1
    return LAYERS[cur_layer_index-1]

def get_layers():
    import layers # Force all registrations to occur.
    return LAYERS
