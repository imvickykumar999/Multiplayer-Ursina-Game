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
ExecStart=/usr/bin/python3 /path/to/your_server_script.py
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
    server_name your_domain_or_ip;

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
