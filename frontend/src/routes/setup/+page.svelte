<script lang="ts">
	import { goto } from '$app/navigation';
	import { apiClient } from '$lib/api';
	import SelectTheme from '$lib/SelectTheme.svelte';
	import SetTitle from '$lib/SetTitle.svelte';
	import { ArrowRight } from 'lucide-svelte';

	let email = $state('');
	let password = $state('');

	let title = $state('');
	let theme = $state('');

	async function finishSetup(event: Event) {
		event.preventDefault();

		const resp = await apiClient.POST('/api/controllers/v1/setup', {
			body: {
				site_title: title,
				// @ts-ignore
				theme: theme,
				email: email,
				password: password
			}
		});

		if (!resp.error) {
			goto('/admin', { replaceState: true });
		}
	}
</script>

<div class="pt-5">
	<form onsubmit={finishSetup}>
		<SetTitle bind:value={title} />

		<SelectTheme bind:value={theme} />

		<h1 class="h2 pt-5">Admin</h1>
		<p>Create the root admin account, this account has complete control over Inviterr.</p>
		<label class="label pt-5">
			<span class="label-text">
				<h1 class="h5">Email</h1>
			</span>
			<input bind:value={email} class="input" required name="username" type="email" />
		</label>
		<label class="label pt-3">
			<span class="label-text">
				<h1 class="h5">Password</h1>
			</span>
			<input bind:value={password} class="input" required name="password" type="password" />
		</label>

		<div class="flex w-full justify-end">
			<button type="submit" class="btn preset-filled mt-5">
				<span>
					<ArrowRight />
				</span>
				<span>Complete setup</span>
			</button>
		</div>
	</form>
</div>
