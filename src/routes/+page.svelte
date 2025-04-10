<script lang="ts">
	import { onMount } from 'svelte';

	import { config } from '$lib/config/config';

	import {
		fetchPrayerTimes,
		fetchDates,
		combineTimeAndDate,
		calculateRemainingTime,
		checkWhichPrayerTime,
		type Prayers,
		getTomorrowHijriDate,
		convertToLocalIsoDate,
		type Quote,
		getRandomQuote
	} from '$lib/prayer';

	import { locale } from '$lib/i10l/i10l';
	import OsmanBeyCami from './components/OsmanBeyCami.svelte';
	import Announcements from './components/announcements.svelte';

	let prayerTimesRaw: any;
	let currentPrayer: Prayers | undefined;
	let currentPayerTime = '';

	let remainingTime: string;
	let currentTime: string;

	$locale = 'De';

	let quaotOfTheDay: Quote;
	let isFetchingQuote = false;
	let attemptCount = 0;
	let intervalTime = 1000; // Initial interval time in milliseconds
	function fetchQuote() {
		if (!isFetchingQuote) {
			isFetchingQuote = true;
			getRandomQuote().then((quote) => {
				console.log(`[${new Date().toISOString()}] fetching quote`);
				if (quote !== null && quote !== undefined) {
					quaotOfTheDay = quote;
					clearInterval(quoteInterval);
				} else {
					attemptCount++;
					adjustIntervalTime();
				}
				isFetchingQuote = false;
			});
		}
	}

	function adjustIntervalTime() {
		if (attemptCount % 100 < 3) {
			intervalTime = 1000; // Set interval time to 1 second for the first 3 attempts
		} else if (attemptCount % 100 >= 3 && attemptCount % 100 < 6) {
			intervalTime = 5000; // Set interval time to 5 seconds for the next 3 attempts
		} else if (attemptCount % 100 >= 6 && attemptCount % 100 < 9) {
			intervalTime = 10000; // Set interval time to 10 seconds for the next 3 attempts
		} else if (attemptCount % 100 >= 9) {
			intervalTime = 30000; // Set interval time to 30 seconds for the remaining attempts
		}
		clearInterval(quoteInterval);
		quoteInterval = setInterval(fetchQuote, intervalTime);
	}

	let quoteInterval = setInterval(fetchQuote, intervalTime);

	onMount(async () => {
		prayerTimesRaw = await fetchPrayerTimes(config.prayerJson);

		if (prayerTimesRaw === null) {
			return;
		}

		let datesRaw = await fetchDates();

		let res = combineTimeAndDate(prayerTimesRaw, datesRaw);
		console.log(res);
		let currentDate = new Date();
		let timeOffset = 0;
		let convertMS = 3600000;

		currentPrayer = res.find(
			(prayer) =>
				prayer.date ===
				`${currentDate.getFullYear()}-${String(currentDate.getMonth() + 1).padStart(2, '0')}-${String(currentDate.getDate()).padStart(2, '0')}`
		);

		// get the current time and update it every second
		// update the remaining time every second
		remainingTime = '00:00:00';
		currentTime = currentDate.toLocaleTimeString('de-DE');

		if (quaotOfTheDay === null || quaotOfTheDay === undefined) {
			fetchQuote();
			// let isFetchingQuote = false;
			// const quoteInterval = setInterval(async () => {
			// 	if (!isFetchingQuote) {
			// 		isFetchingQuote = true;
			// 		getRandomQuote().then((quote) => {
			// 			console.log(`[${new Date().toISOString()}] fetching quote`);
			// 			if (quote !== null && quote !== undefined) {
			// 				quaotOfTheDay = quote;
			// 			}
			// 			isFetchingQuote = false;
			// 			if (quote !== null && quote !== undefined) {
			// 				console.log('clearing interval');
			// 				clearInterval(quoteInterval);
			// 			}
			// 		});
			// 	}
			// }, 1000);
		}

		setInterval(async () => {
			currentDate = new Date(Date.now() + timeOffset * convertMS);

			currentTime = currentDate.toLocaleTimeString('de-DE');
			if (currentPrayer !== undefined) {
				remainingTime = calculateRemainingTime(currentPrayer, currentDate);
				currentPayerTime = checkWhichPrayerTime(currentPrayer, currentDate);

				// check if it is aksam then change the hijri date to the next day
				if (currentPayerTime === 'aksam' && !config.changeIslamicDayOnMidnight) {
					currentPrayer.hicriDate = getTomorrowHijriDate(datesRaw);
				}

				// check if it is midnight then change everything prayer times dates and quotes
				if (
					currentDate.getHours() === 0 &&
					currentDate.getMinutes() === 0 &&
					currentDate.getSeconds() === 0
				) {
					currentPrayer = res.find((prayer) => prayer.date === convertToLocalIsoDate(currentDate));
					fetchQuote();
					// let isFetchingQuote = false;
					// const quoteInterval2 = setInterval(async () => {
					// 	if (!isFetchingQuote) {
					// 		isFetchingQuote = true;
					// 		getRandomQuote().then((quote) => {
					// 			console.log(`[${new Date().toISOString()}] fetching quote 2`);
					// 			if (quote !== null && quote !== undefined) {
					// 				quaotOfTheDay = quote;
					// 			}
					// 			isFetchingQuote = false;
					// 			if (quote !== null && quote !== undefined) {
					// 				console.log('clearing interval');
					// 				clearInterval(quoteInterval2);
					// 			}
					// 		});
					// 	}
					// }, 10000);
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
	<OsmanBeyCami {currentPrayer} {currentTime} {remainingTime} {currentPayerTime} {quaotOfTheDay} />
{/if}

{#if config.showAnnouncements}
	<Announcements />
{/if}

{#if prayerTimesRaw === null}
	<div class="error-container">
		<h1>Error 404</h1>
		<p>Prayer time json file not found</p>
	</div>
{/if}

<style>
	.error-container {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		height: 100vh;
		text-align: center;
		background-color: #f8d7da;
		color: #721c24;
		padding: 20px;
		border: 1px solid #f5c6cb;
		border-radius: 5px;
	}

	.error-container h1 {
		font-size: 2rem;
		margin-bottom: 1rem;
	}

	.error-container p {
		font-size: 1.2rem;
		margin-bottom: 1.5rem;
	}
</style>
