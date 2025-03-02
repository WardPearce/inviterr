import { writable } from "svelte/store";

export const siteNameStore = writable('Inviterr');
export const siteThemeStore = writable('wintry');

// Set default as true, as more often then not that will be the response from the API
export const siteSetupCompletedStore = writable(true);
