<script lang="ts">
	import { siteNameStore, siteThemeStore } from '$lib/stores';
	import { onMount } from 'svelte';
	import '../app.css';

	import { apiClient } from '$lib/api';
	import { AppBar } from '@skeletonlabs/skeleton-svelte';
	import { Github } from 'lucide-svelte';

	let { children } = $props();

	onMount(() => {
		apiClient.GET('/api/controllers/v1/setup').then((resp) => {
			if (resp.data) {
				siteNameStore.set(resp.data.site_title);
				siteThemeStore.set(resp.data.theme);
			}
		});

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
