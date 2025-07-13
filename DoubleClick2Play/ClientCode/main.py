import os
import sys
import socket
import threading
import traceback
import ursina
from network import Network
from floor import Floor
from map import Map
from player import Player
from enemy import Enemy
from bullet import Bullet
import tkinter as tk
from tkinter import font, ttk
from PIL import Image, ImageTk
import psutil
import pygame
from ursina import application

PORT = 11923

stop_receiving = False  # For clean shutdown of receiver thread


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


def get_connected_devices():
    ip_addresses = []
    for conn in psutil.net_connections(kind='inet'):
        if conn.raddr and conn.laddr.ip.startswith('192.168.0.'):
            ip_addresses.append(conn.raddr.ip)
    return list(set(ip_addresses))


def get_user_input():
    root = tk.Tk()
    root.attributes('-fullscreen', True)
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    bg_image = Image.open(resource_path("assets/background.jpg"))
    bg_image = bg_image.resize((screen_width, screen_height), Image.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)

    canvas = tk.Canvas(root, width=screen_width, height=screen_height)
    canvas.pack(fill='both', expand=True)
    canvas.create_image(0, 0, image=bg_photo, anchor='nw')

    custom_font = font.Font(family="Helvetica", size=28, weight="bold")
    input_font = font.Font(family="Arial", size=20, weight="normal")

    frame = tk.Frame(root, bg='#010d25')
    canvas.create_window(screen_width // 2, screen_height // 2, window=frame, anchor='center')

    username_label = tk.Label(frame, text="Enter your username:", font=custom_font, fg='lightblue', bg='#010d25')
    username_label.pack(pady=20)

    username_var = tk.StringVar(value="Default")
    username_entry = tk.Entry(frame, textvariable=username_var, font=input_font, width=25, justify='center')
    username_entry.pack(pady=10)

    server_label = tk.Label(frame, text="Enter server address:", font=custom_font, fg='lightblue', bg='#010d25')
    server_label.pack(pady=(20, 10))

    server_var = tk.StringVar(value="vicks.imvickykumar999.online")
    ip_addresses = get_connected_devices()
    server_combobox = ttk.Combobox(frame, textvariable=server_var, values=ip_addresses, font=input_font, width=25, justify='center')
    server_combobox.pack(pady=(0, 20))

    port_label = tk.Label(frame, text="Enter port number:", font=custom_font, fg='lightblue', bg='#010d25')
    port_label.pack(pady=(0, 10))

    port_var = tk.StringVar(value=PORT)
    port_entry = tk.Entry(frame, textvariable=port_var, font=input_font, width=25, justify='center')
    port_entry.pack(pady=(0, 30))

    def on_ok():
        root.destroy()

    def on_close():
        root.destroy()
        exit()

    tk.Button(frame, text="Play", command=on_ok, font=input_font, bg='green', fg='white').pack(side=tk.RIGHT, padx=10)
    tk.Button(frame, text="Close", command=on_close, font=input_font, bg='red', fg='white').pack(side=tk.LEFT, padx=10)

    root.bind('<Return>', lambda event: on_ok())
    root.bind('<Escape>', lambda event: on_close())

    try:
        pygame.mixer.init()
        pygame.mixer.music.load(resource_path("assets/music.mp3"))
        pygame.mixer.music.play(-1)
    except pygame.error as e:
        print(f"[WARNING] Audio failed: {e}")

    root.mainloop()
    return username_var.get(), server_var.get(), int(port_var.get())


username, server_addr, server_port = get_user_input()

while True:
    try:
        server_port = int(server_port)
    except ValueError:
        print("Invalid port, try again...")
        continue

    n = Network(server_addr, server_port, username)
    n.settimeout(5)
    error_occurred = False

    try:
        n.connect()
    except ConnectionRefusedError:
        print("Server not started or full.")
        error_occurred = True
    except socket.timeout:
        print("Server timed out.")
        error_occurred = True
    except socket.gaierror:
        print("Invalid server address.")
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
    texture=ursina.load_texture("assets/sky.png"),
    scale=9999,
    double_sided=True
)

network = Network(server_addr, server_port, username)
player = Player(ursina.Vec3(0, 1, 0), network)
prev_pos = player.world_position
prev_dir = player.world_rotation_y
enemies = []

def receive():
    global stop_receiving
    while not stop_receiving:
        try:
            info = n.receive_info()
        except Exception as e:
            print(f"[receive error] {e}")
            traceback.print_exc()
            break

        if not info:
            print("Server closed.")
            break

        obj = info.get("object")
        if obj == "player":
            enemy_id = info["id"]
            if info.get("joined"):
                new_enemy = Enemy(ursina.Vec3(*info["position"]), enemy_id, info["username"])
                new_enemy.health = info["health"]
                enemies.append(new_enemy)
                continue

            enemy = next((e for e in enemies if e.id == enemy_id), None)
            if not enemy:
                continue

            if info.get("left"):
                enemies.remove(enemy)
                ursina.destroy(enemy)
                continue

            enemy.world_position = ursina.Vec3(*info["position"])
            enemy.rotation_y = info["rotation"]

        elif obj == "bullet":
            Bullet(
                ursina.Vec3(*info["position"]),
                info["direction"],
                info["x_direction"],
                n,
                info["damage"],
                slave=True
            )

        elif obj == "health_update":
            enemy_id = info["id"]
            target = player if enemy_id == n.id else next((e for e in enemies if e.id == enemy_id), None)
            if target:
                target.health = info["health"]

def update():
    global stop_receiving, prev_pos, prev_dir
    if ursina.held_keys['escape']:
        print("Escape pressed. Exiting...")
        stop_receiving = True
        try: network.sock.close()
        except: pass
        application.quit()

    if player.health > 0:
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
    global stop_receiving
    receiver = threading.Thread(target=receive)
    receiver.start()
    try:
        app.run()
    finally:
        print("Shutting down...")
        stop_receiving = True
        receiver.join(timeout=2)
        try:
            network.sock.close()
        except:
            pass
        print("Clean exit.")

if __name__ == "__main__":
    main()
