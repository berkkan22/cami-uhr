#!/bin/bash

set -e  # Exit immediately if a command fails

# Function to check and fix DNS issues
fix_dns_if_needed() {
    if grep -q "Could not resolve host" <<< "$1"; then
        echo "⚠️  DNS resolution failed! Fixing DNS settings..."
        echo "nameserver 8.8.8.8" | sudo tee /etc/resolv.conf
        echo "nameserver 8.8.4.4" | sudo tee -a /etc/resolv.conf
        echo "✅ DNS fixed. Retrying..."
    fi
}

# Update system
echo "Updating system..."
UPDATE_OUTPUT=$(sudo apt-get update 2>&1) || { fix_dns_if_needed "$UPDATE_OUTPUT"; sudo apt-get update; }
UPGRADE_OUTPUT=$(sudo apt-get upgrade -y 2>&1) || { fix_dns_if_needed "$UPGRADE_OUTPUT"; sudo apt-get upgrade -y; }

# Install required packages
echo "Installing required packages..."
INSTALL_OUTPUT=$(sudo apt-get install -y git nano tmux wireguard resolvconf 2>&1) || { fix_dns_if_needed "$INSTALL_OUTPUT"; sudo apt-get install -y git nano tmux wireguard resolvconf; }

# Install NVM
echo "Installing NVM (Node Version Manager)..."
NVM_INSTALL_OUTPUT=$(curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash 2>&1) || { fix_dns_if_needed "$NVM_INSTALL_OUTPUT"; curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash; }

# Load NVM immediately
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"

# Check NVM installation
echo "Checking NVM installation..."
if ! command -v nvm &> /dev/null; then
    echo "❌ NVM installation failed!"
    exit 1
fi

# Install Node.js
echo "Installing Node.js (version 20)..."
nvm install 20

# Check Node.js and npm versions
echo "Checking Node.js and npm versions..."
NODE_VERSION=$(node -v)
NPM_VERSION=$(npm -v)

if [ -z "$NODE_VERSION" ] || [ -z "$NPM_VERSION" ]; then
    echo "❌ Node.js or npm installation failed!"
    exit 1
fi

echo "✅ Node.js installed: $NODE_VERSION"
echo "✅ npm installed: $NPM_VERSION"

# Clone the project
echo "Cloning the project repository..."
GIT_CLONE_OUTPUT=$(git clone https://github.com/berkkan22/cami-uhr.git 2>&1) || { fix_dns_if_needed "$GIT_CLONE_OUTPUT"; git clone https://github.com/berkkan22/cami-uhr.git; }

# Ask user for WireGuard configuration
echo "Please enter your WireGuard configuration. Press CTRL+D when done:"
WG_CONFIG_CONTENT=$(cat) # Read multi-line input until CTRL+D

# Validate input
if [ -z "$WG_CONFIG_CONTENT" ]; then
    echo "❌ No WireGuard configuration provided!"
    exit 1
fi

# Save configuration
echo "$WG_CONFIG_CONTENT" | sudo tee /etc/wireguard/wg0.conf > /dev/null
sudo chmod 600 /etc/wireguard/wg0.conf
echo "✅ WireGuard configuration saved to /etc/wireguard/wg0.conf"

# Test WireGuard connection
echo "Testing WireGuard connection..."
if sudo wg-quick up wg0; then
    echo "✅ WireGuard VPN activated successfully!"
else
    echo "❌ Failed to start WireGuard VPN!"
    exit 1
fi

# Create vpn.sh script
echo "Creating VPN script..."
VPN_SCRIPT_PATH="$HOME/vpn.sh"
SCRIPT_SOURCE="$HOME/cami-uhr/scripts/vpn.sh"

if [ -f "$SCRIPT_SOURCE" ]; then
    cp "$SCRIPT_SOURCE" "$VPN_SCRIPT_PATH"
    chmod +x "$VPN_SCRIPT_PATH"
    echo "✅ vpn.sh script created and made executable."
else
    echo "❌ vpn.sh script not found in the repository!"
    exit 1
fi

# Test vpn.sh
echo "Testing vpn.sh script..."
if "$VPN_SCRIPT_PATH"; then
    echo "✅ vpn.sh executed successfully."
else
    echo "❌ vpn.sh execution failed!"
    exit 1
fi

# Add VPN check to cron
echo "Adding VPN auto-reconnect to cron..."
CRON_JOB="*/5 * * * * $VPN_SCRIPT_PATH >> /var/log/wg-check.log 2>&1"
REBOOT_JOB="@reboot sleep 30 && $VPN_SCRIPT_PATH >> /var/log/wg-check.log 2>&1"

# Add to crontab if not already present
(crontab -l 2>/dev/null | grep -F "$VPN_SCRIPT_PATH" || (crontab -l 2>/dev/null; echo "$CRON_JOB")) | crontab -
(crontab -l 2>/dev/null | grep -F "@reboot" || (crontab -l 2>/dev/null; echo "$REBOOT_JOB")) | crontab -

echo "✅ VPN auto-reconnect cron jobs added (every 5 min & at reboot)."

# Check public IP
echo "Checking public IP address..."
PUBLIC_IP=$(curl -s http://whatismyip.akamai.com)
echo "🌍 Your public IP address is: $PUBLIC_IP"

echo "🎉 Installation completed successfully!"
echo "Reboot your system to apply all changes."