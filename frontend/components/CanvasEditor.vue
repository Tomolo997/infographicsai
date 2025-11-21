<template>
  <div class="canvas-container">
    <div
      ref="canvasWrapper"
      class="canvas-wrapper"
      tabindex="0"
      @mousedown="handleMouseDown($event)"
      @mousemove="isRepositioningBackground ? null : handleMouseMove"
      @mouseup="isRepositioningBackground ? null : handleMouseUp"
      @wheel="handleWheel"
    >
      <div class="canvas-centering-wrapper" ref="canvasCenteringWrapper">
        <div
          class="canvas-grid"
          :style="{
            transform: `scale(${zoom})`,
            width: `${canvasWidth}px`,
            height: `${canvasHeight}px`,
          }"
        ></div>

        <div ref="canvas" class="canvas" :style="canvasStyle">
          <!-- Guide lines -->
          <div
            v-for="(guide, index) in guides"
            :key="index"
            class="guide-line"
            :class="{ 'canvas-edge': guide.isCanvasEdge }"
            :style="{
              position: 'absolute',
              pointerEvents: 'none',
              ...(guide.type === 'vertical'
                ? {
                    left: `${guide.position}px`,
                    top: `${guide.start}px`,
                    width: '1px',
                    height: `${guide.end - guide.start}px`,
                    transform: 'translateX(-0.5px)',
                  }
                : {
                    top: `${guide.position}px`,
                    left: `${guide.start}px`,
                    height: '1px',
                    width: `${guide.end - guide.start}px`,
                    transform: 'translateY(-0.5px)',
                  }),
            }"
          />

          <!-- Reposition Mode Indicator Overlay -->
          <div v-if="isRepositioningBackground" class="reposition-overlay">
            <div class="reposition-hint">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="24"
                height="24"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
                stroke-linecap="round"
                stroke-linejoin="round"
              >
                <circle cx="12" cy="12" r="10"></circle>
                <line x1="12" y1="8" x2="12" y2="16"></line>
                <line x1="8" y1="12" x2="16" y2="12"></line>
              </svg>
              <span>Drag to reposition background</span>
              <span v-if="bgScale > 1" class="scale-hint">
                Zoomed in ({{ Math.round(bgScale * 100) }}%)
              </span>
            </div>
          </div>

          <!-- Canvas Content - only visible when not repositioning -->
          <div
            class="canvas-content"
            :style="{ opacity: isRepositioningBackground ? 0.5 : 1 }"
          >
            <!-- Render all elements - your existing code -->
            <div
              v-for="element in store.elements"
              :key="element.id"
              class="canvas-element"
              :class="{ selected: selectedElementIndex === element.id }"
              :style="{
                position: 'absolute',
                left: `${element.x}px`,
                top: `${element.y}px`,
                width: `${element.width}px`,
                height: `${element.height}px`,
                transform: `rotate(${element.rotation || 0}deg)`,
                textAlign: element.textAlign,
                background: 'transparent',
                cursor: isDragging ? 'grabbing' : 'grab',
                pointerEvents: isRepositioningBackground ? 'none' : 'auto', // Disable interaction with elements during repositioning
              }"
              @mousedown.stop="
                isRepositioningBackground
                  ? null
                  : selectElement(element, $event)
              "
            >
              <!-- Your existing element components -->
              <TextElement
                v-if="element.type === 'text'"
                :element="element"
                :isDragging="isDragging"
                :draggedElementId="draggedElementId"
                :ref="`textElement-${element.id}`"
              />
              <ShapesElement
                v-else-if="element.type === 'shape'"
                :element="element"
                :isDragging="isDragging"
                :draggedElementId="draggedElementId"
                :ref="`shapeElement-${element.id}`"
              />
              <MediaElement
                v-else-if="element.type === 'media'"
                :element="element"
                :isDragging="isDragging"
                :draggedElementId="draggedElementId"
                :ref="`mediaElement-${element.id}`"
              />
              <IconElement
                v-else-if="element.type === 'graphic'"
                :element="element"
                :isDragging="isDragging"
                :draggedElementId="draggedElementId"
                :ref="`graphicElement-${element.id}`"
              />
            </div>
          </div>

          <!-- Background Repositioning Controls -->
          <div
            v-if="isRepositioningBackground"
            :style="repositionControlsStyle"
          >
            <button
              @click="scaleBackground('down')"
              class="control-btn"
              title="Zoom out"
              :disabled="bgScale <= 1"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="20"
                height="20"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
                stroke-linecap="round"
                stroke-linejoin="round"
              >
                <circle cx="11" cy="11" r="8"></circle>
                <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
                <line x1="8" y1="11" x2="14" y2="11"></line>
              </svg>
            </button>

            <div class="scale-display" :class="{ 'at-minimum': bgScale <= 1 }">
              {{ Math.round(bgScale * 100) }}%
            </div>

            <button
              @click="scaleBackground('up')"
              class="control-btn"
              title="Zoom in"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="20"
                height="20"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
                stroke-linecap="round"
                stroke-linejoin="round"
              >
                <circle cx="11" cy="11" r="8"></circle>
                <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
                <line x1="11" y1="8" x2="11" y2="14"></line>
                <line x1="8" y1="11" x2="14" y2="11"></line>
              </svg>
            </button>

            <button @click="applyBackgroundChanges" class="apply-btn">
              Done
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Bottom Controls Area -->
    <div class="bottom-controls">
      <!-- Background Repositioning Button - only show when a background image exists -->

      <!-- Your existing ZoomControls -->
      <ZoomControls
        :zoom="zoom"
        @zoom-in="zoomIn"
        @zoom-out="zoomOut"
        @reset-zoom="resetZoom"
        @update-zoom="setZoom"
      />
    </div>
  </div>
</template>

<script>
import { useEditorStore } from "@/stores/editorStore";
import TextElement from "./TextElement.vue";
import ZoomControls from "./ZoomControls.vue";
import domtoimage from "dom-to-image";
import apiClient, { setupCSRF } from "~/services/apiClient";
import { useToastStore } from "~/stores/toast";

export default {
  name: "CanvasEditor",
  components: {
    TextElement,
    ZoomControls,
  },

  setup() {
    const toastStore = useToastStore();
    const store = useEditorStore();
    return { store, toastStore };
  },

  data() {
    return {
      canPaste: true,
      zoom: 0.7,
      selectedElementIndex: null,
      isDragging: false,
      isResizing: false,
      draggedElementId: null,
      isShiftKeyPressed: false, // Add this to track shift key state
      elementStartPositions: {}, // For tracking multiple element positions during drag
      startX: 0,
      startY: 0,
      resizeHandles: [
        { position: "top-left" },
        { position: "top-right" },
        { position: "bottom-left" },
        { position: "bottom-right" },
      ],
      dragStartPos: { x: 0, y: 0 },
      elementStartPos: { x: 0, y: 0 },
      lastPasteTime: 0, // Add this instead of a boolean flag
      handlers: {
        keydown: null,
        keyup: null,
        zoomControls: null,
      },
      _rafId: null, // For requestAnimationFrame
      _centerCheckTimeout: null, // For debouncing center checks
      elementCache: new Map(), // For caching element references
      guides: [],
      SNAP_THRESHOLD: 4, // Distance in pixels for snapping
      isRepositioningBackground: false,
      bgPositionX: 50,
      bgPositionY: 50,
      bgScale: 1,
      bgDragStart: { x: 0, y: 0 },
      bgPositionStart: { x: 50, y: 50 },
      isDraggingBackground: false,
    };
  },

  props: {
    loading: {
      type: Boolean,
      default: false,
    },
  },

  computed: {
    selectedElements() {
      return this.store.selectedElementIds
        .map((id) => this.store.elements.find((el) => el.id === id))
        .filter(Boolean);
    },
    canvasWidth() {
      return this.store.canvasWidth;
    },
    canvasHeight() {
      return this.store.canvasHeight;
    },

    backgroundUrl() {
      if (this.store.backgroundImage) {
        return this.store.backgroundImage;
      }
      if (this.store.backgroundPatternUrl) {
        return this.store.backgroundPatternUrl;
      }
      return "none";
    },

    isMultiSelectActive() {
      return this.isShiftKeyPressed && this.store.selectedElementIds.length > 0;
    },
    // Replace your canvasStyle computed property with this:
    // Update your canvasStyle computed property:
    canvasStyle() {
      let style = {
        transform: `scale(${this.zoom})`,
        width: `${this.canvasWidth}px`,
        height: `${this.canvasHeight}px`,
        backgroundColor: `${this.store.backgroundPatternUrl ? 'transparent' : this.store.backgroundColorCanvas}`,
        backgroundRepeat: `${this.store.backgroundPatternUrl ? 'repeat' : 'no-repeat'}`,
        backgroundBlendMode: "normal",
        opacity: this.store.backgroundPatternSettings.opacity,
      };

      // Check if we have a background image
      if (this.backgroundUrl) {
        style.backgroundImage = `url(${this.backgroundUrl})`;

        // Use cover as base behavior, but allow zooming in (scale > 1)
        if (this.isRepositioningBackground) {
          // During repositioning mode
          style.backgroundSize =
            this.bgScale === 1 ? "cover" : `${this.bgScale * 100}%`;
          style.backgroundPosition = `${this.bgPositionX}% ${this.bgPositionY}%`;
          style.cursor = this.isDraggingBackground ? "grabbing" : "grab";
        } else {
          // During normal mode
          style.backgroundSize =
            this.store.backgroundImageSettings.scale === 1
              ? "cover"
              : `${this.store.backgroundImageSettings.scale * 100}%`;
          style.backgroundPosition =
            this.store.backgroundImageSettings.position === "custom"
              ? `${this.store.backgroundImageSettings.positionX} ${this.store.backgroundImageSettings.positionY}`
              : this.store.backgroundImageSettings.position;
        }
      } else if (this.store.backgroundPatternUrl) {
        // Pattern handling - fixed to properly handle repeating
        style.backgroundImage = `url(${this.store.backgroundPatternUrl})`;
        
        // Set appropriate background size and repeat based on pattern settings
        if (this.store.backgroundPatternSettings.size === "repeat") {
          style.backgroundSize = "auto"; // Use actual pattern size
          style.backgroundRepeat = "repeat"; // Enable repeating
          style.backgroundColor = 'transparent'; // Ensure transparent background
        } else if (this.store.backgroundPatternSettings.size === "contain") {
          style.backgroundSize = "contain";
          style.backgroundRepeat = "no-repeat";
        } else {
          // Default to cover
          style.backgroundSize = this.store.backgroundPatternSettings.size;
          style.backgroundRepeat = "no-repeat";
        }
        
        style.backgroundPosition = "center";
        // Apply opacity from pattern settings
        style.opacity = this.store.backgroundPatternSettings.opacity;
      }

      return style;
    },
    repositionControlsStyle() {
      return {
        position: "absolute",
        bottom: "20px",
        left: "50%",
        transform: "translateX(-50%)",
        display: "flex",
        alignItems: "center",
        gap: "12px",
        padding: "10px 15px",
        backgroundColor: "white",
        borderRadius: "8px",
        boxShadow: "0 2px 8px rgba(0, 0, 0, 0.15)",
        zIndex: 100,
      };
    },
  },

  methods: {
    toggleBackgroundRepositioning() {
      this.isRepositioningBackground = !this.isRepositioningBackground;

      if (this.isRepositioningBackground) {
        // Initialize with current values from store
        const settings = this.store.backgroundImageSettings;
        this.bgPositionX = parseFloat(settings.positionX) || 50;
        this.bgPositionY = parseFloat(settings.positionY) || 50;
        this.bgScale = settings.scale || 1;

        // Add event listeners for background dragging
        this.$refs.canvas.addEventListener(
          "mousedown",
          this.startBackgroundDrag
        );
        window.addEventListener("mousemove", this.dragBackground);
        window.addEventListener("mouseup", this.stopBackgroundDrag);

        // Deselect any selected elements when entering reposition mode
        this.store.clearSelection();
      } else {
        // Remove event listeners when exiting reposition mode
        this.$refs.canvas.removeEventListener(
          "mousedown",
          this.startBackgroundDrag
        );
        window.removeEventListener("mousemove", this.dragBackground);
        window.removeEventListener("mouseup", this.stopBackgroundDrag);
      }
    },

    // Start dragging the background
    startBackgroundDrag(event) {
      if (!this.isRepositioningBackground) return;

      // Prevent normal element selection when in reposition mode
      event.preventDefault();
      event.stopPropagation();

      this.isDraggingBackground = true;
      this.bgDragStart = {
        x: event.clientX,
        y: event.clientY,
      };
      this.bgPositionStart = {
        x: this.bgPositionX,
        y: this.bgPositionY,
      };
    },

    // Drag the background
    dragBackground(event) {
      if (!this.isDraggingBackground || !this.isRepositioningBackground) return;

      const canvas = this.$refs.canvas;
      if (!canvas) return;

      const rect = canvas.getBoundingClientRect();

      // Calculate the movement as percentage of canvas size
      // Note: We invert the calculation for intuitive movement
      const deltaXPercent =
        ((event.clientX - this.bgDragStart.x) / (rect.width * this.zoom)) * 100;
      const deltaYPercent =
        ((event.clientY - this.bgDragStart.y) / (rect.height * this.zoom)) *
        100;

      // Update position (inverted for intuitive dragging)
      this.bgPositionX = Math.max(
        0,
        Math.min(100, this.bgPositionStart.x - deltaXPercent)
      );
      this.bgPositionY = Math.max(
        0,
        Math.min(100, this.bgPositionStart.y - deltaYPercent)
      );
    },

    // Stop dragging the background
    stopBackgroundDrag() {
      this.isDraggingBackground = false;
    },

    // Scale background up/down
    scaleBackground(direction) {
      if (direction === "up") {
        // Zoom in (zoom level increases)
        this.bgScale = Math.min(3, this.bgScale + 0.1);
      } else {
        // Zoom out but never below 1.0 (100%) to maintain full coverage
        this.bgScale = Math.max(1.0, this.bgScale - 0.1);
      }
    },

    // Apply background changes
    applyBackgroundChanges() {
      // Save to store with all values
      this.store.repositionBackgroundImage(
        this.bgPositionX,
        this.bgPositionY,
        this.bgScale
      );

      // Exit reposition mode
      this.toggleBackgroundRepositioning();
    },

    // Add to your created or mounted lifecycle hook
    initializeBackgroundPosition() {
      if (this.store.backgroundImage) {
        const settings = this.store.backgroundImageSettings;
        this.bgPositionX = parseFloat(settings.positionX) || 50;
        this.bgPositionY = parseFloat(settings.positionY) || 50;
        // Ensure scale is never below 1.0
        this.bgScale = Math.max(1.0, settings.scale || 1.0);
      }
    },

    // Clean up event listeners
    cleanupBackgroundReposition() {
      this.$refs.canvas?.removeEventListener(
        "mousedown",
        this.startBackgroundDrag
      );
      window.removeEventListener("mousemove", this.dragBackground);
      window.removeEventListener("mouseup", this.stopBackgroundDrag);
    },
    checkAlignment(activeElement, newX, newY) {
      const newGuides = [];
      const SNAP_THRESHOLD = 8; // Slightly increased threshold

      // Calculate active element edges and center
      const active = {
        left: newX,
        right: newX + activeElement.width,
        top: newY,
        bottom: newY + activeElement.height,
        centerX: newX + activeElement.width / 2,
        centerY: newY + activeElement.height / 2,
      };

      // Track closest alignments
      let closestAlignment = {
        vertical: { distance: Infinity, guide: null },
        horizontal: { distance: Infinity, guide: null },
      };

      // Check alignment against canvas edges
      const canvasEdges = {
        left: 0,
        right: this.canvasWidth,
        top: 0,
        bottom: this.canvasHeight,
        centerX: this.canvasWidth / 2,
        centerY: this.canvasHeight / 2,
      };

      // Check vertical alignments with canvas edges (left, center, right)
      const canvasVerticalAlignments = [
        { type: "edge", pos: canvasEdges.left, activePos: active.left },
        { type: "edge", pos: canvasEdges.right, activePos: active.right },
        { type: "center", pos: canvasEdges.centerX, activePos: active.centerX },
      ];

      canvasVerticalAlignments.forEach(({ pos, activePos, type }) => {
        const distance = Math.abs(pos - activePos);
        if (
          distance < SNAP_THRESHOLD &&
          distance < closestAlignment.vertical.distance
        ) {
          closestAlignment.vertical = {
            distance,
            guide: {
              type: "vertical",
              position: pos,
              start: 0,
              end: this.canvasHeight,
              isCanvasEdge: true,
            },
          };
        }
      });

      // Check horizontal alignments with canvas edges (top, center, bottom)
      const canvasHorizontalAlignments = [
        { type: "edge", pos: canvasEdges.top, activePos: active.top },
        { type: "edge", pos: canvasEdges.bottom, activePos: active.bottom },
        { type: "center", pos: canvasEdges.centerY, activePos: active.centerY },
      ];

      canvasHorizontalAlignments.forEach(({ pos, activePos, type }) => {
        const distance = Math.abs(pos - activePos);
        if (
          distance < SNAP_THRESHOLD &&
          distance < closestAlignment.horizontal.distance
        ) {
          closestAlignment.horizontal = {
            distance,
            guide: {
              type: "horizontal",
              position: pos,
              start: 0,
              end: this.canvasWidth,
              isCanvasEdge: true,
            },
          };
        }
      });

      // Check alignment against all other elements
      this.store.elements.forEach((element) => {
        if (element.id === activeElement.id) return;

        const other = {
          left: element.x,
          right: element.x + element.width,
          top: element.y,
          bottom: element.y + element.height,
          centerX: element.x + element.width / 2,
          centerY: element.y + element.height / 2,
        };

        // Check vertical alignments (left, center, right)
        const verticalAlignments = [
          { type: "edge", pos: other.left, activePos: active.left },
          { type: "edge", pos: other.right, activePos: active.right },
          { type: "center", pos: other.centerX, activePos: active.centerX },
        ];

        verticalAlignments.forEach(({ pos, activePos, type }) => {
          const distance = Math.abs(pos - activePos);
          if (
            distance < SNAP_THRESHOLD &&
            distance < closestAlignment.vertical.distance
          ) {
            closestAlignment.vertical = {
              distance,
              guide: {
                type: "vertical",
                position: pos,
                start: Math.min(active.top, other.top),
                end: Math.max(active.bottom, other.bottom),
              },
            };
          }
        });

        // Check horizontal alignments (top, center, bottom)
        const horizontalAlignments = [
          { type: "edge", pos: other.top, activePos: active.top },
          { type: "edge", pos: other.bottom, activePos: active.bottom },
          { type: "center", pos: other.centerY, activePos: active.centerY },
        ];

        horizontalAlignments.forEach(({ pos, activePos, type }) => {
          const distance = Math.abs(pos - activePos);
          if (
            distance < SNAP_THRESHOLD &&
            distance < closestAlignment.horizontal.distance
          ) {
            closestAlignment.horizontal = {
              distance,
              guide: {
                type: "horizontal",
                position: pos,
                start: Math.min(active.left, other.left),
                end: Math.max(active.right, other.right),
              },
            };
          }
        });
      });

      // Only add the closest guides
      if (closestAlignment.vertical.guide) {
        newGuides.push(closestAlignment.vertical.guide);
      }
      if (closestAlignment.horizontal.guide) {
        newGuides.push(closestAlignment.horizontal.guide);
      }

      this.guides = newGuides;
      return newGuides;
    },
    snapToGuides(element, newX, newY) {
      let snappedX = newX;
      let snappedY = newY;

      this.guides.forEach((guide) => {
        if (guide.type === "vertical") {
          const elementCenterX = newX + element.width / 2;
          if (Math.abs(guide.position - elementCenterX) < this.SNAP_THRESHOLD) {
            snappedX = guide.position - element.width / 2;
          }
          if (Math.abs(guide.position - newX) < this.SNAP_THRESHOLD) {
            snappedX = guide.position;
          }
          if (
            Math.abs(guide.position - (newX + element.width)) <
            this.SNAP_THRESHOLD
          ) {
            snappedX = guide.position - element.width;
          }
        } else {
          const elementCenterY = newY + element.height / 2;
          if (Math.abs(guide.position - elementCenterY) < this.SNAP_THRESHOLD) {
            snappedY = guide.position - element.height / 2;
          }
          if (Math.abs(guide.position - newY) < this.SNAP_THRESHOLD) {
            snappedY = guide.position;
          }
          if (
            Math.abs(guide.position - (newY + element.height)) <
            this.SNAP_THRESHOLD
          ) {
            snappedY = guide.position - element.height;
          }
        }
      });

      return { x: snappedX, y: snappedY };
    },

    // In CanvasEditor.vue, update the downloadCanvas method:
    async downloadCanvas(format = "png") {
      try {
        // First, check if download is allowed
        await setupCSRF();
        const response = await apiClient.post(`/infos/download/`);
        if (response.status !== 200) {
          throw new Error(
            response.error.message || "Failed to process download"
          );
        }

        await this.$nextTick();
        await new Promise((resolve) => setTimeout(resolve, 300));

        const element = this.$refs.canvas;

        // Create hidden container
        const hiddenContainer = document.createElement("div");
        Object.assign(hiddenContainer.style, {
          position: "fixed",
          left: "-99999px",
          top: "-99999px",
          width: this.store.canvasWidth,
          height: this.store.canvasHeight,
          overflow: "hidden",
          opacity: "0",
          pointerEvents: "none",
          zIndex: "-9999",
        });

        // Clone the canvas
        const clonedCanvas = element.cloneNode(true);
        Object.assign(clonedCanvas.style, {
          position: "absolute",
          width: this.store.canvasWidth,
          height: this.store.canvasHeight,
          transform: "none",
        });

        // Clean up UI elements from clone
        clonedCanvas
          .querySelectorAll(".resize-handle, .rotate-handle")
          .forEach((el) => el.remove());

        // Add clone to hidden container
        hiddenContainer.appendChild(clonedCanvas);
        document.body.appendChild(hiddenContainer);

        let dataUrl;
        // Handle different formats
        switch (format.toLowerCase()) {
          case "png":
            dataUrl = await domtoimage.toPng(clonedCanvas, {
              width: this.store.canvasWidth,
              height: this.store.canvasHeight,
              style: {
                transform: "none",
              },
            });
            break;
          case "jpeg":
          case "jpg":
            dataUrl = await domtoimage.toJpeg(clonedCanvas, {
              width: this.store.canvasWidth,
              height: this.store.canvasHeight,
              style: {
                transform: "none",
              },
              quality: 0.95,
            });
            break;
          case "webp":
            // For WebP, we'll first get a PNG then convert it to WebP
            const pngUrl = await domtoimage.toPng(clonedCanvas, {
              width: this.store.canvasWidth,
              height: this.store.canvasHeight,
              style: {
                transform: "none",
              },
            });

            // Create a temporary image to load the PNG
            const img = new Image();
            await new Promise((resolve, reject) => {
              img.onload = resolve;
              img.onerror = reject;
              img.src = pngUrl;
            });

            // Create a temporary canvas to convert to WebP
            const tempCanvas = document.createElement("canvas");
            tempCanvas.width = this.store.canvasWidth;
            tempCanvas.height = this.store.canvasHeight;
            const ctx = tempCanvas.getContext("2d");
            ctx.drawImage(img, 0, 0);

            // Convert to WebP
            dataUrl = tempCanvas.toDataURL("image/webp", 0.95);
            break;
          default:
            throw new Error("Unsupported format");
        }

        // Download
        const link = document.createElement("a");
        link.href = dataUrl;
        link.download = `${
          this.store.templateName || "my-design"
        }.${format.toLowerCase()}`;
        document.body.appendChild(link);
        link.click();

        // Cleanup
        link.remove();
        hiddenContainer.remove();

        this.toastStore.success(response.data?.message);
      } catch (error) {
        this.toastStore.error("Failed to download infographic, try again");
        throw error; // Re-throw to be caught by the component
      }
    },
    // Fallback method using canvas API if dom-to-image fails
    async fallbackCapture(element) {
      const canvas = document.createElement("canvas");
      const ctx = canvas.getContext("2d");
      const scale = window.devicePixelRatio;

      canvas.width = element.offsetWidth * scale;
      canvas.height = element.offsetHeight * scale;

      // Scale for higher resolution
      ctx.scale(scale, scale);

      // Draw background
      ctx.fillStyle = this.store.backgroundColorCanvas || "#ffffff";
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      // Convert SVGs to images and draw content
      const svgElements = element.querySelectorAll("svg");
      await Promise.all(
        Array.from(svgElements).map(async (svg) => {
          const svgData = new XMLSerializer().serializeToString(svg);
          const img = new Image();
          img.src = "data:image/svg+xml;base64," + btoa(svgData);
          await new Promise((resolve) => (img.onload = resolve));
          const rect = svg.getBoundingClientRect();
          ctx.drawImage(img, rect.left, rect.top, rect.width, rect.height);
        })
      );

      return canvas.toDataURL("image/png", 1.0);
    },
    // Modified selection method
    selectElement(element, event) {
      // Check if element is being edited (for text elements)
      const textElement = this.$refs[`textElement-${element.id}`]?.[0];
      if (textElement?.isEditing) {
        return;
      }

      const shapeElement = this.$refs[`shapeElement-${element.id}`]?.[0];
      if (shapeElement?.isEditing) {
        return;
      }

      // Select the element in the store
      if (event.shiftKey) {
        // Multi-select logic with shift key
        if (this.store.selectedElementIds.includes(element.id)) {
          // If already selected, remove from selection
          const newSelectedIds = this.store.selectedElementIds.filter(
            (id) => id !== element.id
          );
          this.store.selectedElementIds = newSelectedIds;
          if (newSelectedIds.length > 0) {
            const lastSelected = this.store.elements.find(
              (el) => el.id === newSelectedIds[newSelectedIds.length - 1]
            );
            this.store.selectedElementId = lastSelected.id;
            this.store.selectedElement = lastSelected;
          } else {
            this.store.selectedElementId = null;
            this.store.selectedElement = {};
          }
        } else {
          // Add to selection
          this.store.selectedElementIds.push(element.id);
          this.store.selectedElementId = element.id;
          this.store.selectedElement = element;
        }
      } else {
        // Single select logic without shift key
        if (!this.store.selectedElementIds.includes(element.id)) {
          this.store.selectedElementIds = [element.id];
          this.store.selectedElementId = element.id;
          this.store.selectedElement = element;
        }
      }

      // Start drag if appropriate (element is not locked)
      if (element.id !== null && !element.locked) {
        this.startDrag(event);
      }
    },

    // Dragging methods
    drag(event) {
      if (!this.isDragging) return;

      const dx = (event.clientX - this.dragStartPos.x) / this.zoom;
      const dy = (event.clientY - this.dragStartPos.y) / this.zoom;

      // Move all selected elements
      Object.keys(this.elementStartPositions).forEach((id) => {
        const startPos = this.elementStartPositions[id];
        if (!startPos) return;

        const newX = startPos.x + dx;
        const newY = startPos.y + dy;

        this.store.updateElement(id, {
          x: newX,
          y: newY,
        });
      });
    },

    stopDrag() {
      this.isDragging = false;
      this.draggedElementId = null;
      document.removeEventListener("mousemove", this.drag);
      document.removeEventListener("mouseup", this.stopDrag);
      this.elementStartPositions = {};
    },

    // Also update your startDrag method to check if the drag starts within canvas bounds
    startDrag(event) {
      if (!this.store.selectedElementIds.length) return;

      // Check if target is a handle or in editing mode
      if (
        event.target.closest(".resize-handle") ||
        event.target.closest(".rotate-handle")
      ) {
        return;
      }

      // Store initial positions for all selected elements
      this.elementStartPositions = {};
      this.store.selectedElementIds.forEach((id) => {
        const element = this.store.elements.find((el) => el.id === id);
        if (element) {
          this.elementStartPositions[id] = {
            x: element.x,
            y: element.y,
          };
        }
      });

      this.isDragging = true;
      this.draggedElementId = this.store.selectedElementId;
      this.dragStartPos = {
        x: event.clientX,
        y: event.clientY,
      };

      document.addEventListener("mousemove", this.drag);
      document.addEventListener("mouseup", this.stopDrag);
    },

    // Add a method to handle mouse leaving the canvas
    handleMouseLeave() {
      if (this.isDragging) {
        this.stopDrag();
      }
    },

    // Resize methods
    startResize(position, event) {
      if (this.selectedElementIndex === null) return;

      this.isResizing = true;
      this.resizeStartPos = {
        x: event.clientX,
        y: event.clientY,
      };

      const element = this.elements[this.selectedElementIndex];
      this.elementStartSize = {
        width: element.width,
        height: element.height,
      };

      document.addEventListener("mousemove", this.resize);
      document.addEventListener("mouseup", this.stopResize);
    },
    handleWheel(event) {
      if (event.ctrlKey) {
        event.preventDefault();
        this.handleZoom(event);
      }
      // Otherwise let natural scrolling happen
    },

    resize(event) {
      if (!this.isResizing || this.selectedElementIndex === null) return;

      const dx = (event.clientX - this.resizeStartPos.x) / this.zoom;
      const dy = (event.clientY - this.resizeStartPos.y) / this.zoom;

      const element = this.elements[this.selectedElementIndex];
      element.width = Math.max(20, this.elementStartSize.width + dx);
      element.height = Math.max(20, this.elementStartSize.height + dy);
    },

    stopResize() {
      this.isResizing = false;
      document.removeEventListener("mousemove", this.resize);
      document.removeEventListener("mouseup", this.stopResize);
    },

    // Zoom methods
    handleZoom(event) {
      if (!event.ctrlKey) return;

      // Get the wrapper element and its scroll position
      const wrapper = this.$refs.canvasWrapper;
      const rect = wrapper.getBoundingClientRect();

      // Calculate mouse position relative to the wrapper
      const mouseX = event.clientX - rect.left;
      const mouseY = event.clientY - rect.top;

      // Calculate the scroll position as a percentage
      const scrollXPercent =
        (wrapper.scrollLeft + mouseX) / wrapper.scrollWidth;
      const scrollYPercent =
        (wrapper.scrollTop + mouseY) / wrapper.scrollHeight;

      // Update zoom
      const delta = event.deltaY;
      const zoomSpeed = 0.005;
      const newZoom = Math.min(Math.max(0.1, this.zoom - delta * zoomSpeed), 3);
      this.zoom = newZoom;

      // Wait for DOM update
      this.$nextTick(() => {
        // Calculate and set new scroll position
        wrapper.scrollLeft = scrollXPercent * wrapper.scrollWidth - mouseX;
        wrapper.scrollTop = scrollYPercent * wrapper.scrollHeight - mouseY;
      });
    },

    setZoom(newZoom) {
      this.zoom = Math.min(Math.max(0.1, newZoom), 3);
    },

    zoomIn() {
      this.setZoom(this.zoom + 0.1);
    },

    zoomOut() {
      this.setZoom(this.zoom - 0.1);
    },

    resetZoom() {
      this.zoom = 1;
    },
    // Add to methods in CanvasEditor.vue
    deselectAllElements() {
      // Skip if in repositioning mode
      if (this.isRepositioningBackground) return;

      this.store.selectedElementIds.forEach((id) => {
        // Call deselect on all element types
        const textElement = this.$refs[`textElement-${id}`]?.[0];
        const shapeElement = this.$refs[`shapeElement-${id}`]?.[0];
        const mediaElement = this.$refs[`mediaElement-${id}`]?.[0];
        const iconElement = this.$refs[`graphicElement-${id}`]?.[0];

        // Call deselect on whichever element exists
        textElement?.deselect();
        shapeElement?.deselect();
        mediaElement?.deselect();
        iconElement?.deselect();
      });

      // Clear selection in store
      this.store.clearSelection();

      // Clear guides
      this.guides = [];
    },
    handleMouseDown(event) {
      if (
        event.target === this.$refs.canvas ||
        event.target === this.$refs.canvasCenteringWrapper ||
        // Check for any click on the empty parts of the canvas area
        (this.$refs.canvasWrapper && event.target === this.$refs.canvasWrapper)
      ) {
        // If clicking directly on canvas (not on an element)
        this.deselectAllElements();
      }
    },
    // Mouse event handlers
    handleMouseMove(event) {
      if (!this.isDragging || !this.draggedElementId) return;

      const element = this.elements.find(
        (el) => el.id === this.draggedElementId
      );
      if (!element) return;

      // Calculate new position
      let newX = (event.clientX - this.dragOffset.x) / this.zoom;
      let newY = (event.clientY - this.dragOffset.y) / this.zoom;

      // Check alignment and get guides
      this.checkAlignment(element, newX, newY);

      // Snap to guides if close enough
      const snapped = this.snapToGuides(element, newX, newY);
      newX = snapped.x;
      newY = snapped.y;

      // Update element position
      this.updateElement(this.draggedElementId, {
        x: newX,
        y: newY,
      });
    },

    handleMouseMove(event) {
      // Handle general mouse movement
    },

    // In CanvasEditor.vue, add new method:
    async generatePreviewImage() {
      try {
        await this.$nextTick();
        await new Promise((resolve) => setTimeout(resolve, 300));

        const element = this.$refs.canvas;

        // Calculate preview dimensions (300px width)
        const PREVIEW_WIDTH = 300;
        const aspectRatio = this.store.canvasHeight / this.store.canvasWidth;
        const PREVIEW_HEIGHT = Math.round(PREVIEW_WIDTH * aspectRatio);

        // Create hidden container
        const hiddenContainer = document.createElement("div");
        Object.assign(hiddenContainer.style, {
          position: "fixed",
          left: "-99999px",
          top: "-99999px",
          width: `${this.store.canvasWidth}px`,
          height: `${this.store.canvasHeight}px`,
          overflow: "hidden",
          opacity: "0",
          pointerEvents: "none",
          zIndex: "-9999",
        });

        // Clone the canvas
        const clonedCanvas = element.cloneNode(true);
        Object.assign(clonedCanvas.style, {
          position: "absolute",
          width: `${this.store.canvasWidth}px`,
          height: `${this.store.canvasHeight}px`,
          transform: "none",
        });

        // Clean up UI elements from clone
        clonedCanvas
          .querySelectorAll(".resize-handle, .rotate-handle")
          .forEach((el) => el.remove());

        // Add clone to hidden container
        hiddenContainer.appendChild(clonedCanvas);
        document.body.appendChild(hiddenContainer);

        // Capture full-size image first
        const fullSizeDataUrl = await domtoimage.toPng(clonedCanvas, {
          width: this.store.canvasWidth,
          height: this.store.canvasHeight,
          style: {
            transform: "none",
          },
        });

        // Create a canvas to resize the image
        const canvas = document.createElement("canvas");
        canvas.width = PREVIEW_WIDTH;
        canvas.height = PREVIEW_HEIGHT;
        const ctx = canvas.getContext("2d");

        // Create an image from the full-size capture
        const img = new Image();
        await new Promise((resolve, reject) => {
          img.onload = resolve;
          img.onerror = reject;
          img.src = fullSizeDataUrl;
        });

        // Draw and scale down the image
        ctx.drawImage(img, 0, 0, PREVIEW_WIDTH, PREVIEW_HEIGHT);

        // Get the scaled-down image data
        const previewDataUrl = canvas.toDataURL("image/png", 0.8);

        // Convert to blob
        const response = await fetch(previewDataUrl);
        const blob = await response.blob();

        // Cleanup
        hiddenContainer.remove();

        return blob;
      } catch (error) {
        console.error("Error generating preview image:", error.message);
        throw error;
      }
    },

    // Add method to handle save with preview
    // async handleSave() {
    //   try {
    //     const previewBlob = await this.generatePreviewImage();
    //     await this.store.saveInfographic(previewBlob);
    //   } catch (error) {
    //     console.error("Error saving:", error);
    //   }
    // },

    handleMouseUp() {
      this.isDragging = false;
      this.isResizing = false;
    },
    handleKeyUp(event) {
      if (event.key === "v" || event.ctrlKey || event.metaKey) {
        this.isPasting = false;
      }
      if (event.key === "Shift") {
        event.preventDefault();
        this.isShiftKeyPressed = false;
      }
    },
    // Update the handleKeyDown method in CanvasEditor.vue
    // In your handleKeyDown method in CanvasEditor.vue
    async handleKeyDown(event) {
      if (!this.$refs.canvasWrapper?.contains(event.target)) {
        return;
      }

      // Skip handling if the event is coming from a textarea or input
      if (event.target.matches("textarea, input")) {
        // Only handle global shortcuts like zoom, but let the textarea handle text operations
        const isModifierKey = event.ctrlKey || event.metaKey;
        if (isModifierKey) {
          // Still handle zoom shortcuts
          if (event.ctrlKey) {
            if (event.key === "=" || event.key === "+") {
              event.preventDefault();
              this.zoomIn();
            } else if (event.key === "-") {
              event.preventDefault();
              this.zoomOut();
            } else if (event.key === "0") {
              event.preventDefault();
              this.resetZoom();
            }
          }
        }
        return;
      }

      if (event.key === "Shift") {
        event.preventDefault();
        this.isShiftKeyPressed = true;
      }

      // Handle deletion
      if (
        (event.key === "Delete" || event.key === "Backspace") &&
        this.store.selectedElementIds.length > 0
      ) {
        // Don't delete if target is an input or editing is in progress
        if (event.target.matches("input, textarea")) {
          return;
        }

        // Check if any selected element is being edited
        const isAnyEditing = this.store.selectedElementIds.some((id) => {
          return this.$refs[`textElement-${id}`]?.[0]?.isEditing;
        });

        if (isAnyEditing) return;

        event.preventDefault();
        // Delete all selected elements
        this.store.selectedElementIds.forEach((id) => {
          this.store.deleteElement(id);
        });
        this.selectedElementIndex = null;
        return;
      }

      const isModifierKey = event.ctrlKey || event.metaKey;
      if (isModifierKey) {
        if (event.key === "z") {
          event.preventDefault();
          if (event.shiftKey) {
            this.store.redo();
          } else {
            this.store.undo();
          }
          return;
        }

        // Handle copy (Ctrl+C)
        if (event.key === "c") {
          if (this.store.selectedElementIds.length > 0) {
            event.preventDefault();
            // Pass all selected IDs to copyElement
            this.store.copyElement(this.store.selectedElementIds);
          }
        }

        // Handle paste (Ctrl+V)
        if (event.key === "v") {
          if (this.store.copiedElement) {
            event.preventDefault();
            await this.store.pasteElement();
          }
        }

        // Handle zoom shortcuts
        if (event.ctrlKey) {
          if (event.key === "=" || event.key === "+") {
            event.preventDefault();
            this.zoomIn();
          } else if (event.key === "-") {
            event.preventDefault();
            this.zoomOut();
          } else if (event.key === "0") {
            event.preventDefault();
            this.resetZoom();
          }
        }
      }
    },
  },

  mounted() {
    // Keep only these
    this.handlers.keydown = this.handleKeyDown.bind(this);
    this.handlers.keyup = this.handleKeyUp.bind(this);
    window.addEventListener("keydown", this.handlers.keydown);
    window.addEventListener("keyup", this.handlers.keyup);
    this.initializeBackgroundPosition();
  },

  beforeDestroy() {
    // Remove both listeners
    window.removeEventListener("keydown", this.handleKeyDown);
    window.removeEventListener("keyup", this.handleKeyUp);
    this.cleanupBackgroundReposition();
  },
  beforeUnmount() {
    if (this._rafId) {
      cancelAnimationFrame(this._rafId);
    }
    if (this._centerCheckTimeout) {
      clearTimeout(this._centerCheckTimeout);
    }
    this.elementCache.clear();
    this.cleanupBackgroundReposition();
  },
};
</script>

<style scoped>
.canvas-container {
  width: calc(100% - 320px);
  height: 100%;
  position: relative;
  overflow: hidden; /* Add this */
}
.canvas-wrapper {
  position: relative; /* Change from sticky to relative */
  width: 100%;
  height: calc(100vh - 80px);
  overflow: auto;
  padding: 20px;
  outline: none; /* Remove default focus outline */
}

.canvas-centering-wrapper {
  position: relative;
  min-width: min-content;
  min-height: max-content;
  margin: 0 auto;
  display: flex;
  justify-content: center;
  align-items: center; /* Add this */
  padding: 50px;
}
.canvas {
  position: relative;
  background-color: white;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  transform-origin: top center;
  overflow: hidden;
}
.canvas-grid {
  position: absolute;
  background-image: linear-gradient(rgba(0, 0, 0, 0.1) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0, 0, 0, 0.1) 1px, transparent 1px);
  background-size: 20px 20px;
  pointer-events: auto;
  transform-origin: top center;
}

.canvas-element {
  position: absolute;
  user-select: none;
  pointer-events: auto;
  will-change: transform;
  transform-style: preserve-3d;
}

.resize-handle {
  position: absolute;
  width: 8px;
  height: 8px;
  background-color: white;
  border: 1px solid #4a90e2;
  pointer-events: all;
}

.resize-handle.top-left {
  top: -4px;
  left: -4px;
  cursor: nw-resize;
}
.resize-handle.top-right {
  top: -4px;
  right: -4px;
  cursor: ne-resize;
}
.resize-handle.bottom-left {
  bottom: -4px;
  left: -4px;
  cursor: sw-resize;
}
.resize-handle.bottom-right {
  bottom: -4px;
  right: -4px;
  cursor: se-resize;
}

.text-element {
  width: 100%;
  height: 100%;
  padding: 4px;
  cursor: text;
  white-space: pre-wrap;
}

/* Zoom controls styles */
.zoom-controls {
  position: absolute;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.zoom-btn {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  background-color: white;
  color: #666;
  cursor: pointer;
  transition: all 0.2s ease;
}

.zoom-btn:hover:not(:disabled) {
  background-color: #f5f5f5;
}

.zoom-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.zoom-display {
  min-width: 60px;
  text-align: center;
  font-size: 14px;
  color: #666;
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 4px;
}

.zoom-display:hover {
  background-color: #f5f5f5;
}
.text-element {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  user-select: none;
  cursor: text;
  padding: 4px;
  box-sizing: border-box;
}

.add-text-btn {
  position: absolute;
  top: 20px;
  left: 20px;
  padding: 8px 16px;
  background-color: #4a90e2;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.add-text-btn:hover {
  background-color: #357abd;
}
.export-canvas {
  position: absolute !important;
  transform: none !important;
  width: 600px !important;
  height: 1200px !important;
  left: 0 !important;
  top: 0 !important;
  margin: 0 !important;
  padding: 0 !important;
}
.guide-line {
  background-color: transparent;
  border: 1px dashed #4a90e2;
  pointer-events: none;
  position: absolute;
  z-index: 1000;
}

.guide-line.canvas-edge {
  border: 1.5px dashed #e24a4a;
  opacity: 0.8;
}

.reposition-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10;
}

.reposition-hint {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 20px;
  background-color: rgba(0, 0, 0, 0.6);
  color: white;
  border-radius: 8px;
  font-size: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.bottom-controls {
  position: absolute;
  bottom: 20px;
  left: 0;
  right: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 16px;
  z-index: 10;
}

.bg-reposition-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 14px;
  background-color: white;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  color: #333;
  cursor: pointer;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
  transition: all 0.2s ease;
}

.bg-reposition-btn:hover {
  background-color: #f5f5f5;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

.control-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border: 1px solid #ddd;
  border-radius: 4px;
  background-color: white;
  color: #555;
  cursor: pointer;
  transition: background-color 0.2s;
}

.control-btn:hover {
  background-color: #f0f0f0;
}

.scale-display {
  min-width: 50px;
  text-align: center;
  font-size: 14px;
  color: #333;
}

.apply-btn {
  padding: 8px 16px;
  background-color: #3b82f6;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s;
}

.apply-btn:hover {
  background-color: #2563eb;
}

/* Modify canvas styles during repositioning */
.canvas-wrapper:focus-visible {
  outline: none;
}

.canvas.repositioning {
  cursor: grab;
}

.canvas.repositioning:active {
  cursor: grabbing;
}
.scale-hint {
  font-size: 0.9em;
  opacity: 0.8;
  margin-left: 4px;
  background-color: rgba(0, 0, 0, 0.3);
  padding: 2px 6px;
  border-radius: 4px;
}
.at-minimum {
  color: #999;
}

.control-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}
</style>