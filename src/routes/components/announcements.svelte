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
		fetch(`${config.apiUrl}/announcements`, {
			method: 'POST',
			body: JSON.stringify({ mosque: config.camiNameIdentifier })
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

		const socket = new WebSocket(`${config.wsUrl}/ws-listen?mosque=${config.camiNameIdentifier}`);

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
			calculateDuration();
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

		setTimeout(() => {
			calculateDuration();
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

	function calculateDuration(): void {
		const minDuration = 20;
		const calculatedDuration = calculateLength() * 0.156;
		const duration = Math.max(minDuration, calculatedDuration);
		console.log(duration);

		const element1 = document.querySelector('.line__wrap');
		const element2 = document.querySelector('.line');
		if (element1) {
			(element1 as HTMLElement).style.animationDuration = `${duration}s`;
		}
		if (element2) {
			(element2 as HTMLElement).style.animationDuration = `${duration}s`;
		}
	}

	function calculateLength(): number {
		const lineElement = document.querySelector('.line');
		let chars = 0;
		if (lineElement) {
			const textContent = lineElement.textContent || '';
			chars = textContent.length;
		}
		console.log(chars);
		return chars;
	}
</script>

{#if announcements != undefined && announcements.length > 0 && showAnnouncements()}
	<p class="marquee">
		<span class="line__wrap" style="top: 30px;">
			<span class="line">
				{#key announcements}
					{#each announcements as announcement}
						{#if announcement.visible}
							{announcement.deutsch}
							&nbsp; • &nbsp;
							{announcement.tuerkisch}
							&nbsp; • &nbsp;
						{/if}
					{/each}
				{/key}
			</span>
		</span>
	</p>
{/if}

<style>
	.marquee {
		margin: 0 auto;
		white-space: nowrap;
		overflow: hidden;
		position: absolute;
		color: #000000;
		background-color: #ffffff;
		font-family: Arial Rounded MT Bold;

		height: 150px;
		width: 100%;
		left: 0;
		bottom: 0;
		font-size: 5rem;
	}
	.marquee .line__wrap {
		display: block;
		position: absolute;
		width: auto;
		left: 0;
		animation: marquee__wrap linear infinite;

		font-size: 5rem;
	}
	.marquee .line {
		position: relative;
		margin-left: -100%;
		animation: marquee linear infinite;
	}
	@keyframes marquee__wrap {
		from {
			margin-left: 100%;
		}
		to {
			margin-left: 0%;
		}
	}
	@keyframes marquee {
		from {
			left: 100%;
		}
		to {
			left: 0%;
		}
	}
</style>
