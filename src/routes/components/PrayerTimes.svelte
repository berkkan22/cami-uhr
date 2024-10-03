<script lang="ts">
	import { formatTime } from '$lib/prayer';
	import { t } from '$lib/i10l/i10l';

	export let currentPrayer;
	export let currentPayerTime: string;
</script>

<div class="prayer-times">
	{#each ['imsak', 'gunes', 'ogle', 'ikindi', 'aksam', 'yatsi'] as prayer}
		<div class="prayer-time {currentPayerTime == prayer ? 'current-prayer' : ''}">
			<div class="prayer-label">{$t(prayer)}</div>
			<div class="prayer-time-value">{formatTime(currentPrayer[prayer])}</div>
		</div>
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
		width: 250px;
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
</style>
