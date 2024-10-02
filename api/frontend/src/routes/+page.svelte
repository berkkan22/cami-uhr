<script lang="ts">
	import Ankuendigungen from './components/Ankuendigungen.svelte';
	import Hadith from './components/Hadith.svelte';

	let isMenuOpen = false;
	let showHadith = true;

	function toggleMenu() {
		isMenuOpen = !isMenuOpen;
	}

	function showContent(content: string) {
		if (content === 'hadith') {
			showHadith = true;
			isMenuOpen = false;
		} else {
			showHadith = false;
			isMenuOpen = false;
		}
	}

	function clickOutside(element: HTMLDivElement, callbackFunction: { (): void; (): void }) {
		function onClick(event: { target: any }) {
			if (!element.contains(event.target)) {
				callbackFunction();
			}
		}

		document.body.addEventListener('click', onClick);

		return {
			update(newCallbackFunction: any) {
				callbackFunction = newCallbackFunction;
			},
			destroy() {
				document.body.removeEventListener('click', onClick);
			}
		};
	}
</script>

<div class="container">
	<div class="sidebar {isMenuOpen ? 'open' : ''}">
		<div class="hamburger" on:click={toggleMenu}>&#10005; Menu</div>

		<ul>
			<li>
				<a class={showHadith ? 'cur' : ''} href="#hadith" on:click={() => showContent('hadith')}
					>Hadith</a
				>
			</li>
			<li>
				<a
					class={showHadith ? '' : 'cur'}
					href="#ankuendigung"
					on:click={() => showContent('ankuendigung')}>Ankündigung</a
				>
			</li>
		</ul>
	</div>

	<div class="content">
		<div
			class="hamburger"
			on:click={toggleMenu}
			use:clickOutside={() => {
				// TODO: look into the clickOutside function because does not work as I like
				// console.log('clicked outside');
				isMenuOpen = false;
			}}
		>
			&#9776; Menu
		</div>

		{#if showHadith}
			<Hadith />
		{:else}
			<Ankuendigungen />
		{/if}
	</div>
</div>

<style>
	.container {
		display: flex;
		font-family: 'Arial', sans-serif;
	}

	.sidebar {
		width: 250px;
		height: 100vh;
		background-color: #f4f4f4;
		padding: 20px;
		border-radius: 8px;
		box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
	}

	.sidebar ul {
		list-style: none;
		padding: 0;
	}

	.sidebar li {
		margin-bottom: 15px;
	}

	.sidebar a {
		text-decoration: none;
		color: #333;
		font-size: 1.1em;
		font-weight: bold;
		display: block;
		padding: 10px;
		border-radius: 4px;
		transition:
			background-color 0.3s,
			color 0.3s;
	}

	.sidebar a.cur {
		background-color: #333;
		color: #fff;
	}
	.sidebar a:hover {
		background-color: #ddd;
		color: #000;
	}

	.content {
		flex-grow: 1;
		padding: 20px;
	}

	.hamburger {
		display: none;
		cursor: pointer;
		font-size: 1.2em;
		margin-bottom: 20px;
		width: 100px;
	}

	@media (max-width: 768px) {
		.sidebar {
			display: none;
		}

		.sidebar.open {
			display: block;
			position: absolute;
			width: 250px;
			height: 100%;
			background-color: #f4f4f4;
			z-index: 1000;
			border-radius: 0 8px 8px 0;
			box-shadow: 2px 0 4px rgba(0, 0, 0, 0.1);
		}

		.hamburger {
			display: block;
		}
	}
</style>
