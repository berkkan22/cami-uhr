<script>
	import { signIn, signOut } from '@auth/sveltekit/client';
	import { page } from '$app/stores';
</script>

<div class="login-container">
	{#if $page.data.session}
		<h1>Welcome, {$page.data.session.user?.name}</h1>
		<button type="submit" on:click={() => signOut()}>Logout</button>
	{:else}
		<button type="submit" on:click={() => signIn('authentik')}>Login with Authentik</button>
	{/if}
</div>

<style>
	.login-container {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		height: 100vh;
		background-color: #f0f0f0;
	}

	button {
		padding: 0.5rem;
		font-size: 1rem;
		background-color: #007bff;
		color: white;
		border: none;
		border-radius: 4px;
		cursor: pointer;
	}

	button:hover {
		background-color: #0056b3;
	}
</style>
