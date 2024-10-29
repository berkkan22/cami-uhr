import { SvelteKitAuth } from "@auth/sveltekit"
import Authentik from "@auth/sveltekit/providers/authentik"
import { CLIENT_ID, CLIENT_SECRET, AUTH_SECRET, AUTHENTIK_ISSUER } from "$env/static/private"


export const { handle, signIn, signOut } = SvelteKitAuth(async (event) => {
  const authOptions = {
    providers: [
      Authentik({
        clientId: CLIENT_ID,
        clientSecret: CLIENT_SECRET,
        issuer: AUTHENTIK_ISSUER,
      }),
    ],
    secret: AUTH_SECRET,
    trustHost: true,
    session: {
      strategy: "jwt"
    },
    callbacks: {
      jwt({ token, account }) {
        if (account) {
          token.accessToken = account.access_token
        }
        return token
      },
      session({ session, token, user }) {
        session.access_token = token.accessToken
        return session
      },
    },
  }
  return authOptions
})

