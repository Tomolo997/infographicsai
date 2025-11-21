// stores/fontStore.js
import { defineStore } from "pinia"

export const useFontStore = defineStore("fontStore", {
  state: () => ({
    fonts: {},
    isLoading: false,
    error: null,
    availableFonts: [
      {
        name: "Roboto",
        weights: ["regular"],
        type: "woff2",
      },
      {
        name: "OpenSans",
        weights: ["regular", "bold"],
        type: "woff2",
      },
      {
        name: "Academy",
        weights: ["Engraved"],
        type: "ttf",
      },
      {
        name: "Times New Roman",
        weights: ["regular", "bold"],
        type: "ttf",
      },
      {
        name: "GentySans",
        weights: ["regular"],
        type: "ttf",
      },
      {
        name: "SansSerif",
        weights: ["regular"],
        type: "ttf",
      },
      {
        name: "Inter",
        weights: ["regular"],
        type: "ttf",
      },
      {
        name: "Tahoma",
        weights: ["regular"],
        type: "ttf",
      },
      {
        name: "Verdana",
        weights: ["regular"],
        type: "ttf",
      },
      {
        name: "Helvetica",
        weights: ["regular"],
        type: "ttc",
      },
      {
        name: "Andale Mono",
        weights: ["regular"],
        type: "ttf",
      },
      {
        name: "Chalkduster",
        weights: ["regular"],
        type: "ttf",
      },
      {
        name: "Geneva",
        weights: ["regular"],
        type: "ttf",
      },
      {
        name: "Kokonor",
        weights: ["regular"],
        type: "ttf",
      },
      {
        name: "Mishafi Gold",
        weights: ["regular"],
        type: "ttf",
      },
      {
        name: "Peace Sans",
        weights: ["regular"],
        type: "otf",
      },
      {
        name: "Cy Grotesk Wide",
        weights: ["regular"],
        type: "ttf",
      },
      {
        name: "Josefine Sans",
        weights: ["regular", "bold"],
        type: "ttf",
      },
      {
        name: "Open Sauce",
        weights: ["regular", "bold"],
        type: "woff2",
      },
    ],
  }),

  actions: {
    async loadFonts() {
      if (!process.client) return

      this.isLoading = true
      try {
        const styleSheet = document.createElement("style")
        styleSheet.id = "preloaded-fonts"
        let fontFaceRules = ""

        this.availableFonts.forEach((font) => {
          font.weights.forEach((weight) => {
            const fontWeight =
              {
                regular: "400",
                medium: "500",
                bold: "700",
                light: "300",
              }[weight] || "400"

            // Determine source URLs based on font type
            let srcUrls = []
            const type = font.type || "both"

            if (type === "woff2" || type === "both") {
              srcUrls.push(
                `url('/fonts/${font.name}/${font.name}-${weight}.woff2') format('woff2')`
              )
            }
            if (type === "ttf" || type === "both") {
              srcUrls.push(
                `url('/fonts/${font.name}/${font.name}-${weight}.ttf') format('truetype')`
              )
            }
            if (type === "ttc") {
              srcUrls.push(
                `url('/fonts/${font.name}/${font.name}-${weight}.ttc') format('truetype-collections')`
              )
            }
            if (type === "otf") {
              srcUrls.push(
                `url('/fonts/${font.name}/${font.name}-${weight}.otf') format('opentype')`
              )
            }

            fontFaceRules += `
              @font-face {
                font-family: '${font.name}';
                src: ${srcUrls.join(",\n                     ")};
                font-weight: ${fontWeight};
                font-style: normal;
                font-display: swap;
              }
            `
          })
        })

        const existingStyle = document.getElementById("preloaded-fonts")
        if (existingStyle) {
          existingStyle.remove()
        }

        styleSheet.textContent = fontFaceRules
        document.head.appendChild(styleSheet)

        // Preload fonts
        this.availableFonts.forEach((font) => {
          font.weights.forEach((weight) => {
            const type = font.type || "both"

            if (type === "woff2" || type === "both") {
              const woff2Link = document.createElement("link")
              woff2Link.rel = "preload"
              woff2Link.as = "font"
              woff2Link.type = "font/woff2"
              woff2Link.href = `/fonts/${font.name}/${font.name}-${weight}.woff2`
              woff2Link.crossOrigin = "anonymous"
              document.head.appendChild(woff2Link)
            }

            if (type === "ttf" || type === "both") {
              const ttfLink = document.createElement("link")
              ttfLink.rel = "preload"
              ttfLink.as = "font"
              ttfLink.href = `/fonts/${font.name}/${font.name}-${weight}.ttf`
              ttfLink.crossOrigin = "anonymous"
              document.head.appendChild(ttfLink)
            }

            if (type === "ttc") {
              const ttcLink = document.createElement("link")
              ttcLink.rel = "preload"
              ttcLink.as = "font"
              ttcLink.href = `/fonts/${font.name}/${font.name}-${weight}.ttc`
              ttcLink.crossOrigin = "anonymous"
              document.head.appendChild(ttcLink)
            }

            if (type === "otf") {
              const otfLink = document.createElement("link")
              otfLink.rel = "preload"
              otfLink.as = "font"
              otfLink.href = `/fonts/${font.name}/${font.name}-${weight}.otf`
              otfLink.crossOrigin = "anonymous"
              document.head.appendChild(otfLink)
            }
          })
        })

        this.error = null
      } catch (error) {
        console.error("Error loading fonts:", error)
        this.error = error.message
      } finally {
        this.isLoading = false
      }
    },
  },

  getters: {
    getFontOptions: (state) => {
      return state.availableFonts.map((font) => ({
        label: font.name,
        value: font.name,
        style: { fontFamily: font.name },
      }))
    },
  },
})
