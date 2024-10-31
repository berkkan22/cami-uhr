<script lang="ts">
	import { formatTime } from '$lib/prayer';
	import { t } from '$lib/i10l/i10l';

	export let currentPrayer;
	export let currentPayerTime: string;

	import { onMount } from 'svelte';

	let showFirstDiv = true;

	function toggleVisibility() {
		showFirstDiv = !showFirstDiv;
	}

	onMount(() => {
		const interval = setInterval(toggleVisibility, 2000);
		return () => clearInterval(interval);
	});
</script>

<div class="prayer-times">
	{#each ['imsak', 'gunes', 'ogle', 'ikindi', 'aksam', 'yatsi'] as prayer}
		{#if prayer == 'gunes'}
			{#if showFirstDiv}
				<div class="prayer-time {currentPayerTime == prayer ? 'current-prayer' : ''}">
					<div class="prayer-label {prayer}">{$t(prayer)}</div>
					<div class="prayer-time-value">{formatTime(currentPrayer[prayer])}</div>
				</div>
			{:else}
				<div class="prayer-time {currentPayerTime == prayer ? 'current-prayer' : ''} sabah">
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
		min-width: 250px;
		height: 130px;

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

	.current-prayer + .sabah {
		background-color: green;
	}

	.sabah > .prayer-label {
		font-size: 2rem;
		white-space: nowrap;
		overflow: hidden;
		text-overflow: ellipsis;
	}
</style>
