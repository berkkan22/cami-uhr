<script lang="ts">
	import { page } from '$app/stores';
	import { config } from '$lib/config';
	import { getValidAccessToken } from '$lib/utils';
	import { checkWebsocketConnection, connectToWebsocket } from '$lib/websocket';
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
	let announcements: any[] = [];
	let deleteOldAnnouncement = -1;

	onMount(async () => {
		const { validAccessToken } = await getValidAccessToken($page.data.session);

		socket = connectToWebsocket(`${config.wsUrl}/ws?token=${validAccessToken}`);
	});

	async function handleSubmit(event: Event) {
		const { validAccessToken } = await getValidAccessToken($page.data.session);
		if (deleteOldAnnouncement !== -1) {
			await fetch(`${config.apiUrl}/deleteAnnouncement`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
					'X-Token': `${validAccessToken}`,
					id: `${deleteOldAnnouncement}`
				}
			});
			deleteOldAnnouncement = -1;
		}
		isLoading = true;
		event.preventDefault();

		// check if websocket is connected else reconnect
		socket = await checkWebsocketConnection(socket, $page.data.session);

		const data = {
			type: 'announcement',
			message_german: deutsch,
			message_turkish: tuerkisch,
			start_date: starttime,
			end_date: endtime
		};

		console.log(data);
		socket.send(JSON.stringify(data));
		socket.onmessage = function (event) {
			if (event.data.includes('successful')) {
				toast.success('Announcement submitted successfully.', {
					position: 'bottom-center'
				});
				clearInputs();
			} else if (event.data.includes('failed') || event.data.includes('Error')) {
				toast.error('Failed to submit announcement.', {
					position: 'bottom-center'
				});
			}
			console.log('Message from server ', event.data);
			isLoading = false;
		};
	}

	function clearInputs() {
		deutsch = '';
		tuerkisch = '';
		starttime = new Date().toLocaleString('sv-SE', { timeZone: 'Europe/Berlin' }).replace(' ', 'T');
		endtime = '';
	}

	async function showAllAnnouncements() {
		isLoading = true;

		try {
			const { validAccessToken } = await getValidAccessToken($page.data.session);
			const response = await fetch(`${config.apiUrl}/announcements`, {
				method: 'POST',
				body: JSON.stringify({ token: validAccessToken })
			});
			if (!response.ok) {
				isLoading = false;
				throw new Error('Failed to fetch announcements');
			}
			const result = await response.json();
			announcements = result['announcements'];
			console.log(announcements);
			isLoading = false;
			toast.success('Fetched all announcements successfully.', {
				position: 'bottom-center'
			});
		} catch (error) {
			isLoading = false;
			console.error(error);
			toast.error('Failed to fetch announcements.', {
				position: 'bottom-center'
			});
		}
	}

	function editAnnouncement(announcement) {
		deutsch = announcement[1];
		tuerkisch = announcement[2];
		starttime = announcement[4];
		endtime = announcement[5];
		deleteOldAnnouncement = announcement[0];
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
		<button class="second" on:click={showAllAnnouncements}>Zeige alle Ankündigungen</button>
	</form>

	{#if announcements.length > 0}
		<div class="announcements">
			{#each announcements as announcement}
				<div class="announcement">
					<div class="announcement-text">
						<p><strong>Deutsch:</strong> {announcement[1]}</p>
						<p><strong>Türkisch:</strong> {announcement[2]}</p>
						<p><strong>Start Time:</strong> {announcement[4]}</p>
						<p><strong>End Time:</strong> {announcement[5]}</p>
					</div>
					<button class="edit-button" on:click={() => editAnnouncement(announcement)}> ✏️ </button>
				</div>
			{/each}
		</div>
	{/if}
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

	.announcements {
		margin-top: 20px;
	}
	.announcement {
		border: 1px solid #ccc;
		padding: 10px;
		margin-bottom: 10px;
		border-radius: 4px;
		display: flex;
		justify-content: space-between;
		align-items: center;
	}

	.announcement-text {
		flex-grow: 1;
	}

	.edit-button {
		background: none;
		border: none;
		cursor: pointer;
		font-size: 1.2em;
	}

	.second {
		background-color: #6c757d;
		margin-left: 10px;
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
