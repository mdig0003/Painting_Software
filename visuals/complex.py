from main import MyWindow, run_with_func

def test_styles(window: MyWindow):
    import time
    from layers import rainbow, lighten, black, invert
    # Set draw mode
    window.on_paint(black, 0, 0)
    window.on_paint(black, 31, 31)
    window.on_paint(rainbow, 0, 31)
    time.sleep(0.5)
    window.on_redo() # Nothing
    window.on_undo()
    time.sleep(0.3)
    window.on_undo()
    time.sleep(0.3)
    window.on_redo()
    window.on_special()
    time.sleep(1)
    window.start_replay()
    time.sleep(2)
    # Additive draw mode
    window.change_draw_mode()
    window.on_increase_brush_size()
    window.on_increase_brush_size()
    window.on_increase_brush_size()
    for point in [
        (15, 15),
        (17, 17),
        (19, 17),
        (21, 18),
    ]:
        window.on_paint(rainbow, point[0], point[1])
        time.sleep(0.1)
    time.sleep(0.9)
    for _ in range(4):
        window.on_undo()
        time.sleep(0.1)
    time.sleep(0.9)
    for _ in range(2):
        window.on_redo()
        time.sleep(0.1)
    window.on_decrease_brush_size()
    window.on_decrease_brush_size()
    for point in [
        (15, 15),
        (17, 17),
        (19, 17),
        (21, 18),
    ]:
        window.on_paint(lighten, point[0], point[1])
        time.sleep(0.1)
    for _ in range(4):
        window.on_redo() # Should do nothing
        time.sleep(0.2)
    for _ in range(3):
        window.on_undo()
        time.sleep(0.3)
    time.sleep(0.5)
    window.start_replay()
    time.sleep(2)
    # Sequential draw mode
    window.change_draw_mode()
    window.on_paint(rainbow, 10, 20)
    time.sleep(0.2)
    window.on_paint(rainbow, 20, 10)
    time.sleep(0.2)
    window.on_paint(rainbow, 15, 15)
    time.sleep(0.2)
    window.on_paint(rainbow, 10, 10)
    time.sleep(0.2)
    window.on_paint(rainbow, 20, 20)
    for _ in range(4): # nothing
        window.on_redo()
        time.sleep(0.1)
    for _ in range(4):
        window.on_undo()
        time.sleep(0.1)
        window.on_undo()
        time.sleep(0.1)
        window.on_redo()
        time.sleep(0.3)
    window.on_paint(black, 0, 0)
    time.sleep(0.4)
    window.on_redo() # Do nothing
    time.sleep(1)
    window.start_replay()
    time.sleep(2)



if __name__ == "__main__":
    run_with_func(test_styles, True)
