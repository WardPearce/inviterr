// See https://svelte.dev/docs/kit/types#app.d.ts

import type { Db } from "mongodb";

// for information about these interfaces
declare global {
	namespace App {
		// interface Error {}
		// interface Locals {}
		// interface PageData {}
		// interface PageState {}
		// interface Platform {}
		interface Locals {
			mongo: Db;
		}
	}
}

export { };

