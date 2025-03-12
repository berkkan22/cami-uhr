<script lang="ts">
	import { onMount } from 'svelte';
	import { config } from '$lib/config/config';
	import { goto } from '$app/navigation';

	interface Announcement {
		deutsch: string;
		tuerkisch: string;
		starttime: string;
		endtime: string;
		visible: boolean;
	}
	let announcements: Announcement[] = [];
	let showAnnouncement = false;
	let slidingTime = 10;

	onMount(async () => {
		const temp = await getAllAnnouncements();
		announcements = temp;

		const socket = new WebSocket(`${config.wsUrl}/ws-listen?mosque=${config.camiNameIdentifier}`);

		// Connection opened
		socket.addEventListener('open', function (event) {
			console.log("It's open");
		});

		socket.addEventListener('message', async (event) => {
			console.log('Message from server ', event.data);

			const temp = await getAllAnnouncements();
			announcements = temp;
			slidingTime = await getSlidingTime();
			console.log('Sliding time: ', slidingTime);

			setTimeout(() => {
				calculateDuration();
			}, 1000);
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

	async function getAllAnnouncements() {
		let tempArray: Announcement[] = [];
		const response = await fetch(`${config.apiUrl}/announcements`, {
			method: 'POST',
			body: JSON.stringify({ mosque: config.camiNameIdentifier })
		});

		const data = await response.json();

		if (data) {
			for (let i = 0; i < data['announcements'].length; i++) {
				let temp: Announcement = {
					deutsch: data['announcements'][i][1],
					tuerkisch: data['announcements'][i][2],
					starttime: data['announcements'][i][4],
					endtime: data['announcements'][i][5],
					visible: false
				};
				tempArray.push(temp);
				// tempArray.push(temp);
			}
			console.log(tempArray);
		}

		return tempArray;
	}

	async function getSlidingTime() {
		const response = await fetch(`${config.apiUrl}/slidingTime`, {
			method: 'POST',
			body: JSON.stringify({ mosque: config.camiNameIdentifier })
		});

		const data = await response.json();

		if (data) {
			return data['slidingTime'];
		}
	}

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
		const calculatedDuration = calculateLength() * (slidingTime / 100);
		const duration = Math.max(minDuration, calculatedDuration);

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
		announcements.forEach((element) => {
			shouldAnnouncementBeDisplayed(element);
		});

		let chars = 0;
		announcements.forEach((announcement) => {
			if (announcement.visible) {
				chars += announcement.deutsch.length + announcement.tuerkisch.length + 6; // 6 for the separators
			}
		});
		return chars;
	}
</script>

<!-- {#key announcements} -->
{#if announcements != undefined && announcements.length > 0 && showAnnouncements()}
	<p class="marquee">
		<span class="line__wrap" style="top: 30px;">
			<span class="line">
				{#each announcements as announcement}
					{#if announcement.visible}
						{announcement.deutsch}
						&nbsp; • &nbsp;
						{announcement.tuerkisch}
						&nbsp; • &nbsp;
					{/if}
				{/each}
			</span>
		</span>
	</p>
{/if}

<!-- {/key} -->

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
