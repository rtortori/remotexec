#!/bin/bash
sudo tee -a /etc/profile >/dev/null << EOF
export https_proxy="http://my.proxy.company.com:80"
export no_proxy="localhost,127.0.0.1,10.96.0.1"
EOF
