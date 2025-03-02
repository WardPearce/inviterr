<script lang="ts">
	import { siteSetupCompletedStore } from '$lib/stores';
	import { ShieldIcon, Sparkles, TicketCheck } from 'lucide-svelte';
</script>

<div class="flex h-screen items-center justify-center">
	<div class="flex flex-col items-center space-y-5 text-center">
		<h2 class="h2 leading-tight">Welcome to Inviterr</h2>
		<p class="leading-relaxed">The modern invitation system for Jellyfin, Plex & Emby</p>

		{#if $siteSetupCompletedStore}
			<div>
				<a href="/redeem" class="btn preset-filled">
					<span>
						<TicketCheck />
					</span>
					<span>Redeem a code</span>
				</a>

				<a href="/admin" class="btn preset-outlined">
					<span>
						<ShieldIcon />
					</span>
					<span>Admin Panel</span>
				</a>
			</div>
		{:else}
			<a href="/setup" class="btn preset-filled">
				<span>
					<Sparkles />
				</span>
				<span>Get started</span>
			</a>
		{/if}
	</div>
</div>
