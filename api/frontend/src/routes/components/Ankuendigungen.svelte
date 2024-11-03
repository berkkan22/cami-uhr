<script lang="ts">
	import { page } from '$app/stores';
	import { config } from '$lib/config';
	import { getValidAccessToken } from '$lib/utils';
	import { onMount } from 'svelte';
	import toast, { Toaster } from 'svelte-french-toast';

	let deutsch = '';
	let tuerkisch = '';
	let starttime = new Date()
		.toLocaleString('sv-SE', { timeZone: 'Europe/Berlin' })
		.replace(' ', 'T');
	let endtime = '';
	let socket: WebSocket;

	let isLoading: boolean = false;

	onMount(async () => {
		const { validAccessToken } = await getValidAccessToken($page.data.session);

		socket = new WebSocket(`${config.wsUrl}/ws?token=${validAccessToken}`);

		// Connection opened
		socket.addEventListener('open', function (event) {
			console.log("It's open");
		});

		socket.addEventListener('disconnect', () => {
			console.log('Disconnected from WebSocket server');
		});

		socket.addEventListener('message', (event) => {
			console.log('Message from server ', event.data);
		});
	});

	function handleSubmit(event: Event) {
		isLoading = true;
		event.preventDefault();

		const data = {
			type: 'announcement',
			message_german: deutsch,
			message_turkish: tuerkisch,
			start_date: starttime,
			end_date: endtime
		};

		console.log(data);
		socket.send(JSON.stringify(data));
		isLoading = false;
		toast.success('Announcement submitted successfully.', {
			position: 'bottom-center'
		});
		clearInputs();
	}

	function clearInputs() {
		deutsch = '';
		tuerkisch = '';
		starttime = new Date().toLocaleString('sv-SE', { timeZone: 'Europe/Berlin' }).replace(' ', 'T');
		endtime = '';
	}
</script>

{#if isLoading}
	<div class="loading-overlay">
		<div class="loading-spinner"></div>
	</div>
{/if}

<section id="ankuendigung">
	<h2>Ankündigung</h2>

	<form>
		<div>
			<label for="deutsch">Deutsch</label>
			<input type="text" id="deutsch" name="deutsch" bind:value={deutsch} />
		</div>
		<div>
			<label for="tuerkisch">Türkisch</label>
			<input type="text" id="tuerkisch" name="tuerkisch" bind:value={tuerkisch} />
		</div>
		<div>
			<label for="starttime">Start Time</label>
			<input type="datetime-local" id="starttime" name="starttime" bind:value={starttime} />
		</div>
		<div>
			<label for="endtime">End Time</label>
			<input type="datetime-local" id="endtime" name="endtime" bind:value={endtime} />
		</div>
		<button type="submit" on:click={handleSubmit}>Submit</button>
	</form>
</section>
<Toaster />

<style>
	section {
		margin-bottom: 40px;
	}

	h2 {
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

	input[type='text'] {
		width: 100%;
		padding: 10px;
		border: 1px solid #ccc;
		border-radius: 4px;
		box-sizing: border-box;
		font-size: 1em;
	}

	input[type='datetime-local'] {
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
