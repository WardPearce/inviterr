<script lang="ts">
	import { ProgressRing } from '@skeletonlabs/skeleton-svelte';

	let { loadingText = undefined }: { loadingText: string | undefined } = $props();
</script>

<div class="flex min-h-screen flex-col items-center justify-center">
	<ProgressRing
		value={null}
		size="size-40"
		meterStroke="stroke-primary-600-400"
		trackStroke="stroke-primary-50-950"
	/>

	{#if loadingText}
		<h1 class="h5 mt-10">{loadingText}</h1>
	{/if}
</div>
