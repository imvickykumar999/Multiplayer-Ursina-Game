# 🐳 How to Dockerize a GUI-based Ursina Game Client

**by [imvickykumar999](https://hub.docker.com/repositories/imvickykumar999)**

If you're building a Python game using [Ursina Engine](https://www.ursinaengine.org/) and want to **distribute it without requiring your users to install Python**, Docker is a great solution.

In this post, I'll walk you through how I Dockerized my multiplayer shooting game client that uses **Tkinter** for user input and **Ursina/Pygame** for rendering the game.

---

## 📁 Project Structure

Here's what the `client/` folder looked like before Dockerizing:

```
client/
├── assets/
├── main.py
├── bullet.py
├── enemy.py
├── floor.py
├── map.py
├── network.py
├── player.py
├── setup.py
└── requirements.txt
```

---

## 🐋 Dockerfile Explained

Below is the Dockerfile I used to build the image for my game:

```dockerfile
# Use official Python image with minimal footprint
FROM python:3.10-slim

# Metadata
LABEL maintainer="imvickykumar999"

# Set working directory inside container
WORKDIR /usr/src/app

# Install system dependencies required for Ursina and GUI support
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libxrender1 \
    libxrandr2 \
    libxcursor1 \
    libxi6 \
    libxcomposite1 \
    libasound2 \
    libpulse0 \
    ffmpeg \
    build-essential \
    python3-dev \
    python3-tk && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the game files
COPY . .

# Run the game
CMD ["python", "main.py"]
```

---

## 🧰 Building the Docker Image

In your terminal, from inside the `client` folder (or wherever your Dockerfile is located):

```bash
docker build -t ursina-client .
```

You can then tag and push it to Docker Hub:

```bash
docker tag ursina-client imvickykumar999/ursina-client:latest
docker push imvickykumar999/ursina-client:latest
```

---

## 🖥️ Running the Game (on Ubuntu/Linux)

Running GUI apps in Docker on **Linux** is straightforward:

```bash
xhost +local:docker

docker run -it --rm \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  imvickykumar999/ursina-client:latest
```

> ✅ This shares the host's X11 display with the container, allowing your game to show a window even though it's inside Docker.

---

## 🪟 What About Windows?

On Windows, running GUI from Docker requires additional tools like:

* **VcXsrv** or **X410** to create an X11 server
* Using `host.docker.internal:0.0` as the display

But honestly, **Linux is simpler** and recommended for testing GUI Docker containers.

---

## 🧪 Want to Test if X11 Works?

Run this command to test if GUI works from Docker:

```bash
docker run -it --rm \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  x11apps/xeyes
```

If you see 👀 eyes following your cursor, X11 works — and so will your game!

---

## 📦 Final Image on Docker Hub

You can pull and run my Ursina game client from:

👉 [docker.io/imvickykumar999/ursina-client](https://hub.docker.com/r/imvickykumar999/ursina-client)

```bash
docker pull imvickykumar999/ursina-client
```

---

## 💡 Bonus: No GUI?

If you want to skip GUI popups and pass arguments instead of using Tkinter, you can modify `main.py` to accept command-line arguments (`argparse`), which makes the container even more portable — even to headless environments.
