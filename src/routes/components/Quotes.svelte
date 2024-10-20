<script lang="ts">
	import { config } from '$lib/config/config';
	import { t, locale } from '$lib/i10l/i10l';

	export let quaotOfTheDay;
</script>

<div id="quote-container">
	{#if config.quotes && config.apiKey.trim() === ''}
		<h1 class="no-api-key">{$t('noApiKey')}</h1>
	{/if}
	{#if config.quotes && config.apiKey.trim() !== ''}
		{#if quaotOfTheDay !== undefined}
			<div id="quote-text">
				{$t('hadith', { name: $locale == 'De' ? quaotOfTheDay.quoteDe : quaotOfTheDay.quoteTr })}
			</div>
			<div id="quote-author">{quaotOfTheDay.author}</div>
		{/if}
	{/if}
</div>

<style>
	.no-api-key {
		margin-top: 9vh;
		color: red;
		font-size: 2rem;
		margin-top: 20px;
		font-weight: bold;
	}

	#quote-container {
		margin-top: 9vh;
		color: white;
		padding: 64px;
	}

	#quote-text {
		font-size: 3rem;
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
