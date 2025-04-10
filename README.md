
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

To deploy this project on a Raspberry Pi and run it in kiosk mode. 

#### Prerequisites

- Install Raspbian 64-bit **Lite** on an SD card.
- Plug in the Raspberry Pi and connect it to power.

#### Steps

1. **Scan the Network for the Device and Get the IP of the Raspberry Pi**

Use the following command to scan the network and find the IP address of the Raspberry Pi:

```sh
sudo nmap -sn 192.168.1.0/24 | grep raspberrypi
```

The IP address is the local IP address of the Raspberry Pi on the network.

SSH to the Raspberry Pi

Use the following command to SSH into the Raspberry Pi:

```bash
ssh pi@IP
```

Replace IP with the actual IP address of the Raspberry Pi.

3. Run the Installation Script

Use the following command to run the installation script:


```bash
curl -o- https://raw.githubusercontent.com/berkkan22/cami-uhr/refs/heads/main/scripts/init_install.sh | bash
```

4. Follow the Output Instructions

Follow the instructions provided by the output of the installation script.

5. Create a User in Authentik

Create a user in Authentik with the appropriate group.

6. Add Quotes to the Database for the Mosque

Add some quotes to the database for the mosque.

- Create a New Branch for the Mosque

Create a new branch for the mosque and make UI adjustments in that branch.

- Duplicate a Hadith

Duplicate a hadith and use the given name in the config.ts as the identifier.

Create a User in Authentik

- Create a user in Authentik with a group that is used as the identifier in the config.ts.

7. If you have dual screen (mirroring) then past this command in the .bash_profile
```bash
DISPLAY=:0 xrandr --output HDMI-2 --same-as HDMI-1
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








--


sudo iw dev wlan0 scan | grep SSID:
sudo nmcli dev wifi connect "SSID" password "password"
