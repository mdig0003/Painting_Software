"""
All layers are defined here.
"""

import colorsys
from layer_util import background, register

@register
@background(200, 0, 120)
def rainbow(color, timestamp, x, y):
    return tuple(
        int(255*x)
        for x in colorsys.hls_to_rgb((timestamp/20 + x/20 + y/20)%1, 0.6, 0.6)
    )

@register
@background(170, 170, 170)
def black(color, timestamp, x, y):
    return (0, 0, 0)

@register
@background(240, 240, 240)
def lighten(color, timestamp, x, y):
    return tuple(
        min(255, x + 40)
        for x in color
    )

@register
@background(0, 255, 255)
def invert(color, timestamp, x, y):
    return tuple(
        255 - c
        for c in color
    )

@register
@background(255, 0, 0)
def red(color, timestamp, x, y):
    return (255, 0, 0)

@register
@background(0, 255, 0)
def green(color, timestamp, x, y):
    return (0, 255, 0)

@register
@background(0, 0, 255)
def blue(color, timestamp, x, y):
    return (0, 0, 255)

@register
@background(100, 170, 255)
def sparkle(color, timestamp, x, y):
    ts = int((timestamp + x/3 + y/5) * 3)
    other = x
    for _ in range(10 + (ts * 31 % 17)):
        other = (1103515245 * other + 12345) % (1 << 31)
    other += y
    for _ in range(10 + (ts * 31 % 17)):
        other = (1103515245 * other + 12345) % (1 << 31)
    ts = int((timestamp + x/10 + y/20) * 3)
    other = (other & ((1 << 31)-1)) >> 16
    if other/(1 << 15) < 0.1:
        return lighten.apply(color, timestamp, x, y)
    return darken.apply(color, timestamp, x, y)

@register
@background(30, 30, 30)
def darken(color, timestamp, x, y):
    return tuple(
        max(0, x - 40)
        for x in color
    )
