#!/bin/bash

set -e  # Exit immediately if a command fails

echo "Updating system..."
sudo apt-get update && sudo apt-get upgrade -y

echo "Installing required packages..."
sudo apt-get install -y git nano tmux wireguard resolvconf

echo "Installing NVM (Node Version Manager)..."
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash

# Load NVM immediately to use it in the script
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"

echo "Checking NVM installation..."
if ! command -v nvm &> /dev/null; then
    echo "❌ NVM installation failed!"
    exit 1
fi

echo "Installing Node.js (version 20)..."
nvm install 20

echo "Checking Node.js and npm versions..."
NODE_VERSION=$(node -v)
NPM_VERSION=$(npm -v)

if [ -z "$NODE_VERSION" ] || [ -z "$NPM_VERSION" ]; then
    echo "❌ Node.js or npm installation failed!"
    exit 1
fi

echo "✅ Node.js installed: $NODE_VERSION"
echo "✅ npm installed: $NPM_VERSION"

echo "Cloning the project repository..."
git clone https://github.com/berkkan22/cami-uhr.git

# Prompt for WireGuard configuration
echo "Please enter your WireGuard configuration. Press CTRL+D when done:"
WG_CONFIG_CONTENT=$(cat)

# Save WireGuard configuration
WG_CONFIG_PATH="/etc/wireguard/wg0.conf"
echo "$WG_CONFIG_CONTENT" | sudo tee "$WG_CONFIG_PATH" > /dev/null

# Set correct permissions
sudo chmod 600 "$WG_CONFIG_PATH"

# Check if wg0 is already up
if sudo wg show wg0 > /dev/null 2>&1; then
    echo "✅ WireGuard VPN is already active."
else
    # Bring up the WireGuard connection if it's not already active
    echo "Bringing up WireGuard VPN..."
    if sudo wg-quick up wg0; then
        echo "✅ WireGuard VPN activated successfully."
    else
        echo "❌ WireGuard failed to start!"
        exit 1
    fi
fi

# Copy content from cami-uhr/scripts/vpn.sh to /home/pi/vpn.sh
echo "Copying vpn.sh content..."
sudo cp ./cami-uhr/scripts/vpn.sh /home/pi/vpn.sh

# Make vpn.sh executable
sudo chmod +x /home/pi/vpn.sh

# Add cron jobs to root's crontab
echo "Adding cron jobs to ensure VPN stays connected..."
(sudo crontab -l 2>/dev/null; echo "*/5 * * * * /home/pi/vpn.sh >> /var/log/wg-check.log 2>&1") | sudo crontab -
(sudo crontab -l 2>/dev/null; echo "@reboot /home/pi/vpn.sh >> /var/log/wg-check.log 2>&1") | sudo crontab -

echo "✅ Cron jobs added to root's crontab."

# Display current public IP
echo "Checking public IP address..."
curl -s http://whatismyip.akamai.com && echo

# Display current local IP
echo "Checking local IP address..."
hostname -I

echo "🎉 Installation completed successfully!"
echo "Reboot your system to apply changes."