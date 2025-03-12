import fs from "fs";
import { json } from "@sveltejs/kit";

export async function POST({ request }) {
  const { message } = await request.json();
  const logEntry = `[${new Date().toISOString()}] ${message}\n`;

  try {
    fs.appendFileSync("./error_logs.txt", logEntry, "utf8");
    return json({ success: true });
  } catch (error) {
    console.error("Error writing to file:", error);
    return json({ success: false, error: error }, { status: 500 });
  }
}
