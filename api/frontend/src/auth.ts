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
        authorization: { params: { access_type: "offline", prompt: "consent", scope: "openid profile email offline_access" } },
      }),
    ],

    secret: AUTH_SECRET,
    trustHost: true,
    session: {
      strategy: "jwt"
    },
    callbacks: {
      async jwt({ token, account, user }) {
        // console.log("jwt", token, account, user)
        if (account) {
          token.accessToken = account.access_token
          token.refreshToken = account.refresh_token
          token.expires_at = account.expires_at
        }
        return token
      },
      session({ session, token, user }) {
        session.access_token = token.accessToken
        session.expires_at = token.expires_at
        session.refresh_token = token.refreshToken
        return session
      },
    },
  }
  return authOptions
})

