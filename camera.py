class Camera:
    """
    카메라. 자세한건 복붙해와서 나도 몰러
    """
    """
    출처:
    https://code.harrywykman.com/the-python-revised-roguelike-tutorial-with-a-scrolling-map.html
    """
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def apply(self, x, y):
        x = x + self.x
        y = y + self.y
        return (x, y)

    def update(self, entity):
        x = - entity.x + int(self.width / 2)
        y = - entity.y + int(self.height / 2)

        self.x, self.y = (x, y)
