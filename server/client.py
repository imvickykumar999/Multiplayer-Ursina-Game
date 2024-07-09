import os
import sys
import socket
import threading
from ursina import Ursina, InputField, Button, Entity, Vec3, destroy, held_keys, window, Text, camera, color
from network import Network
from floor import Floor
from map import Map
from player import Player
from enemy import Enemy
from bullet import Bullet

class MyGame:
    def __init__(self):
        self.username = "vicky"
        self.server_addr = "127.0.0.1"
        self.server_port = 8000
        self.input_fields = []
        self.network = None
        self.player = None
        self.prev_pos = None
        self.prev_dir = None
        self.enemies = []

        self.app = Ursina()
        self.create_input_fields()
        self.submit_button = Button(text='Submit', scale=(.3, .1), position=(0, -0.3), color=color.azure)
        self.submit_button.on_click = self.submit

    def create_input_fields(self):
        camera.ui.color = color.light_gray

        self.username_label = Text(text="Username:", position=(-0.5, 0.1), origin=(0, 0), background=True)
        self.username_label.background.color = color.clear
        self.username_field = InputField(position=(0, 0.1), scale=(0.6, 0.1), color=color.white, origin=(0, 0))
        self.input_fields.append(self.username_field)

        self.ip_label = Text(text="Server Address:", position=(-0.5, -0.1), origin=(0, 0), background=True)
        self.ip_label.background.color = color.clear
        self.ip_field = InputField(position=(0, -0.1), scale=(0.6, 0.1), color=color.white, origin=(0, 0))
        self.input_fields.append(self.ip_field)

    def submit(self):
        self.username = self.username_field.text
        self.server_addr = self.ip_field.text
        print(f'Username: {self.username}, Server Address: {self.server_addr}')
        for field in self.input_fields:
            field.enabled = False
        self.submit_button.enabled = False
        self.username_label.enabled = False
        self.ip_label.enabled = False
        self.start_game()

    def start_game(self):
        while True:
            try:
                self.server_port = int(self.server_port)
            except ValueError:
                print("\nThe port you entered was not a number, try again with a valid port...")
                continue

            self.network = Network(self.server_addr, self.server_port, self.username)
            self.network.settimeout(5)
            error_occurred = False

            try:
                self.network.connect()
            except ConnectionRefusedError:
                print("\nConnection refused! This can be because server hasn't started or has reached its player limit.")
                error_occurred = True
            except socket.timeout:
                print("\nServer took too long to respond, please try again...")
                error_occurred = True
            except socket.gaierror:
                print("\nThe IP address you entered is invalid, please try again with a valid address...")
                error_occurred = True
            finally:
                self.network.settimeout(None)

            if not error_occurred:
                break

        window.borderless = False
        window.title = "Ursina FPS"
        window.exit_button.visible = False

        self.floor = Floor()
        self.map = Map()
        self.sky = Entity(
            model="sphere",
            texture=os.path.join("assets", "sky.png"),
            scale=9999,
            double_sided=True
        )

        self.player = Player(Vec3(0, 1, 0), self.network)
        self.prev_pos = self.player.world_position
        self.prev_dir = self.player.world_rotation_y

        self.msg_thread = threading.Thread(target=self.receive, daemon=True)
        self.msg_thread.start()

    def receive(self):
        while True:
            try:
                info = self.network.receive_info()
            except Exception as e:
                print(e)
                continue

            if not info:
                print("Server has stopped! Exiting...")
                sys.exit()

            if info["object"] == "player":
                enemy_id = info["id"]

                if info["joined"]:
                    new_enemy = Enemy(Vec3(*info["position"]), enemy_id, info["username"])
                    new_enemy.health = info["health"]
                    self.enemies.append(new_enemy)
                    continue

                enemy = None

                for e in self.enemies:
                    if e.id == enemy_id:
                        enemy = e
                        break

                if not enemy:
                    continue

                if info["left"]:
                    self.enemies.remove(enemy)
                    destroy(enemy)
                    continue

                enemy.world_position = Vec3(*info["position"])
                enemy.rotation_y = info["rotation"]

            elif info["object"] == "bullet":
                b_pos = Vec3(*info["position"])
                b_dir = info["direction"]
                b_x_dir = info["x_direction"]
                b_damage = info["damage"]
                new_bullet = Bullet(b_pos, b_dir, b_x_dir, self.network, b_damage, slave=True)
                destroy(new_bullet, delay=2)

            elif info["object"] == "health_update":
                enemy_id = info["id"]
                enemy = None

                if enemy_id == self.network.id:
                    enemy = self.player
                else:
                    for e in self.enemies:
                        if e.id == enemy_id:
                            enemy = e
                            break

                if not enemy:
                    continue

                enemy.health = info["health"]

    def update(self):
        if held_keys['escape']:
            exit()

        if self.player.health > 0:
            if self.prev_pos != self.player.world_position or self.prev_dir != self.player.world_rotation_y:
                self.network.send_player(self.player)

            self.prev_pos = self.player.world_position
            self.prev_dir = self.player.world_rotation_y

    def input(self, key):
        if key == "left mouse down" and self.player.health > 0:
            b_pos = self.player.position + Vec3(0, 2, 0)
            bullet = Bullet(b_pos, self.player.world_rotation_y, -self.player.camera_pivot.world_rotation_x, self.network)
            self.network.send_bullet(bullet)
            destroy(bullet, delay=2)

    def run(self):
        self.app.run()

if __name__ == "__main__":
    game = MyGame()
    game.run()
