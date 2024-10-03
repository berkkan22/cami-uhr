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
	<div class="wrapper">
		<div class="marquee">
			<p>
				{announcement.deutsch}
			</p>
			<p class="spacer">---</p>
			<p>
				{announcement.tuerkisch}
			</p>
		</div>
	</div>
{/if}

<style>
	.wrapper {
		position: absolute;
		bottom: 0;
		width: 100%;
		overflow: hidden;
		font-size: 2rem;
		background-color: gold;
		z-index: -1;
		padding: 8px;
	}

	.marquee {
		background-color: gold;
		white-space: nowrap;
		overflow: hidden;
		animation: marquee 20s linear infinite;
	}

	.marquee p {
		display: inline-block;
	}

	@keyframes marquee {
		0% {
			transform: translateX(100%);
		}
		100% {
			transform: translateX(calc(-100%));
		}
	}

	.spacer {
		padding-left: 20px;
		padding-right: 20px;
	}
</style>
