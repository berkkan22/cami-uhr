<script lang="ts">
	import { onMount } from 'svelte';
	import {
		fetchPrayerTimes,
		fetchDates,
		combineTimeAndDate,
		getHijriDateFromGregorian,
		formatTime,
		formatDate,
		calculateRemainingTime,
		checkWhichPrayerTime,
		type Prayers,
		getTomorrowHijriDate,
		convertToLocalIsoDate,
		type Quote,
		convertToQuotes,
		fetchQuotes,
		getRandomQuote
	} from '$lib/prayer';

	// load prayr times from csv
	// load date and hijri date from file
	// create class
	// add then to a list of the objects
	// on start up get the current date and display the current prayer times and date and hijri date
	// on aksam namazi change hijri date to the next date
	// on midnight change everything prayer times dates and quaot
	// quoates erst später zuerst die zeiten

	let currentPrayer: Prayers | undefined;
	let currentPayerTime = ''; // TODO: auo

	let remainingTime: string;
	let currentTime: string;

	let quaotOfTheDay: Quote;

	onMount(async () => {
		let prayerTimesRaw = await fetchPrayerTimes();
		let datesRaw = await fetchDates();
		let quotesRaw = await fetchQuotes();

		let res = combineTimeAndDate(prayerTimesRaw, datesRaw);
		let quotes = convertToQuotes(quotesRaw);

		let currentDate = new Date();
		let timeOffset = 0;
		let convertMS = 3600000;

		currentPrayer = res.find((prayer) => prayer.date === currentDate.toISOString().split('T')[0]);

		// get the current time and update it every second
		// update the remaining time every second
		remainingTime = '00:00:00';
		currentTime = currentDate.toLocaleTimeString();

		quaotOfTheDay = getRandomQuote(quotes);

		setInterval(() => {
			currentDate = new Date(Date.now() + timeOffset * convertMS);

			currentTime = currentDate.toLocaleTimeString();
			if (currentPrayer !== undefined) {
				remainingTime = calculateRemainingTime(currentPrayer, currentDate);
				currentPayerTime = checkWhichPrayerTime(currentPrayer, currentDate);
				// console.log(currentPayerTime);

				// check if it is aksam then change the hijri date to the next day
				if (currentPayerTime === 'aksam') {
					currentPrayer.hicriDate = getTomorrowHijriDate(datesRaw);
				}

				// check if it is midnight then change everything prayer times dates and quotes
				if (
					currentDate.getHours() === 0 &&
					currentDate.getMinutes() === 0 &&
					currentDate.getSeconds() === 0
				) {
					currentPrayer = res.find((prayer) => prayer.date === convertToLocalIsoDate(currentDate));
					quaotOfTheDay = getRandomQuote(quotes);
				}
			}
		}, 1000);
	});
</script>

<h1>Gebetszeiten</h1>

{#if currentPrayer !== undefined}
	<!-- content here -->
	<div id="current-time-container">
		<div id="islamic-date">
			<div class="time-title">Islamisches Datum</div>
			<div class="time-value" id="islamic-date-value">{currentPrayer.hicriDate}</div>
		</div>
		<div id="today-date">
			<div class="time-title">Heutiges Datum</div>
			<div class="time-value" id="today-date-value">{formatDate(currentPrayer.date)}</div>
		</div>
		<div id="current-time">
			<div class="time-title">Aktuelle Zeit</div>
			<div class="time-value">{currentTime}</div>
		</div>
		<div id="next-prayer-time">
			<div class="time-title">Verbleibende Zeit</div>
			<div class="time-value">{remainingTime}</div>
		</div>
	</div>

	<div id="prayer-times">
		<div class="prayer-time {currentPayerTime == 'imsak' ? 'current-prayer' : ''}">
			<div class="prayer-label">Imsak</div>
			<div class="prayer-time-value">{formatTime(currentPrayer.imsak)}</div>
		</div>
		<div class="prayer-time {currentPayerTime == 'gunes' ? 'current-prayer' : ''}">
			<div class="prayer-label">Günes</div>
			<div class="prayer-time-value">{formatTime(currentPrayer.gunes)}</div>
		</div>
		<div class="prayer-time {currentPayerTime == 'oglen' ? 'current-prayer' : ''}">
			<div class="prayer-label">Öglen</div>
			<div class="prayer-time-value">{formatTime(currentPrayer.ogle)}</div>
		</div>
		<div class="prayer-time {currentPayerTime == 'ikindi' ? 'current-prayer' : ''}">
			<div class="prayer-label">Ikindi</div>
			<div class="prayer-time-value">{formatTime(currentPrayer.ikindi)}</div>
		</div>
		<div class="prayer-time {currentPayerTime == 'aksam' ? 'current-prayer' : ''}">
			<div class="prayer-label">Aksam</div>
			<div class="prayer-time-value">{formatTime(currentPrayer.aksam)}</div>
		</div>
		<div class="prayer-time {currentPayerTime == 'yatzi' ? 'current-prayer' : ''}">
			<div class="prayer-label">yatsi</div>
			<div class="prayer-time-value">{formatTime(currentPrayer.yatsi)}</div>
		</div>
	</div>
	<!-- Hier werden die Gebetszeiten angezeigt -->

	{#if quaotOfTheDay !== undefined}
		<!-- content here -->
		<div id="quote-container">
			<div id="quote-text">{quaotOfTheDay.quote}</div>
			<div id="quote-author">{quaotOfTheDay.author}</div>
		</div>
	{/if}
{:else}
	<h1>Error</h1>
{/if}

<style>
	h1 {
		margin-bottom: 50px; /* Abstand zwischen Titel und restlichem Inhalt */
	}

	#prayer-times {
		display: flex;
		justify-content: center;
		gap: 20px; /* Standardabstand zwischen den Gebetszeiten */
		padding: 0 20px; /* Zusätzlicher Abstand zum Rand */
	}

	.prayer-time {
		display: flex;
		flex-direction: column;
		align-items: center;
		width: 150px;
		padding: 15px;
		border-radius: 5px;
		background-color: #008b8b; /* Dunklerer Türkis-Ton */
		color: white;
		transition:
			transform 0.3s ease,
			margin 0.3s ease;
		box-sizing: border-box;
	}

	.prayer-label {
		font-size: 20px; /* Größere Schriftgröße für die Bezeichnung */
		margin-bottom: 5px;
	}

	.prayer-time-value {
		font-size: 24px; /* Größere Schriftgröße für die Zeit */
		font-weight: bold;
	}

	.current-prayer {
		background-color: #ff6347; /* Hervorhebung der aktuellen Gebetszeit */
		transform: scale(1.2); /* Vergrößert die Gebetszeit noch mehr */
		transform-origin: center; /* Vergrößert zentriert */
		margin: 0 40px; /* Zusätzlicher Abstand für die vergrößerte Gebetszeit */
	}

	#current-time-container {
		display: flex;
		justify-content: center;
		margin-bottom: 40px; /* Größerer Abstand zum Gebetszeiten-Bereich */
		font-size: 24px;
		color: white;
	}

	#current-time,
	#next-prayer-time,
	#today-date,
	#islamic-date {
		text-align: center;
		margin: 0 20px;
	}

	.time-title {
		font-size: 24px;
		font-weight: bold;
		margin-bottom: 5px;
	}

	.time-value {
		font-size: 24px;
	}

	#quote-container {
		margin-top: 50px;
		color: white;
	}

	#quote-text {
		font-size: 24px;
	}

	#quote-author {
		font-size: 20px;
		font-style: italic;
		margin-top: 10px;
	}
</style>
