import { redirect } from "@sveltejs/kit";
import type { PageServerLoad } from "./$types";
import { config } from "$lib/config";
import { getValidAccessToken } from "$lib/utils";

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

    // TODO: This call needs to go to /auth page.server.ts because if the user logges in in the /auth then the group should be check and removde
    const { validAccessToken } = await getValidAccessToken(session);
    const response = await fetch(`${config.apiUrl}/checkUserLogin`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'X-Token': `${validAccessToken}`
      }
    });

    if (!response.ok) {
      throw new Error('Network response was not ok');
    }

    const result = await response.json();
    console.log('Success:', result);

    redirect(302, '/');
  }

  return {
    session: session
  };
}

export const actions = {
  setCookies: async ({ request, cookies }) => {
    // Parse the incoming JSON body from the request
    const data = await request.formData(); // Expect form data

    const action = data.get('action');

    if (action === 'setCookies') {
      // Assuming the data contains your new cookies
      const newCookies = data.get('cookies'); // Example: { userId: '12345', sessionToken: 'abcdefg' }

      if (!newCookies) {
        console.log('Setting cookies:', newCookies);
        // Set the cookies
        cookies.set('session', newCookies ?? "", {
          path: '/',
          maxAge: 60 * 60 * 24, // 1 day
          httpOnly: false, // Allow access via JavaScript if needed
          sameSite: 'lax',
          secure: true, // Set to true if you're on HTTPS
        });
      }

      // Optionally redirect or return a response
      throw redirect(302, '/'); // Redirect to another page after setting the cookie
    }
  },
};