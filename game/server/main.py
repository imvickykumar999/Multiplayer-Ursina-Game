"""
Server script for hosting games
"""

import socket
import json
import time
import random
import threading
from art import *

PORT = 8080 # this should be same as you define in playit.gg dashboard
ADDR = "0.0.0.0"
MAX_PLAYERS = 10
MSG_SIZE = 2048

# Setup server socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((ADDR, PORT))
s.listen(MAX_PLAYERS)

players = {}

def generate_id(player_list: dict, max_players: int):
    """
    Generate a unique identifier

    Args:
        player_list (dict): dictionary of existing players
        max_players (int): maximum number of players allowed

    Returns:
        str: the unique identifier
    """

    while True:
        unique_id = str(random.randint(1, max_players))
        if unique_id not in player_list:
            return unique_id


def handle_messages(identifier: str):
    client_info = players[identifier]
    conn: socket.socket = client_info["socket"]
    username = client_info["username"]

    while True:
        try:
            msg = conn.recv(MSG_SIZE)
        except ConnectionResetError:
            break

        if not msg:
            break

        msg_decoded = msg.decode("utf8")

        try:
            left_bracket_index = msg_decoded.index("{")
            right_bracket_index = msg_decoded.index("}") + 1
            msg_decoded = msg_decoded[left_bracket_index:right_bracket_index]
        except ValueError:
            continue

        try:
            msg_json = json.loads(msg_decoded)
        except Exception as e:
            print(e)
            continue

        print(f"Received message from player {username} with ID {identifier}")

        if msg_json["object"] == "player":
            players[identifier]["position"] = msg_json["position"]
            players[identifier]["rotation"] = msg_json["rotation"]
            players[identifier]["health"] = msg_json["health"]

            # Make player invisible if health is 0
            if msg_json["health"] <= 0:
                players[identifier]["visible"] = False
            else:
                players[identifier]["visible"] = True

        elif msg_json["object"] == "respawn":
            players[identifier]["position"] = msg_json["position"]
            players[identifier]["health"] = msg_json["health"]
            players[identifier]["visible"] = True

            # Broadcast respawn event to other players
            respawn_message = json.dumps({
                "object": "player_respawn",
                "id": identifier,
                "position": players[identifier]["position"],
                "health": players[identifier]["health"]
            })

            for player_id in list(players):
                if player_id != identifier:
                    player_info = players[player_id]
                    player_conn: socket.socket = player_info["socket"]
                    try:
                        player_conn.sendall(respawn_message.encode("utf8"))
                    except OSError:
                        pass

        # Tell other players about player moving or visibility change
        for player_id in list(players):
            if player_id != identifier:
                player_info = players[player_id]
                player_conn: socket.socket = player_info["socket"]
                try:
                    player_conn.sendall(msg_decoded.encode("utf8"))
                except OSError:
                    pass

    # Tell other players about player leaving
    for player_id in list(players):
        if player_id != identifier:
            player_info = players[player_id]
            player_conn: socket.socket = player_info["socket"]
            try:
                player_conn.send(json.dumps({"id": identifier, "object": "player", "joined": False, "left": True}).encode("utf8"))
            except OSError:
                pass

    print(f"Player {username} with ID {identifier} has left the game...")
    del players[identifier]
    conn.close()


def main():
    hostname = socket.gethostname()
    server_addr = f'{socket.gethostbyname(hostname)}:{PORT}'

    print("\nServer started, listening for new connections...")
    print(f'IPV4 Address = {server_addr}\n')
    tprint(server_addr)

    while True:
        # Accept new connection and assign unique ID
        conn, addr = s.accept()
        new_id = generate_id(players, MAX_PLAYERS)
        conn.send(new_id.encode("utf8"))

        try:
            username = conn.recv(MSG_SIZE).decode("utf8")
        except UnicodeDecodeError as e:
            print(f"Failed to decode username: {e}")
            conn.close()
            continue

        new_player_info = {"socket": conn, "username": username, "position": (0, 1, 0), "rotation": 0, "health": 100, "visible": True}

        # Tell existing players about new player
        for player_id in list(players):
            if player_id != new_id:
                player_info = players[player_id]
                player_conn: socket.socket = player_info["socket"]
                try:
                    player_conn.send(json.dumps({
                        "id": new_id,
                        "object": "player",
                        "username": new_player_info["username"],
                        "position": new_player_info["position"],
                        "health": new_player_info["health"],
                        "joined": True,
                        "left": False
                    }).encode("utf8"))
                except OSError:
                    pass

        # Tell new player about existing players
        for player_id in list(players):
            if player_id != new_id:
                player_info = players[player_id]
                try:
                    conn.send(json.dumps({
                        "id": player_id,
                        "object": "player",
                        "username": player_info["username"],
                        "position": player_info["position"],
                        "health": player_info["health"],
                        "joined": True,
                        "left": False
                    }).encode("utf8"))
                    time.sleep(0.1)
                except OSError:
                    pass

        # Add new player to players list, effectively allowing it to receive messages from other players
        players[new_id] = new_player_info

        # Start thread to receive messages from client
        msg_thread = threading.Thread(target=handle_messages, args=(new_id,), daemon=True)
        msg_thread.start()

        print(f"New connection from {addr}, assigned ID: {new_id}...")


if __name__ == "__main__":
    while True:
        try:
            main()
        except KeyboardInterrupt:
            print("Server stopped manually.")
            break  # Allow graceful shutdown on Ctrl+C
        except SystemExit:
            print("System exit triggered.")
            break
        except Exception as e:
            print(f"Server crashed with error: {e}")
            print("Restarting server in 5 seconds...\n")
            time.sleep(5)
        finally:
            s.close()
