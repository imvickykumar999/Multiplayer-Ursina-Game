import os
import sys
import socket
import threading
import ursina
from network import Network
from floor import Floor
from map import Map
from player import Player
from enemy import Enemy
from bullet import Bullet
import tkinter as tk
from tkinter import font

def get_user_input():
    root = tk.Tk()
    root.attributes('-fullscreen', True)
    custom_font = font.Font(family="Helvetica", size=28, weight="bold")

    frame = tk.Frame(root)
    frame.pack(expand=True)

    username_label = tk.Label(frame, text="Enter your username:", font=custom_font)
    username_label.pack(pady=20)

    username_var = tk.StringVar()
    username_entry = tk.Entry(frame, textvariable=username_var, font=custom_font, width=20)
    username_entry.pack(pady=10)
    username_entry.focus_set()

    server_label = tk.Label(frame, text="Enter server address:", font=custom_font)
    server_label.pack(pady=20)

    server_var = tk.StringVar()
    server_entry = tk.Entry(frame, textvariable=server_var, font=custom_font, width=20)
    server_entry.pack(pady=(10, 50))

    def on_ok():
        root.destroy()

    def on_close():
        root.destroy()
        exit()

    ok_button = tk.Button(frame, text="Play", command=on_ok, font=custom_font, bg='green', fg='white')
    ok_button.pack(side=tk.LEFT, padx=10)

    close_button = tk.Button(frame, text="Close", command=on_close, font=custom_font, bg='red', fg='white')
    close_button.pack(side=tk.RIGHT, padx=10)

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    root.update_idletasks()
    window_width = root.winfo_width()
    window_height = root.winfo_height()
    x_position = (screen_width - window_width) // 2
    y_position = (screen_height - window_height) // 2

    root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
    root.mainloop()

    username = username_var.get() or "default"
    server_addr = server_var.get()
    return username, server_addr

server_port = 8000
username, server_addr = get_user_input()

print()
print(username, server_addr)

while True:
    try:
        server_port = int(server_port)
    except ValueError:
        print("\nThe port you entered was not a number, try again with a valid port...")
        continue

    n = Network(server_addr, server_port, username)
    n.settimeout(5)
    error_occurred = False

    try:
        n.connect()
    except ConnectionRefusedError:
        print("\nConnection refused! This can be because server hasn't started or has reached it's player limit.")
        error_occurred = True
    except socket.timeout:
        print("\nServer took too long to respond, please try again...")
        error_occurred = True
    except socket.gaierror:
        print("\nThe IP address you entered is invalid, please try again with a valid address...")
        error_occurred = True
    finally:
        n.settimeout(None)

    if not error_occurred:
        break

app = ursina.Ursina(fullscreen=True)
ursina.window.borderless = False
ursina.window.title = "Ursina FPS"
ursina.window.exit_button.visible = False

floor = Floor()
map = Map()
sky = ursina.Entity(
    model="sphere",
    texture=os.path.join("assets", "sky.png"),
    scale=9999,
    double_sided=True
)

network = Network(server_addr, server_port, username)  
player = Player(ursina.Vec3(0, 1, 0), network)
prev_pos = player.world_position
prev_dir = player.world_rotation_y
enemies = []

def receive():
    while True:
        try:
            info = n.receive_info()
        except Exception as e:
            print(e)
            continue

        if not info:
            print("Server has stopped! Exiting...")
            sys.exit()

        if info["object"] == "player":
            enemy_id = info["id"]

            if info["joined"]:
                new_enemy = Enemy(ursina.Vec3(*info["position"]), enemy_id, info["username"])
                new_enemy.health = info["health"]
                enemies.append(new_enemy)
                continue

            enemy = None

            for e in enemies:
                if e.id == enemy_id:
                    enemy = e
                    break

            if not enemy:
                continue

            if info["left"]:
                enemies.remove(enemy)
                ursina.destroy(enemy)
                continue

            enemy.world_position = ursina.Vec3(*info["position"])
            enemy.rotation_y = info["rotation"]

        elif info["object"] == "bullet":
            b_pos = ursina.Vec3(*info["position"])
            b_dir = info["direction"]
            b_x_dir = info["x_direction"]
            b_damage = info["damage"]
            new_bullet = Bullet(b_pos, b_dir, b_x_dir, n, b_damage, slave=True)
            ursina.destroy(new_bullet, delay=2)

        elif info["object"] == "health_update":
            enemy_id = info["id"]
            enemy = None

            if enemy_id == n.id:
                enemy = player
            else:
                for e in enemies:
                    if e.id == enemy_id:
                        enemy = e
                        break

            if not enemy:
                continue

            enemy.health = info["health"]


def update():
    if ursina.held_keys['escape']:
        exit()
        # ursina.mouse.locked = False
        # ursina.mouse.visible = True

    if player.health > 0:
        global prev_pos, prev_dir

        if prev_pos != player.world_position or prev_dir != player.world_rotation_y:
            n.send_player(player)

        prev_pos = player.world_position
        prev_dir = player.world_rotation_y


def input(key):
    if key == "left mouse down" and player.health > 0:
        b_pos = player.position + ursina.Vec3(0, 2, 0)
        bullet = Bullet(b_pos, player.world_rotation_y, -player.camera_pivot.world_rotation_x, n)
        n.send_bullet(bullet)
        ursina.destroy(bullet, delay=2)


def main():
    msg_thread = threading.Thread(target=receive, daemon=True)
    msg_thread.start()
    app.run()


if __name__ == "__main__":
    main()
