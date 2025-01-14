import { env } from '$env/dynamic/private';
import { redirect } from '@sveltejs/kit';
import { sign, unsign } from 'cookie-signature';

export async function load({ cookies, locals }) {
  // Only allowed the 1st browser to visit setup page to continue.
  const setupCookie = await locals.mongo.collection('setup').findOne();
  if (!setupCookie) {
    const token = crypto.randomUUID();
    cookies.set('setupLock', sign(token, env.COOKIE_SECRET), {
      httpOnly: true,
      secure: process.env.NODE_ENV === 'production',
      path: '/',
      maxAge: 60 * 60 * 24 * 120,
    });
    await locals.mongo.collection('setup').insertOne({ token: token });
  } else {
    const givenSetupCookie = cookies.get('setupLock');
    if (!givenSetupCookie) {
      throw redirect(302, '/?error=setupStarted');
    }

    const givenToken = unsign(givenSetupCookie, env.COOKIE_SECRET);
    if (!givenToken || givenToken !== setupCookie.token) {
      throw redirect(302, '/?error=setupStarted');
    }
  }
}