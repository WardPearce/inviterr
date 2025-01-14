import { serializeMongo } from '$lib/serialize';

export async function load({ locals }) {
  const customization = await locals.mongo.collection('customization').findOne();
  return { customization: serializeMongo(customization) };
}