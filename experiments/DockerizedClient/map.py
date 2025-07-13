import os
import ursina


class Wall(ursina.Entity):
    def __init__(self, position):
        super().__init__(
            position=position,
            scale=2,
            model="cube",
            texture=os.path.join("assets", "wall.png"),
            origin_y=-0.5
        )
        self.texture.filtering = None
        self.collider = ursina.BoxCollider(self, size=ursina.Vec3(1, 2, 1))


# class Map:
#     def __init__(self):
#         for y in range(1, 4, 2):
#             Wall(ursina.Vec3(6, y, 0))
#             Wall(ursina.Vec3(6, y, 2))
#             Wall(ursina.Vec3(6, y, 4))
#             Wall(ursina.Vec3(6, y, 6))
#             Wall(ursina.Vec3(6, y, 8))

#             Wall(ursina.Vec3(4, y, 8))
#             Wall(ursina.Vec3(2, y, 8))
#             Wall(ursina.Vec3(0, y, 8))
#             Wall(ursina.Vec3(-2, y, 8))

class Map:
    def __init__(self):
        # Maze with openings (0 = path, 1 = wall)
        layout = [
            [0, 1, 1, 1, 1, 1, 0],
            [0, 0, 0, 1, 0, 0, 0],
            [1, 0, 1, 1, 1, 1, 0],
            [1, 0, 0, 0, 1, 0, 0],
            [1, 1, 1, 0, 1, 1, 0],
            [0, 0, 1, 0, 0, 0, 0],
            [0, 1, 1, 1, 1, 1, 0],
        ]

        for y in range(1, 4, 2):  # Two wall levels: y=1 and y=3
            for z, row in enumerate(layout):
                for x, cell in enumerate(row):
                    if cell == 1:
                        Wall(ursina.Vec3(x * 2, y, z * 2))
