<script>
	import cami from '$lib/001-removebg-preview.png';
	import ditib from '$lib/ditib_logo.png';
	import kiswah from '$lib/kiswah.jpg';
	import PrayerTimes from './PrayerTimes.svelte';
	import DateTimeDisplay from './DateTimeDisplay.svelte';
	import { t } from '$lib/i10l/i10l';

	export let currentPrayer;
	export let currentTime;
	export let remainingTime;
	export let currentPayerTime;
	export let quaotOfTheDay;
</script>

<div class="content">
	<div class="background-image" style="background-image: url({kiswah});"></div>

	<div class="main-content">
		<DateTimeDisplay {currentPrayer} {currentTime} {remainingTime} />

		<PrayerTimes {currentPrayer} {currentPayerTime} />

		<!-- {#if quaotOfTheDay !== undefined}
			<div id="quote-container">
				<div id="quote-text">{quaotOfTheDay.quote}</div>
				<div id="quote-author">{quaotOfTheDay.author}</div>
			</div>
		{/if} -->
	</div>
	<div class="ditib-logo">
		<img src={ditib} alt="" srcset="" />
	</div>
</div>

<style>
	.content {
		width: 100%;
		margin-top: 50px;
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

	.remove {
		display: none;
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

	#quote-container {
		margin-top: 16vh;
		color: white;
	}

	#quote-text {
		font-size: 2rem;
	}

	#quote-author {
		font-size: 1.5rem;
		font-style: italic;
		margin-top: 20px;
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
