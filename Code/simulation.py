
def update_projectile(main_window):

    #motion
    canvas = main_window.canvas
    r = canvas.ball_radius

    dt = 0.016


    canvas.vy += canvas.g * dt
    canvas.ball_x += canvas.vx * dt
    canvas.ball_y += canvas.vy * dt

    canvas.path_points.append((canvas.ball_x, canvas.ball_y))

    ground_y = canvas.height()

    #bounce
    if canvas.ball_y + r > ground_y:

        # clamp to ground
        canvas.ball_y = ground_y - r

        # bounce physics
        restitution = 0.7
        friction = 0.98

        canvas.vy = -canvas.vy * restitution
        canvas.vx = canvas.vx * friction

        # stop if the bounce is basically dead
        if abs(canvas.vy) < 5 and abs(canvas.vx) < 5:
            canvas.vy = 0.0
            canvas.vx = 0.0
            return False

    return True

