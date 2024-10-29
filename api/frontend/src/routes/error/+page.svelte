<script>
	export let status = 404;
	export let message = 'Page not found';

	function goHome() {
		window.location.href = '/';
	}
</script>

<div class="error-container">
	<div class="error-code">{status}</div>
	<div class="error-message">{message}</div>
	<button class="home-button" on:click={goHome}>Go to Home</button>
</div>

<style>
	.error-container {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		height: 100vh;
		text-align: center;
		background-color: #f8f9fa;
		color: #343a40;
	}

	.error-code {
		font-size: 6rem;
		font-weight: bold;
	}

	.error-message {
		font-size: 1.5rem;
		margin-bottom: 1rem;
	}

	.home-button {
		padding: 0.5rem 1rem;
		font-size: 1rem;
		color: #fff;
		background-color: #007bff;
		border: none;
		border-radius: 0.25rem;
		cursor: pointer;
	}

	.home-button:hover {
		background-color: #0056b3;
	}
</style>
