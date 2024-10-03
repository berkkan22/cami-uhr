<script lang="ts">
	import { config } from '$lib/config/config';
	import { t } from '$lib/i10l/i10l';
	import cami from '$lib/images/001-removebg-preview.png';
	import allah from '$lib/images/allah_trans.png';
	import muhammed from '$lib/images/muhammed_trans.png';
</script>

{#if config.header}
	<div class="header">
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
	</div>
{:else}
	<div class="spacer"></div>
{/if}

<style>
	.header {
		display: flex;
		justify-content: space-evenly;
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
	}

	.header-title > img {
		width: 70%;
		height: auto;
	}

	.title {
		position: relative;
		top: -30px;
		color: white;
		border-top: 2px solid white;
		width: fit-content;
		padding: 3px;
		font-size: 1.5rem;
	}

	.spacer {
		height: 120px;
	}
</style>
