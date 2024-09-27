<script lang="ts">
	import { formatDate, type Prayers } from '$lib/prayer';
	import { t } from '$lib/i10l/i10l';

	export let currentPrayer: Prayers;
	export let currentTime: string;
	export let remainingTime: string;
</script>

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

<style>
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
		min-width: 300px;
		max-width: 500px;
		/* padding: 10px 30px 10px 30px; top right bottom left */
		/* background-color: gray; */
		/* border-radius: 10px; */
		color: white;
		transition:
			transform 0.3s ease,
			margin 0.3s ease;
	}

	.time-title {
		font-size: 1.5rem;
		margin-bottom: 14px;
	}

	.time-value {
		font-size: 2rem;
	}

	#next-prayer-time > .time-value {
		font-size: 2.5rem;
		color: #89001c;
		font-weight: bold;
		text-shadow:
			-1px 0 white,
			0 1px white,
			1px 0 white,
			0 -1px white;
	}
</style>
