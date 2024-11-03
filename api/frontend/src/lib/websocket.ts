import { config } from "./config";
import { getValidAccessToken } from "./utils";

export const connectToWebsocket = (url: string) => {
  const ws = new WebSocket(url);

  ws.onopen = () => {
    console.log('connected');
  };

  ws.onmessage = (event) => {
    console.log(event.data);
  };

  ws.onclose = () => {
    console.log('disconnected');
  };

  return ws;
}

export const checkWebsocketConnection = async (ws: WebSocket, session) => {
  if (ws.readyState === ws.OPEN) {
    console.log('connected');
    return ws;
  } else {
    console.log('disconnected');
    ws.close();
    const { validAccessToken } = await getValidAccessToken(session);

    return connectToWebsocket(`${config.wsUrl}/ws?token=${validAccessToken}`);
  }

}

export const disconnectFromWebsocket = (ws: WebSocket) => {
  ws.close();
}