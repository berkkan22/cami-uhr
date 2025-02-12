#!/bin/bash

set -e  # Exit immediately if a command fails

# Check if the WireGuard config file exists
WG_CONFIG_PATH="./wg0.conf"

if [ ! -f "$WG_CONFIG_PATH" ]; then
    echo "❌ The WireGuard configuration file 'wg0.conf' is missing in the current directory."
    echo "Please create the WireGuard configuration file and run the script again."
    exit 1
fi

echo "Updating system..."
sudo apt-get update && sudo apt-get upgrade -y

echo "Installing required packages..."
sudo apt-get install -y git nano tmux wireguard

# Install Kiosk Mode packages
echo "Installing kiosk mode dependencies..."
sudo apt install --no-install-recommends xserver-xorg x11-xserver-utils xinit matchbox-window-manager chromium-browser -y
sudo apt-get install gldriver-test -y
sudo apt install unclutter -y

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

# Copy the WireGuard configuration to /etc/wireguard/wg0.conf
echo "Copying WireGuard configuration to /etc/wireguard/wg0.conf..."
sudo cp "$WG_CONFIG_PATH" /etc/wireguard/wg0.conf
sudo rm "$WG_CONFIG_PATH"

# Set correct permissions for the WireGuard configuration file
sudo chmod 600 /etc/wireguard/wg0.conf

# Install resolvconf
sudo apt install resolvconf -y

# Check if wg0 is already up
if sudo wg show wg0 > /dev/null 2>&1; then
    echo "✅ WireGuard VPN is already active."
else
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
sudo chmod +x /home/pi/vpn.sh

# Add cron jobs to root's crontab
echo "Adding cron jobs to ensure VPN stays connected..."
(sudo crontab -l 2>/dev/null; echo "*/5 * * * * /home/pi/vpn.sh >> /var/log/wg-check.log 2>&1") | sudo crontab -
(sudo crontab -l 2>/dev/null; echo "@reboot sleep 30 && /home/pi/vpn.sh >> /var/log/wg-check.log 2>&1") | sudo crontab -

echo "✅ Cron jobs added to root's crontab."

# Create start-kiosk.sh
echo "Creating start-kiosk.sh..."
cat << EOF | sudo tee ~/start-kiosk.sh > /dev/null
#!/bin/bash
xset -dpms          # Disable display power management
xset s off          # Disable screen saver
xset s noblank      # Prevent blank screen

# Hide cursor after 0.1s of inactivity
unclutter -idle 0.1 -root &

# Start Matchbox Window Manager
matchbox-window-manager &

# Start Chromium in kiosk mode
chromium-browser --noerrdialogs --disable-infobars --kiosk "http://localhost:5173"
EOF

# Make start-kiosk.sh executable
sudo chmod +x ~/start-kiosk.sh

# Configure auto-start on login
echo "Configuring auto-start for kiosk mode..."
cat << EOF | sudo tee ~/.bash_profile > /dev/null
if [ -f ~/.bashrc ]; then
    source ~/.bashrc
fi

if [[ -z \$DISPLAY ]] && [[ \$(tty) == /dev/tty1 ]]; then
    startx ~/start-kiosk.sh
fi
EOF

# Copy content from ./script/run_website.sh to run-prayer-monitor.sh
echo "Copying run_website.sh content to run-prayer-monitor.sh..."
sudo cp ./cami-uhr/scripts/run_website.sh /home/pi/run-prayer-monitor.sh
sudo chmod +x /home/pi/run-prayer-monitor.sh

# Add /home/pi/run-prayer-monitor.sh to .bash_profile
echo "Adding run-prayer-monitor.sh to .bash_profile..."
echo "" >> ~/.bash_profile
echo "/home/pi/run-prayer-monitor.sh" >> ~/.bash_profile

# Change to project directory
cd cami-uhr

# Install npm dependencies
echo "Installing npm dependencies..."
npm install

# Copy .env.example to .env
echo "Copying .env.example to .env..."
cp .env.example .env

cd

# Display current public IP
echo "Checking public IP address..."
curl -s http://whatismyip.akamai.com && echo

# Display current local IP
echo "Checking local IP address..."
hostname -I

echo "🎉 Installation completed successfully!"
echo "Please add the URLs to the .env file."
echo "Please add date_data.json and time_data.json to the project directory and update the config as needed."

echo "Run: sudo raspi-config and go to System Options → Boot / Auto Login → Console Autologin."
echo "Reboot your system to apply changes."

