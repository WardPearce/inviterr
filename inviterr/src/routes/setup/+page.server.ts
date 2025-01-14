import { validateSetup } from '$lib/forms/setup.js';
import { redirect } from '@sveltejs/kit';

export const actions = {
  default: async ({ request, locals }) => {
    const data = await request.formData();
    validateSetup(data);

    await locals.mongo.collection('customization').insertOne({
      themeName: data.get('themeName'),
      siteName: data.get('siteTitle')
    });

    redirect(301, '/dashboard');
  }
};