
# Prayer Time Display

This application displays real-time prayer times on a TV, using a Raspberry Pi for easy installation and setup. Designed for simplicity and convenience.

> [!NOTE]
> This project is still in an early state and development is ongoing. Bugs may be present. If you notice any issues, please submit an issue.


## Demo

Insert gif or link to demo


## Deployment

You can deploy it as a website or on a raspi in kiosk mode both installations are listed step by step down bellow,..

### Deploy as a Website
To deploy the prayer time application as a website, follow these steps:

1. **Build the application:**
This command compiles the app for production, optimizing it for performance:

```bash
npm run build
```

2. **Preview the build:**
After building, you can preview the application locally to ensure everything works as expected:

```bash
npm run preview
```

3. **Host the application:**
Once verified, you can host the built files on any web server or deployment platform (e.g., Netlify, Vercel, or a custom server).

### Install on Raspberry Pi (Kiosk Mode)

To deploy this project on a Raspberry Pi and run it in kiosk mode. It consists of 3 Steps. First install the project it self. Second step setup the kiosk mode. Third step connect to a VPN instance (e.g. wireguard) so you can ssh into the server without port forwarding.

#### 1. Install the project

1. **Clone the repository:**

```bash
git clone https://github.com/berkkan22/cami-uhr.git
cd prayer-time-display
```

2. **Install dependencies:**

```bash
npm install
```

3. **Run the website**

```bash
npm run dev
```

#### 2. Setup Kiosk mode 

1. **Setup Kisok mode on Raspberry Pi**
Follow this guide https://www.techox.de/blog/einrichten-des-kiosk-modus-raspberry-pi/

2. **Done**
Now if you plug in the raspi into the TV it should automaticly start in kiosk mode and show the prayer times

#### 3. Setup VPN connection with wireguard
I assume you have a running wireguard instance on a server that you can connect to.

1. Install wireguard on the client (raspi) in order to connect to wireguard
```bash
sudo apt install wireguard resolvconf
```

2. Create a new client and download the config file
3. Rename the config file to `wg0.conf`
4. Move the file to `/etc/wireguard/`
5. Test if wireguard connection works
```bash
sudo wg-quick up wg0
```
6. Create a file `vpn.sh` and copy the content from `scripts\vpn.sh` into the newly created file
```bash
nano vpn.sh
```
7. Change the privileges of the file
```bash
chmod +x vpn.sh
```
8. Test if it works
```bash
./vpn.sh
```
Should get a similar output like this
```bash
[#] ip -6 rule add table main suppress_prefixlength 0
[#] nft -f /dev/fd/63
[#] ip -4 route add 0.0.0.0/0 dev wg0 table 51820
[#] ip -4 rule add not fwmark 51820 table 51820
[#] ip -4 rule add table main suppress_prefixlength 0
[#] sysctl -q net.ipv4.conf.all.src_valid_mark=1
[#] nft -f /dev/fd/63
WireGuard VPN activated successfully.
VPN is connected.
WireGuard VPN is now active and connected.
```

9. Create a cron job that check if the VPN the connection every 5 min incase the internet connection brakes then reconnect to it
```bash
sudo crontab -e
```
```bash
*/5 * * * * /home/pi/vpn.sh >> /var/log/wg-check.log 2>&1
```
This will execute the script every 5 min.

10. Check which public IP address you have
```bash
curl http://whatismyip.akamai.com
```

## Environment Variables

To run this project, you will need to add the following environment variables to your `src\lib\config\config.ts` file

```ts
export const config = {
  cami: 'osman_bey',
  prayerJson: '/winsen_luhe_prayer_times.json',
}
```

`cami`: Defines the layout *osman_bey* is the horizontal layout and else it is vertical without the header

`prayerJson`: Defines where the json with the prayer times are located
## Scripts

To get the prayer times you can download the whole year on https://namazvakitleri.diyanet.gov.tr/tr-TR/11012/hamburg-icin-namaz-vakti and export it as xlsx and to convert it to JSON you can use the provided script in `scripts\excel_prepare.py`

First save the file in the same direcorty as `prayer.xlsx`. Then execute the python script
```bash
python excel_prepare.py
```
This will create a file `time_data.json`. Now you need to move this into this folder `/static/` and add the file name (in this case `tim_data.json`) into the config file (see [Environment Variables](#environment-variables))

TODO: add 3 days of the next years which are the first 3 days of this year so you have time to add the new prayer times and also add in the hijri date the 3 days

## Roadmap

- Add automatic prayer time fetching for the next year
- Add more quaotes 
- Add a "news line" on the bottom for announcments
- Add backend to add new announcments


## Used By

This project is used by the following mosques:

- Osman Bey Cami Finkenwerder
- Winsen (Luhe) Muradiye Cami








---

update:
sudo apt-get update
sudo apt-get upgrade -y

sudo apt-get install git -y
sudo apt-get install tmux -y

bis hier hin alles gut 

install node:
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.0/install.sh | bash

export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion

nvm install 20
node -v
npm -v

git clone https://github.com/berkkan22/cami-uhr.git

cd cami-uhr
npm install


setup kiosk mode:
sudo apt-get install --no-install-recommends xserver-xorg x11-xserver-utils xinit openbox xdotool

sudo apt-get install --no-install-recommends chromium-browser

sudo nano /etc/xdg/openbox/autostart

xset -dpms            # turn off display power management system
xset s noblank        # turn off screen blanking
xset s off            # turn off screen saver

# Remove exit errors from the config files that could trigger a warning
sed -i 's/"exited_cleanly":false/"exited_cleanly":true/' ~/.config/chromium/'Local State'
sed -i 's/"exited_cleanly":false/"exited_cleanly":true/; s/"exit_type":"[^"]\+"/"exit_type":"Normal"/' ~/.config/chromium/Default/Preferences

# Run Chromium in kiosk mode
chromium-browser  --noerrdialogs --check-for-update-interval=31536000 --disable-infobars --kiosk $KIOSK_URL &

sudo nano /etc/xdg/openbox/environment

export KIOSK_URL=https://DEINE_HA_URL

sudo nano ~/.bash_profile
[[ -z $DISPLAY && $XDG_VTNR -eq 1 ]] && startx -- -nocursor



 nano run-prayer-monitor.sh

 modify the script to execute npm install if needed 

 #!/bin/bash

# Variables
SESSION_NAME="prayer_times"
COMMAND="source ~/.bashrc && cd /home/pi/cami-uhr && npm run dev"

# Check if tmux session exists
tmux has-session -t $SESSION_NAME 2>/dev/null

if [ $? != 0 ]; then
  # If session doesn't exist, create a new one and run the command
  tmux new-session -d -s $SESSION_NAME
  tmux send-keys -t $SESSION_NAME "$COMMAND" C-m
else
  # If session exists, send the command to the existing session
  tmux send-keys -t $SESSION_NAME "$COMMAND" C-m
fi

# Attach to the session (optional)
# tmux attach -t $SESSION_NAME

chmod +x run-prayer-monitor.sh

/home/pi/run-prayer-monitor.sh

in .bash_profile 


sudo iw dev wlan0 scan | grep SSID:
sudo nmcli dev wifi connect "SSID" password "password"