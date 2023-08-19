from main import MyWindow, run_with_func

def test_basics(window: MyWindow):
    import time
    from layers import rainbow, lighten, black
    window.on_increase_brush_size()
    window.on_increase_brush_size()
    # Brush size of 4
    # Paint
    window.on_paint(rainbow, 8, 8)
    time.sleep(1)
    # Brush size of 2
    window.on_decrease_brush_size()
    window.on_decrease_brush_size()
    window.on_paint(lighten, 10, 8)
    window.on_paint(lighten, 6, 8)
    time.sleep(1)
    # Brush size of 0
    window.on_decrease_brush_size()
    window.on_decrease_brush_size()
    window.on_paint(black, 8, 8)
    window.on_paint(black, 8, 9)
    window.on_paint(black, 8, 7)
    time.sleep(1)
    window.on_special()
    time.sleep(1)
    # Try the corner.
    window.on_increase_brush_size()
    window.on_increase_brush_size()
    window.on_increase_brush_size()
    window.on_paint(rainbow, 0, 0)

if __name__ == "__main__":
    run_with_func(test_basics)
