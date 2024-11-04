<script>
	import ditib from '$lib/images/ditib_logo_rgb.png';
	import kiswah from '$lib/images/kiswah.jpg';
	import PrayerTimes from './PrayerTimes.svelte';
	import DateTimeDisplay from './DateTimeDisplay.svelte';
	import { config } from '$lib/config/config';
	import Quotes from './Quotes.svelte';
	import Header from './Header.svelte';
	import { t } from '$lib/i10l/i10l';
	import { formatDate } from '$lib/prayer';
	import cami from '$lib/images/001-removebg-preview.png';
	import allah from '$lib/images/allah_trans.png';
	import muhammed from '$lib/images/muhammed_trans.png';

	export let currentPrayer;
	export let currentTime;
	export let remainingTime;
	export let currentPayerTime;
	export let quaotOfTheDay;
</script>

<div class="content">
	<div class="background-image" style="background-image: url({kiswah});"></div>
	<!-- <Header /> -->
	{#if config.header}
		<div
			class="header"
			style="justify-content: {!config.dateOneLiner ? 'flex-start' : 'space-evenly'};"
		>
			{#if config.headerNames}
				<img class="arabic-caligrafi" src={muhammed} alt="Muhammed" />
			{/if}
			<div class="header-title">
				<img src={cami} alt="" class="background" />
				<h1 class="title">{$t('title', { name: config.camiName })}</h1>
			</div>
			{#if config.headerNames}
				<img class="arabic-caligrafi" src={allah} alt="Allah" />
			{/if}
			{#if !config.dateOneLiner}
				<!-- else content here -->
				<div class="date-container">
					<div id="today-date" class="date">
						<div class="time-value" id="today-date-value">{formatDate(currentPrayer.date)}</div>
					</div>
					<div id="islamic-date" class="date">
						<div class="time-value" id="islamic-date-value">{currentPrayer.hicriDate}</div>
					</div>
					<!-- <div class="weather">weather</div> -->
				</div>
				<div class="spacer-date"></div>
				<div class="time-container">
					<div id="current-time" class="date">
						<!-- <div class="time-title">{$t('currentTime')}</div> -->
						<div class="time-value">{currentTime}</div>
					</div>
					<div id="next-prayer-time" class="date">
						<div class="time-title">{$t('nextPrayer')}</div>
						<div class="time-value">{remainingTime}</div>
					</div>
				</div>
			{/if}
		</div>
	{:else}
		<div class="spacer"></div>
	{/if}

	<div class="main-content">
		{#if config.dateOneLiner}
			<DateTimeDisplay {currentPrayer} {currentTime} {remainingTime} />
		{/if}

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

	/* HEADER */
	.header {
		display: flex;
		/* justify-content: flex-start; */
		/* justify-content: space-evenly; */
		align-items: center;
		padding: 20px;
	}

	.arabic-caligrafi {
		width: 10%;
		height: auto;
	}

	.header-title {
		/* position: relative; */
		display: flex;
		justify-content: center;
		align-items: center;
		flex-direction: column;
		margin-left: 50px;
		margin-right: 100px;
	}

	.header-title > img {
		width: 90%;
		height: auto;
	}

	.title {
		position: relative;
		top: -30px;
		color: white;
		border-top: 2px solid white;
		width: fit-content;
		padding: 3px;
		font-size: 2rem;
	}

	.spacer {
		height: 120px;
	}

	/* DATE */
	.date {
		display: flex;
		flex-direction: column;
		align-items: start;
		min-width: 400px;
		max-width: 600px;
		color: white;
		transition:
			transform 0.3s ease,
			margin 0.3s ease;
		/* margin-bottom: 20px; */
	}

	#islamic-date-value {
		font-size: 3rem;
		color: #cacaca;
		margin-top: 10px;
	}

	.time-title {
		font-size: 2rem;
		margin-bottom: 14px;
	}

	.time-value {
		font-size: 5rem;
	}

	#next-prayer-time > .time-value {
		color: #89001c;
		font-weight: bold;
		font-size: 5rem;
		/* text-shadow:
			-1px 0 white,
			0 1px white,
			1px 0 white,
			0 -1px white; */
	}

	#next-prayer-time > .time-title {
		font-size: 2.5rem;
		margin-bottom: 0px;
	}

	/* .date-container {
		margin-right: 40%;
	} */

	#current-time > .time-value {
		margin-top: 50px;
		font-size: 8rem;
		margin-bottom: 15px;
	}

	.spacer-date {
		width: 10%;
	}

	.weather {
		margin-top: 20px;
		background-color: antiquewhite;
		width: 200px;
		height: 100px;
	}
</style>
