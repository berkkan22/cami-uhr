import { jwtDecode } from 'jwt-decode';
import { config } from '$lib/config';

interface DecodedToken {
  exp: number;
}

export async function getRefreshToken(refreshToken: string): Promise<{ access_token: string; refresh_token?: string, expires_in: number }> {
  try {
    console.log('Refreshing token...');
    const response = await fetch(`${config.apiUrl}/refresh-token`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ refresh_token: refreshToken }),
    });

    if (!response.ok) {
      throw new Error(`Failed to refresh token: ${response.statusText}`);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error refreshing token:', error);
    throw error;
  }
}

export function isTokenExpired(token: string): boolean {
  const decoded: DecodedToken = jwtDecode(token);
  const currentTime = Math.floor(Date.now() / 1000);
  return decoded.exp < currentTime;
}

export function updateTokens(cookies: any, newToken: { access_token: string; refresh_token?: string, expires_in: number }): void {
  console.log('Updating tokens...');
  console.log('Old tokens:', cookies.access_token, cookies.refresh_token, cookies.expires_at);
  console.log('New tokens:', newToken.access_token, newToken.refresh_token, newToken.expires_in);
  cookies.access_token = newToken.access_token;
  if (newToken.refresh_token) {
    console.log('Updating refresh token...');
    cookies.refresh_token = newToken.refresh_token;
  }
  console.log('Updating expires_at...');
  cookies.expires_at = Math.floor(Date.now() / 1000) + newToken.expires_in;


  return cookies;
}

export async function getValidAccessToken(cookies: any): Promise<{ validAccessToken: string, }> {
  if (isTokenExpired(cookies.access_token)) {
    console.log('Access token expired, refreshing...');
    const newTokens = await getRefreshToken(cookies.refresh_token);
    const newCookies = updateTokens(cookies, newTokens);
    console.log('New cookies:', newCookies);
    document.cookie = `session=${JSON.stringify(newCookies)}; path=/; max-age=${60 * 60 * 24}; samesite=lax; secure=true; httponly=false;`;

    return { validAccessToken: newTokens.access_token };
  }
  return { validAccessToken: cookies.access_token };
}
