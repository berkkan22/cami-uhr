// src/routes/+layout.server.ts
import { redirect } from '@sveltejs/kit';
import type { LayoutServerLoad } from './$types';


export const load: LayoutServerLoad = async (event) => {
  const session = event.cookies.get('session');

  // console.log('session', session);

  if (session !== undefined) {
    // console.log('session', session);
    return {
      session: JSON.parse(session)
    };
  }

  if (event.url.pathname !== '/auth' && event.url.pathname !== '/error') {
    redirect(302, '/auth');
  }
};
