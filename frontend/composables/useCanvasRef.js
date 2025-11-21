// composables/useCanvasRef.ts  (or .js if not using TypeScript)
import { useState } from "#app"

export const useCanvasRef = () => {
  const canvasEditor = useState("canvasEditor", () => null)

  const setCanvasEditor = (editor) => {
    canvasEditor.value = editor

    // Only set window.canvasEditor if we have a valid editor reference
    if (typeof window !== "undefined" && editor) {
      window.canvasEditor = {
        generatePreviewImage: async () => {
          return await editor.generatePreviewImage()
        },
        // Add any other methods you need to expose
      }
    }
  }

  return {
    canvasEditor,
    setCanvasEditor,
  }
}
