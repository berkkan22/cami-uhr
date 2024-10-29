import { redirect } from "@sveltejs/kit";
import type { PageServerLoad } from "./$types";

export const load: PageServerLoad = async (event) => {
  const session = await event.locals.auth();

  if (session !== null) {
    event.cookies.set('session', JSON.stringify(session), {
      httpOnly: false,
      secure: true,
      sameSite: 'lax',
      path: '/',
      maxAge: 60 * 60 * 24
    });

    redirect(302, '/');
  }

  return {
    session: session
  };
}