import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// let url = "mipt.site";
let url = "51.250.110.235";
let backend = "https://" + url + ":8000/";
let user = "https://" + url + ":8088/";

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue(),
  ],
  server: {
    watch: {
        usePolling: true,
    },
    port: 8080,
    strictPort: true,
    host: '0.0.0.0', // или 'localhost' или '127.0.0.1'
    proxy: {
      "/backend-api": {
        target: backend,
        changeOrigin: true,
        secure: false,
        rewrite: (p) => p.replace(/^\/backend-api/, ""),
      },
      "/user-api": {
        target: user,
        changeOrigin: true,
        secure: false,
        rewrite: (p) => p.replace(/^\/user-api/, ""),
      },
    },
    cors: false,
  },
  preview: {
    proxy: {
      "/backend-api": {
        target: backend,
        changeOrigin: true,
        secure: false,
        rewrite: (p) => p.replace(/^\/backend-api/, ""),
      },
      "/user-api": {
        target: user,
        changeOrigin: true,
        secure: false,
        rewrite: (p) => p.replace(/^\/user-api/, ""),
      },
    },
    cors: false,
  },
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  }
})
