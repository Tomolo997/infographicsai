export default defineNuxtConfig({
  devtools: { enabled: true },
  
  modules: [
    '@nuxtjs/tailwindcss',
    '@pinia/nuxt',
    '@vueuse/nuxt'
  ],
  
  css: ['~/assets/css/main.css'],
  ssr: true,
  routeRules: {
    '/dashboard/create': { ssr: false },
    '/dashboard/create/**': { ssr: false }
  },
  runtimeConfig: {
    public: {
      apiBase: process.env.API_BASE_URL || 'http://localhost:8000/api/v1',
      stripePublishableKey: process.env.STRIPE_PUBLISHABLE_KEY || '',
      googleClientId: process.env.GOOGLE_CLIENT_ID || '',
    }
  },

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
  
  
  tailwindcss: {
    cssPath: '~/assets/css/main.css',
    configPath: 'tailwind.config.js'
  },
  
  app: {
    head: {
      title: 'ainfographic',
      meta: [
        { charset: 'utf-8' },
        { name: 'viewport', content: 'width=device-width, initial-scale=1' },
        { name: 'description', content: 'SaaS MVP - Your next big idea starts here' },
        // Open Graph / Facebook
        { property: 'og:type', content: 'website' },
        { property: 'og:title', content: 'Ainfographic' },
        { property: 'og:description', content: 'AI-powered infographic generator' },
        { property: 'og:image', content: 'https://yourdomain.com/og-image.jpg' }, // Update with your actual image URL
        { property: 'og:url', content: 'https://yourdomain.com' }, // Update with your actual domain
        // Twitter
        { name: 'twitter:card', content: 'summary_large_image' },
        { name: 'twitter:title', content: 'ainfographic' },
        { name: 'twitter:description', content: 'SaaS MVP - Your next big idea starts here' },
        { name: 'twitter:image', content: 'https://yourdomain.com/og-image.jpg' } // Update with your actual image URL
      ],
      link: [
        { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' }
      ],
      script: [
        {
          src: 'https://scripts.simpleanalyticscdn.com/latest.js',
          async: true
        }
      ]
    }
  },
  
  compatibilityDate: '2025-11-14',
})