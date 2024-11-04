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
		// const duration = calculateLength() * 0.256;
		const minDuration = 20;
		const calculatedDuration = calculateLength() * 0.256;
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
		// let chars = 0;
		// for (let i = 0; i < announcements.length; i++) {
		// 	chars += announcements[i].deutsch.length + announcements[i].tuerkisch.length;
		// }
		console.log(chars);
		return chars;
	}
</script>

<!-- {#if announcements != undefined && announcements.length > 0 && showAnnouncements()} -->
<!-- <div class="wrapper1"> -->
<!-- <div class="wrapper"> -->
<!-- {#each announcements as announcement} -->
<!-- <div class="loop-text"> -->
<!-- This -->
<!-- {#if announcement.visible} -->
<!-- <p> -->
<!-- {announcement.deutsch} -->
<!-- </p> -->
<!-- <p class="spacer">---</p> -->
<!-- <p> -->
<!-- {announcement.tuerkisch} -->
<!-- </p> -->
<!-- <p class="spacer2"></p> -->
<!-- {/if} -->
<!-- </div> -->
<!-- {/each} -->
<!-- </div> -->
<!-- </div> -->
<!-- {/if} -->

<!-- <div class="mymarquee-container">
	<span class="mymarquee"
		>Das ist ein Text Das ist ein Text Das ist ein Text Das ist ein Text Das ist ein Text Das ist
		ein Text Das ist ein Text Das ist ein Text</span
	>
</div> -->

<p id="PassengerNews_Scrollbar" class="microsoft mymarquee">
	<!-- <span class="line__wrap">
		<span class="line">|*NewsData*|</span>
	</span> -->

	<span class="line__wrap" style="top: 30px;">
		<span class="line">
			Baryma Mollit ex deserunt minim mollit Lorem non. Baryma Mollit ex deserunt minim mollit Lorem
			non.Baryma Mollit ex deserunt minim mollit Lorem non.Baryma Mollit ex deserunt minim mollit
			Lorem non.
		</span>
	</span>
</p>

<style>
	.mymarquee {
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
	.mymarquee .line__wrap {
		display: block;
		position: absolute;
		width: auto;
		left: 0;
		animation: marquee__wrap linear infinite;

		font-size: 5rem;
	}
	.mymarquee .line {
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
	/* .wrapper1 {
		position: absolute;
		bottom: 0;
		display: flex;
		white-space: nowrap;
		width: 100%;
		height: auto;
		overflow: hidden;
		font-family: sans-serif;
		background-color: #f1f1f1;
	} */

	/* .wrapper {
		position: absolute;
		bottom: 0;
		display: flex;
		white-space: nowrap;
		width: max-content; */
	/* height: clamp(3em, 10vw, 6em); */
	/* overflow: hidden;
		font-family: sans-serif;
		background-color: #f1f1f1;
		animation: loopText 20s infinite linear; */
	/* padding-left: 100%; */
	/* } */

	/* .loop-text {
		font-size: 3rem;
		font-size: clamp(2.5rem, 8vw, 5.5rem);
		text-transform: uppercase;
		font-weight: 700;
		padding: 20px;
		padding: 0 0.25em;
		display: flex;
	} */

	/* @keyframes loopText {
		from {
			transform: translateX(0);
		}
		to {
			transform: translateX(-100%);
		}
	}

	.spacer {
		padding-left: 20px;
		padding-right: 20px;
	}

	.spacer2 {
		padding-left: 100px;
		padding-right: 100px;
	} */
</style>
