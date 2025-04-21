<script lang="ts">
	import { siteThemeStore } from '$lib/stores';

	let { value = $bindable() }: { value: string } = $props();

	value = $siteThemeStore;

	function changeTheme(dataTheme: string) {
		siteThemeStore.set(dataTheme);
		value = dataTheme;
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

<h1 class="h2 pt-5">Select a theme</h1>

<input type="text" required name="themeName" hidden value={$siteThemeStore} />

<div class="grid grid-cols-1 gap-2 md:grid-cols-2 2xl:grid-cols-3">
	{#each themesPreviews as theme}
		<button
			data-theme={theme.name}
			onclick={() => changeTheme(theme.name)}
			class="bg-surface-50-950 hover:preset-outlined-surface-800-200 grid w-full grid-cols-[auto_1fr_auto] items-center gap-4 rounded-md p-4"
			class:preset-outlined-primary-500={theme.name === $siteThemeStore}
			class:preset-outlined-surface-100-900={theme.name !== $siteThemeStore}
			type="button"
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
				<div class="bg-error-500 aspect-square w-5 rounded-full border-[1px] border-black/10"></div>
				<div
					class="bg-surface-500 aspect-square w-5 rounded-full border-[1px] border-black/10"
				></div>
			</div>
		</button>
	{/each}
</div>
