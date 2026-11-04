import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// En dev, /api est redirigé vers FastAPI local, comme le fait nginx en prod
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      "/api": {
        target: "http://localhost:8000",
        rewrite: (path) => path.replace(/^\/api/, ""),
      },
    },
  },
});
