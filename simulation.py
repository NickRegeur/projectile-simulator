
def update_projectile(main_window):

    canvas = main_window.canvas
    r = canvas.ball_radius

    dt = 0.016

    canvas.vy += canvas.g * dt
    canvas.ball_x += canvas.vx * dt
    canvas.ball_y += canvas.vy * dt

    canvas.path_points.append((canvas.ball_x, canvas.ball_y))

    ground_y = canvas.height()

    if canvas.ball_y + r > ground_y:
        canvas.ball_y = ground_y - r
        canvas.vy = 0.0
        canvas.vx = 0.0
        main_window.is_running = False