#!/bin/bash

# Variables
WG_INTERFACE="wg0"   # Replace with your WireGuard interface name
CHECK_PEER_IP="8.8.8.8"   # IP to ping to check connectivity, Google DNS as an example
WG_CONFIG="/etc/wireguard/wg0.conf"   # Replace with your WireGuard configuration file path

# Function to check if WireGuard interface is up
is_wg_up() {
    sudo wg show $WG_INTERFACE > /dev/null 2>&1
    if [ $? -eq 0 ]; then
        echo "WireGuard interface $WG_INTERFACE is up."
        return 0
    else
        echo "WireGuard interface $WG_INTERFACE is down."
        return 1
    fi
}

# Function to check if VPN is connected
is_vpn_connected() {
    # Try to ping a known IP (can be a server inside your VPN or a public IP)
    ping -c 2 $CHECK_PEER_IP > /dev/null 2>&1
    if [ $? -eq 0 ]; then
        echo "VPN is connected."
        return 0
    else
        echo "VPN is not connected."
        return 1
    fi
}

# Function to activate the WireGuard interface
activate_wg() {
    echo "Attempting to activate WireGuard VPN..."
    sudo wg-quick up $WG_CONFIG
    if [ $? -eq 0 ]; then
        echo "WireGuard VPN activated successfully."
    else
        echo "Failed to activate WireGuard VPN."
        exit 1
    fi
}

# Main logic
if is_wg_up; then
    if is_vpn_connected; then
        echo "WireGuard VPN is active and connected."
    else
        echo "WireGuard interface is up, but VPN seems to be disconnected."
    fi
else
    echo "WireGuard VPN is not active. Trying to activate it..."
    activate_wg
    # After activating, check if it's connected again
    if is_vpn_connected; then
        echo "WireGuard VPN is now active and connected."
    else
        echo "WireGuard VPN was activated, but VPN connection still failed."
    fi
fi
