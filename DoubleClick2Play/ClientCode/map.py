import ursina
import os
import sys
from pathlib import Path

def resource_path(relative_path):
    """ Get absolute path to resource, works in dev and PyInstaller """
    try:
        base_path = Path(sys._MEIPASS)
    except AttributeError:
        base_path = Path(__file__).parent
    return base_path / relative_path


class Wall(ursina.Entity):
    def __init__(self, position):
        wall_texture_path = resource_path("assets/wall.png")
        texture = ursina.load_texture(str(wall_texture_path))

        if texture:
            texture.filtering = None
            kwargs = {'texture': texture}
        else:
            print(f"❌ Could not load wall texture from {wall_texture_path} — using orange color.")
            kwargs = {'color': ursina.color.orange}

        super().__init__(
            position=position,
            scale=2,
            model="cube",
            origin_y=-0.5,
            **kwargs
        )

        self.collider = ursina.BoxCollider(self, size=ursina.Vec3(1, 2, 1))


class Map:
    def __init__(self):
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
