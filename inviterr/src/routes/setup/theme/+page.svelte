<script lang="ts">
	import { siteNameStore } from '$lib/stores';
	import { ArrowRight } from 'lucide-svelte';
	import { get } from 'svelte/store';

	function changeTheme(dataTheme: string) {
		document.body.setAttribute('data-theme', dataTheme);
	}

	const themesPreviews: { name: string; emoji: string }[] = [
		{ name: 'catppuccin', emoji: '🐈' },
		{ name: 'cerberus', emoji: '🐺' },
		{ name: 'concord', emoji: '🤖' },
		{ name: 'crimson', emoji: '🩸' },
		{ name: 'fennec', emoji: '🦊' },
		{ name: 'hamlindigo', emoji: '👔' },
		{ name: 'legacy', emoji: '💀' },
		{ name: 'mint', emoji: '🍃' },
		{ name: 'modern', emoji: '🌸' },
		{ name: 'mona', emoji: '🐙' },
		{ name: 'nosh', emoji: '🥙' },
		{ name: 'nouveau', emoji: '👑' },
		{ name: 'pine', emoji: '🌲' },
		{ name: 'reign', emoji: '📒' },
		{ name: 'rocket', emoji: '🚀' },
		{ name: 'rose', emoji: '🌷' },
		{ name: 'sahara', emoji: '🏜️' },
		{ name: 'seafoam', emoji: '🧜‍♀️' },
		{ name: 'terminus', emoji: '🌑' },
		{ name: 'vintage', emoji: '📺' },
		{ name: 'vox', emoji: '👾' },
		{ name: 'wintry', emoji: '🌨️' }
	];
</script>

<div class="pt-5">
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
			value={get(siteNameStore)}
		/>
	</label>

	<h1 class="h2 pt-5">Select a theme</h1>

	<div class="grid grid-cols-1 gap-2 md:grid-cols-2 2xl:grid-cols-3">
		{#each themesPreviews as theme}
			<button
				data-theme={theme.name}
				onclick={() => changeTheme(theme.name)}
				class="bg-surface-50-950 preset-outlined-surface-100-900 hover:preset-outlined-surface-800-200 grid w-full grid-cols-[auto_1fr_auto] items-center gap-4 rounded-md p-4 !ring-[1px]"
			>
				<span>{theme.emoji}</span>
				<h3 class="h6 !text-surface-950-50 text-left">{theme.name}</h3>
				<div class="flex items-center justify-center -space-x-1">
					<div
						class="bg-primary-500 aspect-square w-5 rounded-full border-[1px] border-black/10"
					></div>
					<div
						class="bg-secondary-500 aspect-square w-5 rounded-full border-[1px] border-black/10"
					></div>
					<div
						class="bg-tertiary-500 aspect-square w-5 rounded-full border-[1px] border-black/10"
					></div>
					<div
						class="bg-success-500 aspect-square w-5 rounded-full border-[1px] border-black/10"
					></div>
					<div
						class="bg-warning-500 aspect-square w-5 rounded-full border-[1px] border-black/10"
					></div>
					<div
						class="bg-error-500 aspect-square w-5 rounded-full border-[1px] border-black/10"
					></div>
					<div
						class="bg-surface-500 aspect-square w-5 rounded-full border-[1px] border-black/10"
					></div>
				</div>
			</button>
		{/each}
	</div>

	<div class="flex w-full justify-end">
		<a href="/setup/instances" class="btn preset-filled mt-5">
			<span>
				<ArrowRight />
			</span>
			<span>Setup Instances</span>
		</a>
	</div>
</div>
