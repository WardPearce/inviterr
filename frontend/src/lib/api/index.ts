import createClient from 'openapi-fetch';
import type { paths } from './v1';

export const apiClient = createClient<paths>({ baseUrl: import.meta.env.VITE_DEFAULT_BACKEND });