<!-- IconElement.vue -->
<template>
  <div
    class="icon-element"
    :class="elementClasses"
    :style="{
      cursor: element.locked ? 'default' : (isResizing ? 'se-resize' : isDragging ? 'grabbing' : 'grab'),
      opacity: element.opacity,
      transform: `scale(${element.scaleX || 1}, ${element.scaleY || 1})`,
    }"
    @mousedown.stop="handleMouseDown"
  >
    <div class="icon-wrapper">
      <!-- Use img tag for external SVGs -->
      <img
        v-if="element.svgType === 'external' && element.src"
        class="w-full h-full"
        :src="element.src"
        :style="{
          color: element.currentColor,
          pointerEvents: 'none' /* Allow mouse events to pass through to parent */
        }"
        alt="Icon"
      />
      <!-- Use inline SVG content when available -->
      <div
        v-else
        class="w-full h-full"
        :style="{
          color: element.currentColor,
        }"
        v-html="element.svgContent"
      ></div>
    </div>

    <!-- Lock icon when element is locked -->
    <div 
      v-if="element.locked && isElementSelected" 
      class="lock-icon"
      style="position: absolute; top: -10px; right: -10px; width: 25px; height: 25px; background-color: white; border-radius: 50%; display: flex; justify-content: center; align-items: center; box-shadow: 0 2px 4px rgba(0,0,0,0.2); z-index: 10;"
    >
      <svg width="20" height="20" viewBox="0 0 24 24">
        <path
           fill="#9E9E9E"
          d="M12 17a2 2 0 0 0 2-2a2 2 0 0 0-2-2a2 2 0 0 0-2 2a2 2 0 0 0 2 2m6-9a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V10a2 2 0 0 1 2-2h1V6a5 5 0 0 1 5-5a5 5 0 0 1 5 5v2h1m-6-5a3 3 0 0 0-3 3v2h6V6a3 3 0 0 0-3-3Z"
        />
      </svg>
    </div>

    <!-- Show handles only when selected and not locked -->
    <template v-if="(isElementSelected || isResizing || isRotating) && !element.locked">
      <!-- Resize Handles -->
      <div
        v-for="handle in resizeHandles"
        :key="handle.position"
        class="resize-handle"
        :class="handle.position"
        :style="{ cursor: getHandleCursor(handle.position) }"
        @mousedown.stop="startResize($event, handle.position)"
      ></div>

      <!-- Rotation Handle -->
      <div class="rotate-handle" @mousedown.stop="startRotate">
        <svg width="16" height="16" viewBox="0 0 24 24">
          <path
            fill="currentColor"
            d="M12,5V1L7,6L12,11V7A6,6 0 0,1 18,13A6,6 0 0,1 12,19A6,6 0 0,1 6,13H4A8,8 0 0,0 12,21A8,8 0 0,0 20,13A8,8 0 0,0 12,5Z"
          />
        </svg>
      </div>
    </template>
  </div>
</template>

<script>
import { useEditorStore } from "@/stores/editorStore";

export default {
  name: "IconElement",

  props: {
    element: {
      type: Object,
      required: true,
    },
    draggedElementId: {
      type: [String, Number, null],
      default: null,
    },
  },

  data() {
    return {
      store: useEditorStore(),
      isResizing: false,
      isRotating: false,
      isDragging: false,
      startX: 0,
      startY: 0,
      startWidth: 0,
      startHeight: 0,
      startRotation: 0,
      resizeDirection: null,
      dragStartPos: { x: 0, y: 0 },
      elementStartPos: { x: 0, y: 0 },
      resizeHandles: [
        { position: "top-left" },
        { position: "top-right" },
        { position: "bottom-right" },
        { position: "bottom-left" },
      ],
      aspectRatio: 1,
      initialRotation: 0,
      startAngle: 0,
      lastAngle: 0,
      // Add new state tracking
      dragStartState: null,
      resizeStartState: null,
      rotateStartState: null,
    };
  },

  computed: {
    isElementSelected() {
      return this.store.selectedElementIds.includes(this.element.id);
    },

    elementClasses() {
      return {
        "center-snapped-x": this.isCentered.x && this.isThisElementDragging,
        "center-snapped-y": this.isCentered.y && this.isThisElementDragging,
        selected: this.isElementSelected || this.isResizing || this.isRotating,
      };
    },

    isThisElementDragging() {
      return this.isDragging && this.draggedElementId === this.element.id;
    },

    isCentered() {
      const canvasWidth = 600;
      const canvasHeight = 1200;
      const elementCenterX = this.element.x + this.element.width / 2;
      const elementCenterY = this.element.y + this.element.height / 2;
      const canvasCenterX = canvasWidth / 2;
      const canvasCenterY = canvasHeight / 2;

      return {
        x: Math.abs(elementCenterX - canvasCenterX) < 5,
        y: Math.abs(elementCenterY - canvasCenterY) < 5,
      };
    },

    resizeHandleCursors() {
      const rotation = (((this.element.rotation || 0) % 360) + 360) % 360;
      const quadrant = Math.floor((rotation + 45) / 90) % 4;
      const cursors = ["nw-resize", "ne-resize", "se-resize", "sw-resize"];

      return {
        "top-left": cursors[(0 + quadrant) % 4],
        "top-right": cursors[(1 + quadrant) % 4],
        "bottom-right": cursors[(2 + quadrant) % 4],
        "bottom-left": cursors[(3 + quadrant) % 4],
        top: "ns-resize",
        right: "ew-resize",
        bottom: "ns-resize",
        left: "ew-resize",
      };
    },
  },

  methods: {
    handleMouseDown(event) {
      if (
        event.target.closest(".resize-handle") ||
        event.target.closest(".rotate-handle") ||
        this.isResizing ||
        this.isRotating
      ) {
        return;
      }

      this.select();

      // Start drag only if the element is not locked
      if (this.element.id !== null && !this.element.locked) {
        this.startDrag(event);
      }
    },

    select() {
      const isShiftPressed = window.event?.shiftKey;

      if (this.isResizing || this.isRotating) return;

      if (isShiftPressed) {
        if (this.store.selectedElementIds.includes(this.element.id)) {
          const newSelectedIds = this.store.selectedElementIds.filter(
            (id) => id !== this.element.id
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
          this.store.selectedElementIds.push(this.element.id);
          this.store.selectedElementId = this.element.id;
          this.store.selectedElement = this.element;
        }
      } else {
        if (!this.store.selectedElementIds.includes(this.element.id)) {
          this.store.selectedElementIds = [this.element.id];
          this.store.selectedElementId = this.element.id;
          this.store.selectedElement = this.element;
        }
      }
    },

    deselect() {
      this.isSelected = false;
      this.store.clearSelection();
    },

    startDrag(event) {
      if (this.isResizing || this.isRotating || this.element.locked) return;

      // Save the initial state of all selected elements
      this.dragStartState = {
        elements: this.store.selectedElementIds.map((id) => {
          const element = this.store.elements.find((el) => el.id === id);
          return {
            id,
            x: element.x,
            y: element.y,
          };
        }),
      };

      const zoom = this.$parent.zoom || 1;

      this.dragStartPos = {
        x: event.clientX,
        y: event.clientY,
      };

      // Store element positions
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

      document.addEventListener("mousemove", this.drag);
      document.addEventListener("mouseup", this.stopDrag);
    },

    // In IconElement.vue, modify the drag method:
    drag(event) {
      if (!this.isDragging) return;

      const zoom = this.$parent.zoom || 1;
      const dx = (event.clientX - this.dragStartPos.x) / zoom;
      const dy = (event.clientY - this.dragStartPos.y) / zoom;

      requestAnimationFrame(() => {
        const updates = {};
        Object.keys(this.elementStartPositions).forEach((id) => {
          const startPos = this.elementStartPositions[id];
          if (!startPos) return;

          let newX = startPos.x + dx;
          let newY = startPos.y + dy;

          // Check alignment and get guides
          const element = this.store.elements.find((el) => el.id === id);
          if (element) {
            this.$parent.checkAlignment(element, newX, newY);
            const snapped = this.$parent.snapToGuides(element, newX, newY);
            newX = snapped.x;
            newY = snapped.y;
          }

          updates[id] = {
            x: newX,
            y: newY,
          };
        });

        // Update all elements in one go
        this.store.batchUpdateElements(updates);
      });
    },

    // And modify the stopDrag method:
    stopDrag() {
      if (this.isDragging && this.dragStartState) {
        const finalState = {
          elements: this.store.selectedElementIds.map((id) => {
            const element = this.store.elements.find((el) => el.id === id);
            return {
              id,
              x: element.x,
              y: element.y,
            };
          }),
        };

        this.store.saveDragOperation(this.dragStartState, finalState);
      }

      this.isDragging = false;
      this.dragStartState = null;
      this.$parent.guides = []; // Clear guides when drag ends
      document.removeEventListener("mousemove", this.drag);
      document.removeEventListener("mouseup", this.stopDrag);
    },

    startResize(event, position) {
      // Prevent resizing if the element is locked
      if (this.element.locked) return;
      
      event.stopPropagation();
      this.isResizing = true;
      this.resizeDirection = position;
      this.startX = event.clientX;
      this.startY = event.clientY;
      this.startWidth = this.element.width;
      this.startHeight = this.element.height;
      this.startPosition = {
        x: this.element.x,
        y: this.element.y,
      };

      // Save initial state for resizefhandleResize
      this.resizeStartState = {
        elements: [
          {
            id: this.element.id,
            width: this.element.width,
            height: this.element.height,
            x: this.element.x,
            y: this.element.y,
          },
        ],
      };

      document.addEventListener("mousemove", this.handleResize);
      document.addEventListener("mouseup", this.stopResize);
    },

    handleResize(event) {
      if (!this.isResizing) return;

      // Transform mouse position into element's coordinate system
      const angleRad = ((this.element.rotation || 0) * Math.PI) / 180;
      const dx = (event.clientX - this.startX) / (this.$parent.zoom || 1);
      const dy = (event.clientY - this.startY) / (this.$parent.zoom || 1);

      // Transform dx/dy into rotated space
      const rotatedDelta = {
        x: dx * Math.cos(-angleRad) - dy * Math.sin(-angleRad),
        y: dx * Math.sin(-angleRad) + dy * Math.cos(-angleRad),
      };

      const rotate = (x, y, cx, cy, angle) => [
        (x - cx) * Math.cos(angle) - (y - cy) * Math.sin(angle) + cx,
        (x - cx) * Math.sin(angle) + (y - cy) * Math.cos(angle) + cy,
      ];

      let newWidth = this.startWidth;
      let newHeight = this.startHeight;
      const aspectRatio = this.startWidth / this.startHeight;

      const startCenter = [
        this.startPosition.x + this.startWidth / 2,
        this.startPosition.y + this.startHeight / 2,
      ];

      const rotatedCenter = rotate(
        startCenter[0],
        startCenter[1],
        startCenter[0],
        startCenter[1],
        angleRad
      );

      switch (this.resizeDirection) {
        case "bottom-right": {
          // Use the rotated delta for more natural resizing
          newWidth = Math.max(20, this.startWidth + rotatedDelta.x);
          newHeight = newWidth / aspectRatio;

          // Keep the original anchor point logic
          const rotatedTopLeft = rotate(
            this.startPosition.x,
            this.startPosition.y,
            rotatedCenter[0],
            rotatedCenter[1],
            angleRad
          );

          const newBottomRight = rotate(
            this.startPosition.x + newWidth,
            this.startPosition.y + newHeight,
            rotatedCenter[0],
            rotatedCenter[1],
            angleRad
          );

          const newCenter = [
            (rotatedTopLeft[0] + newBottomRight[0]) / 2,
            (rotatedTopLeft[1] + newBottomRight[1]) / 2,
          ];

          const [newX, newY] = rotate(
            rotatedTopLeft[0],
            rotatedTopLeft[1],
            newCenter[0],
            newCenter[1],
            -angleRad
          );

          this.store.updateElementWithoutHistory(this.element.id, {
            width: newWidth,
            height: newHeight,
            x: newX,
            y: newY,
          });
          break;
        }

        // Other cases would follow the same pattern...
        case "top-left": {
          newWidth = Math.max(20, this.startWidth - rotatedDelta.x);
          newHeight = newWidth / aspectRatio;

          const rotatedBottomRight = rotate(
            this.startPosition.x + this.startWidth,
            this.startPosition.y + this.startHeight,
            rotatedCenter[0],
            rotatedCenter[1],
            angleRad
          );

          const newTopLeft = rotate(
            this.startPosition.x + this.startWidth - newWidth,
            this.startPosition.y + this.startHeight - newHeight,
            rotatedCenter[0],
            rotatedCenter[1],
            angleRad
          );

          const newCenter = [
            (rotatedBottomRight[0] + newTopLeft[0]) / 2,
            (rotatedBottomRight[1] + newTopLeft[1]) / 2,
          ];

          const [newX, newY] = rotate(
            newTopLeft[0],
            newTopLeft[1],
            newCenter[0],
            newCenter[1],
            -angleRad
          );

          this.store.updateElementWithoutHistory(this.element.id, {
            width: newWidth,
            height: newHeight,
            x: newX,
            y: newY,
          });
          break;
        }
        case "top-right": {
          newWidth = Math.max(20, this.startWidth + rotatedDelta.x);
          newHeight = newWidth / aspectRatio;

          // Get fixed bottom-left as anchor
          const rotatedBottomLeft = rotate(
            this.startPosition.x,
            this.startPosition.y + this.startHeight,
            rotatedCenter[0],
            rotatedCenter[1],
            angleRad
          );

          // Calculate new moving corner relative to fixed point
          const newTopRight = rotate(
            this.startPosition.x + newWidth,
            this.startPosition.y + this.startHeight - newHeight,
            rotatedCenter[0],
            rotatedCenter[1],
            angleRad
          );

          const newCenter = [
            (rotatedBottomLeft[0] + newTopRight[0]) / 2,
            (rotatedBottomLeft[1] + newTopRight[1]) / 2,
          ];

          const [newX, newY] = rotate(
            rotatedBottomLeft[0],
            rotatedBottomLeft[1],
            newCenter[0],
            newCenter[1],
            -angleRad
          );

          this.store.updateElementWithoutHistory(this.element.id, {
            width: newWidth,
            height: newHeight,
            x: newX,
            y: newY - newHeight,
          });
          break;
        }

        case "bottom-left": {
          newWidth = Math.max(20, this.startWidth - rotatedDelta.x);
          newHeight = newWidth / aspectRatio;

          const rotatedTopRight = rotate(
            this.startPosition.x + this.startWidth,
            this.startPosition.y,
            rotatedCenter[0],
            rotatedCenter[1],
            angleRad
          );

          const newBottomLeft = rotate(
            this.startPosition.x + this.startWidth - newWidth,
            this.startPosition.y + newHeight,
            rotatedCenter[0],
            rotatedCenter[1],
            angleRad
          );

          const newCenter = [
            (rotatedTopRight[0] + newBottomLeft[0]) / 2,
            (rotatedTopRight[1] + newBottomLeft[1]) / 2,
          ];

          const [newX, newY] = rotate(
            rotatedTopRight[0],
            rotatedTopRight[1],
            newCenter[0],
            newCenter[1],
            -angleRad
          );

          this.store.updateElementWithoutHistory(this.element.id, {
            width: newWidth,
            height: newHeight,
            x: newX - newWidth,
            y: newY,
          });
          break;
        }

        case "top": {
          newHeight = Math.max(20, this.startHeight - rotatedDelta.y);
          newWidth = this.startWidth;

          // Fixed bottom points
          const rotatedBottomLeft = rotate(
            this.startPosition.x,
            this.startPosition.y + this.startHeight,
            rotatedCenter[0],
            rotatedCenter[1],
            angleRad
          );

          const rotatedBottomRight = rotate(
            this.startPosition.x + this.startWidth,
            this.startPosition.y + this.startHeight,
            rotatedCenter[0],
            rotatedCenter[1],
            angleRad
          );

          // Moving top points
          const newTopLeft = rotate(
            this.startPosition.x,
            this.startPosition.y + this.startHeight - newHeight,
            rotatedCenter[0],
            rotatedCenter[1],
            angleRad
          );

          const newTopRight = rotate(
            this.startPosition.x + this.startWidth,
            this.startPosition.y + this.startHeight - newHeight,
            rotatedCenter[0],
            rotatedCenter[1],
            angleRad
          );

          const newCenter = [
            (rotatedBottomLeft[0] +
              rotatedBottomRight[0] +
              newTopLeft[0] +
              newTopRight[0]) /
              4,
            (rotatedBottomLeft[1] +
              rotatedBottomRight[1] +
              newTopLeft[1] +
              newTopRight[1]) /
              4,
          ];

          const [newX, newY] = rotate(
            rotatedBottomLeft[0],
            rotatedBottomLeft[1],
            newCenter[0],
            newCenter[1],
            -angleRad
          );

          this.store.updateElementWithoutHistory(this.element.id, {
            width: newWidth,
            height: newHeight,
            x: newX,
            y: newY - newHeight,
          });
          break;
        }

        case "bottom": {
          newHeight = Math.max(20, this.startHeight + rotatedDelta.y);
          newWidth = this.startWidth;

          // Fixed top points
          const rotatedTopLeft = rotate(
            this.startPosition.x,
            this.startPosition.y,
            rotatedCenter[0],
            rotatedCenter[1],
            angleRad
          );

          const rotatedTopRight = rotate(
            this.startPosition.x + this.startWidth,
            this.startPosition.y,
            rotatedCenter[0],
            rotatedCenter[1],
            angleRad
          );

          // Moving bottom points
          const newBottomLeft = rotate(
            this.startPosition.x,
            this.startPosition.y + newHeight,
            rotatedCenter[0],
            rotatedCenter[1],
            angleRad
          );

          const newBottomRight = rotate(
            this.startPosition.x + this.startWidth,
            this.startPosition.y + newHeight,
            rotatedCenter[0],
            rotatedCenter[1],
            angleRad
          );

          const newCenter = [
            (rotatedTopLeft[0] +
              rotatedTopRight[0] +
              newBottomLeft[0] +
              newBottomRight[0]) /
              4,
            (rotatedTopLeft[1] +
              rotatedTopRight[1] +
              newBottomLeft[1] +
              newBottomRight[1]) /
              4,
          ];

          const [newX, newY] = rotate(
            rotatedTopLeft[0],
            rotatedTopLeft[1],
            newCenter[0],
            newCenter[1],
            -angleRad
          );

          this.store.updateElementWithoutHistory(this.element.id, {
            width: newWidth,
            height: newHeight,
            x: newX,
            y: newY,
          });
          break;
        }

        case "left": {
          newWidth = Math.max(20, this.startWidth - rotatedDelta.x);
          newHeight = this.startHeight;

          // Fixed right points
          const rotatedTopRight = rotate(
            this.startPosition.x + this.startWidth,
            this.startPosition.y,
            rotatedCenter[0],
            rotatedCenter[1],
            angleRad
          );

          const rotatedBottomRight = rotate(
            this.startPosition.x + this.startWidth,
            this.startPosition.y + this.startHeight,
            rotatedCenter[0],
            rotatedCenter[1],
            angleRad
          );

          // Moving left points
          const newTopLeft = rotate(
            this.startPosition.x + this.startWidth - newWidth,
            this.startPosition.y,
            rotatedCenter[0],
            rotatedCenter[1],
            angleRad
          );

          const newBottomLeft = rotate(
            this.startPosition.x + this.startWidth - newWidth,
            this.startPosition.y + this.startHeight,
            rotatedCenter[0],
            rotatedCenter[1],
            angleRad
          );

          const newCenter = [
            (rotatedTopRight[0] +
              rotatedBottomRight[0] +
              newTopLeft[0] +
              newBottomLeft[0]) /
              4,
            (rotatedTopRight[1] +
              rotatedBottomRight[1] +
              newTopLeft[1] +
              newBottomLeft[1]) /
              4,
          ];

          const [newX, newY] = rotate(
            rotatedTopRight[0],
            rotatedTopRight[1],
            newCenter[0],
            newCenter[1],
            -angleRad
          );

          this.store.updateElementWithoutHistory(this.element.id, {
            width: newWidth,
            height: newHeight,
            x: newX - newWidth,
            y: newY,
          });
          break;
        }

        case "right": {
          newWidth = Math.max(20, this.startWidth + rotatedDelta.x);
          newHeight = this.startHeight;

          // Fixed left points
          const rotatedTopLeft = rotate(
            this.startPosition.x,
            this.startPosition.y,
            rotatedCenter[0],
            rotatedCenter[1],
            angleRad
          );

          const rotatedBottomLeft = rotate(
            this.startPosition.x,
            this.startPosition.y + this.startHeight,
            rotatedCenter[0],
            rotatedCenter[1],
            angleRad
          );

          // Moving right points
          const newTopRight = rotate(
            this.startPosition.x + newWidth,
            this.startPosition.y,
            rotatedCenter[0],
            rotatedCenter[1],
            angleRad
          );

          const newBottomRight = rotate(
            this.startPosition.x + newWidth,
            this.startPosition.y + this.startHeight,
            rotatedCenter[0],
            rotatedCenter[1],
            angleRad
          );

          const newCenter = [
            (rotatedTopLeft[0] +
              rotatedBottomLeft[0] +
              newTopRight[0] +
              newBottomRight[0]) /
              4,
            (rotatedTopLeft[1] +
              rotatedBottomLeft[1] +
              newTopRight[1] +
              newBottomRight[1]) /
              4,
          ];

          const [newX, newY] = rotate(
            rotatedTopLeft[0],
            rotatedTopLeft[1],
            newCenter[0],
            newCenter[1],
            -angleRad
          );

          this.store.updateElementWithoutHistory(this.element.id, {
            width: newWidth,
            height: newHeight,
            x: newX,
            y: newY,
          });
          break;
        }
      }

      if (["rectangle", "roundedRectangle"].includes(this.element.shapeType)) {
        const newSvgContent = this.updateSvgDimensions(
          this.element,
          newWidth,
          newHeight
        );
        if (newSvgContent) {
          this.store.updateElementWithoutHistory(this.element.id, {
            svgContent: newSvgContent,
          });
        }
      }
    },

    stopResize() {
      if (this.isResizing && this.resizeStartState) {
        // Create the final state
        const finalState = {
          elements: [
            {
              id: this.element.id,
              width: this.element.width,
              height: this.element.height,
              x: this.element.x,
              y: this.element.y,
            },
          ],
        };

        // Save the complete resize operation to history
        this.store.saveTransformOperation(
          "resize",
          this.resizeStartState,
          finalState
        );
      }

      this.isResizing = false;
      this.resizeStartState = null;
      document.removeEventListener("mousemove", this.handleResize);
      document.removeEventListener("mouseup", this.stopResize);
    },

    startRotate(event) {
      // Prevent rotation if the element is locked
      if (this.element.locked) return;
      
      event.stopPropagation();
      this.isRotating = true;
      const bbox = this.$el.getBoundingClientRect();
      const centerX = bbox.left + bbox.width / 2;
      const centerY = bbox.top + bbox.height / 2;

      this.startAngle = Math.atan2(
        event.clientY - centerY,
        event.clientX - centerX
      );
      this.lastAngle = this.startAngle;
      this.initialRotation = this.element.rotation || 0;

      // Save initial state for rotation
      this.rotateStartState = {
        elements: [
          {
            id: this.element.id,
            rotation: this.element.rotation || 0,
          },
        ],
      };

      document.addEventListener("mousemove", this.handleRotate);
      document.addEventListener("mouseup", this.stopRotate);
    },

    handleRotate(event) {
      if (!this.isRotating) return;

      const bbox = this.$el.getBoundingClientRect();
      const centerX = bbox.left + bbox.width / 2;
      const centerY = bbox.top + bbox.height / 2;

      const currentAngle = Math.atan2(
        event.clientY - centerY,
        event.clientX - centerX
      );
      let delta = currentAngle - this.lastAngle;

      if (delta > Math.PI) delta -= 2 * Math.PI;
      if (delta < -Math.PI) delta += 2 * Math.PI;

      this.lastAngle = currentAngle;
      let deltaRotation = ((delta * 180) / Math.PI) * 0.5;
      let newRotation = this.initialRotation + deltaRotation;
      newRotation = ((newRotation % 360) + 360) % 360;

      this.store.updateElementWithoutHistory(this.element.id, {
        rotation: newRotation,
      });

      this.initialRotation = newRotation;
    },

    stopRotate() {
      if (this.isRotating && this.rotateStartState) {
        // Create the final state
        const finalState = {
          elements: [
            {
              id: this.element.id,
              rotation: this.element.rotation || 0,
            },
          ],
        };

        // Save the complete rotation operation to history
        this.store.saveTransformOperation(
          "rotate",
          this.rotateStartState,
          finalState
        );
      }

      this.isRotating = false;
      this.rotateStartState = null;
      document.removeEventListener("mousemove", this.handleRotate);
      document.removeEventListener("mouseup", this.stopRotate);
    },

    getHandleCursor(position) {
      return this.resizeHandleCursors[position] || "default";
    },
  },
};
</script>

<style scoped>
.icon-element {
  width: 100%;
  height: 100%;
  position: relative;
  user-select: none;
  touch-action: none;
  transform-origin: center center;
  transition: all 0.2s ease;
  will-change: transform;
  transform-style: preserve-3d;
}

.icon-wrapper {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  transform-style: preserve-3d;
  overflow: hidden;
  border-radius: 4px;
}

.icon-element.selected {
  outline: none;
  box-shadow: 0 0 0 2px rgba(107, 114, 128, 0.15), 0 0 0 1px #6b7280;
  border-radius: 4px;
}

/* Resize Handles */
.resize-handle {
  position: absolute;
  width: 12px;
  height: 12px;
  background: white;
  border: 2px solid #6b7280;
  pointer-events: all;
  opacity: 0;
  visibility: hidden;
  transition: all 0.2s ease;
  border-radius: 50%;
  z-index: 10;
}

.icon-element:hover .resize-handle,
.icon-element.selected .resize-handle {
  opacity: 1;
  visibility: visible;
}

.resize-handle:hover {
  background: #6b7280;
  transform: scale(1.2);
  box-shadow: 0 0 8px rgba(107, 114, 128, 0.4);
}

/* Corner Handles */
.resize-handle.top-left {
  top: -6px;
  left: -6px;
}

.resize-handle.top-right {
  top: -6px;
  right: -6px;
}

.resize-handle.bottom-left {
  bottom: -6px;
  left: -6px;
}

.resize-handle.bottom-right {
  bottom: -6px;
  right: -6px;
}

/* Middle Handles */
.resize-handle.top {
  top: -6px;
  left: 50%;
  transform: translateX(-50%);
}

.resize-handle.right {
  top: 50%;
  right: -6px;
  transform: translateY(-50%);
}

.resize-handle.bottom {
  bottom: -6px;
  left: 50%;
  transform: translateX(-50%);
}

.resize-handle.left {
  top: 50%;
  left: -6px;
  transform: translateY(-50%);
}

/* Rotate Handle */
.rotate-handle {
  position: absolute;
  top: -30px;
  left: 50%;
  transform: translateX(-50%);
  width: 20px;
  height: 20px;
  background: white;
  border: 2px solid #6b7280;
  border-radius: 50%;
  cursor: grab;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #6b7280;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  opacity: 0;
  visibility: hidden;
  transition: all 0.2s ease;
  z-index: 10;
}

.icon-element:hover .rotate-handle,
.icon-element.selected .rotate-handle {
  opacity: 1;
  visibility: visible;
}

.rotate-handle:hover {
  transform: translateX(-50%) scale(1.1);
  background: #6b7280;
  color: white;
}

.rotate-handle:active {
  cursor: grabbing;
  transform: translateX(-50%) scale(0.95);
}

/* Center snapping guidelines */
.center-snapped-x::before {
  content: "";
  position: fixed;
  border-right: 2px dashed rgba(107, 114, 128, 0.3);
  height: 100vh;
  left: 50%;
  transform: translateX(-50%);
  pointer-events: none;
  z-index: 9999;
}

.center-snapped-y::after {
  content: "";
  position: fixed;
  width: 100vw;
  border-top: 2px dashed rgba(107, 114, 128, 0.3);
  top: 50%;
  transform: translateY(-50%);
  pointer-events: none;
  z-index: 9999;
}
</style>