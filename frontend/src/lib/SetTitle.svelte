<script lang="ts">
	import { siteNameStore } from '$lib/stores';
	import { get } from 'svelte/store';
</script>

<label class="label">
	<span class="label-text">
		<h1 class="h2">Site title</h1>
	</span>
	<input
		oninput={(e: Event) => {
			siteNameStore.set((e.target as HTMLInputElement).value);
		}}
		class="input"
		type="text"
		name="siteTitle"
		required
		value={get(siteNameStore)}
	/>
</label>
