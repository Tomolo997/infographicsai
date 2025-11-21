// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  devtools: { enabled: true },

  modules: [
    "@pinia/nuxt", 
    "@nuxt/icon", 
    "@nuxtjs/tailwindcss", 
    "@nuxt/image",
    "@nuxtjs/sitemap",
    "@nuxtjs/robots"
  ],
  css: ["@/assets/css/fonts.css", "@/assets/css/main.css"],

  // Built-in Nitro proxy configuration
  nitro: {
    devProxy: {
      "/api": {
        target: "http://127.0.0.1:8000/api",
        changeOrigin: true,
      },
      "/static": {
        // Simplified static proxy
        target: "http://127.0.0.1:8000",
        changeOrigin: true,
        ws: false,
      },
    },
  },

  // Sitemap Configuration
  sitemap: {
    hostname: 'https://ainfographic.com',
    exclude: [
      '/admin/**',
      '/dashboard/**',
    ],
    routes: () => import('./sitemap-routes.js').then(r => r.default)
  },

  // Robots Configuration
  robots: {
    UserAgent: '*',
    Allow: '/',
    Disallow: ['/admin', '/dashboard/settings'],
    Sitemap: 'https://ainfographic.com/sitemap.xml'
  },

  plugins: [
    { src: "~/plugins/google-analytics.js", mode: "client" },
    { src: "~/plugins/csrf.js", mode: "client" }
  ],
  app: {
    head: {
      script: [
        {
          src: "https://www.googletagmanager.com/gtag/js?id=G-KE2DL77CHV",
          async: true,
        },
      ],
      meta: [
        { charset: "utf-8" },
        { name: "viewport", content: "width=device-width, initial-scale=1" },
        {
          key: "description",
          name: "description",
          content:
            "Engage your audience across platforms with engaging infographics. Start creating for free today.",
        },
        {
          key: "og:title",
          property: "og:title",
          content: "AInfographic - Create professional infographics in minutes",
        },
        {
          key: "og:description",
          property: "og:description",
          content:
            "Engage your audience across platforms with engaging infographics. Start creating for free today.",
        },
        {
          key: "og:image",
          property: "og:image",
          content: "https://images.ainfographic.com/opengraph.png",
        },
        { key: "og:url", property: "og:url", content: "https://ainfographic.com" },
        { key: "og:type", property: "og:type", content: "website" },
        {
          name: "title",
          content: "AInfographic - Create professional infographs in minutes",
        },
      ],
    },
  },
  compatibilityDate: "2024-08-29",
})
