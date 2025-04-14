import { fileURLToPath, URL } from 'node:url'
import { visualizer } from "rollup-plugin-visualizer";

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import autoprefixer from 'autoprefixer'
import tailwind from 'tailwindcss'
import vueDevTools from 'vite-plugin-vue-devtools'

// https://vite.dev/config/
export default defineConfig({
  server: {
    host: true, // listen on all interfaces (0.0.0.0)
    port: 5173,
    hmr: {
      protocol: 'ws',
      host: 'note.henryfield.net', // your domain
    },
  },
  plugins: [
    vue(),
    vueDevTools(),
    visualizer(),
  ],
  base: './', // added
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  },
  css: {
    postcss: {
      plugins: [tailwind(), autoprefixer()],
    },
  },
  preview: {
    allowedHosts: ['note.henryfield.net'],
  },
})
