def detect_goal(camera):

    img = camera.getImage()
    w = camera.getWidth()
    h = camera.getHeight()

    if img is None:
        return False

    g = 0
    t = 0

    for dx in range(-5, 6):
        for dy in range(-4, 5):

            x = w // 2 + dx
            y = h // 2 + dy

            if x < 0 or x >= w or y < 0 or y >= h:
                continue

            r = camera.imageGetRed(img, w, x, y)
            gr = camera.imageGetGreen(img, w, x, y)
            b = camera.imageGetBlue(img, w, x, y)

            t += 1

            if gr > r + 15 and gr > b + 15:
                g += 1

    return t > 0 and (g / t) > 0.65