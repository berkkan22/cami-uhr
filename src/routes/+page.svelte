<script lang="ts">
	import { onMount } from 'svelte';
	import cami from '$lib/001-removebg-preview.png';
	import ditib from '$lib/ditib_logo.png';
	import kiswah from '$lib/kiswah.jpg';

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

	import { t, locale, locales } from '../i10l/i10l';

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

	$locale = 'De';
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
		currentTime = currentDate.toLocaleTimeString('de-DE');

		quaotOfTheDay = getRandomQuote(quotes);

		setInterval(() => {
			currentDate = new Date(Date.now() + timeOffset * convertMS);

			currentTime = currentDate.toLocaleTimeString('de-DE');
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

		setInterval(() => {
			if ($locale === 'De') {
				$locale = 'Tr';
			} else {
				$locale = 'De';
			}
		}, 10000);
	});
</script>

{#if currentPrayer !== undefined}
	<div class="content">
		<div class="background-image" style="background-image: url({kiswah});"></div>
		<div class="header">
			<img src={cami} alt="" class="background" />
			<h1 class="title">{$t('title')}</h1>
		</div>

		<div class="main-content">
			<div class="date-time-container">
				<div id="islamic-date" class="date">
					<div class="time-title">{$t('islamicDate')}</div>
					<div class="time-value" id="islamic-date-value">{currentPrayer.hicriDate}</div>
				</div>
				<div id="today-date" class="date">
					<div class="time-title">{$t('todayDate')}</div>
					<div class="time-value" id="today-date-value">{formatDate(currentPrayer.date)}</div>
				</div>
				<div id="current-time" class="date">
					<div class="time-title">{$t('currentTime')}</div>
					<div class="time-value">{currentTime}</div>
				</div>
				<div id="next-prayer-time" class="date">
					<div class="time-title">{$t('nextPrayer')}</div>
					<div class="time-value">{remainingTime}</div>
				</div>
			</div>
			<div class="prayer-times">
				<div class="prayer-time {currentPayerTime == 'imsak' ? 'current-prayer' : ''}">
					<div class="prayer-label">{$t('imsak')}</div>
					<div class="prayer-time-value">{formatTime(currentPrayer.imsak)}</div>
				</div>
				<div class="prayer-time {currentPayerTime == 'gunes' ? 'current-prayer' : ''}">
					<div class="prayer-label">{$t('gunes')}</div>
					<div class="prayer-time-value">{formatTime(currentPrayer.gunes)}</div>
				</div>
				<div class="prayer-time {currentPayerTime == 'oglen' ? 'current-prayer' : ''}">
					<div class="prayer-label">{$t('ogle')}</div>
					<div class="prayer-time-value">{formatTime(currentPrayer.ogle)}</div>
				</div>
				<div class="prayer-time {currentPayerTime == 'ikindi' ? 'current-prayer' : ''}">
					<div class="prayer-label">{$t('ikindi')}</div>
					<div class="prayer-time-value">{formatTime(currentPrayer.ikindi)}</div>
				</div>
				<div class="prayer-time {currentPayerTime == 'aksam' ? 'current-prayer' : ''}">
					<div class="prayer-label">{$t('aksam')}</div>
					<div class="prayer-time-value">{formatTime(currentPrayer.aksam)}</div>
				</div>
				<div class="prayer-time {currentPayerTime == 'yatzi' ? 'current-prayer' : ''}">
					<div class="prayer-label">{$t('yatsi')}</div>
					<div class="prayer-time-value">{formatTime(currentPrayer.yatsi)}</div>
				</div>
			</div>
			{#if quaotOfTheDay !== undefined}
				<div id="quote-container">
					<div id="quote-text">{quaotOfTheDay.quote}</div>
					<div id="quote-author">{quaotOfTheDay.author}</div>
				</div>
			{/if}
		</div>
		<div class="ditib-logo">
			<img src={ditib} alt="" srcset="" />
		</div>
	</div>
{/if}

<style>
	.content {
		width: 100%;
		margin-top: 20px;
		text-align: center;
	}

	.background-image {
		position: absolute;
		background-position: center;
		top: 0;
		left: 0;
		/* background-image: url('kiswah.jpg'); */
		width: 100%;
		height: 100vh;
		object-fit: contain;
		z-index: -1;
	}

	.background-image::after {
		content: '';
		position: absolute;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		background-color: rgba(0, 0, 0, 0.4);
		backdrop-filter: blur(1px);
	}

	.header {
		position: relative;
	}

	.header > img {
		width: 15%;
		height: auto;
	}

	.title {
		position: relative;
		left: 50vw;
		transform: translate(-50%, -1.7vw);
		color: white;
		border-top: 2px solid white;
		width: fit-content;
		padding: 3px;
		font-size: 1.5rem;
	}

	.date-time-container {
		display: flex;
		justify-content: center;
		gap: 0vw;
		margin-top: 20px;
		margin-bottom: 40px;
		color: white;
	}

	.date {
		display: flex;
		flex-direction: column;
		align-items: center;
		width: 250px;
		/* padding: 10px 30px 10px 30px; top right bottom left */
		/* background-color: gray; */
		/* border-radius: 10px; */
		color: white;
		transition:
			transform 0.3s ease,
			margin 0.3s ease;
	}

	.time-title {
		font-size: 1.25rem;
		margin-bottom: 5px;
	}

	.time-value {
		font-size: 1.5rem;
	}

	.prayer-times {
		display: flex;
		justify-content: center;
		gap: 20px;
		padding: 0 20px;
		margin-top: 30px;
		color: white;
	}

	.prayer-time {
		display: flex;
		flex-direction: column;
		align-items: center;
		width: 150px;
		padding: 10px 30px 10px 30px; /* top right bottom left */
		background-color: gray;
		border-radius: 10px;
		color: white;
		transition:
			transform 0.3s ease,
			margin 0.3s ease;
	}

	.prayer-label {
		font-size: 1.25rem;
		margin-bottom: 5px;
	}

	.prayer-time-value {
		font-size: 1.5rem;
		font-weight: bold;
	}

	.current-prayer {
		/* background-color: #ff6347; */
		background-color: #89001c;
		transform: scale(1.3);
		transform-origin: center;
		margin: 0 25px;
	}

	#quote-container {
		margin-top: 50px;
		color: white;
	}

	#quote-text {
		font-size: 1.5rem;
	}

	#quote-author {
		font-size: 1.25rem;
		font-style: italic;
		margin-top: 10px;
	}

	#quote-author::after,
	#quote-author::before {
		content: ' ~ ';
		font-style: italic;
	}

	.ditib-logo > img {
		position: absolute;
		bottom: 0;
		right: 0;
		margin: 14px;
		width: 120px;
		height: auto;
	}
</style>
