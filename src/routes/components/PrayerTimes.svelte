<script lang="ts">
	import { formatTime, isGunesPassed, type Prayers } from '$lib/prayer';
	import { t } from '$lib/i10l/i10l';
	import { onMount } from 'svelte';
	import { config } from '$lib/config/config';

	export let currentPrayer: Prayers;
	export let currentPayerTime: string;
	// pass the current time to test it when I set the offset
	export let currentTime: string;
	let showSabahBackgroundColor = false;

	let showFirstDiv = false;

	function toggleVisibility() {
		showFirstDiv = !showFirstDiv;
	}

	function showSabahBG() {
		const [hours, minutes] = currentTime.split(':').map(Number);
		const currentDate = new Date();
		currentDate.setHours(hours, minutes);
		showSabahBackgroundColor = isGunesPassed(currentPrayer, currentDate);
	}

	onMount(() => {
		const interval = setInterval(toggleVisibility, 2000);
		const sabahBG = setInterval(showSabahBG, 1000);
		return () => {
			clearInterval(interval);
			clearInterval(sabahBG);
		};
	});
</script>

<div class="prayer-times">
	{#each ['imsak', 'gunes', 'ogle', 'ikindi', 'aksam', 'yatsi'] as prayer}
		{#if prayer == 'gunes' && config.showSabahNamazi}
			{#if showFirstDiv}
				<div class="prayer-time {currentPayerTime == prayer ? 'current-prayer' : ''}">
					<div class="prayer-label {prayer}">{$t(prayer)}</div>
					<div class="prayer-time-value">{formatTime(currentPrayer[prayer])}</div>
				</div>
			{:else}
				<div
					class="prayer-time {currentPayerTime == prayer
						? 'current-prayer'
						: ''} sabah {showSabahBackgroundColor ? 'show' : ''}"
				>
					<div class="prayer-label">{$t('sabah')}</div>
					<div class="prayer-time-value">
						{formatTime(new Date(new Date(currentPrayer[prayer]).getTime() - 30 * 60 * 1000))}
					</div>
				</div>
			{/if}
		{:else}
			<div class="prayer-time {currentPayerTime == prayer ? 'current-prayer' : ''}">
				<div class="prayer-label {prayer}">{$t(prayer)}</div>
				<div class="prayer-time-value">{formatTime(currentPrayer[prayer])}</div>
			</div>
		{/if}
	{/each}
</div>

<style>
	.prayer-times {
		display: flex;
		justify-content: center;
		gap: 20px;
		padding: 0 20px;
		margin-top: 30px;
		color: white;
		align-items: center;
	}

	.prayer-time {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: space-between;
		min-width: 270px;
		max-width: 270px;
		/* height: 130px; */
		/* height: 165px; */

		padding: 10px 30px 10px 30px; /* top right bottom left */
		background-color: rgb(36, 36, 36);
		border-radius: 10px;
		color: white;
		transition:
			transform 0.3s ease,
			margin 0.3s ease;
	}

	.prayer-label {
		font-size: 2.5rem;
		margin-bottom: 5px;
	}

	.prayer-time-value {
		font-size: 3rem;
		font-weight: bold;
	}

	.current-prayer {
		/* background-color: #ff6347; */
		background-color: #89001c;
		transform: scale(1.4);
		transform-origin: center;
		margin: 0 60px;
	}

	.current-prayer.sabah {
		background-color: green;
	}

	.sabah.show {
		background-color: rgb(36, 36, 36);
	}

	.sabah > .prayer-label {
		padding-top: 15px;
		margin-bottom: 14px;
		font-size: 2rem;
		white-space: nowrap;
		overflow: hidden;
		text-overflow: ellipsis;
	}
</style>
