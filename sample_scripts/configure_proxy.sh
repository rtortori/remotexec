#!/bin/bash
sudo mkdir -p /etc/systemd/system/docker.service.d

# Create HTTPS and HTTP Proxy configuration and exceptions
sudo tee /etc/systemd/system/docker.service.d/https-proxy.conf >/dev/null << EOF
[Service]
Environment="HTTPS_PROXY=http://my.proxy.example.com:80/" "NO_PROXY=localhost,127.0.0.1,my.private.registry.local"
EOF

sudo tee /etc/systemd/system/docker.service.d/http-proxy.conf >/dev/null << EOF
[Service]
Environment="HTTP_PROXY=http://my.proxy.example.com:80/" "NO_PROXY=localhost,127.0.0.1,my.private.registry.local"
EOF

# Restart Docker daemon
sudo systemctl daemon-reload
sudo systemctl restart docker
