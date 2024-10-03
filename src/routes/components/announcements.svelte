<script lang="ts">
	import { onMount } from 'svelte';

	interface Announcement {
		deutsch: string;
		tuerkisch: string;
		starttime: string;
		endtime: string;
	}
	let announcement: Announcement;

	onMount(() => {
		const socket = new WebSocket('ws://127.0.0.1:8000/ws');

		// Connection opened
		socket.addEventListener('open', function (event) {
			console.log("It's open");
		});

		socket.addEventListener('message', (event) => {
			console.log('Message from server ', event.data);
			const data = JSON.parse(event.data);
			announcement = data;
			console.log(announcement);
		});

		socket.addEventListener('disconnect', () => {
			console.log('Disconnected from WebSocket server');
		});
	});
</script>

{#if announcement != undefined}
	<p>{announcement.deutsch}</p>
{/if}

<style>
</style>
