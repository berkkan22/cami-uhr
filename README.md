
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

To deploy this project on a Raspberry Pi and run it in kiosk mode, follow these steps:
1. **Clone the repository:**

```bash
git clone https://github.com/your-repo/prayer-time-display.git
cd prayer-time-display
```

2. **Install dependencies:**

```bash
npm install
```

3. **Setup Kisok mode on Raspberry Pi**
Follow this guide https://www.techox.de/blog/einrichten-des-kiosk-modus-raspberry-pi/

4. **Done**
Now if you plug in the raspi into the TV it should automaticly start in kiosk mode and show the prayer times
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

