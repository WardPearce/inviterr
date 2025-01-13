<script lang="ts">
	import { siteNameStore } from '$lib/stores';
	import '../app.css';
	let { children } = $props();

	import { AppBar } from '@skeletonlabs/skeleton-svelte';
	import { Github } from 'lucide-svelte';
</script>

<AppBar>
	{#snippet lead()}
		<h5 class="h5">{$siteNameStore}</h5>
	{/snippet}
	{#snippet trail()}
		<a href="https://github.com/WardPearce/inviterr" target="_blank" rel="noopener noreferrer"
			><Github size={30} /></a
		>
	{/snippet}
</AppBar>

<div class="md:container md:mx-auto">
	{@render children()}
</div>
