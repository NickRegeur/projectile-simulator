
def update_projectile(main_window):

    #motion
    canvas = main_window.canvas
    r = canvas.ball_radius

    dt = 0.016

    canvas.vy += canvas.g * dt
    canvas.ball_x += canvas.vx * dt
    canvas.ball_y += canvas.vy * dt

    canvas.path_points.append((canvas.ball_x, canvas.ball_y))

    max_points = 800
    if len(canvas.path_points) > max_points:
        canvas.path_points.pop(0)

    width = canvas.width()
    height = canvas.height()

    restitution = canvas.wall_restitution

    # LEFT WALL
    if canvas.ball_x - r < 0:
        canvas.ball_x = r
        canvas.vx = -canvas.vx * restitution

    # RIGHT WALL
    if canvas.ball_x + r > width:
        canvas.ball_x = width - r
        canvas.vx = -canvas.vx * restitution

    # CEILING
    if canvas.ball_y - r < 0:
        canvas.ball_y = r
        canvas.vy = -canvas.vy * restitution

    # GROUND (original)
    if canvas.ball_y + r > height:

        # clamp to ground
        canvas.ball_y = height - r

        # bounce physics
        floor_restitution = 0.7
        friction = 0.98

        canvas.vy = -canvas.vy * floor_restitution
        canvas.vx = canvas.vx * friction

        # stop if the bounce is basically dead
        if abs(canvas.vy) < 5 and abs(canvas.vx) < 5:
            canvas.vy = 0.0
            canvas.vx = 0.0
            return False

    return True