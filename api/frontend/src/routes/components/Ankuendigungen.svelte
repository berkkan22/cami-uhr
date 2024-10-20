<script lang="ts">
	import { config } from '$lib/config';
	import { onMount } from 'svelte';

	let deutsch = '';
	let tuerkisch = '';
	let starttime = new Date()
		.toLocaleString('sv-SE', { timeZone: 'Europe/Berlin' })
		.replace(' ', 'T');
	let endtime = '';
	let socket: WebSocket;

	onMount(() => {
		socket = new WebSocket(`wss://cms.prayer-time.berkkan.de/api//ws?token=${config.apiKey}`);

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
	}
</script>

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
</style>
