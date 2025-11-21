<template>
  <div
    class="text-element"
    :class="elementClasses"
    @dblclick="startEditing"
    @mousedown.stop="handleMouseDown"
    :style="{
      cursor: element.locked ? 'default' : (isEditing ? 'text' : isDragging ? 'grabbing' : 'grab'),
    }"
  >
    <!-- Text Content -->
    <div
      v-if="!isEditing"
      class="text-content"
      :style="{
        fontSize: `${element.fontSize}px`,
        fontFamily: element.fontFamily,
        color: element.color,
        fontWeight: element.fontWeight,
        fontStyle: element.fontStyle,
        textAlign: element.textAlign,
        textDecoration: element.textDecoration,
        letterSpacing: element.letterSpacing,
        lineHeight: element.lineHeight,
        width: '100%',
        opacity: element.opacity,
        textShadow: element.hasShadow
          ? `${element.shadowOffsetX}px ${element.shadowOffsetY}px ${element.shadowBlur}px ${element.shadowColor}`
          : '',
      }"
    >
      {{ element.content }}
    </div>
    <!-- Edit Mode -->
    <textarea
      v-else
      ref="textInput"
      v-model="editableContent"
      :style="{
        fontSize: `${element.fontSize}px`,
        fontFamily: element.fontFamily,
        color: element.color,
        fontWeight: element.fontWeight,
        fontStyle: element.fontStyle,
        textAlign: element.textAlign,
        textDecoration: element.textDecoration,
        letterSpacing: element.letterSpacing,
        lineHeight: element.lineHeight,
        width: '100%',
        opacity: element.opacity,
        textShadow: element.hasShadow
          ? `${element.shadowOffsetX}px ${element.shadowOffsetY}px ${element.shadowBlur}px ${element.shadowColor}`
          : '',
      }"
      @input="adjustHeight"
      @blur="stopEditing"
      @keydown="handleTextareaKeyDown"
      @keydown.enter.prevent="stopEditing"
    ></textarea>

    <!-- Lock icon when element is locked and selected -->
    <div 
      v-if="element.locked && isElementSelected" 
      class="lock-icon"
      style="position: absolute; top: -10px; right: -10px; background-color: white; border-radius: 50%; padding: 3px; box-shadow: 0 1px 2px rgba(0,0,0,0.2); z-index: 10;"
    >
      <svg width="20" height="20" viewBox="0 0 24 24">
       <path fill="#9E9E9E" d="M12,17A2,2 0 0,0 14,15C14,13.89 13.1,13 12,13A2,2 0 0,0 10,15A2,2 0 0,0 12,17M18,8A2,2 0 0,1 20,10V20A2,2 0 0,1 18,22H6A2,2 0 0,1 4,20V10C4,8.89 4.9,8 6,8H7V6A5,5 0 0,1 12,1A5,5 0 0,1 17,6V8H18M12,3A3,3 0 0,0 9,6V8H15V6A3,3 0 0,0 12,3Z" />
      </svg>
    </div>

    <!-- Resize and Rotate Handles - Only show when selected or in edit mode and not locked -->
    <template v-if="(isElementSelected || isEditing) && !element.locked">
      <div
        class="resize-handle left"
        @mousedown.stop="startResize($event, 'left')"
      ></div>
      <div
        class="resize-handle right"
        @mousedown.stop="startResize($event, 'right')"
      ></div>

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
const SNAP_THRESHOLD = 2; // Degrees within which to snap
const SNAP_ANGLES = [0, 90, 180, 270, 360]; // Angles to snap to
import { useEditorStore } from "@/stores/editorStore";

export default {
  name: "TextElement",

  props: {
    element: {
      type: Object,
      required: true,
    },
  },

  data() {
    return {
      store: useEditorStore(),
      isEditing: false,
      editableContent: "",
      isResizing: false,
      isRotating: false,
      startX: 0,
      startWidth: 0,
      startRotation: 0,
      isDragging: false,
      dragStartPos: { x: 0, y: 0 },
      elementStartPositions: {},
      startPosition: { x: 0, y: 0 }, // Add this
      resizePosition: null, // Add this
      dragStartState: null,
      resizeStartState: null,
      rotateStartState: null,
      _heightAdjustTimeout: null,
      _transformRAF: null,
    };
  },

  computed: {
    elementClasses() {
      return {
        editing: this.isEditing,
        selected: this.isElementSelected || this.isResizing || this.isRotating,
      };
    },

    isElementSelected() {
      return this.store.selectedElementIds.includes(this.element.id);
    },

    isDraggable() {
      return !this.isEditing;
    },
    isCentered() {
      const canvasWidth = 600; // Get this from your canvas width
      const canvasHeight = 1200; // Get this from your canvas height

      // Calculate element center position
      const elementCenterX = this.element.x + this.element.width / 2;
      const elementCenterY = this.element.y + this.element.height / 2;

      // Calculate canvas center position
      const canvasCenterX = canvasWidth / 2;
      const canvasCenterY = canvasHeight / 2;

      // Check if element is centered (within threshold)
      const isCenteredX =
        Math.abs(elementCenterX - canvasCenterX) < SNAP_THRESHOLD;
      const isCenteredY =
        Math.abs(elementCenterY - canvasCenterY) < SNAP_THRESHOLD;

      return {
        x: isCenteredX,
        y: isCenteredY,
      };
    },
  },

  watch: {
    "element.content": {
      handler() {
        this.$nextTick(() => {
          this.adjustHeight();
        });
      },
    },
    "element.fontSize": {
      handler() {
        this.$nextTick(() => {
          this.adjustHeight();
        });
      },
    },
    "element.lineHeight": {
      handler() {
        this.$nextTick(() => {
          this.adjustHeight();
        });
      },
    },
    "element.fontFamily": {
      handler() {
        this.$nextTick(() => {
          this.adjustHeight();
        });
      },
    },
    "element.x"() {
      this.checkAndSnapToCenter();
    },
    "element.y"() {
      this.checkAndSnapToCenter();
    },
  },

  mounted() {
    this.$nextTick(() => {
      this.adjustHeightMounted();
    });
  },

  methods: {
    // Add this new method to handle keydown events in the textarea
    handleTextareaKeyDown(event) {
      // Let the textarea handle copy and paste events naturally
      // This will prevent the event from bubbling up to the canvas handler
      if ((event.ctrlKey || event.metaKey) && (event.key === 'c' || event.key === 'v' || event.key === 'x')) {
        event.stopPropagation();
        // Let the default browser behavior handle the copy/paste
      }
    },
    
    handleMouseDown(event) {
      // Prevent drag if clicking on resize/rotate handles
      if (
        event.target.closest(".resize-handle") ||
        event.target.closest(".rotate-handle") ||
        this.isResizing ||
        this.isRotating ||
        this.isEditing
      ) {
        return;
      }

      // Handle selection
      this.select();

      // Start drag if appropriate and not locked
      if (this.element.id !== null && !this.element.locked) {
        this.startDrag(event);
      }
    },

    deselect() {
      if (this.store.selectedElementIds.includes(this.element.id)) {
        this.store.selectedElementIds = this.store.selectedElementIds.filter(
          (id) => id !== this.element.id
        );
        if (this.store.selectedElementId === this.element.id) {
          this.store.selectedElementId =
            this.store.selectedElementIds[0] || null;
          this.store.selectedElement =
            this.store.elements.find(
              (el) => el.id === this.store.selectedElementId
            ) || {};
        }
      }
    },
    // Also update the drag method for safety

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

        this.store.batchUpdateElements(updates);
      });
    },

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
    select() {
      const isShiftPressed = window.event?.shiftKey;

      if (this.isEditing || this.isResizing || this.isRotating) return;

      if (isShiftPressed) {
        // Multi-select logic
        if (this.store.selectedElementIds.includes(this.element.id)) {
          const newSelectedIds = this.store.selectedElementIds.filter(
            (id) => id !== this.element.id
          );
          this.store.selectedElementIds = newSelectedIds;
          // Update main selection if there's still an element selected
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
    checkAndSnapToCenter() {
      if (!this.isEditing) {
        const canvasWidth = 600; // Get this from your canvas width
        const canvasHeight = 1200; // Get this from your canvas height

        // Calculate current center positions
        const elementCenterX = this.element.x + this.element.width / 2;
        const elementCenterY = this.element.y + this.element.height / 2;

        // Calculate canvas center
        const canvasCenterX = canvasWidth / 2;
        const canvasCenterY = canvasHeight / 2;

        // Check if near center
        if (Math.abs(elementCenterX - canvasCenterX) < SNAP_THRESHOLD) {
          // Snap to center X
          const newX = canvasCenterX - this.element.width / 2;
          this.store.updateElement(this.element.id, { x: newX });
        }

        if (Math.abs(elementCenterY - canvasCenterY) < SNAP_THRESHOLD) {
          // Snap to center Y
          const newY = canvasCenterY - this.element.height / 2;
          this.store.updateElement(this.element.id, { y: newY });
        }
      }
    },
    adjustHeight() {
      if (this.isEditing && this.$refs.textInput) {
        const textarea = this.$refs.textInput;
        textarea.style.height = "auto";
        textarea.style.height = textarea.scrollHeight + "px";
      }

      // Update element height in store based on content height
      const contentEl = this.isEditing
        ? this.$refs.textInput
        : this.$el.querySelector(".text-content");
      if (contentEl) {
        // Calculate minimum height based on font size and line height
        const fontSize = parseInt(this.element.fontSize);
        const lineHeight = parseFloat(this.element.lineHeight);
        const minHeight = Math.ceil(fontSize * lineHeight + 16); // Add padding

        // Get actual content height
        const contentHeight = contentEl.scrollHeight;

        // Use the larger of minimum height or content height
        const finalHeight = Math.max(minHeight, contentHeight);

        this.store.updateElement(this.element.id, {
          height: finalHeight,
        });
      }
    },
    calculateTextHeight() {
      const fontSize = parseInt(this.element.fontSize);
      const lineHeight = parseFloat(this.element.lineHeight);
      const width = this.element.width;
      const content = this.element.content;
      
      // Create a temporary div to measure text
      const tempDiv = document.createElement('div');
      tempDiv.style.position = 'absolute';
      tempDiv.style.visibility = 'hidden';
      tempDiv.style.whiteSpace = 'pre-wrap';
      tempDiv.style.width = `${width}px`;
      tempDiv.style.fontSize = `${fontSize}px`;
      tempDiv.style.lineHeight = lineHeight;
      tempDiv.style.fontFamily = this.element.fontFamily;
      tempDiv.style.padding = '8px';
      tempDiv.textContent = content;
      
      document.body.appendChild(tempDiv);
      const height = tempDiv.offsetHeight;
      document.body.removeChild(tempDiv);
      
      return Math.max(height + 16, fontSize * lineHeight + 16); // Add padding and ensure minimum height
    },
    adjustHeightMounted() {
      if (this.isEditing && this.$refs.textInput) {
        const textarea = this.$refs.textInput;
        textarea.style.height = "auto";
        textarea.style.height = textarea.scrollHeight + "px";
      }

      // Calculate and update height based on content
      const calculatedHeight = this.calculateTextHeight();
      this.store.updateElement(this.element.id, {
        height: calculatedHeight,
      });
    },

    startEditing() {
      // Prevent editing if element is locked
      if (this.element.locked) return;
      
      if (!this.isEditing) {
        this.isEditing = true;
        this.editableContent = this.element.content;
        this.$nextTick(() => {
          if (this.$refs.textInput) {
            this.$refs.textInput.focus();
            this.adjustHeight();
          }
        });
      }
    },

    stopEditing() {
      if (this.isEditing) {
        this.store.updateElement(this.element.id, {
          content: this.editableContent,
        });
        this.isEditing = false;
        this.$nextTick(() => {
          this.adjustHeight();
        });
      }
    },

    startResize(event, position) {
      // Prevent resizing if element is locked
      if (this.element.locked) return;
      
      this.isResizing = true;
      this.startX = event.clientX;
      this.startWidth = this.element.width;
      this.resizePosition = position;
      this.startPosition = {
        x: this.element.x,
        y: this.element.y,
      };

      // Save initial state for resize
      this.resizeStartState = {
        elements: [
          {
            id: this.element.id,
            width: this.element.width,
            x: this.element.x,
            y: this.element.y,
            height: this.element.height,
          },
        ],
      };

      document.addEventListener("mousemove", this.handleResize);
      document.addEventListener("mouseup", this.stopResize);
    },
    handleResize(event) {
      if (!this.isResizing) return;
      if (this._transformRAF) {
        cancelAnimationFrame(this._transformRAF);
      }

      this._transformRAF = requestAnimationFrame(() => {
        // Cache zoom and angle calculations
        const zoom = this.$parent.zoom || 1;
        const dx = (event.clientX - this.startX) / zoom;
        const angleRad = ((this.element.rotation || 0) * Math.PI) / 180;

        // Cache trigonometric calculations
        const cosAngle = Math.cos(angleRad);
        const sinAngle = Math.sin(angleRad);

        // Optimized rotate function using cached trig values
        const rotate = (x, y, cx, cy, angle) => {
          const cosA = angle === angleRad ? cosAngle : Math.cos(angle);
          const sinA = angle === angleRad ? sinAngle : Math.sin(angle);
          return [
            (x - cx) * cosA - (y - cy) * sinA + cx,
            (x - cx) * sinA + (y - cy) * cosA + cy,
          ];
        };

        // Cache center point calculation
        const rotatedCenter = [
          this.startPosition.x + this.startWidth / 2,
          this.startPosition.y + this.element.height / 2,
        ];

        // Cache vertical center point
        const verticalCenter = this.startPosition.y + this.element.height / 2;

        let newWidth = this.startWidth;
        let updates;

        if (this.resizePosition === "left") {
          newWidth = Math.max(50, this.startWidth - dx);

          // Cache point calculations
          const rightPoint = rotate(
            this.startPosition.x + this.startWidth,
            verticalCenter,
            rotatedCenter[0],
            rotatedCenter[1],
            angleRad
          );

          const newLeftPoint = rotate(
            this.startPosition.x + this.startWidth - newWidth,
            verticalCenter,
            rotatedCenter[0],
            rotatedCenter[1],
            angleRad
          );

          const newCenter = [
            (rightPoint[0] + newLeftPoint[0]) / 2,
            (rightPoint[1] + newLeftPoint[1]) / 2,
          ];

          const [newX, newY] = rotate(
            rightPoint[0],
            rightPoint[1],
            newCenter[0],
            newCenter[1],
            -angleRad
          );

          updates = {
            width: newWidth,
            x: newX - newWidth,
            y: newY - this.element.height / 2,
          };
        } else if (this.resizePosition === "right") {
          newWidth = Math.max(50, this.startWidth + dx);

          const leftPoint = rotate(
            this.startPosition.x,
            verticalCenter,
            rotatedCenter[0],
            rotatedCenter[1],
            angleRad
          );

          const newRightPoint = rotate(
            this.startPosition.x + newWidth,
            verticalCenter,
            rotatedCenter[0],
            rotatedCenter[1],
            angleRad
          );

          const newCenter = [
            (leftPoint[0] + newRightPoint[0]) / 2,
            (leftPoint[1] + newRightPoint[1]) / 2,
          ];

          const [newX, newY] = rotate(
            leftPoint[0],
            leftPoint[1],
            newCenter[0],
            newCenter[1],
            -angleRad
          );

          updates = {
            width: newWidth,
            x: newX,
            y: newY - this.element.height / 2,
          };
        }

        // Batch update the element
        this.store.updateElementWithoutHistory(this.element.id, updates);

        // Debounce height adjustment
        if (this._heightAdjustTimeout) {
          clearTimeout(this._heightAdjustTimeout);
        }
        this._heightAdjustTimeout = setTimeout(() => {
          this.adjustHeight();
        }, 16); // ~60fps
      });
    },
    stopResize() {
      if (this.isResizing && this.resizeStartState) {
        // Create the final state
        const finalState = {
          elements: [
            {
              id: this.element.id,
              width: this.element.width,
              x: this.element.x,
              y: this.element.y,
              height: this.element.height,
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

    // ... keep rotation methods the same ...
    startRotate(event) {
      // Prevent rotation if element is locked
      if (this.element.locked) return;
      
      event.stopPropagation();
      this.isRotating = true;
      const bbox = event.target.getBoundingClientRect();
      const centerX = bbox.left + bbox.width / 2;
      const centerY = bbox.top + bbox.height / 2;
      this.startRotation = Math.atan2(
        event.clientY - centerY,
        event.clientX - centerX
      );

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

      requestAnimationFrame(() => {
        const bbox = this.$el.getBoundingClientRect();
        const centerX = bbox.left + bbox.width / 2;
        const centerY = bbox.top + bbox.height / 2;
        const angle = Math.atan2(
          event.clientY - centerY,
          event.clientX - centerX
        );

        let rotation = (angle - this.startRotation) * (180 / Math.PI);
        rotation = ((rotation % 360) + 360) % 360;

        // Optimize snapping check with early return
        const snapAngle = SNAP_ANGLES.find(
          (snap) => Math.abs(rotation - snap) < SNAP_THRESHOLD
        );

        if (snapAngle !== undefined) {
          rotation = snapAngle;
          this.$el.classList.add("rotation-snapped");
        } else {
          this.$el.classList.remove("rotation-snapped");
        }

        this.store.updateElementWithoutHistory(this.element.id, { rotation });
      });
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
      this.$el.classList.remove("rotation-snapped");
      document.removeEventListener("mousemove", this.handleRotate);
      document.removeEventListener("mouseup", this.stopRotate);
    },
  },
};
</script>
<style scoped>
.text-element {
  width: 100%;
  position: relative;
  transition: all 0.2s ease;
}

.text-content {
  width: 100%;
  padding-top: 8px;
  padding-bottom: 8px;
  white-space: pre-wrap;
  word-wrap: break-word;
  overflow: visible;
  text-align: center;
  border-radius: 4px;
}

textarea {
  width: 100%;
  padding-top: 8px;
  padding-bottom: 8px;
  border: none;
  background: transparent;
  resize: none;
  outline: none;
  overflow: visible;
  white-space: pre-wrap;
  word-wrap: break-word;
  height: max-content;
  border-radius: 4px;
  transition: background-color 0.2s ease;
}

textarea:focus {
  background-color: rgba(75, 85, 99, 0.05);
}

.editing {
  outline: none;
  box-shadow: 0 0 0 2px rgba(75, 85, 99, 0.2), 0 0 0 1px #4b5563;
  border-radius: 4px;
  backdrop-filter: brightness(100%);
}

/* Circular resize handles */
.resize-handle {
  position: absolute;
  width: 12px;
  height: 12px;
  background: white;
  border: 2px solid #6b7280;
  border-radius: 50%;
  top: 50%;
  transform: translateY(-50%);
  transition: all 0.2s ease;
  opacity: 0;
  z-index: 10;
}

.resize-handle.left {
  left: -6px;
  cursor: w-resize;
}

.resize-handle.right {
  right: -6px;
  cursor: e-resize;
}

/* Show resize handles on hover/selection */
.text-element:hover .resize-handle,
.selected .resize-handle {
  opacity: 1;
}

.resize-handle:hover {
  background: #6b7280;
  transform: translateY(-50%) scale(1.2);
  box-shadow: 0 0 8px rgba(107, 114, 128, 0.4);
}

/* Additional touch target for resize handles */
.resize-handle::before {
  content: "";
  position: absolute;
  width: 24px;
  height: 24px;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: -1;
}

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
  transition: all 0.2s ease;
  opacity: 0;
}

.text-element:hover .rotate-handle,
.selected .rotate-handle {
  opacity: 1;
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

.rotation-snapped {
  outline: none !important;
  box-shadow: 0 0 0 2px rgba(107, 114, 128, 0.2), 0 0 0 1px #6b7280;
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

/* Selection state */
.selected:not(.editing) {
  box-shadow: 0 0 0 2px rgba(107, 114, 128, 0.15), 0 0 0 1px #6b7280;
  border-radius: 4px;
}

.rotation-snapped::before,
.rotation-snapped::after {
  content: "";
  position: absolute;
  background-color: rgba(107, 114, 128, 0.2);
  pointer-events: none;
}

.rotation-snapped::before {
  width: 1px;
  height: 100vh;
  left: 50%;
  top: 50%;
  transform: translateX(-50%);
}

.rotation-snapped::after {
  width: 100vw;
  height: 1px;
  left: 50%;
  top: 50%;
  transform: translateY(-50%);
}
</style>