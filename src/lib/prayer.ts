import { config } from "./config/config";
import fs from "fs";



export interface Prayers {
  date: string;
  hicriDate: string;
  imsak: Date;
  gunes: Date;
  ogle: Date;
  ikindi: Date;
  aksam: Date;
  yatsi: Date;
  nextImsak: Date;
}

export interface Quote {
  quoteDe: string;
  quoteTr: string;
  author: string;
}


export async function fetchPrayerTimes(file: string) {
  try {
    const response = await fetch(file);
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error fetching prayer times:', error);
    return null;
    // throw error;
  }
}

export async function fetchDates() {
  try {
    const response = await fetch(config.dateJson);
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error fetching dates:', error);
    throw error;
  }
}

export function combineTimeAndDate(prayerTimes, dates): Prayers[] {
  return Object.keys(prayerTimes).map((key, index) => {
    const prayer = prayerTimes[key];
    if (index < Object.keys(prayerTimes).length - 1) {
      return {
        date: key,
        hicriDate: getHijriDateFromGregorian(dates, new Date(key)),
        imsak: new Date(`${prayer["Imsak"]}`) as Date,
        gunes: new Date(`${prayer["Güneş"]}`) as Date,
        ogle: new Date(`${prayer["Öğle"]}`) as Date,
        ikindi: new Date(`${prayer["İkindi"]}`) as Date,
        aksam: new Date(`${prayer["Akşam"]}`) as Date,
        yatsi: new Date(`${prayer["Yatsı"]}`) as Date,
        nextImsak: new Date(`${prayerTimes[Object.keys(prayerTimes)[index + 1]]["Imsak"]}`) as Date
      }
    }
    else {
      return {
        date: key,
        hicriDate: getHijriDateFromGregorian(dates, new Date(key)),
        imsak: new Date(`${prayer["Imsak"]}`) as Date,
        gunes: new Date(`${prayer["Güneş"]}`) as Date,
        ogle: new Date(`${prayer["Öğle"]}`) as Date,
        ikindi: new Date(`${prayer["İkindi"]}`) as Date,
        aksam: new Date(`${prayer["Akşam"]}`) as Date,
        yatsi: new Date(`${prayer["Yatsı"]}`) as Date,
        nextImsak: (() => {
          const date = new Date(`${prayerTimes[Object.keys(prayerTimes)[0]]["Imsak"]}`);
          date.setFullYear(date.getFullYear() + 1);
          return date;
        })()
      }
    }
  });
}

export function calculateRemainingTime(currentPrayer: Prayers, currentTime: Date): string {
  let remainingTime = '';
  // const currentTime = new Date();
  if (currentTime < currentPrayer.imsak) {
    remainingTime = calculateTimeDifference(currentTime, currentPrayer.imsak);
  } else if (currentTime < currentPrayer.gunes) {
    remainingTime = calculateTimeDifference(currentTime, currentPrayer.gunes);
  } else if (currentTime < currentPrayer.ogle) {
    remainingTime = calculateTimeDifference(currentTime, currentPrayer.ogle);
  } else if (currentTime < currentPrayer.ikindi) {
    remainingTime = calculateTimeDifference(currentTime, currentPrayer.ikindi);
  } else if (currentTime < currentPrayer.aksam) {
    remainingTime = calculateTimeDifference(currentTime, currentPrayer.aksam);
  } else if (currentTime < currentPrayer.yatsi) {
    remainingTime = calculateTimeDifference(currentTime, currentPrayer.yatsi);
  }
  else {
    remainingTime = calculateTimeDifference(currentTime, currentPrayer.nextImsak);
  }

  return remainingTime;
}

export function calculateTimeDifference(currentTime: Date, prayerTime: Date): string {
  const diff = prayerTime.getTime() - currentTime.getTime();

  const hours = Math.floor(diff / 1000 / 60 / 60);
  const minutes = Math.floor(diff / 1000 / 60 % 60);
  const seconds = Math.floor(diff / 1000 % 60);
  // TODO: Time formating

  return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
}


export function getTomorrowHijriDate(dates) {
  const tomorrow = new Date();
  tomorrow.setDate(tomorrow.getDate() + 1);

  return getHijriDateFromGregorian(dates, tomorrow)
}

export function getHijriDateFromGregorian(hijri_dates: any, date: Date) {
  let tempDate;
  if (date) {
    tempDate = new Date(date).toISOString().split('T')[0];
  } else {
    tempDate = new Date().toISOString().split('T')[0];
  }

  const hijriDate = hijri_dates[tempDate];
  return hijriDate["day"] + " " + hijriDate["month"] + " " + hijriDate["year"];

}

export function formatDate(date: string) {
  return String(date).split('-').reverse().join('.');
}

export function formatTime(time: Date): string {
  return time.toLocaleTimeString('tr-TR', { hour: '2-digit', minute: '2-digit' });
}

export function checkWhichPrayerTime(currentPrayer: Prayers, currentTime: Date): string {
  // const currentTime = new Date();
  // currentTime.setHours(20);
  // currentTime.setMinutes(40);

  // if (currentTime >= currentPrayer.imsak && currentTime < currentPrayer.gunes) {
  //   return "imsak";
  // } else if (currentTime >= currentPrayer.gunes && currentTime < currentPrayer.ogle) {
  if (currentTime >= currentPrayer.imsak && currentTime < new Date(currentPrayer.gunes.getTime() - 30 * 60 * 1000)) {
    return "imsak";
  } else if (currentTime >= new Date(currentPrayer.gunes.getTime() - 30 * 60 * 1000) && currentTime < currentPrayer.ogle) {
    return "gunes";
  } else if (currentTime >= currentPrayer.ogle && currentTime < currentPrayer.ikindi) {
    return "ogle";
  } else if (currentTime >= currentPrayer.ikindi && currentTime < currentPrayer.aksam) {
    return "ikindi";
  } else if (currentTime >= currentPrayer.aksam && currentTime < currentPrayer.yatsi) {
    return "aksam";
  } else {
    // Covers the time after yatsi until the next imsak
    return "yatsi";
  }
}

export function isGunesPassed(currentPrayer: Prayers, currentTime: Date): boolean {
  return currentTime >= currentPrayer.gunes;
}

export function convertToLocalIsoDate(date: Date) {
  const localISODate = date.toLocaleDateString('de-de');
  return localISODate.split('.').map((part) => part.padStart(2, '0')).reverse().join('-');
}

export async function fetchQuotes() {
  try {
    const response = await fetch('./quotes.json');
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error fetching quotes:', error);
    throw error;
  }
}

export function convertToQuotes(quotes): Quote[] {
  return quotes.map((quote) => {
    return {
      quote: quote["text"],
      author: quote["author"]
    }
  });
}

export async function getRandomQuote(retries = 10): Promise<any> {
  let retryDelay = 2 * 1000; // Start with 2 seconds

  for (let attempt = 1; attempt <= retries; attempt++) {
    try {
      const response = await fetch(`${config.apiUrl}/randomHadith`, {
        method: "POST",
        body: JSON.stringify({ mosque: config.camiNameIdentifier }),
      });

      if (!response.ok) {
        console.error(`Attempt ${attempt}: Network response was not ok`);
        logError(`Attempt ${attempt}: Network response was not ok (${response.status})`);
      }

      const data = await response.json();
      if (!data || Object.keys(data).length === 0) {
        console.error(`Attempt ${attempt}: Received empty response`);
        logError(`Attempt ${attempt}: Received empty response`);
      }

      return {
        quoteDe: data.deutsch,
        quoteTr: data.turkisch,
        author: data.quelle
      };
    } catch (error) {
      console.error(`Attempt ${attempt} failed:`, error);
      logError(`Attempt ${attempt} failed: ${error}`);

      if (attempt < retries) {
        if (attempt % 3 === 0) {
          retryDelay = 5 * 60 * 1000; // After every 3rd failure, wait 10 minutes

        }
        console.log(`Waiting ${retryDelay / 1000} seconds before retrying...`);
        logError(`Waiting ${retryDelay / 1000} seconds before retrying...`);
        await new Promise((resolve) => setTimeout(resolve, retryDelay));
      } else {
        console.error("All retry attempts failed.");
        logError(`All retry attempts failed.`);
        return null;
      }
    }
  }
}


// Function to log errors locally
export async function logError(message: string) {
  try {
    await fetch("/log", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message }),
    });
  } catch (error) {
    console.error("Failed to send log:", error);
  }
}
