import { API_URL } from "@/lib/config";

export async function fetchJson<T>(
  path: string,
  signal: AbortSignal,
): Promise<T> {
  const response = await fetch(`${API_URL}${path}`, { signal });
  if (!response.ok) {
    throw new Error(`The API answered with status ${response.status}`);
  }
  return response.json() as Promise<T>;
}
