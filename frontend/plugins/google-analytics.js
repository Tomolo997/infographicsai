// plugins/google-analytics.js
export default defineNuxtPlugin((nuxtApp) => {
  if (process.client) {
    nuxtApp.hook("app:mounted", () => {
      window.dataLayer = window.dataLayer || []
      function gtag() {
        dataLayer.push(arguments)
      }
      gtag("js", new Date())
      gtag("config", "G-KE2DL77CHV")
    })
  }
})
