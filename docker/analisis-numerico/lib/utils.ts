import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

// codigo refactorizado por mí

export const API_BASE_URL = "http://sd-4140038-h00002.ferozo.net/api";

export async function fetchTexto(url: string): Promise<string> {
  try {
    const res = await fetch(url);
    if (!res.ok) throw new Error(`Error ${res.status}: ${await res.text()}`);
    return await res.text();
  } catch (error) {
    console.warn(`⚠️ fetchTexto(${url}) →`, error);
    return "";
  }
}

export async function fetchJSON<T = unknown>(url: string): Promise<T | null> {
  try {
    const res = await fetch(url, {
      method: "GET",
      headers: { "Content-Type": "application/json" },
    });
    if (!res.ok) throw new Error(`Error ${res.status}: ${await res.text()}`);
    return await res.json();
  } catch (error) {
    console.warn(`⚠️ fetchJSON(${url}) →`, error);
    return null;
  }
}

export async function fetchImagen(url: string): Promise<string | null> {
  try {
    const res = await fetch(url, { headers: { Accept: "image/png" } });
    if (!res.ok) throw new Error(`Error ${res.status}: ${await res.text()}`);
    const blob = await res.blob();
    return URL.createObjectURL(blob);
  } catch (error) {
    console.warn(`⚠️ fetchImagen(${url}) →`, error);
    return null;
  }
}
