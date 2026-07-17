"use client";

import { Toaster } from "sonner";

/**
 * Client-side providers for the /tints segment.
 * Rendered from layout.jsx so every tints route gets the toaster.
 */
export default function Providers({ children }) {
  return (
    <>
      {children}
      <Toaster theme="dark" position="top-right" richColors />
    </>
  );
}
