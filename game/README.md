# 🎮 How to Join the Multiplayer Shooting Game (Locally)

> 🕹️ Play with friends on your own network using the open-source [Multiplayer Shooting Game](https://github.com/imvickykumar999/Multiplayer-Shooting-Game).

---

## ✅ Step 1: Download the Game

1. Go to the GitHub repo:
   👉 [https://github.com/imvickykumar999/Multiplayer-Shooting-Game](https://github.com/imvickykumar999/Multiplayer-Shooting-Game)

2. Click on **Code > Download ZIP**, then extract it to a folder.

3. Or clone it using Git:

   ```bash
   git clone https://github.com/imvickykumar999/Multiplayer-Shooting-Game
   ```

---

## ⚙️ Step 2: Install Python Requirements

Make sure you have **Python 3.10+** installed.

Open terminal (or PowerShell) and navigate to the project directory:

```bash
cd Multiplayer-Shooting-Game
pip install -r requirements.txt
```

---

## 🖥️ Step 3: Start the Server

1. Navigate to the `server` directory:

   ```bash
   cd game/server
   ```

2. Run the server:

   ```bash
   python main.py
   ```

3. You will see output like:

   ```
   Server started, listening for new connections...
   IPV4 Address = 192.168.0.100:8080
   ```

🔍 This means your **local IP is `192.168.0.100`** and the **port is `8080`**.

---

## 👥 Step 4: Join the Game from Client

1. Open a new terminal and go to the `client` folder:

   ```bash
   cd ../client
   ```

2. Run the game:

   ```bash
   python main.py
   ```

3. You'll see a GUI like this:

![Client Game Menu](attachment\:e716e199-6711-4784-85a9-0b0d3f3fa7ad.png)

---

## 📝 Fill in the Form:

* **Enter your username:**
  Example: `Player1`

* **Enter server address:**
  If you're playing on the **same PC**, use:

  ```
  127.0.0.1
  ```

  If you're playing on **another device on the same Wi-Fi**, use the server's local IP (e.g.):

  ```
  192.168.0.100
  ```

* **Enter port number:**

  ```
  8080
  ```

4. Click **Play** ✅ and you’re in the game!

---

## 🧑‍🤝‍🧑 Invite Your Friends (Same Network Only)

Share your server’s IP (e.g. `192.168.0.100:8080`) with others on your local Wi-Fi. They can:

* Run the client the same way.
* Enter the IP and port to connect to your server.

---

## 🚫 Common Issues

| Problem                     | Fix                                        |
| --------------------------- | ------------------------------------------ |
| Game won’t start            | Check Python & requirements installed      |
| Connection failed           | Ensure firewall allows port 8080           |
| Other players can’t connect | Make sure you're all on the **same Wi-Fi** |

---

## 🚀 Want to Play Online?

You're currently playing **locally**. If you want to:

* Deploy server on a VPS or domain (you already did it ✅)
* Distribute game without heavy repo downloads (via Docker or `.exe`)

Check back for upcoming blog posts on **public server hosting** and **easy game packaging**!

---

Happy gaming!
Feel free to star the repo ⭐ or contribute:
👉 [github.com/imvickykumar999/Multiplayer-Shooting-Game](https://github.com/imvickykumar999/Multiplayer-Shooting-Game)
