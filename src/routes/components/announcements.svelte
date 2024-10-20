<script lang="ts">
	import { onMount } from 'svelte';
	import { config } from '$lib/config/config';

	interface Announcement {
		deutsch: string;
		tuerkisch: string;
		starttime: string;
		endtime: string;
		visible: boolean;
	}
	let announcements: Announcement[] = [];
	let showAnnouncement = false;

	onMount(() => {
		fetch('https://cms.prayer-time.berkkan.de/api/announcements', {
			method: 'GET',
			headers: {
				'X-API-Key': `${config.apiKey}`
			}
		})
			.then((response) => response.json())
			.then((data) => {
				if (data) {
					for (let i = 0; i < data['announcements'].length; i++) {
						let temp: Announcement = {
							deutsch: data['announcements'][i][1],
							tuerkisch: data['announcements'][i][2],
							starttime: data['announcements'][i][4],
							endtime: data['announcements'][i][5],
							visible: data['announcements'][i][6]
						};
						temp.visible = false;
						announcements = [...announcements, temp];
					}
					console.log(announcements);
				}
			})
			.catch((error) => console.error('Error fetching announcements:', error));

		const socket = new WebSocket(`wss://cms.prayer-time.berkkan.de/api/ws?token=${config.apiKey}`);

		// Connection opened
		socket.addEventListener('open', function (event) {
			console.log("It's open");
		});

		socket.addEventListener('message', (event) => {
			console.log('Message from server ', event.data);
			const data = JSON.parse(event.data);
			let temp: Announcement = {
				deutsch: data['message_german'],
				tuerkisch: data['message_turkish'],
				starttime: data['start_date'],
				endtime: data['end_date'], // ? data['end_date'] : new Date(new Date(data['start_date']).setFullYear(new Date(data['start_date']).getFullYear() + 10)).toISOString(),
				visible: false
			};
			announcements = [...announcements, temp];
			console.log(announcements);
		});

		socket.addEventListener('disconnect', () => {
			console.log('Disconnected from WebSocket server');
		});

		// TODO: if mounted check backend database if there are any announcements
		// if there are any announcements, display them

		setInterval(() => {
			if (announcements != undefined && announcements.length > 0) {
				announcements.forEach((element) => {
					shouldAnnouncementBeDisplayed(element);
				});
			}
		}, 1000);
	});

	function shouldAnnouncementBeDisplayed(announcement: Announcement) {
		let currentTime = new Date();
		let startTime = new Date(announcement.starttime);
		let endTime: Date | undefined;

		if (announcement.endtime) {
			endTime = new Date(announcement.endtime);
		} else {
			endTime = undefined;
		}
		showAnnouncement =
			currentTime &&
			startTime &&
			currentTime >= startTime &&
			(endTime != undefined ? currentTime <= endTime : true);
		announcement.visible = showAnnouncement;
		announcements = [...announcements];
	}

	function showAnnouncements(): boolean {
		let visible = false;
		for (let i = 0; i < announcements.length; i++) {
			if (announcements[i].visible) {
				visible = true;
				break;
			}
		}
		return visible;
	}
</script>

{#if announcements != undefined && announcements.length > 0 && showAnnouncements()}
	<div class="wrapper">
		<div class="marquee">
			{#key announcements}
				{#each announcements as announcement}
					{#if announcement.visible}
						<p>
							{announcement.deutsch}
						</p>
						<p class="spacer">---</p>
						<p>
							{announcement.tuerkisch}
						</p>
						<p class="spacer2"></p>
					{/if}
				{/each}
			{/key}
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

	.spacer2 {
		padding-left: 100px;
		padding-right: 100px;
	}
</style>
