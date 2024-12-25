<script lang="ts">
	import { config } from '$lib/config/config';
	import { t, locale } from '$lib/i10l/i10l';

	export let quaotOfTheDay;
</script>

<div id="quote-container">
	{#if config.quotes}
		{#if quaotOfTheDay !== undefined && quaotOfTheDay !== null}
			<div id="quote-text">
				{$t('hadith', { name: $locale == 'De' ? quaotOfTheDay.quoteDe : quaotOfTheDay.quoteTr })}
			</div>
			<div id="quote-author">{quaotOfTheDay.author}</div>
		{/if}
	{/if}
</div>

<style>
	#quote-container {
		margin-top: 4vh;
		color: white;
		padding: 40px 64px 64px 64px;
	}

	#quote-text {
		font-size: 3.1rem;
	}

	#quote-author {
		font-size: 2rem;
		font-style: italic;
		margin-top: 20px;
	}

	#quote-author::after,
	#quote-author::before {
		content: ' ~ ';
		font-style: italic;
	}
</style>
