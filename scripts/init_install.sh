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

echo "🎉 Installation completed successfully!"
echo "Restart your system"