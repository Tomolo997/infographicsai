// editorStore.js
import { defineStore } from "pinia"
import { inject } from "vue"
import apiClient, { setupCSRF } from "~/services/apiClient"
import domtoimage from "dom-to-image"
import { v4 as uuidv4 } from "uuid"

export const useEditorStore = defineStore("editorStore", {
  state: () => ({
    infographId: null,
    selectedNavigationDesign: null,
    templateName: "My Template Name",
    backgroundColorCanvas: "#ffffff",
    backgroundPatternUrl: null,
    backgroundPatternSettings: {
      size: "repeat", // Changed from "cover" to "repeat"
      opacity: 1,
    },
    copiedElement: null,
    canvasWidth: 800, // Default size
    backgroundImage: null,
    backgroundImageSettings: {
      url: null,
      size: "cover", // can be "cover", "contain", or "custom"
      opacity: 1,
      position: "center", // can be "center" or "custom"
      positionX: "50%", // horizontal position percentage
      positionY: "50%", // vertical position percentage
      scale: 1, // zoom factor for custom size
    },
    canvasHeight: 2000,
    selectedElementType: null,
    elements: [],
    elementIndexMap: new Map(),
    lastUpdateTime: 0,
    updateQueue: new Map(),
    selectedElementId: null,
    selectedElement: {},
    canvasDownloadFn: null,
    history: {
      past: [],
      future: [],
      maxSize: 10, // Increased from 5 to allow for more undo steps
      isUndoRedo: false, // Flag to prevent recording history during undo/redo
      lastActionType: null, // Store the type of the last action
      pendingSave: null, // For debounced history saving
      pendingActionType: null, // Track pending action type for debounced saves
      debounceDelay: 500, // Delay in ms for debouncing history saves
    },
    isSaving: false,
    lastSavedId: null,
    saveError: null,
    recentUploads: [],
    isPasting: false,
    defaultElementWidth: 250,
    defaultElementHeight: 50,
    selectedElementIds: [], // Array for multiple selectionsđ
    selectedElementProperties: {},
    textStyles: {
      Title1: {
        fontSize: 38,
        fontWeight: 400, // extrabold
        color: "black",
        textAlign: "center",
        fontStyle: "normal",
        class: "text-2xl font-extrabold",
      },
      Title2: {
        fontSize: 32,
        fontWeight: 400, // extrabold
        class: "text-xl font-extrabold",
      },
      subTitle: {
        fontSize: 24,
        fontWeight: 400, // bold
        class: "text-lg font-bold",
      },
      body: {
        fontSize: 20,
        fontWeight: 400, // normal
        class: "text-sm font-normal",
      },
      Caption: {
        fontSize: 14,
        fontWeight: 200, // extralight
        class: "text-sm font-extralight",
      },
    },
    svgShapes: {
      square: `<svg viewBox="0 0 100 100" width="100%" height="100%" preserveAspectRatio="none">
    <rect x="0" y="0" width="100" height="100" fill="#3E57DA"/>
  </svg>`,

      circle: `<svg viewBox="0 0 100 100" width="100%" height="100%" preserveAspectRatio="none">
    <circle cx="50" cy="50" r="50" fill="#3E57DA"/>
  </svg>`,

      rectangle: `<svg viewBox="0 0 100 100" width="100%" height="100%" preserveAspectRatio="none">
  <rect x="0" y="0" width="100" height="100" fill="#3E57DA"></rect>
</svg>`,

      roundedRectangle: `<svg viewBox="0 0 100 100" width="100%" height="100%" preserveAspectRatio="none">
  <rect x="0" y="0" width="100" height="100" rx="12" ry="12" fill="#3E57DA"/>
</svg>`,

      diamond: `<svg viewBox="0 0 100 100" width="100%" height="100%" preserveAspectRatio="none">
    <path d="M50 0 L100 50 L50 100 L0 50 Z" fill="#3E57DA"/>
  </svg>`,

      octagon: `<svg viewBox="0 0 100 100" width="100%" height="100%" preserveAspectRatio="none">
    <path d="M29 0 L71 0 L100 29 L100 71 L71 100 L29 100 L0 71 L0 29 Z" fill="#3E57DA"/>
  </svg>`,
      triangle: `<svg viewBox="0 0 100 100" width="100%" height="100%" preserveAspectRatio="none">
        <path d="M50 0 L100 100 L0 100 Z" fill="#3E57DA"/>
      </svg>`,

      pentagon: `<svg viewBox="0 0 100 100" width="100%" height="100%" preserveAspectRatio="none">
        <path d="M50 0 L100 38 L81 100 L19 100 L0 38 Z" fill="#3E57DA"/>
      </svg>`,

      hexagon: `<svg viewBox="0 0 100 100" width="100%" height="100%" preserveAspectRatio="none">
        <path d="M25 0 L75 0 L100 50 L75 100 L25 100 L0 50 Z" fill="#3E57DA"/>
      </svg>`,

      star: `<svg viewBox="0 0 100 100" width="100%" height="100%" preserveAspectRatio="none">
        <path d="M50 0 L61 35 L100 35 L70 60 L80 100 L50 75 L20 100 L30 60 L0 35 L39 35 Z" fill="#3E57DA"/>
      </svg>`,

      starburst: `<svg viewBox="0 0 100 100" width="100%" height="100%" preserveAspectRatio="none">
        <path d="M50,0L59.7057,13.7778L75,6.6988L76.5165,23.4834L93.3012,25L86.2222,40.2943L100,50L86.2222,59.7057L93.3012,75L76.5165,76.5165L75,93.3012L59.7057,86.2222L50,100L40.2943,86.2222L25,93.3012L23.4834,76.5165L6.6988,75L13.7778,59.7057L0,50L13.7778,40.2943L6.6988,25L23.4834,23.4834L25,6.6988L40.2943,13.7778L50,0Z" fill="#3E57DA"/>
      </svg>`,

      //       arrow: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100%" height="100%" preserveAspectRatio="none">
      //   <g stroke="#3E57DA" stroke-width="4">
      //     <line x1="0" y1="50" x2="80" y2="50"/>
      //     <path d="M80,35 L100,50 L80,65 Z" fill="#3E57DA" stroke="none"/>
      //   </g>
      // </svg>`,

      cloud: `<svg viewBox="0 0 100 100" width="100%" height="100%" preserveAspectRatio="none">
        <path d="M25 50 Q5 50 5 35 Q5 15 25 15 Q25 5 40 5 Q60 5 60 15 Q80 15 80 35 Q80 50 60 50 Z" fill="#3E57DA"/>
      </svg>`,

      heart: `<svg viewBox="0 0 100 100" width="100%" height="100%" preserveAspectRatio="none">
        <path d="M50 95 Q25 70 5 40 Q0 25 0 15 Q0 0 20 0 Q35 0 50 20 Q65 0 80 0 Q100 0 100 15 Q100 25 95 40 Q75 70 50 95 Z" fill="#3E57DA"/>
      </svg>`,

      message: `<svg viewBox="0 0 100 100" width="100%" height="100%" preserveAspectRatio="none">
        <path d="M0 0 H100 V85 H60 L50 100 L40 85 H0 V0 Z" fill="#3E57DA"/>
      </svg>`,
      line: `<svg viewBox="0 0 100 100" width="100%" height="100%" preserveAspectRatio="none">
    <line x1="0" y1="50" x2="100" y2="50" stroke="#3E57DA" stroke-width='0' fill="#3E57DA"/>
  </svg>`,
    },

    defaultShapeSettings: {
      backgroundColor: "#3E57DA",
      opacity: 1,
      width: 150,
      height: 150,
      hasShadow: false,
      shadowOffsetX: 0,
      shadowOffsetY: 0,
      shadowBlur: 0,
      shadowColor: "#000000",
    },
    defaultLineSettings: {
      backgroundColor: "#3E57DA",
      opacity: 1,
      width: 200, // wider default for horizontal lines
      height: 4, // increased height for better visibility
    },
    defaultArrowSettings: {
      backgroundColor: "#3E57DA",
      opacity: 1,
      width: 200, // wider default for horizontal lines
      height: 50, // increased height for better visibility
      strokeWidth: 4,
    },

    defaultVerticalLineSettings: {
      backgroundColor: "#3E57DA",
      opacity: 1,
      width: 4, // thinner default for vertical lines
      height: 200, // taller default for vertical lines
    },
    defaultMediaSettings: {
      width: 300,
      height: 200,
      opacity: 1,
      objectFit: "cover",
      maxWidth: 800,
      maxHeight: 800,
      minWidth: 50,
      minHeight: 50,
      scaleX: 1,
      scaleY: 1,
    },
  }),

  actions: {
    // In editorStore.js, modify saveInfographic:

    setBackgroundColor(color) {
      this.saveToHistory("colorChange")
      this.clearBackgroundImage()
      this.clearBackgroundPattern()
      this.backgroundColorCanvas = color
      // Clear any existing pattern when setting a background color
      this.backgroundPatternUrl = null
      this.backgroundPatternSettings = {
        size: "cover",
        opacity: 1,
      }
    },

    setBackgroundPattern(patternUrl, settings = {}) {
      this.saveToHistory("styleChange")
      this.clearBackgroundImage()
      this.backgroundPatternUrl = patternUrl

      // Store the current background color if we need to restore it later
      this._previousBackgroundColor = this.backgroundColorCanvas

      // Set background color to transparent when pattern is applied
      this.backgroundColorCanvas = "transparent"

      // Set pattern settings with proper defaults for repeating patterns
      this.backgroundPatternSettings = {
        size: settings.size || "repeat", // Default to repeat instead of cover
        opacity: settings.opacity !== undefined ? settings.opacity : 1,
        ...settings,
      }
    },

    clearBackgroundPattern() {
      this.saveToHistory("styleChange")
      this.backgroundPatternUrl = null

      // Restore previous background color if it exists
      if (this._previousBackgroundColor) {
        this.backgroundColorCanvas = this._previousBackgroundColor
        this._previousBackgroundColor = null
      }

      this.backgroundPatternSettings = {
        size: "cover",
        opacity: 1,
      }
    },
    updateElementIndexMap() {
      this.elementIndexMap.clear()
      this.elements.forEach((el, index) => {
        this.elementIndexMap.set(el.id, index)
      })
    },
    updateElement(id, updates) {
      // Determine the action type based on what's being updated
      let actionType = "general"
      if (updates.x !== undefined || updates.y !== undefined) {
        actionType = "drag"
      } else if (updates.width !== undefined || updates.height !== undefined) {
        actionType = "resize"
      } else if (
        updates.backgroundColor !== undefined ||
        updates.color !== undefined
      ) {
        actionType = "colorChange"
      } else if (
        updates.fontWeight !== undefined ||
        updates.fontStyle !== undefined ||
        updates.textAlign !== undefined
      ) {
        actionType = "styleChange"
      }

      this.saveToHistory(actionType)
      const index = this.elementIndexMap.get(id) // Use map instead of findIndex
      if (index !== undefined) {
        this.elements[index] = {
          ...this.elements[index],
          ...updates,
        }
        if (this.selectedElementId === id) {
          this.selectedElement = this.elements[index]
        }
      }
    },
    async saveInfographic(previewBlob) {
      if (this.isSaving) return

      try {
        this.isSaving = true
        this.saveError = null

        // Create form data
        const formData = new FormData()

        // Add the preview image if provided
        if (previewBlob) {
          formData.append("preview_image", previewBlob, "preview.png")
        }

        // Serialize canvas state and stringify it properly
        const payload = this.serializeCanvasState()

        // Important: Stringify the entire content object
        formData.append("content", JSON.stringify(payload))
        formData.append("infograph_id", this.infographId || "")
        formData.append("title", this.templateName)
        formData.append("width", this.canvasWidth.toString())
        formData.append("height", this.canvasHeight.toString())
        formData.append("background_color", this.backgroundColorCanvas)

        // Send to backend
        const response = await apiClient.post(
          "/infos/save-infographic/",
          formData,
          {
            headers: {
              "Content-Type": "multipart/form-data",
            },
          }
        )

        return response.data
      } catch (error) {
        console.error("Error saving infographic:", error)
        this.saveError =
          error.response?.data?.error || "Failed to save infographic"
        throw error
      } finally {
        this.isSaving = false
      }
    },
    async saveInfographicsAdmin(previewBlob) {
      if (this.isSaving) return

      try {
        this.isSaving = true
        this.saveError = null

        // Create form data
        const formData = new FormData()

        // Add the infograph UUID
        formData.append("infograph_uuid", this.infographId)

        // Add the preview image if provided
        if (previewBlob) {
          formData.append("preview_image", previewBlob, "preview.png")
        } else {
          console.warn("No preview blob provided")
        }

        // Get CSRF token
        await setupCSRF()

        // Post to the correct endpoint
        const response = await apiClient.post(
          "/infos/save-infographic-admin/",
          formData,
          {
            headers: {
              "Content-Type": "multipart/form-data",
            },
          }
        )

        console.log("Save successful:", response.data)
        return response.data
      } catch (error) {
        console.error("Error saving infographic:", error)
        this.saveError =
          error.response?.data?.error || "Failed to save infographic"
        throw error
      } finally {
        this.isSaving = false
      }
    },

    setBackgroundImage(imageUrl, settings = {}) {
      this.saveToHistory("styleChange")
      this.clearBackgroundPattern()
      this.backgroundImage = imageUrl
      this.backgroundImageSettings = {
        ...this.backgroundImageSettings,
        url: imageUrl,
        position: settings.position || "center",
        positionX: settings.positionX || "50%",
        positionY: settings.positionY || "50%",
        scale: settings.scale || 1,
        size: settings.size || "cover",
        opacity: settings.opacity || 1,
        ...settings,
      }

      // Clear pattern when setting image
      this.backgroundPatternUrl = null
      this.backgroundPatternSettings = {
        size: "cover",
        opacity: 1,
      }
    },

    // Add a specific method for repositioning
    repositionBackgroundImage(positionX, positionY, scale) {
      this.saveToHistory("styleChange")
      this.backgroundImageSettings = {
        ...this.backgroundImageSettings,
        position: "custom",
        positionX: `${positionX}%`,
        positionY: `${positionY}%`,

        // Ensure scale is never below 1.0
        scale: Math.max(1.0, scale || 1.0),
      }
    },
    clearBackgroundImage() {
      this.saveToHistory("styleChange")
      this.backgroundImage = null
      this.backgroundImageSettings = {
        url: null,
        size: "cover",
        opacity: 1,
        position: "center",
      }
    },

    updateBackgroundImageSettings(settings) {
      this.saveToHistory("styleChange")
      this.backgroundImageSettings = {
        ...this.backgroundImageSettings,
        ...settings,
      }
    },
    serializeCanvasState() {
      // Create a clean copy of the elements without Vue reactivity
      const cleanElements = this.elements.map((element) => {
        const cleanElement = { ...element }

        switch (element.type) {
          case "text":
            return {
              type: "text",
              id: element.id,
              content: element.content,
              x: element.x,
              y: element.y,
              width: element.width,
              height: element.height,
              rotation: element.rotation,
              textAlign: element.textAlign,
              fontSize: element.fontSize,
              fontFamily: element.fontFamily,
              fontWeight: element.fontWeight,
              color: element.color,
              opacity: element.opacity,
              textType: element.textType,
              lineHeight: element.lineHeight,
              locked: element.locked || false,
              letterSpacing: element.letterSpacing,
              textDecoration: element.textDecoration,
              hasShadow: element.hasShadow || false,
              shadowOffsetX: element.shadowOffsetX || 0,
              shadowOffsetY: element.shadowOffsetY || 0,
              shadowBlur: element.shadowBlur || 0,
              shadowColor: element.shadowColor || "#000000",
            }

          case "shape":
            return {
              type: "shape",
              id: element.id,
              shapeType: element.shapeType,
              isLine: element.isLine,
              x: element.x,
              y: element.y,
              width: element.width,
              height: element.height,
              rotation: element.rotation,
              backgroundColor: element.backgroundColor,
              opacity: element.opacity,
              svgContent: element.svgContent,
              svgProps: element.svgProps,
              locked: element.locked || false,
              hasShadow: element.hasShadow || false,
              shadowOffsetX: element.shadowOffsetX || 0,
              shadowOffsetY: element.shadowOffsetY || 0,
              shadowBlur: element.shadowBlur || 0,
              shadowColor: element.shadowColor || "#000000",
            }

          case "media":
            return {
              type: "media",
              id: element.id,
              src: element.src,
              alt: element.alt,
              x: element.x,
              y: element.y,
              width: element.width,
              height: element.height,
              rotation: element.rotation,
              opacity: element.opacity,
              objectFit: element.objectFit,
              scaleX: element.scaleX,
              scaleY: element.scaleY,
              locked: element.locked || false,
            }

          case "graphic":
            return {
              type: "graphic",
              id: element.id,
              svgType: element.svgType,
              svgContent: element.svgContent,
              src: element.src,
              x: element.x,
              y: element.y,
              width: element.width,
              height: element.height,
              scaleX: element.scaleX,
              scaleY: element.scaleY,
              rotation: element.rotation,
              opacity: element.opacity,
              currentColor: element.currentColor,
              locked: element.locked || false,
              iconType: element.iconType,
            }

          default:
            // Make sure we include the locked property in the default case too
            return {
              ...cleanElement,
              locked: element.locked || false,
            }
        }
      })

      // Return the complete canvas state
      return {
        canvas_data: {
          elements: cleanElements,
          background: {
            color: this.backgroundColorCanvas,
            patternUrl: this.backgroundPatternUrl,
            patternSettings: this.backgroundPatternSettings,
            imageUrl: this.backgroundImage,
            imageSettings: this.backgroundImageSettings,
          },
        },
      }
    },

    async loadInfographic(uuid) {
      try {
        const response = await apiClient.get(`/infos/infographic/${uuid}/`)
        if (response.status === 200) {
          const data = response.data
          this.templateName = data.title
          this.canvasWidth = data.width || this.canvasWidth
          this.canvasHeight = data.height || this.canvasHeight
          this.backgroundColorCanvas = data.background_color || "#ffffff"

          if (data.content) {
            this.elements = data.content?.canvas_data?.elements || []

            if (data.content.canvas_data.background) {
              const bg = data.content.canvas_data.background

              // Load background pattern
              this.backgroundPatternUrl = bg.patternUrl
              this.backgroundPatternSettings = {
                ...this.backgroundPatternSettings,
                ...bg.patternSettings,
              }

              // Load background image
              this.backgroundImage = bg.imageUrl
              this.backgroundImageSettings = {
                ...this.backgroundImageSettings,
                ...bg.imageSettings,
              }
            }

            this.updateElementIndexMap()
          }

          this.infographId = data.uuid
          return data
        }
      } catch (error) {
        console.error("Error loading infographic:", error)
        throw error
      }
    },

    setSelection(id) {
      this.selectedElementIds = [id]
      this.selectedElementId = id
      this.selectedElement = this.elements.find((el) => el.id === id) || {}
    },

    addToSelection(id) {
      if (!this.selectedElementIds.includes(id)) {
        this.selectedElementIds.push(id)
      }
    },

    removeFromSelection(id) {
      this.selectedElementIds = this.selectedElementIds.filter(
        (elementId) => elementId !== id
      )
    },
    bringToFront(id) {
      this.saveToHistory("zIndex")
      const index = this.elementIndexMap.get(id)
      if (index !== undefined) {
        // Remove the element from its current position
        const [element] = this.elements.splice(index, 1)

        // Add it to the end of the array (top layer)
        this.elements.push(element)

        // Update the element index map
        this.updateElementIndexMap()
      }
    },
    bringToBack(id) {
      this.saveToHistory("zIndex")
      const index = this.elementIndexMap.get(id)
      if (index !== undefined) {
        // Remove the element from its current position
        const [element] = this.elements.splice(index, 1)

        // Add it to the beginning of the array (bottom layer)
        this.elements.unshift(element)

        // Update the element index map
        this.updateElementIndexMap()
      }
    },
    saveToHistory(actionType = "general", immediate = false) {
      if (this.history.isUndoRedo) return

      // Clear any pending debounced save when a different action type occurs or immediate save requested
      if (this.history.pendingActionType !== actionType || immediate) {
        this._clearPendingSave()
      }

      // Create the current state snapshot
      const currentState = {
        type: actionType,
        elements: JSON.parse(JSON.stringify(this.elements)),
        selectedElementIds: [...this.selectedElementIds],
        selectedElementId: this.selectedElementId,
        selectedElement: this.selectedElement
          ? { ...this.selectedElement }
          : {},
        background: {
          color: this.backgroundColorCanvas,
          patternUrl: this.backgroundPatternUrl,
          patternSettings: { ...this.backgroundPatternSettings },
          imageUrl: this.backgroundImage,
          imageSettings: { ...this.backgroundImageSettings },
        },
        canvasWidth: this.canvasWidth,
        canvasHeight: this.canvasHeight,
        timestamp: Date.now(),
      }

      // Properties that should be debounced when changing rapidly
      const debouncedActionTypes = [
        "colorChange",
        "styleChange",
        "resize",
        "drag",
      ]

      // If this is a debounced action type and not immediate, set up debounced save
      if (debouncedActionTypes.includes(actionType) && !immediate) {
        this._clearPendingSave()

        this.history.pendingSave = setTimeout(() => {
          this._actualSaveToHistory(currentState)
          this.history.pendingSave = null
          this.history.pendingActionType = null
        }, this.history.debounceDelay)

        this.history.pendingActionType = actionType
      } else {
        // For non-debounced action types or immediate saves, save right away
        this._actualSaveToHistory(currentState)
      }
    },

    // Helper method to clear any pending save
    _clearPendingSave() {
      if (this.history.pendingSave) {
        clearTimeout(this.history.pendingSave)
        this.history.pendingSave = null
      }
    },

    // The actual logic to save to history
    _actualSaveToHistory(currentState) {
      // Check if this is the same as the last saved state to avoid duplicates
      const lastState = this.history.past[this.history.past.length - 1]
      if (lastState) {
        // Extremely simple check - just make sure it's not the exact same state
        const lastElements = JSON.stringify(lastState.elements)
        const currentElements = JSON.stringify(currentState.elements)
        if (lastElements === currentElements) {
          return // Skip identical states
        }
      }

      this.history.past.push(currentState)
      this.history.lastActionType = currentState.type

      // Limit history size
      if (this.history.past.length > this.history.maxSize) {
        this.history.past.shift()
      }

      // Clear redo stack when a new action is performed
      this.history.future = []
    },

    undo() {
      // Commit any pending changes before performing undo
      if (this.history.pendingSave) {
        this._clearPendingSave()
        // Force save the current state before undoing
        this.saveToHistory(this.history.pendingActionType || "general", true)
      }

      if (this.history.past.length === 0) return

      this.history.isUndoRedo = true

      try {
        // Create a snapshot of current state before applying undo
        const currentState = {
          type: this.history.lastActionType || "general",
          elements: JSON.parse(JSON.stringify(this.elements)),
          selectedElementIds: [...this.selectedElementIds],
          selectedElementId: this.selectedElementId,
          selectedElement: this.selectedElement
            ? { ...this.selectedElement }
            : {},
          background: {
            color: this.backgroundColorCanvas,
            patternUrl: this.backgroundPatternUrl,
            patternSettings: { ...this.backgroundPatternSettings },
            imageUrl: this.backgroundImage,
            imageSettings: { ...this.backgroundImageSettings },
          },
          canvasWidth: this.canvasWidth,
          canvasHeight: this.canvasHeight,
          timestamp: Date.now(),
        }

        // Push current state to future for redo
        this.history.future.push(currentState)

        // Get previous state from history
        const previousState = this.history.past.pop()

        // Apply the previous state
        this._applyHistoryState(previousState)

        // Update last action type for coherent history tracking
        this.history.lastActionType = previousState.type || "general"
      } finally {
        // Always reset the undo/redo flag
        this.history.isUndoRedo = false
      }
    },

    redo() {
      // Commit any pending changes before performing redo
      if (this.history.pendingSave) {
        this._clearPendingSave()
        // Force save the current state before redoing
        this.saveToHistory(this.history.pendingActionType || "general", true)
      }

      if (this.history.future.length === 0) return

      this.history.isUndoRedo = true

      try {
        // Create a snapshot of current state before applying redo
        const currentState = {
          type: this.history.lastActionType || "general",
          elements: JSON.parse(JSON.stringify(this.elements)),
          selectedElementIds: [...this.selectedElementIds],
          selectedElementId: this.selectedElementId,
          selectedElement: this.selectedElement
            ? { ...this.selectedElement }
            : {},
          background: {
            color: this.backgroundColorCanvas,
            patternUrl: this.backgroundPatternUrl,
            patternSettings: { ...this.backgroundPatternSettings },
            imageUrl: this.backgroundImage,
            imageSettings: { ...this.backgroundImageSettings },
          },
          canvasWidth: this.canvasWidth,
          canvasHeight: this.canvasHeight,
          timestamp: Date.now(),
        }

        // Push current state to past for undo
        this.history.past.push(currentState)

        // Get next state from future history
        const nextState = this.history.future.pop()

        // Apply the next state
        this._applyHistoryState(nextState)

        // Update last action type for coherent history tracking
        this.history.lastActionType = nextState.type || "general"
      } finally {
        // Always reset the undo/redo flag
        this.history.isUndoRedo = false
      }
    },

    // Helper method to apply a history state
    _applyHistoryState(state) {
      if (!state) return

      // Restore elements with validation
      if (Array.isArray(state.elements)) {
        this.elements = state.elements.map((element) => ({
          ...element,
          x: typeof element.x === "number" ? element.x : 0,
          y: typeof element.y === "number" ? element.y : 0,
        }))
      }

      // Restore selection state
      this.selectedElementIds = Array.isArray(state.selectedElementIds)
        ? state.selectedElementIds
        : []
      this.selectedElementId = state.selectedElementId || null
      this.selectedElement = state.selectedElement || {}

      // Restore background state
      if (state.background) {
        this.backgroundColorCanvas = state.background.color || "#ffffff"
        this.backgroundPatternUrl = state.background.patternUrl || null

        this.backgroundPatternSettings = {
          size: "cover",
          opacity: 1,
          ...(state.background.patternSettings || {}),
        }

        this.backgroundImage = state.background.imageUrl || null
        this.backgroundImageSettings = {
          ...(this.backgroundImageSettings || {}),
          ...(state.background.imageSettings || {}),
        }
      }

      // Restore canvas dimensions if they were saved
      if (state.canvasWidth !== undefined) {
        this.canvasWidth = state.canvasWidth
      }

      if (state.canvasHeight !== undefined) {
        this.canvasHeight = state.canvasHeight
      }

      // Update element index map
      this.updateElementIndexMap()
    },

    // Update element without saving to history (reuse existing method)
    updateElementWithoutHistory(id, updates) {
      const index = this.elements.findIndex((el) => el.id === id)
      if (index !== -1) {
        this.elements[index] = {
          ...this.elements[index],
          ...updates,
        }
        if (this.selectedElementId === id) {
          this.selectedElement = this.elements[index]
        }
      }
    },
    saveTransformOperation(type, startState, endState) {
      const historyAction = {
        type,
        startState: {
          ...startState,
          type, // Ensure type is included in startState
        },
        endState: {
          ...endState,
          type, // Ensure type is included in endState
        },
      }

      this.history.past.push(historyAction)
      this.history.future = [] // Clear redo stack

      if (this.history.past.length > this.history.maxSize) {
        this.history.past.shift()
      }
    },
    // In editorStore.js
    batchUpdateElements(updates) {
      // Convert object entries to Map entries
      Object.entries(updates).forEach(([id, props]) => {
        this.updateQueue.set(id, props)
      })

      const now = Date.now()
      if (now - this.lastUpdateTime > 16) {
        // ~60fps
        this._processUpdateQueue()
        this.lastUpdateTime = now
      }
    },

    _processUpdateQueue() {
      if (this.updateQueue.size === 0) return

      this.updateQueue.forEach((props, id) => {
        const index = this.elementIndexMap.get(id)
        if (index !== undefined) {
          Object.assign(this.elements[index], props)

          if (this.selectedElementId === id) {
            this.selectedElement = this.elements[index]
          }
        }
      })

      this.updateQueue.clear()
    },
    updateElementWithoutHistory(id, updates) {
      const index = this.elements.findIndex((el) => el.id === id)
      if (index !== -1) {
        this.elements[index] = {
          ...this.elements[index],
          ...updates,
        }

        // Update selectedElement if needed
        if (this.selectedElementId === id) {
          this.selectedElement = this.elements[index]
        }
      }
    },
    // Add method to save drag operations
    saveDragOperation(startState, endState) {
      // Filter out locked elements from the drag operation
      const filteredEndState = {}

      for (const id in endState) {
        const element = this.elements.find((el) => el.id === id)
        // Only include non-locked elements in the drag operation
        if (element && !element.locked) {
          filteredEndState[id] = endState[id]
        }
      }

      // If no unlocked elements were dragged, return early
      if (Object.keys(filteredEndState).length === 0) return

      // Instead of creating a custom history action, use saveToHistory with type
      this.saveToHistory("drag")
    },

    clearSelection() {
      this.selectedElementIds = []
      this.selectedElementId = null
      this.selectedElement = {}
    },

    updateSetting(key, value) {
      this[key] = value
    },

    toggleElementLock(id) {
      if (!id) return

      this.saveToHistory()
      const index = this.elementIndexMap.get(id)

      if (index !== undefined) {
        // Toggle the locked state
        const currentLocked = this.elements[index].locked || false
        this.elements[index].locked = !currentLocked

        // Update selectedElement if this is the currently selected element
        if (this.selectedElementId === id) {
          this.selectedElement = this.elements[index]
        }
      }
    },

    calculateElementPosition(
      elementWidth = this.defaultElementWidth,
      elementHeight = this.defaultElementHeight
    ) {
      return {
        x: this.canvasWidth / 2 - elementWidth / 2,
        y: this.canvasHeight / 2 - elementHeight / 2,
      }
    },

    addTextElement(style = "body") {
      this.saveToHistory("add")
      const id = `text-${Date.now()}`
      const styleSettings = this.textStyles[style] || this.textStyles.body
      const position = this.calculateElementPosition()

      const textElement = {
        id,
        type: "text",
        content: "Double click to edit",
        x: position.x,
        y: position.y,
        width: this.defaultElementWidth,
        height: this.defaultElementHeight,
        rotation: 0,
        textAlign: "center",
        textType: style,
        hasShadow: false,
        shadowOffsetX: 1,
        shadowOffsetY: 1,
        opacity: 1,
        shadowBlur: 1,
        shadowColor: "#000000",
        ...this.defaultTextSettings,
        ...styleSettings,
        locked: false,
      }

      this.elements.push(textElement)
      this.elementIndexMap.set(id, this.elements.length - 1) // Update map
      this.selectedElementId = id
      return id
    },

    deleteElement(id) {
      this.saveToHistory("delete")
      const index = this.elementIndexMap.get(id)
      if (index !== undefined) {
        this.elements.splice(index, 1)
        this.updateElementIndexMap() // Rebuild map after deletion
        this.selectedElementId = null
        this.selectedElement = {}
      }
    },
    // Add these methods to the actions section of editorStore.js

    // Add these methods to the actions section of editorStore.js

    copyElement(elementId) {
      // Support both single element and array of elements
      const elementIds = Array.isArray(elementId) ? elementId : [elementId]

      // Find all elements to copy
      const elementsToCopy = elementIds
        .map((id) => this.elements.find((el) => el.id === id))
        .filter(Boolean)

      if (elementsToCopy.length === 0) return

      // Calculate the bounding box
      const boundingBox = this.calculateBoundingBox(elementsToCopy)

      // Store elements and their relative positions
      this.copiedElement = {
        elements: elementsToCopy.map((element) => {
          const copy = JSON.parse(JSON.stringify(element))
          // Store relative position from top-left of bounding box
          copy.relativeX = element.x - boundingBox.left
          copy.relativeY = element.y - boundingBox.top
          // Preserve locked status
          copy.locked = element.locked
          return copy
        }),
        boundingBox,
        timestamp: Date.now(),
      }
    },

    async pasteElement() {
      this.saveToHistory("add")
      if (!this.copiedElement || this.isPasting) return

      this.isPasting = true

      try {
        // Handle both single and multiple elements
        if (Array.isArray(this.copiedElement.elements)) {
          const timestamp = Date.now()
          const { elements, boundingBox } = this.copiedElement

          // Calculate offset for the entire group
          const OFFSET = 20 // Consistent offset value
          const offsetX = OFFSET
          const offsetY = OFFSET

          const pastedElements = elements.map((element, index) => {
            const newId = `${element.type}-${timestamp}-${index}`

            // Calculate new position based on original relative position plus group offset
            const newX = boundingBox.left + element.relativeX + offsetX
            const newY = boundingBox.top + element.relativeY + offsetY

            return {
              ...element,
              id: newId,
              x: newX,
              y: newY,
              // Preserve locked status if it exists
              locked: element.locked || false,
              relativeX: undefined, // Clean up temporary properties
              relativeY: undefined,
            }
          })

          // Add all new elements to the canvas
          this.elements.push(...pastedElements)

          // Update element index map
          this.selectedElementIds = pastedElements.map((el) => el.id)
          this.selectedElementId = pastedElements[0].id
          this.selectedElement = pastedElements[0]
          this.updateElementIndexMap()

          return pastedElements.map((el) => el.id)
        } else {
          // Fallback for old single-element copy data
          const newId = `${this.copiedElement.type}-${Date.now()}`
          const pastedElement = {
            ...this.copiedElement,
            id: newId,
            x: this.copiedElement.x + 20,
            y: this.copiedElement.y + 20,
          }

          this.elements.push(pastedElement)
          this.selectedElementId = newId
          this.updateElementIndexMap()
          return newId
        }
      } finally {
        setTimeout(() => {
          this.isPasting = false
        }, 1000)
      }
    },

    // Add this helper method if not already present
    calculateBoundingBox(elements) {
      if (!elements || elements.length === 0) return null

      return elements.reduce(
        (box, element) => {
          const right = element.x + (element.width || 0)
          const bottom = element.y + (element.height || 0)

          return {
            left: Math.min(box.left, element.x),
            top: Math.min(box.top, element.y),
            right: Math.max(box.right, right),
            bottom: Math.max(box.bottom, bottom),
            width: Math.abs(
              Math.max(box.right, right) - Math.min(box.left, element.x)
            ),
            height: Math.abs(
              Math.max(box.bottom, bottom) - Math.min(box.top, element.y)
            ),
          }
        },
        {
          left: Infinity,
          top: Infinity,
          right: -Infinity,
          bottom: -Infinity,
          width: 0,
          height: 0,
        }
      )
    },

    setSelectedElement(element) {
      this.selectedElement = element
    },

    updateIconProperties(properties) {
      // Determine if this is a final change
      const finalChange = properties.finalChange === true
      if (finalChange) {
        delete properties.finalChange
      }

      // Use appropriate action type based on properties
      const actionType =
        properties.fill !== undefined || properties.stroke !== undefined
          ? "colorChange"
          : "styleChange"

      // Save to history with finalChange flag
      this.saveToHistory(actionType, finalChange)

      if (!this.selectedElement?.id || this.selectedElement.type !== "graphic")
        return

      let updates = { ...properties }
      let svgContent = this.selectedElement.svgContent

      // Common SVG elements that can have fill and stroke
      const elements = [
        "path",
        "rect",
        "circle",
        "ellipse",
        "polygon",
        "polyline",
        "line",
      ]

      if (properties.opacity !== undefined) {
        updates.opacity = properties.opacity / 100 // Convert percentage to decimal
      }

      // Handle fill color updates
      if (properties.fill !== undefined) {
        const fillColor = properties.fill

        if (!svgContent.includes("<svg")) {
          console.warn("Invalid SVG content")
          return
        }

        // Update SVG root fill
        if (!svgContent.match(/<svg[^>]*fill=/)) {
          svgContent = svgContent.replace("<svg", `<svg fill="${fillColor}"`)
        } else {
          svgContent = svgContent.replace(
            /<svg([^>]*?)fill="[^"]*"/,
            `<svg$1fill="${fillColor}"`
          )
        }

        // Update fill for all shape elements
        elements.forEach((element) => {
          // Add fill to elements without fill
          svgContent = svgContent.replace(
            new RegExp(`<${element}([^>]*?)(\\/>|>)`, "g"),
            (match, attrs, end) => {
              if (!attrs.includes("fill=")) {
                return `<${element}${attrs} fill="${fillColor}"${end}`
              }
              return match
            }
          )

          // Update existing fill attributes
          svgContent = svgContent.replace(
            new RegExp(`<${element}([^>]*?)fill="[^"]*"`, "g"),
            `<${element}$1fill="${fillColor}"`
          )
        })
      }

      // Handle stroke properties
      if (properties.stroke !== undefined) {
        const strokeColor = properties.stroke
        const strokeWidth = properties.strokeWidth || "2" // Default stroke width if not provided

        // Update SVG root stroke
        if (!svgContent.match(/<svg[^>]*stroke=/)) {
          svgContent = svgContent.replace(
            "<svg",
            `<svg stroke="${strokeColor}"`
          )
        } else {
          svgContent = svgContent.replace(
            /<svg([^>]*?)stroke="[^"]*"/,
            `<svg$1stroke="${strokeColor}"`
          )
        }

        // Add/update stroke-width on SVG root if not present
        if (!svgContent.match(/<svg[^>]*stroke-width=/)) {
          svgContent = svgContent.replace(
            "<svg",
            `<svg stroke-width="${strokeWidth}"`
          )
        } else {
          svgContent = svgContent.replace(
            /<svg([^>]*?)stroke-width="[^"]*"/,
            `<svg$1stroke-width="${strokeWidth}"`
          )
        }

        // Update stroke for all shape elements
        elements.forEach((element) => {
          // Add stroke to elements without stroke
          svgContent = svgContent.replace(
            new RegExp(`<${element}([^>]*?)(\\/>|>)`, "g"),
            (match, attrs, end) => {
              let newAttrs = attrs
              if (!attrs.includes("stroke=")) {
                newAttrs += ` stroke="${strokeColor}"`
              }
              if (!attrs.includes("stroke-width=")) {
                newAttrs += ` stroke-width="${strokeWidth}"`
              }
              return `<${element}${newAttrs}${end}`
            }
          )

          // Update existing stroke attributes
          svgContent = svgContent.replace(
            new RegExp(`<${element}([^>]*?)stroke="[^"]*"`, "g"),
            `<${element}$1stroke="${strokeColor}"`
          )

          // Update existing stroke-width attributes
          svgContent = svgContent.replace(
            new RegExp(`<${element}([^>]*?)stroke-width="[^"]*"`, "g"),
            `<${element}$1stroke-width="${strokeWidth}"`
          )
        })
      }

      updates.svgContent = svgContent
      this.updateElement(this.selectedElement.id, updates)
    },

    // Add this to the actions section of editorStore.js
    updateGraphicTransform(id, properties) {
      this.saveToHistory("transform")
      if (!id) return

      const index = this.elementIndexMap.get(id)
      if (index !== undefined) {
        // Create a copy of the element
        const element = { ...this.elements[index] }

        // Update transform properties
        if (properties.rotation !== undefined) {
          // Normalize rotation to be between 0 and 360
          element.rotation = ((properties.rotation % 360) + 360) % 360
        }
        if (properties.scaleX !== undefined) {
          element.scaleX = properties.scaleX
        }
        if (properties.scaleY !== undefined) {
          element.scaleY = properties.scaleY
        }

        // Update the element
        this.elements[index] = element
        if (this.selectedElementId === id) {
          this.selectedElement = element
        }
      }
    },

    updateShapeProperties(properties) {
      const actionType =
        properties.backgroundColor !== undefined ||
        properties.fill !== undefined
          ? "colorChange"
          : "styleChange"
      const immediate = properties.finalChange === true

      if (properties.finalChange) {
        delete properties.finalChange
      }

      this.saveToHistory(actionType, immediate)

      if (!this.selectedElement?.id || this.selectedElement.type !== "shape")
        return

      // Handle special cases like fill type
      if (properties.fillType) {
        properties.fill =
          properties.fillType === "No Fill"
            ? "transparent"
            : properties.fillColor
        delete properties.fillType
        delete properties.fillColor
      }

      // Handle border type
      if (properties.borderType) {
        const borderStyles = {
          Solid: {
            strokeDasharray: "solid",
            stroke: "#3E57DA",
            strokeWidth: 1,
          },
          Dashed: { strokeDasharray: "5,5", stroke: "#3E57DA", strokeWidth: 1 },
          None: {
            stroke: "",
            strokeDasharray: "none",
            strokeWidth: 0,
          },
        }

        Object.assign(properties, borderStyles[properties.borderType])
        delete properties.borderType
      }

      // Handle backgroundColor property for line shapes directly by updating the element
      if (
        properties.backgroundColor !== undefined &&
        this.selectedElement.shapeType === "line"
      ) {
        this.updateElement(this.selectedElement.id, {
          backgroundColor: properties.backgroundColor,
        })
        // Remove the backgroundColor property to avoid double processing
        delete properties.stroke
        delete properties.backgroundColor
      }

      this.updateShapeElement(this.selectedElement.id, properties)
    },
    mediaProperties: (state) => {
      if (!state.selectedElement || state.selectedElement.type !== "media")
        return null

      return {
        opacity: (state.selectedElement.opacity || 1) * 100,
        objectFit: state.selectedElement.objectFit || "cover",
      }
    },
    async addIconElement(svg, type, iconType) {
      this.saveToHistory("add")
      const id = `graphic-${Date.now()}`
      const position = this.calculateElementPosition()

      try {
        let cleanedSvg = svg

        if (iconType === "flat") {
          // Only remove XML and DOCTYPE declarations, preserve style tag
          cleanedSvg = svg
            .replace(/<\?xml[^>]*\?>/g, "")
            .replace(/<!DOCTYPE[^>]*>/g, "")
        } else {
          // Process other types as before
          cleanedSvg = svg
            .replace(/<\?xml[^>]*\?>/g, "")
            .replace(/<!DOCTYPE[^>]*>/g, "")
            .replace(/<style.*?<\/style>/gs, "")

          if (type === "vector") {
            cleanedSvg = cleanedSvg.replace(
              /fill="#6c63ff"/g,
              'fill="currentColor"'
            )
          } else {
            cleanedSvg = cleanedSvg
              .replace(/fill="#231F20"/g, 'fill="currentColor"')
              .replace(/class="st0"/g, 'fill="currentColor"')
          }
        }

        const iconElement = {
          id,
          type: "graphic",
          svgType: type,
          svgContent: cleanedSvg,
          x: position.x,
          y: position.y,
          width: 250,
          height: 250,
          scaleX: 1,
          scaleY: 1,
          rotation: 0,
          opacity: 1,
          locked: false,
          iconType: iconType,
        }

        this.elements.push(iconElement)
        this.selectedElementId = id
        this.selectedElementType = "graphic"
        this.selectedElement = iconElement
        this.updateElementIndexMap()
        return id
      } catch (error) {
        console.error("Error creating icon element:", error)
        throw error
      }
    },
    async addMediaElement(file) {
      this.saveToHistory("add")
      const id = `media-${Date.now()}`
      const position = this.calculateElementPosition()

      try {
        // Get image dimensions before upload
        let imageDimensions
        let dimensions
        let response
        if (file.url) {
          // For already uploaded files, use default dimensions
          dimensions = {
            width: this.defaultMediaSettings.width,
            height: this.defaultMediaSettings.height,
          }
        } else {
          // Create URL for the uploaded file
          const formData = new FormData()
          formData.append("file", file)

          // Upload file to R2 through our API
          response = await apiClient.post("/infos/upload-media/", formData, {
            headers: {
              "Content-Type": "multipart/form-data",
            },
          })

          // Get the original image dimensions
          imageDimensions = await this.getImageDimensions(file)

          // Use original dimensions directly, with minimal constraints
          dimensions = {
            width: imageDimensions.width,
            height: imageDimensions.height,
          }

          // Only scale down if the image is extremely large
          if (dimensions.width > 1200 || dimensions.height > 1200) {
            const aspectRatio = dimensions.width / dimensions.height
            if (dimensions.width > dimensions.height) {
              dimensions.width = 1200
              dimensions.height = Math.round(1200 / aspectRatio)
            } else {
              dimensions.height = 1200
              dimensions.width = Math.round(1200 * aspectRatio)
            }
          }
        }

        // Create new media element
        const mediaElement = {
          id,
          type: "media",
          src: file.url ? file.url : response?.data?.url,
          alt: file.name,
          x: position.x,
          y: position.y,
          width: dimensions.width,
          height: dimensions.height,
          rotation: 0,
          opacity: this.defaultMediaSettings.opacity,
          objectFit: this.defaultMediaSettings.objectFit,
          scaleX: this.defaultMediaSettings.scaleX,
          scaleY: this.defaultMediaSettings.scaleY,
          locked: false,
        }

        this.elements.push(mediaElement)
        this.selectedElementId = id
        this.selectedElementType = "media"
        this.selectedElement = mediaElement
        this.updateElementIndexMap()
        return id
      } catch (error) {
        console.error("Error uploading media:", error)
        throw error
      }
    },
    setBackgroundImage(imageUrl) {
      // Add this to your editorStore actions/methods
      this.backgroundImage = imageUrl
      // Additional logic for applying the background image to your canvas
    },

    getImageDimensions(file) {
      return new Promise((resolve) => {
        const img = new Image()
        img.onload = () => {
          resolve({
            width: img.width,
            height: img.height,
          })
        }
        img.src = URL.createObjectURL(file)
      })
    },

    // Helper method to calculate dimensions while preserving aspect ratio
    calculateMediaDimensions(imageDimensions) {
      const maxWidth = this.defaultMediaSettings.maxWidth
      const maxHeight = this.defaultMediaSettings.maxHeight
      const minWidth = this.defaultMediaSettings.minWidth
      const minHeight = this.defaultMediaSettings.minHeight

      let width = imageDimensions.width
      let height = imageDimensions.height
      const aspectRatio = width / height

      // Scale down if larger than maximum dimensions
      if (width > maxWidth || height > maxHeight) {
        if (width / maxWidth > height / maxHeight) {
          width = maxWidth
          height = width / aspectRatio
        } else {
          height = maxHeight
          width = height * aspectRatio
        }
      }

      // Scale up if smaller than minimum dimensions
      if (width < minWidth || height < minHeight) {
        if (width / minWidth < height / minHeight) {
          width = minWidth
          height = width / aspectRatio
        } else {
          height = minHeight
          width = height * aspectRatio
        }
      }

      return {
        width: Math.round(width),
        height: Math.round(height),
      }
    },

    updateMediaProperties(properties) {
      const actionType =
        properties.width !== undefined || properties.height !== undefined
          ? "resize"
          : "styleChange"
      const immediate = properties.finalChange === true

      if (properties.finalChange) {
        delete properties.finalChange
      }

      this.saveToHistory(actionType, immediate)

      if (!this.selectedElement?.id || this.selectedElement.type !== "media")
        return

      this.updateElement(this.selectedElement.id, properties)
    },

    updateTextProperties(properties) {
      let actionType = "styleChange"
      let immediate = false

      // Determine action type and whether it should be saved immediately
      if (properties.color !== undefined) {
        actionType = "colorChange"
        // When done typing/selecting a color, save immediately
        if (properties.finalChange === true) {
          immediate = true
          delete properties.finalChange
        }
      } else if (
        properties.fontWeight !== undefined ||
        properties.fontStyle !== undefined
      ) {
        actionType = "formatChange"
        immediate = true // Format changes should be immediate
      }

      this.saveToHistory(actionType, immediate)

      if (!this.selectedElement?.id || this.selectedElement.type !== "text")
        return

      this.updateElement(this.selectedElement.id, properties)
    },
    // In editorStore.js, update the addShapeElement method:

    addShapeElement(shapeType = "triangle") {
      this.saveToHistory("add")
      const id = `shape-${Date.now()}`
      const position = this.calculateElementPosition()

      const isArrow = shapeType === "arrow"
      const isLine = shapeType === "line"

      // Choose appropriate default settings
      let defaultSettings
      if (isArrow) {
        defaultSettings = this.defaultArrowSettings
      } else if (isLine) {
        defaultSettings = this.defaultLineSettings
      } else {
        defaultSettings = this.defaultShapeSettings
      }

      // Create new shape element with SVG content
      const shapeElement = {
        id,
        type: "shape",
        shapeType,
        svgContent: this.svgShapes[shapeType] || this.svgShapes.triangle,
        x: position.x,
        y: position.y,
        width: defaultSettings.width,
        height: defaultSettings.height,
        rotation: 0,
        backgroundColor: defaultSettings.backgroundColor,
        opacity: defaultSettings.opacity,
        isArrow: isArrow,
        isLine,
        svgProps: {
          fill: defaultSettings.backgroundColor,
          stroke: "None",
          strokeWidth: 0,
          strokeDasharray: "none",
        },
        locked: false,
      }

      this.elements.push(shapeElement)
      this.selectedElementIds = [id]
      this.selectedElementId = id
      this.selectedElementType = "shapes"
      this.selectedElement = shapeElement
      this.updateElementIndexMap()

      return id
    },

    // In the updateShapeElement method, modify the rect handling section:

    updateShapeElement(elementId, props = {}) {
      let actionType = "styleChange"
      if (props.backgroundColor !== undefined) {
        actionType = "colorChange"
      } else if (props.width !== undefined || props.height !== undefined) {
        actionType = "resize"
      }
      this.saveToHistory(actionType)
      const element = this.elements.find((el) => el.id === elementId)
      if (!element || element.type !== "shape") return

      let svgContent = element.svgContent
      let updates = { ...props }
      updates.svgProps = { ...element.svgProps }

      // Determine if the element is a circle, ellipse, rect, or path
      const isCircle = svgContent.includes("<circle")
      const isEllipse = svgContent.includes("<ellipse")
      const isRect = svgContent.includes("<rect")
      const isPath = svgContent.includes("<path")

      // Handle common attributes (fill, stroke, opacity)
      if (props.fill !== undefined) {
        svgContent = svgContent.replace(/fill="[^"]*"/, `fill="${props.fill}"`)
        updates.svgProps.fill = props.fill
      }

      if (props.stroke !== undefined) {
        if (svgContent.includes('stroke="')) {
          svgContent = svgContent.replace(
            /stroke="[^"]*"/,
            `stroke="${props.stroke}"`
          )
        } else {
          svgContent = svgContent.replace(
            /(<(?:rect|circle|ellipse|path)[^>]*?)(\/>|>)/,
            `$1 stroke="${props.stroke}"$2`
          )
        }
        updates.svgProps.stroke = props.stroke
      }

      if (props.strokeWidth !== undefined) {
        if (svgContent.includes('stroke-width="')) {
          svgContent = svgContent.replace(
            /stroke-width="[^"]*"/,
            `stroke-width="${props.strokeWidth}"`
          )
        } else {
          svgContent = svgContent.replace(
            /(<(?:rect|circle|ellipse|path)[^>]*?)(\/>|>)/,
            `$1 stroke-width="${props.strokeWidth}"$2`
          )
        }
        updates.svgProps.strokeWidth = props.strokeWidth
      }

      if (props.strokeDasharray !== undefined) {
        const dashValue =
          props.strokeDasharray === "solid" ? "" : props.strokeDasharray
        if (dashValue) {
          if (svgContent.includes('stroke-dasharray="')) {
            svgContent = svgContent.replace(
              /stroke-dasharray="[^"]*"/,
              `stroke-dasharray="${dashValue}"`
            )
          } else {
            svgContent = svgContent.replace(
              /(<(?:rect|circle|ellipse|path)[^>]*?)(\/>|>)/,
              `$1 stroke-dasharray="${dashValue}"$2`
            )
          }
        } else {
          svgContent = svgContent.replace(/\s*stroke-dasharray="[^"]*"/, "")
        }
        updates.svgProps.strokeDasharray = props.strokeDasharray
      }

      if (props.opacity !== undefined) {
        if (svgContent.includes('opacity="')) {
          svgContent = svgContent.replace(
            /opacity="[^"]*"/,
            `opacity="${props.opacity}"`
          )
        } else {
          svgContent = svgContent.replace(
            /(<(?:rect|circle|ellipse|path)[^>]*?)(\/>|>)/,
            `$1 opacity="${props.opacity}"$2`
          )
        }
        updates.svgProps.opacity = props.opacity
      }

      // Handle shape-specific attributes
      if (isRect) {
        // Improved handling of rx/ry attributes for rectangles
        if (props.rx !== undefined || props.ry !== undefined) {
          const rx =
            props.rx !== undefined ? props.rx : element.svgProps?.rx || 0
          const ry =
            props.ry !== undefined ? props.ry : element.svgProps?.ry || 0

          // Remove any existing rx/ry attributes
          svgContent = svgContent.replace(/\s*rx="[^"]*"/, "")
          svgContent = svgContent.replace(/\s*ry="[^"]*"/, "")

          // Add new rx/ry attributes before the closing tag
          svgContent = svgContent.replace(
            /(<rect[^>]*?)(\/>|>)/,
            `$1 rx="${rx}" ry="${ry}"$2`
          )

          updates.svgProps.rx = rx
          updates.svgProps.ry = ry
        }
      } else if (isCircle) {
        if (props.r !== undefined) {
          if (svgContent.includes('r="')) {
            svgContent = svgContent.replace(/r="[^"]*"/, `r="${props.r}"`)
          } else {
            svgContent = svgContent.replace(
              /(<circle[^>]*?)(\/>|>)/,
              `$1 r="${props.r}"$2`
            )
          }
          updates.svgProps.r = props.r
        }
      } else if (isEllipse) {
        if (props.rx !== undefined) {
          if (svgContent.includes('rx="')) {
            svgContent = svgContent.replace(/rx="[^"]*"/, `rx="${props.rx}"`)
          } else {
            svgContent = svgContent.replace(
              /(<ellipse[^>]*?)(\/>|>)/,
              `$1 rx="${props.rx}"$2`
            )
          }
          updates.svgProps.rx = props.rx
        }
        if (props.ry !== undefined) {
          if (svgContent.includes('ry="')) {
            svgContent = svgContent.replace(/ry="[^"]*"/, `ry="${props.ry}"`)
          } else {
            svgContent = svgContent.replace(
              /(<ellipse[^>]*?)(\/>|>)/,
              `$1 ry="${props.ry}"$2`
            )
          }
          updates.svgProps.ry = props.ry
        }
      }
      updates.svgContent = svgContent
      this.updateElement(elementId, updates)
    },
    // Add a method to add custom SVG content
    addCustomSvgElement(svgContent) {
      const id = `shape-${Date.now()}`
      const position = this.calculateElementPosition()

      const svgElement = {
        id,
        type: "shape",
        shapeType: "custom",
        svgContent,
        x: position.x,
        y: position.y,
        width: this.defaultShapeSettings.width,
        height: this.defaultShapeSettings.height,
        rotation: 0,
        backgroundColor: this.defaultShapeSettings.backgroundColor,
        opacity: this.defaultShapeSettings.opacity,
        locked: false,
      }

      this.elements.push(svgElement)
      this.selectedElementId = id
      this.selectedElementType = "shapes"
      this.selectedElement = svgElement
      return id
    },

    duplicateShape(id) {
      const shape = this.elements.find((el) => el.id === id)
      if (shape && shape.type === "shape") {
        const newShape = {
          ...shape,
          id: `shape-${Date.now()}`,
          x: shape.x + 20,
          y: shape.y + 20,
        }
        this.elements.push(newShape)
        this.selectedElementId = newShape.id
        this.selectedElement = newShape
        return newShape.id
      }
    },
    setCanvasDownloadFn(fn) {
      this.canvasDownloadFn = fn
    },
    downloadCanvas() {
      if (this.canvasDownloadFn) {
        this.canvasDownloadFn()
      }
    },
  },
  getters: {
    elementType: (state) => state.selectedElement?.type || null,
    shapeProperties: (state) => {
      if (!state.selectedElement || state.selectedElement.type !== "shape")
        return null

      return {
        // Fill properties
        fillType:
          state.selectedElement.svgProps?.fill === "transparent"
            ? "No Fill"
            : "Solid Color",
        fillColor: state.selectedElement.svgProps?.fill || "#3E57DA",

        // For line shapes, include backgroundColor property
        backgroundColor: state.selectedElement.backgroundColor || "#3E57DA",

        // Border properties
        borderType: !state.selectedElement.svgProps?.stroke
          ? "None"
          : state.selectedElement.svgProps?.strokeDasharray === "5,5"
          ? "Dashed"
          : "Solid",
        borderColor: state.selectedElement.svgProps?.stroke || "#3E57DA",
        borderThickness: state.selectedElement.svgProps?.strokeWidth || 1,
        shapeType: state.selectedElement.shapeType,

        // Rounded corners
        roundedCorners: state.selectedElement.svgProps?.rx || 0,

        // Opacity
        opacity: (state.selectedElement.opacity || 1) * 100,

        // Shadow properties
        hasShadow: state.selectedElement.hasShadow || false,
        shadowOffsetX: state.selectedElement.shadowOffsetX || 0,
        shadowOffsetY: state.selectedElement.shadowOffsetY || 0,
        shadowBlur: state.selectedElement.shadowBlur || 0,
        shadowColor: state.selectedElement.shadowColor || "#000000",

        // Shape type for rounded corners check
        isRoundedCornerSupported: [
          "rectangle",
          "square",
          "roundedSquare",
          "roundedRectangle",
        ].includes(state.selectedElement.shapeType),
      }
    },

    textProperties: (state) => {
      if (!state.selectedElement || state.selectedElement.type !== "text")
        return null

      const decorations = state.selectedElement.textDecoration?.split(" ") || []
      return {
        font: state.selectedElement.fontFamily || "Roboto",
        fontSize: state.selectedElement.fontSize || 120,
        letterSpacing: state.selectedElement.letterSpacing || "0px",
        lineHeight: state.selectedElement.lineHeight || 1,
        color: state.selectedElement.color || "#000000",
        opacity: state.selectedElement.opacity,
        textAlign: state.selectedElement.textAlign || "left",
        hasShadow: state.selectedElement.hasShadow || false,
        shadowOffsetX: state.selectedElement.shadowOffsetX || 0,
        shadowOffsetY: state.selectedElement.shadowOffsetY || 0,
        shadowBlur: state.selectedElement.shadowBlur || 1,
        shadowColor: state.selectedElement.shadowColor || "#000000",

        // Text styles
        isBold: state.selectedElement.fontWeight === "bold",
        isItalic: state.selectedElement.fontStyle === "italic",
        isUnderline: decorations.includes("underline"),
        isStrikethrough: decorations.includes("line-through"),
      }
    },
    graphicProperties: (state) => {
      if (!state.selectedElement || state.selectedElement.type !== "graphic")
        return null

      const svgContent = state.selectedElement.svgContent
      let strokeColor = "black"
      let fillColor = "black"

      // Check for stroke in SVG tag
      const svgStrokeMatch = svgContent?.match(
        /<svg[^>]*stroke="([^"]*)"[^>]*>/
      )
      if (svgStrokeMatch) {
        strokeColor = svgStrokeMatch[1] || "black"
      } else {
        // Check for stroke in child elements
        const strokeMatch = svgContent?.match(/stroke="([^"]*)"/)
        if (strokeMatch) {
          strokeColor = strokeMatch[1] || "black"
        }
      }

      // Check for fill in SVG tag
      const svgFillMatch = svgContent?.match(/<svg[^>]*fill="([^"]*)"[^>]*>/)
      if (svgFillMatch) {
        fillColor = svgFillMatch[1] || "black"
      } else {
        // Check for fill in child elements
        const fillMatch = svgContent?.match(/fill="([^"]*)"/)
        if (fillMatch) {
          fillColor = fillMatch[1] || "black"
        }
      }

      // Handle invalid colors for both stroke and fill
      if (
        !strokeColor ||
        strokeColor === "undefined" ||
        strokeColor === "null" ||
        strokeColor === "currentColor"
      ) {
        strokeColor = "#000000"
      }

      if (
        !fillColor ||
        fillColor === "undefined" ||
        fillColor === "null" ||
        fillColor === "currentColor"
      ) {
        fillColor = "#000000"
      }

      return {
        opacity: Math.round((state.selectedElement.opacity || 1) * 100),
        stroke: strokeColor,
        fill: fillColor,
      }
    },
    canSave: (state) => !state.isSaving && state.elements.length > 0,

    saveStatus: (state) => ({
      isSaving: state.isSaving,
      lastSavedId: state.lastSavedId,
      error: state.saveError,
    }),
  },
})
