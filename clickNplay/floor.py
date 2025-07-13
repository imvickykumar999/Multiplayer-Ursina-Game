import os, sys
import ursina
from pathlib import Path

def resource_path(relative_path):
    """ Get absolute path to resource, works in development and PyInstaller bundle """
    try:
        base_path = Path(sys._MEIPASS)
    except AttributeError:
        base_path = Path(__file__).parent
    return base_path / relative_path


class FloorCube(ursina.Entity):
    def __init__(self, position):
        floor_texture_path = resource_path("assets/floor.png")
        texture = ursina.load_texture(str(floor_texture_path))

        super().__init__(
            position=position,
            scale=2,
            model="cube",
            texture=texture,
            collider="box"
        )

        if texture:
            self.texture.filtering = None


class Floor:
    def __init__(self):
        dark1 = True
        for z in range(-20, 20, 2):
            dark2 = not dark1
            for x in range(-20, 20, 2):
                cube = FloorCube(ursina.Vec3(x, 0, z))
                if dark2:
                    cube.color = ursina.color.color(0, 0.2, 0.8)
                else:
                    cube.color = ursina.color.color(0, 0.2, 1)
                dark2 = not dark2
            dark1 = not dark1
