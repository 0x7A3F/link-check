// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: true },
  modules: [
    "@nuxt/ui",
    "nuxt-resend",
    "@nuxtjs/turnstile"
  ],
  css: ["~/assets/css/main.css"],
  runtimeConfig: {
    resend: {
      apiKey: "",
    },
    turnstile: {
      secretKey: "",
    },
    reportToEmail: "",
    emailFrom: "",
    public: {
      apiBase: "http://localhost:8000",
      turnstile: {
        siteKey: "",
      },
    }
  }
})
