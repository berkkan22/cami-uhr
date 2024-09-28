
# Prayer Time Display

This application displays real-time prayer times on a TV, using a Raspberry Pi for easy installation and setup. Designed for simplicity and convenience.


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
git clone https://github.com/your-repo/prayer-time-display.git
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
chmode +x vpn.sh
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

## Roadmap

- Add automatic prayer time fetching for the next year
- Add more quaotes 
- Add a "news line" on the bottom for announcments
- Add backend to add new announcments


## Used By

This project is used by the following mosques:

- Osman Bey Cami Finkenwerder

