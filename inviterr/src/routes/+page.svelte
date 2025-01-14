<script lang="ts">
	import { page } from '$app/state';
	import { Sparkles } from 'lucide-svelte';
</script>

{#if page.url.searchParams.get('error') === 'setupStarted'}
	<div
		role="alert"
		class="mt-5 rounded border-s-4 border-red-500 bg-red-50 p-4 dark:border-red-600 dark:bg-red-900"
	>
		<div class="flex items-center gap-2 text-red-800 dark:text-red-100">
			<svg
				xmlns="http://www.w3.org/2000/svg"
				viewBox="0 0 24 24"
				fill="currentColor"
				class="size-5"
			>
				<path
					fill-rule="evenodd"
					d="M9.401 3.003c1.155-2 4.043-2 5.197 0l7.355 12.748c1.154 2-.29 4.5-2.599 4.5H4.645c-2.309 0-3.752-2.5-2.598-4.5L9.4 3.003zM12 8.25a.75.75 0 01.75.75v3.75a.75.75 0 01-1.5 0V9a.75.75 0 01.75-.75zm0 8.25a.75.75 0 100-1.5.75.75 0 000 1.5z"
					clip-rule="evenodd"
				/>
			</svg>

			<strong class="block font-medium">Setup progress already started</strong>
		</div>

		<p class="mt-2 text-sm text-red-700 dark:text-red-200">
			A different browser has already started the setup process for this instance of Inviterr.
			Simply delete the MongoDB volume or delete the "setup" collection to fix this.
		</p>
	</div>
{/if}

<div class="flex h-screen items-center justify-center">
	<div class="flex flex-col items-center space-y-5 text-center">
		<h2 class="h2 leading-tight">Welcome to Inviterr</h2>
		<p class="leading-relaxed">The modern invitation system for Jellyfin, Plex & Emby</p>
		<a href="/setup/theme" class="btn preset-filled">
			<span>
				<Sparkles />
			</span>
			<span>Get started</span>
		</a>
	</div>
</div>
