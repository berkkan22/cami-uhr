<script>
	import ditib from '$lib/images/ditib_logo.png';
	import kiswah from '$lib/images/kiswah.jpg';
	import PrayerTimes from './PrayerTimes.svelte';
	import DateTimeDisplay from './DateTimeDisplay.svelte';
	import { config } from '$lib/config/config';
	import Quotes from './Quotes.svelte';
	import Header from './Header.svelte';

	export let currentPrayer;
	export let currentTime;
	export let remainingTime;
	export let currentPayerTime;
	export let quaotOfTheDay;
</script>

<div class="content">
	<div class="background-image" style="background-image: url({kiswah});"></div>
	<Header />

	<div class="main-content">
		<DateTimeDisplay {currentPrayer} {currentTime} {remainingTime} />

		<PrayerTimes {currentPrayer} {currentPayerTime} />

		<Quotes {quaotOfTheDay} />
	</div>

	{#if config.ditib}
		<div class="ditib-logo">
			<img src={ditib} alt="" srcset="" />
		</div>
	{/if}
	
</div>

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

	.ditib-logo > img {
		position: absolute;
		bottom: 0;
		right: 0;
		margin: 14px;
		width: 200px;
		height: auto;
	}
</style>
