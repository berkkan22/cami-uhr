<script lang="ts">
	import { writable } from 'svelte/store';
	import { config } from '$lib/config';
	import Snackbar, { Label, Actions } from '@smui/snackbar';
	import IconButton from '@smui/icon-button';
	import Button from '@smui/button';

	let snackbarSuccess: Snackbar;
	let snackbarError: Snackbar;
	let errorMessage = '';

	let hadithDeutsch = '';
	let hadithTurkisch = '';
	let quelle = '';

	async function handleSubmit(event: Event) {
		event.preventDefault();

		const hadithData = {
			deutsch: hadithDeutsch,
			turkisch: hadithTurkisch,
			quelle: quelle
		};

		console.log(hadithData);

		try {
			const response = await fetch('https://api.cms.prayer-time.berkkan.de/submitHadith', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
					'X-API-Key': `${config.apiKey}`
				},
				body: JSON.stringify(hadithData)
			});

			if (!response.ok) {
				throw new Error('Network response was not ok');
			}

			const result = await response.json();
			console.log('Success:', result);
			snackbarSuccess.open();
		} catch (error) {
			console.error('Error:', error);
			errorMessage = `Something went wrong ${error.message}`;
			snackbarError.open();
		}
	}
</script>

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
	</form>
</section>
<Snackbar bind:this={snackbarSuccess} class="demo-success">
	<Label>Hadith was submitted successfully</Label>
	<Actions>
		<IconButton class="material-icons" title="Dismiss">close</IconButton>
	</Actions>
</Snackbar>
<Snackbar bind:this={snackbarError} labelText={errorMessage} class="demo-error">
	<Label></Label>
	<Actions>
		<IconButton class="material-icons" title="Dismiss">close</IconButton>
	</Actions>
</Snackbar>

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

	button:hover {
		background-color: #0056b3;
	}
</style>
