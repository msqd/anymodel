import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import { TanStackRouterVite as router } from "@tanstack/router-plugin/vite";

// https://vite.dev/config/
export default defineConfig({
  plugins: [router(), react()],
  resolve: {
    alias: {
      src: "/src",
    },
  },
});
