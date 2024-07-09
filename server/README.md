To host your server script on NGINX, you'll need to set up a web server that can reverse proxy your game server. Here's a step-by-step guide:

### 1. **Prepare Your Environment**

Ensure you have NGINX installed on your server. If not, you can install it using:
```bash
sudo apt update
sudo apt install nginx
```

### 2. **Update Your Server Script**

Make sure your server script is ready to run on a public server. You may need to change the `ADDR` variable to the server's public IP address or leave it as `0.0.0.0` to bind to all interfaces.

### 3. **Create a Systemd Service for Your Game Server**

Create a service file to manage your game server process. This will allow it to start on boot and restart if it crashes.

Create a file called `game_server.service` in `/etc/systemd/system/` with the following content:

```ini
[Unit]
Description=Game Server

[Service]
ExecStart=/usr/bin/python3 /home/newbol7/Documents/Multiplayer-Ursina-Game-main/server/main.py
Restart=always
User=nobody
Group=nogroup
Environment=PATH=/usr/bin:/usr/local/bin
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
```

Replace `/path/to/your_server_script.py` with the actual path to your server script.

Enable and start the service:

```bash
sudo systemctl enable game_server.service
sudo systemctl start game_server.service
```

### 4. **Configure NGINX**

Edit the NGINX configuration to reverse proxy your game server. Create a new file in `/etc/nginx/sites-available/` named `game_server`:

```nginx
server {
    listen 80;
    server_name 127.0.0.1;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Replace `your_domain_or_ip` with your server's domain name or IP address.

Create a symbolic link to this configuration in the `sites-enabled` directory:

```bash
sudo ln -s /etc/nginx/sites-available/game_server /etc/nginx/sites-enabled/
```

### 5. **Test and Reload NGINX**

Test the NGINX configuration for syntax errors:

```bash
sudo nginx -t
```

If the test is successful, reload NGINX:

```bash
sudo systemctl reload nginx
```

### 6. **Update Game Client**

Ensure your Ursina game client connects to the correct server address, which will now be the public IP address or domain name of your NGINX server.

### Final Notes

- Ensure your server's firewall allows traffic on port 80 (HTTP) and 8000 (your game server port).
- Consider securing your server with SSL/TLS by using a service like Let's Encrypt.

By following these steps, your Ursina game should be accessible via the public IP or domain name, with NGINX handling the reverse proxy to your game server.

---

The folder `/etc/systemd/system/` is located at the root level of the file system on your Ubuntu laptop. Here are the steps to navigate to this folder:

1. **Open a Terminal:**
   - You can open a terminal window by pressing `Ctrl + Alt + T` on your keyboard.

2. **Navigate to the Directory:**
   - You can change to the `/etc/systemd/system/` directory by running the following command in the terminal:
     ```bash
     cd /etc/systemd/system/
     ```

3. **List the Contents:**
   - To see the contents of the directory, you can use the `ls` command:
     ```bash
     ls
     ```

If you need to create or edit a file in this directory, you will typically need to use `sudo` to gain the necessary permissions. For example, to create or edit the `game_server.service` file, you can use a text editor like `nano`:

```bash
sudo nano /etc/systemd/system/game_server.service
```

This will open the file in the `nano` text editor with elevated permissions, allowing you to make the necessary changes. Once you're done, save the file by pressing `Ctrl + O`, and then exit `nano` by pressing `Ctrl + X`.
