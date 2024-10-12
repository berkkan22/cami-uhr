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
		min-width: 400px;
		max-width: 600px;
		color: white;
		transition:
			transform 0.3s ease,
			margin 0.3s ease;
		margin-bottom: 50px;
	}

	.time-title {
		font-size: 2rem;
		margin-bottom: 14px;
	}

	.time-value {
		font-size: 4rem;
	}

	#next-prayer-time > .time-value {
		color: #89001c;
		font-weight: bold;
	}
</style>
