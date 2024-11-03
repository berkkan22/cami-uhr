<script lang="ts">
	import { writable } from 'svelte/store';
	import { config } from '$lib/config';
	import toast, { Toaster } from 'svelte-french-toast';
	import { page } from '$app/stores';
	import { getValidAccessToken } from '$lib/utils';

	let hadithDeutsch = '';
	let hadithTurkisch = '';
	let quelle = '';
	let hadithList: any[] = [];

	let isLoading: boolean = false;

	async function handleSubmit(event: Event) {
		isLoading = true;
		event.preventDefault();

		if (hadithDeutsch.trim() === '' || hadithTurkisch.trim() === '' || quelle.trim() === '') {
			toast.error('Please fill all fields.', {
				position: 'bottom-center'
			});
			isLoading = false;
			return;
		}

		const hadithData = {
			deutsch: hadithDeutsch,
			turkisch: hadithTurkisch,
			quelle: quelle
		};

		try {
			const { validAccessToken } = await getValidAccessToken($page.data.session);
			const response = await fetch(`${config.apiUrl}/submitHadith`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
					'X-Token': `${validAccessToken}`
				},
				body: JSON.stringify(hadithData)
			});

			if (!response.ok) {
				isLoading = false;
				toast.error('Network response was not ok', {
					position: 'bottom-center'
				});
				throw new Error('Network response was not ok');
			}

			const result = await response.json();
			isLoading = false;
			console.log('Success:', result);
			toast.success('Hadith was submitted successfully.', {
				position: 'bottom-center'
			});
			clearInputs();
		} catch (error) {
			isLoading = false;
			console.error('Error:', error);
			toast.error(`Something went wrong ${error}`, {
				position: 'bottom-center'
			});
		}
	}

	async function showAllHadith() {
		isLoading = true;
		try {
			const { validAccessToken } = await getValidAccessToken($page.data.session);
			const response = await fetch(`${config.apiUrl}/getAllHadith`, {
				method: 'GET',
				headers: {
					'Content-Type': 'application/json',
					'X-Token': `${validAccessToken}`
				}
			});

			if (!response.ok) {
				isLoading = false;
				toast.error('Network response was not ok', {
					position: 'bottom-center'
				});
				throw new Error('Network response was not ok');
			}

			isLoading = false;
			const result = await response.json();
			hadithList = result['hadiths'];
		} catch (error) {
			isLoading = false;
			toast.error(`Something went wrong ${error}`, {
				position: 'bottom-center'
			});
		}
	}

	function clearInputs() {
		hadithDeutsch = '';
		hadithTurkisch = '';
		quelle = '';
	}
</script>

{#if isLoading}
	<div class="loading-overlay">
		<div class="loading-spinner"></div>
	</div>
{/if}

<section id="hadith">
	<h2>Hadith</h2>
	<form>
		<div>
			<label for="input1">Hadith (Deutsch)</label>
			<textarea id="hadith-deutsch" rows="3" bind:value={hadithDeutsch} />
		</div>
		<div>
			<label for="input2">Hadith (Türkisch)</label>
			<textarea id="hadith-turkisch" rows="3" bind:value={hadithTurkisch} />
		</div>
		<div>
			<label for="input3">Quelle</label>
			<input type="text" id="quelle" bind:value={quelle} />
		</div>
		<button type="submit" on:click={handleSubmit}>Speichern</button>
		<button type="submit" class="second" on:click={showAllHadith}>Show all hadith</button>
	</form>

	{#if hadithList.length > 0}
		<div class="allHadith">
			<ul>
				{#each hadithList as hadith}
					<li>
						<p><strong>Deutsch:</strong> {hadith.deutsch}</p>
						<p><strong>Türkisch:</strong> {hadith.turkisch}</p>
						<p><strong>Quelle:</strong> {hadith.quelle}</p>
					</li>
				{/each}
			</ul>
		</div>
	{/if}
</section>
<Toaster />

<style>
	section {
		margin-bottom: 40px;
	}

	h2 {
		font-size: 1.5em;
		margin-bottom: 20px;
	}

	form div {
		margin-bottom: 20px;
	}

	label {
		display: block;
		margin-bottom: 5px;
		font-size: 0.9em;
		color: #333;
	}

	textarea {
		width: 100%;
		padding: 10px;
		border: 1px solid #ccc;
		border-radius: 4px;
		box-sizing: border-box;
		font-size: 1em;
	}

	input[type='text'] {
		width: 100%;
		padding: 10px;
		border: 1px solid #ccc;
		border-radius: 4px;
		box-sizing: border-box;
		font-size: 1em;
	}

	button {
		padding: 10px 20px;
		border: none;
		border-radius: 4px;
		background-color: #007bff;
		color: white;
		font-size: 1em;
		cursor: pointer;
	}

	.second {
		background-color: #6c757d;
		margin-left: 10px;
	}

	button:hover {
		background-color: #0056b3;
	}

	.allHadith {
		margin-top: 20px;
	}

	ul {
		list-style-type: none;
		padding: 0;
	}

	li {
		background-color: #f9f9f9;
		margin-bottom: 10px;
		padding: 15px;
		border: 1px solid #ddd;
		border-radius: 4px;
	}

	li p {
		margin: 5px 0;
	}

	li p strong {
		color: #333;
	}

	.loading-overlay {
		position: fixed;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		background: rgba(0, 0, 0, 0.5);
		display: flex;
		justify-content: center;
		align-items: center;
		z-index: 1000;
	}

	.loading-spinner {
		border: 8px solid rgba(255, 255, 255, 0.3);
		border-top: 8px solid #fff;
		border-radius: 50%;
		width: 60px;
		height: 60px;
		animation: spin 1s linear infinite;
	}

	@keyframes spin {
		0% {
			transform: rotate(0deg);
		}
		100% {
			transform: rotate(360deg);
		}
	}
</style>
