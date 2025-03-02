<script lang="ts">
	import { siteNameStore, siteThemeStore } from '$lib/stores';
	import { onMount } from 'svelte';
	import '../app.css';

	import { AppBar } from '@skeletonlabs/skeleton-svelte';
	import { Github } from 'lucide-svelte';

	let { children } = $props();

	onMount(() => {
		// if (data.customization) {
		// 	document.body.setAttribute('data-theme', data.customization.themeName);

		// 	siteThemeStore.set(data.customization.themeName);
		// 	siteNameStore.set(data.customization.siteName);
		// } else {
		// 	document.body.setAttribute('data-theme', 'wintry');
		// }

		siteThemeStore.subscribe((dataTheme) => document.body.setAttribute('data-theme', dataTheme));
	});
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
