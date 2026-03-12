import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react(), tailwindcss()],
  build: {
    lib: {
      entry: "src/main.tsx",
      name: "HostieWidget",
      fileName: "widget",
      formats: ["iife"],
    },
  },
})
