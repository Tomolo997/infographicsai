<template>
  <div
    class="shape-element"
    :class="{ selected: isSelected && !preview }"
    :style="{
      cursor: preview ? 'default' : (element.locked ? 'default' : (isResizing ? 'se-resize' : isDragging ? 'grabbing' : 'grab')),
      opacity: element.opacity,
      backgroundColor: 'transparent',
      pointerEvents: preview ? 'none' : 'auto',
      filter: element.hasShadow ? `drop-shadow(${element.shadowOffsetX/2}px ${element.shadowOffsetY/2}px ${element.shadowBlur}px ${element.shadowColor})` : 'none'
    }"
    @mousedown.stop="preview ? null : handleMouseDown"
  >
    <div
      class="svg-wrapper"
      v-html="element.svgContent"
      :style="{
        width: '100%',
        height: '100%',
        color: !['line'].includes(element.shapeType)
          ? element.backgroundColor
          : undefined,
        display: 'block',
        position: 'relative',
        overflow: 'visible',
        backgroundColor: ['line'].includes(element.shapeType)
          ? element.backgroundColor
          : 'transparent',
      }"
    ></div>
    
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
        v-for="handle in activeResizeHandles"
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
  name: "ShapesElement",

  props: {
    element: {
      type: Object,
      required: true,
    },
    isDragging: {
      type: Boolean,
      default: false,
    },
    draggedElementId: {
      type: [String, Number],
      default: null,
    },
    preview: {
      type: Boolean,
      default: false
    }
  },

  data() {
    return {
      store: useEditorStore(),
      isResizing: false,
      isRotating: false,
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
        { position: "top" },
        { position: "top-right" },
        { position: "right" },
        { position: "bottom-right" },
        { position: "bottom" },
        { position: "bottom-left" },
        { position: "left" },
      ],
      aspectRatio: 1,
      initialRotation: 0,
      isSelected: false,
      startAngle: 0,
      lastAngle: 0,
      dragStartState: null, // Store initial state when drag starts
      resizeStartState: null,
      rotateStartState: null,
      _transformRAF: null,
      _rotateRAF: null,
    };
  },

  computed: {
    activeResizeHandles() {
      if (
        this.element.shapeType === "arrow" ||
        (this.element.isLine &&
          Math.abs(this.element.width) > Math.abs(this.element.height))
      ) {
        return [{ position: "middle-left" }, { position: "middle-right" }];
      }

      // For rectangles and rounded rectangles, show all handles
      if (
        this.element.shapeType === "rectangle" ||
        this.element.shapeType === "roundedRectangle"
      ) {
        return this.resizeHandles;
      }

      // For other shapes, return only corner handles
      return [
        { position: "top-left" },
        { position: "top-right" },
        { position: "bottom-left" },
        { position: "bottom-right" },
      ];
    },
    isElementSelected() {
      return this.store.selectedElementIds.includes(this.element.id);
    },

    elementClasses() {
      return {
        selected: this.isElementSelected || this.isResizing || this.isRotating,
      };
    },

    isThisElementDragging() {
      return this.isDragging && this.draggedElementId === this.element.id;
    },

    isCentered: {
      get() {
        if (!this.isDragging) return { x: false, y: false };

        // Debounce center checking during drag
        if (!this._centerCheckTimeout) {
          this._centerCheckTimeout = setTimeout(() => {
            const canvasWidth = 600;
            const canvasHeight = 1200;
            const elementCenterX = this.element.x + this.element.width / 2;
            const elementCenterY = this.element.y + this.element.height / 2;
            const canvasCenterX = canvasWidth / 2;
            const canvasCenterY = canvasHeight / 2;

            this._cachedCenter = {
              x: Math.abs(elementCenterX - canvasCenterX) < 5,
              y: Math.abs(elementCenterY - canvasCenterY) < 5,
            };
            this._centerCheckTimeout = null;
          }, 16); // ~ 60fps
        }
        return this._cachedCenter || { x: false, y: false };
      },
    },
    resizeHandleCursors() {
      const rotation = (((this.element.rotation || 0) % 360) + 360) % 360;
      const quadrant = Math.floor((rotation + 45) / 90) % 4;
      const cursors = ["nw-resize", "ne-resize", "se-resize", "sw-resize"];

      // For line and arrow shapes, determine if they're more vertical or horizontal based on rotation
      if (this.element.shapeType === "line" || this.element.shapeType === "arrow") {
        // If line is closer to vertical (near 90° or 270°), use ns-resize for endpoints
        // If line is closer to horizontal (near 0° or 180°), use ew-resize for endpoints
        const isMoreVertical = Math.abs(Math.sin((rotation * Math.PI) / 180)) > Math.abs(Math.cos((rotation * Math.PI) / 180));
        
        return {
          "top-left": cursors[(0 + quadrant) % 4],
          "top-right": cursors[(1 + quadrant) % 4],
          "bottom-right": cursors[(2 + quadrant) % 4],
          "bottom-left": cursors[(3 + quadrant) % 4],
          "top": "ns-resize",
          "right": "ew-resize",
          "bottom": "ns-resize",
          "left": "ew-resize",
          "middle-left": isMoreVertical ? "ns-resize" : "ew-resize",
          "middle-right": isMoreVertical ? "ns-resize" : "ew-resize",
        };
      }

      // For other shapes
      return {
        "top-left": cursors[(0 + quadrant) % 4],
        "top-right": cursors[(1 + quadrant) % 4],
        "bottom-right": cursors[(2 + quadrant) % 4],
        "bottom-left": cursors[(3 + quadrant) % 4],
        "top": "ns-resize",
        "right": "ew-resize",
        "bottom": "ns-resize",
        "left": "ew-resize",
      };
    },
  },

  methods: {
    handleMouseDown(event) {
      // Only allow left-click for dragging
      if (event.button !== 0) return;

      // Prevent selection when clicking resize/rotate handles
      if (
        event.target.closest(".resize-handle") ||
        event.target.closest(".rotate-handle") ||
        this.isResizing ||
        this.isRotating
      ) {
        return;
      }

      // Handle selection - this should always work, even for locked elements
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
          // Add to selection without clearing existing selection
          this.store.selectedElementIds.push(this.element.id);
          this.store.selectedElementId = this.element.id;
          this.store.selectedElement = this.element;
        }
      } else {
        // If clicking already selected element, don't change selection
        if (!this.store.selectedElementIds.includes(this.element.id)) {
          this.store.selectedElementIds = [this.element.id];
          this.store.selectedElementId = this.element.id;
          this.store.selectedElement = this.element;
        }
      }
    },

    deselect() {
      this.isSelected = false;
      this.store.clearSelection(); // This will use the store's clearSelection method
    },

    // Update startDrag to handle multiple elements
    startDrag(event) {
      if (this.isResizing || this.isRotating) return;

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

      const zoom = this.$parent.zoom || 1; // Get current zoom level

      // Calculate cursor position in canvas space
      const rect = this.$el.getBoundingClientRect();
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

    // Update drag to move all selected elements
    drag(event) {
      if (!this.isDragging) return;

      // Cache zoom value
      const zoom = this.$parent.zoom || 1;

      // Calculate the delta in screen space
      const dx = (event.clientX - this.dragStartPos.x) / zoom;
      const dy = (event.clientY - this.dragStartPos.y) / zoom;

      // Use requestAnimationFrame for smooth updates
      requestAnimationFrame(() => {
        // Batch update all selected elements
        const updates = {};
        Object.keys(this.elementStartPositions).forEach((id) => {
          const startPos = this.elementStartPositions[id];
          if (!startPos) return;

          let newX = startPos.x + dx;
          let newY = startPos.y + dy;

          // Check alignment and get guides
          const element = this.store.elements.find((el) => el.id === id);
          if (element) {
            // Check for alignment with other elements and canvas edges
            this.$parent.checkAlignment(element, newX, newY);
            
            // Snap to guides if close enough
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

    stopDrag() {
      if (this.isDragging && this.dragStartState) {
        // Ensure elements stay within canvas boundaries
        const canvasWidth = this.$parent.canvasWidth;
        const canvasHeight = this.$parent.canvasHeight;

        
        // Check and adjust positions of all selected elements
        this.store.selectedElementIds.forEach(id => {
          const element = this.store.elements.find(el => el.id === id);
          if (!element) return;
          
          let newX = element.x;
          let newY = element.y;
          let needsUpdate = false;
          
          // Update element position if needed
          if (needsUpdate) {
            this.store.updateElement(id, {
              x: newX,
              y: newY
            });
          }
        });

        const finalState = {
          elements: [
            {
              id: this.element.id,
              x: this.element.x,
              y: this.element.y,
            },
          ],
        };

        this.store.saveDragOperation(this.dragStartState, finalState);
      }

      this.isDragging = false;
      this.dragStartState = null;
      this.$parent.guides = []; // Clear guides when drag ends
      document.removeEventListener("mousemove", this.drag);
      document.removeEventListener("mouseup", this.stopDrag);
    },
    // Modified startResize to handle different resize modes
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

      // Save initial state for resize
      this.resizeStartState = {
        elements: [
          {
            id: this.element.id,
            width: this.element.width,
            height: this.element.height,
            x: this.element.x,
            y: this.element.y,
            svgContent: this.element.svgContent,
          },
        ],
      };

      // Choose the appropriate resize handler
      let resizeHandler;
      if (
        this.element.shapeType === "line" ||
        this.element.shapeType === "arrow"
      ) {
        resizeHandler = this.handleHorizontalResize;
      } else {
        resizeHandler = this.handleResize;
      }

      document.addEventListener("mousemove", resizeHandler);
      document.addEventListener("mouseup", () =>
        this.stopResize(resizeHandler)
      );
    },

    handleHorizontalResize(event) {
      const rotate = (x, y, cx, cy, angle) => [
        (x - cx) * Math.cos(angle) - (y - cy) * Math.sin(angle) + cx,
        (x - cx) * Math.sin(angle) + (y - cy) * Math.cos(angle) + cy,
      ];
      if (!this.isResizing) return;

      const dx = (event.clientX - this.startX) / (this.$parent.zoom || 1);
      const dy = (event.clientY - this.startY) / (this.$parent.zoom || 1);
      const angleRad = ((this.element.rotation || 0) * Math.PI) / 180;
      
      // Determine if line is more vertical or horizontal based on rotation
      // A line at 0° or 180° is horizontal, while a line at 90° or 270° is vertical
      const isMoreVertical = Math.abs(Math.sin(angleRad)) > Math.abs(Math.cos(angleRad));
      
      // Use the appropriate delta based on line orientation
      const effectiveDelta = isMoreVertical ? dy : dx;

      // Calculate the rotation center
      const rotatedCenter = [
        this.startPosition.x + this.startWidth / 2,
        this.startPosition.y + this.startHeight / 2,
      ];

      let newWidth = this.startWidth;
      let newSvgContent;

      switch (this.resizeDirection) {
        case "middle-left": {
          // For middle-left, use negative effective delta
          newWidth = Math.max(10, this.startWidth - effectiveDelta);

          // Get the fixed right endpoint
          const rightPoint = rotate(
            this.startPosition.x + this.startWidth,
            this.startPosition.y + this.startHeight / 2,
            rotatedCenter[0],
            rotatedCenter[1],
            angleRad
          );

          // Calculate new left endpoint
          const newLeftPoint = rotate(
            this.startPosition.x + this.startWidth - newWidth,
            this.startPosition.y + this.startHeight / 2,
            rotatedCenter[0],
            rotatedCenter[1],
            angleRad
          );

          // Calculate new center between endpoints
          const newCenter = [
            (rightPoint[0] + newLeftPoint[0]) / 2,
            (rightPoint[1] + newLeftPoint[1]) / 2,
          ];

          // Get new position relative to fixed right point
          const [newX, newY] = rotate(
            rightPoint[0],
            rightPoint[1],
            newCenter[0],
            newCenter[1],
            -angleRad
          );

          // Update SVG content for the arrow

              if (this.element.shapeType === "arrow") {
                newSvgContent = this.updateArrowSvg(newWidth);
              } else {
                newSvgContent = this.updateSvgContent(this.element, newWidth, this.startHeight);
              }

          this.store.updateElement(this.element.id, {
            width: newWidth,
            x: newX - newWidth,
            y: newY - this.startHeight / 2,
            svgContent: newSvgContent,
          });
          break;
        }

        case "middle-right": {
          // For middle-right, use positive delta regardless of orientation
          newWidth = Math.max(10, this.startWidth + effectiveDelta);

          // Get the fixed left endpoint
          const leftPoint = rotate(
            this.startPosition.x,
            this.startPosition.y + this.startHeight / 2,
            rotatedCenter[0],
            rotatedCenter[1],
            angleRad
          );

          // Calculate new right endpoint
          const newRightPoint = rotate(
            this.startPosition.x + newWidth,
            this.startPosition.y + this.startHeight / 2,
            rotatedCenter[0],
            rotatedCenter[1],
            angleRad
          );

          // Calculate new center between endpoints
          const newCenter = [
            (leftPoint[0] + newRightPoint[0]) / 2,
            (leftPoint[1] + newRightPoint[1]) / 2,
          ];

          // Get new position relative to fixed left point
          const [newX, newY] = rotate(
            leftPoint[0],
            leftPoint[1],
            newCenter[0],
            newCenter[1],
            -angleRad
          );

          // Update SVG content for the arrow
        
          if (this.element.shapeType === "arrow") {
            newSvgContent = this.updateArrowSvg(newWidth);
          } else {
            newSvgContent = this.updateSvgContent(this.element, newWidth, this.startHeight);
          }


          this.store.updateElement(this.element.id, {
            width: newWidth,
            x: newX,
            y: newY - this.startHeight / 2,
            svgContent: newSvgContent,
          });
          break;
        }
      }
    },
    updateArrowSvg(width) {
      // Calculate where the arrow shaft should end
      const shaftEnd = width - 20; // Keep fixed 20px for arrow head

      return `<svg viewBox="0 0 ${width} 100" width="100%" height="100%" preserveAspectRatio="none">
    <g stroke="#3E57DA" stroke-width="4">
      <line x1="0" y1="50" x2="${shaftEnd}" y2="50"/>
      <path d="M${shaftEnd},35 L${width},50 L${shaftEnd},65 Z" 
            fill="#3E57DA" 
            stroke="none"/>
    </g>
  </svg>`;
    },
    handleVerticalResize(event) {
      if (!this.isResizing) return;

      const dy = (event.clientY - this.startY) / (this.$parent.zoom || 1);

      let newHeight = this.startHeight;
      let newY = this.startPosition.y;

      switch (this.resizeDirection) {
        case "top-left":
        case "top-right":
          newHeight = Math.max(10, this.startHeight - dy);
          newY = this.startPosition.y + (this.startHeight - newHeight);
          break;
        case "bottom-left":
        case "bottom-right":
          newHeight = Math.max(10, this.startHeight + dy);
          newY = this.startPosition.y;
          break;
      }

      this.store.updateElement(this.element.id, {
        height: newHeight,
        y: newY,
        // Keep width and x unchanged
        width: this.startWidth,
        x: this.startPosition.x,
      });
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

      // Get canvas dimensions from parent
      const canvasWidth = this.$parent.canvasWidth;
      const canvasHeight = this.$parent.canvasHeight;

      switch (this.resizeDirection) {
        case "bottom-right": {
          // Use the rotated delta for more natural resizing
          newWidth = Math.max(10, this.startWidth + rotatedDelta.x);
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

          // Constrain to canvas boundaries
          if (newX + newWidth > canvasWidth) {
            newWidth = canvasWidth - newX;
            newHeight = newWidth / aspectRatio;
          }
          
          if (newY + newHeight > canvasHeight) {
            newHeight = canvasHeight - newY;
            newWidth = newHeight * aspectRatio;
          }

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
          newWidth = Math.max(10, this.startWidth - rotatedDelta.x);
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

          // Constrain to canvas boundaries
          if (newX < 0) {
            const xDiff = -newX;
            newX = 0;
            newWidth = Math.max(10, newWidth - xDiff);
            newHeight = newWidth / aspectRatio;
          }
          
          if (newY < 0) {
            const yDiff = -newY;
            newY = 0;
            newHeight = Math.max(10, newHeight - yDiff);
            newWidth = newHeight * aspectRatio;
          }

          this.store.updateElementWithoutHistory(this.element.id, {
            width: newWidth,
            height: newHeight,
            x: newX,
            y: newY,
          });
          break;
        }
        case "top-right": {
          newWidth = Math.max(10, this.startWidth + rotatedDelta.x);
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
          newWidth = Math.max(10, this.startWidth - rotatedDelta.x);
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
          newHeight = Math.max(10, this.startHeight - rotatedDelta.y);
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
          newHeight = Math.max(10, this.startHeight + rotatedDelta.y);
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
          newWidth = Math.max(10, this.startWidth - rotatedDelta.x);
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
          newWidth = Math.max(10, this.startWidth + rotatedDelta.x);
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

      if (this.element.type === "shape") {
        const newSvgContent = this.updateSvgContent(
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
    updateSvgContent(element, newWidth, newHeight) {
      if (!element.svgContent || !element.shapeType) return null;

      const parser = new DOMParser();
      const doc = parser.parseFromString(element.svgContent, "image/svg+xml");
      const svgElement = doc.documentElement;

      // Set viewBox to match the element dimensions exactly
      svgElement.setAttribute("viewBox", `0 0 ${newWidth} ${newHeight}`);
      
      // Ensure the SVG fills the container
      svgElement.setAttribute("width", "100%");
      svgElement.setAttribute("height", "100%");
      svgElement.setAttribute("preserveAspectRatio", "none");

      switch (element.shapeType) {
        case "rectangle":
        case "roundedRectangle": {
          const rect = svgElement.querySelector("rect");
          if (rect) {
            // Make rectangle fill the entire SVG with no padding
            rect.setAttribute("x", "0");
            rect.setAttribute("y", "0");
            rect.setAttribute("width", newWidth);
            rect.setAttribute("height", newHeight);

            if (element.shapeType === "roundedRectangle") {
              const cornerRadius = Math.min(newWidth, newHeight) * 0.1;
              rect.setAttribute("rx", cornerRadius);
              rect.setAttribute("ry", cornerRadius);
            }
          }
          break;
        }

        case "square": {
          const rect = svgElement.querySelector("rect");
          if (rect) {
            // Make square fill the entire SVG with no padding
            rect.setAttribute("x", "0");
            rect.setAttribute("y", "0");
            rect.setAttribute("width", newWidth);
            rect.setAttribute("height", newHeight);
          }
          break;
        }

        case "circle": {
          const circle = svgElement.querySelector("circle");
          if (circle) {
            const centerX = newWidth / 2;
            const centerY = newHeight / 2;
            // Use 50% of the smallest dimension to ensure the circle fills the space
            const radius = Math.min(newWidth, newHeight) / 2;

            circle.setAttribute("cx", centerX);
            circle.setAttribute("cy", centerY);
            circle.setAttribute("r", radius);
          }
          break;
        }

        case "oval": {
          const ellipse = svgElement.querySelector("ellipse");
          if (ellipse) {
            const centerX = newWidth / 2;
            const centerY = newHeight / 2;
            // Use 50% of dimensions to ensure the oval fills the space completely
            const rx = newWidth / 2;
            const ry = newHeight / 2;

            ellipse.setAttribute("cx", centerX);
            ellipse.setAttribute("cy", centerY);
            ellipse.setAttribute("rx", rx);
            ellipse.setAttribute("ry", ry);
          }
          break;
        }

        case "arrow": {
          const path = svgElement.querySelector("path");
          if (path) {
            // Scale to fill entire space
            const arrowTip = newWidth;

            // Create arrow path with no padding
            const d = `M0 ${newHeight * 0.4} 
               L${newWidth * 0.7} ${newHeight * 0.4} 
               L${newWidth * 0.7} ${newHeight * 0.25} 
               L${arrowTip} ${newHeight * 0.5} 
               L${newWidth * 0.7} ${newHeight * 0.75} 
               L${newWidth * 0.7} ${newHeight * 0.6} 
               L0 ${newHeight * 0.6} Z`;

            path.setAttribute("d", d);
          }
          break;
        }

        case "horizontalArrow": {
          const path = svgElement.querySelector("path");
          if (path) {
            // Scale to fill entire space
            const arrowHeight = newHeight * 0.3;
            const centerY = newHeight * 0.5;
            const arrowTip = newWidth;

            // Create arrow path with no padding
            const d = `M0 ${centerY - arrowHeight / 2}
               L${newWidth * 0.75} ${centerY - arrowHeight / 2}
               L${newWidth * 0.75} ${centerY - arrowHeight}
               L${arrowTip} ${centerY}
               L${newWidth * 0.75} ${centerY + arrowHeight}
               L${newWidth * 0.75} ${centerY + arrowHeight / 2}
               L0 ${centerY + arrowHeight / 2} Z`;

            path.setAttribute("d", d);
          }
          break;
        }
        
        case "cloud": {
          const path = svgElement.querySelector("path");
          if (path) {
            // Scale cloud to fill entire space
            const scaleX = newWidth / 100;
            const scaleY = newHeight / 100;
            const d = [
              `M${25 * scaleX} ${50 * scaleY}`,
              `Q${5 * scaleX} ${50 * scaleY} ${5 * scaleX} ${35 * scaleY}`,
              `Q${5 * scaleX} ${15 * scaleY} ${25 * scaleX} ${15 * scaleY}`,
              `Q${25 * scaleX} ${5 * scaleY} ${40 * scaleX} ${5 * scaleY}`,
              `Q${60 * scaleX} ${5 * scaleY} ${60 * scaleX} ${15 * scaleY}`,
              `Q${80 * scaleX} ${15 * scaleY} ${80 * scaleX} ${35 * scaleY}`,
              `Q${80 * scaleX} ${50 * scaleY} ${60 * scaleX} ${50 * scaleY}`,
              "Z",
            ].join(" ");

            path.setAttribute("d", d);
          }
          break;
        }

        case "heart": {
          const path = svgElement.querySelector("path");
          if (path) {
            // Scale heart to fill entire space
            const scaleX = newWidth / 100;
            const scaleY = newHeight / 100;
            const d = [
              `M${50 * scaleX} ${95 * scaleY}`,
              `Q${25 * scaleX} ${70 * scaleY} ${5 * scaleX} ${40 * scaleY}`,
              `Q${0 * scaleX} ${25 * scaleY} ${0 * scaleX} ${15 * scaleY}`,
              `Q${0 * scaleX} ${0 * scaleY} ${20 * scaleX} ${0 * scaleY}`,
              `Q${35 * scaleX} ${0 * scaleY} ${50 * scaleX} ${20 * scaleY}`,
              `Q${65 * scaleX} ${0 * scaleY} ${80 * scaleX} ${0 * scaleY}`,
              `Q${100 * scaleX} ${0 * scaleY} ${100 * scaleX} ${15 * scaleY}`,
              `Q${100 * scaleX} ${25 * scaleY} ${95 * scaleX} ${40 * scaleY}`,
              `Q${75 * scaleX} ${70 * scaleY} ${50 * scaleX} ${95 * scaleY}`,
              "Z",
            ].join(" ");

            path.setAttribute("d", d);
          }
          break;
        }

        case "message": {
          const path = svgElement.querySelector("path");
          if (path) {
            // No padding for message bubble
            const tailHeight = newHeight * 0.15;

            const d = [
              `M0,0`, // Top left
              `H${newWidth}`, // Top right
              `V${newHeight - tailHeight}`, // Right side
              `H${newWidth * 0.6}`, // Right of tail
              `L${newWidth * 0.5},${newHeight}`, // Tail point
              `L${newWidth * 0.4},${newHeight - tailHeight}`, // Left of tail
              `H0`, // Left side
              "Z", // Close path
            ].join(" ");

            path.setAttribute("d", d);
          }
          break;
        }

        // case "line": {
        //   console.log(this.element, "this.element");
        //   const line = svgElement.querySelector("line");
        //   if (line) {
        //     // No padding for line
        //     line.setAttribute("x1", "0");
        //     line.setAttribute("y1", newHeight / 2);
        //     line.setAttribute("x2", newWidth);
        //     line.setAttribute("y2", newHeight / 2);
        //     // Adjust stroke width proportionally
        //     const strokeWidth = Math.max(
        //       2,
        //       Math.min(newWidth, newHeight) * 0.04
        //     );
        //     line.setAttribute("stroke-width", strokeWidth);
        //   }
        //   break;
        // }

        case "triangle": {
          const path = svgElement.querySelector("path");
          if (path) {
            // No padding for triangle
            const points = [
              `${newWidth / 2},0`,
              `${newWidth},${newHeight}`,
              `0,${newHeight}`,
            ];
            path.setAttribute(
              "d",
              `M${points[0]} L${points[1]} L${points[2]} Z`
            );
          }
          break;
        }

        case "pentagon":
        case "hexagon":
        case "octagon": {
          const path = svgElement.querySelector("path");
          if (path) {
            const centerX = newWidth / 2;
            const centerY = newHeight / 2;
            // Use 50% of the smallest dimension to fill the space completely
            const radius = Math.min(newWidth, newHeight) / 2;
            const points = this.generatePolygonPoints(
              element.shapeType === "pentagon"
                ? 5
                : element.shapeType === "hexagon"
                ? 6
                : 8,
              centerX,
              centerY,
              radius
            );
            path.setAttribute("d", `M${points.join(" L")} Z`);
          }
          break;
        }

        case "star": {
          const path = svgElement.querySelector("path");
          if (path) {
            const centerX = newWidth / 2;
            const centerY = newHeight / 2;
            // Use 50% of the smallest dimension to fill the space completely
            const outerRadius = Math.min(newWidth, newHeight) / 2;
            const innerRadius = outerRadius * 0.5;
            const points = this.generateStarPoints(
              5,
              centerX,
              centerY,
              outerRadius,
              innerRadius
            );
            path.setAttribute("d", `M${points.join(" L")} Z`);
          }
          break;
        }
      }

      return new XMLSerializer().serializeToString(svgElement);
    },

    generatePolygonPoints(sides, centerX, centerY, radius) {
      const points = [];
      const angleStep = (Math.PI * 2) / sides;

      for (let i = 0; i < sides; i++) {
        const angle = i * angleStep - Math.PI / 2; // Start from top
        const x = centerX + radius * Math.cos(angle);
        const y = centerY + radius * Math.sin(angle);
        points.push(`${x},${y}`);
      }

      return points;
    },

    generateStarPoints(points, centerX, centerY, outerRadius, innerRadius) {
      const starPoints = [];
      const angleStep = (Math.PI * 2) / points;

      for (let i = 0; i < points * 2; i++) {
        const angle = (i * angleStep) / 2 - Math.PI / 2;
        const radius = i % 2 === 0 ? outerRadius : innerRadius;
        const x = centerX + radius * Math.cos(angle);
        const y = centerY + radius * Math.sin(angle);
        starPoints.push(`${x},${y}`);
      }

      return starPoints;
    },
    adjustRectangle(rectangle, bottomRightX, bottomRightY, angle) {
      const center = [
        rectangle.x + rectangle.width / 2,
        rectangle.y + rectangle.height / 2,
      ];
      const rotatedA = rotate(rectangle.x, rectangle.y, cx, cy);
      const newCenter = [
        (rotatedA[0] + bottomRightX) / 2,
        (rotatedA[1] + bottomRightY) / 2,
      ];
      const newTopLeft = thisrotate(
        rotatedA[0],
        rotatedA[1],
        newCenter[0],
        newCenter[1],
        -angle
      );
      const newBottomRight = rotate(
        bottomRightX,
        bottomRightY,
        newCenter[0],
        newCenter[1],
        -angle
      );

      rectangle.x = newTopLeft[0];
      rectangle.y = newTopLeft[1];
      rectangle.width = newBottomRight[0] - newTopLeft[0];
      rectangle.height = newBottomRight[1] - newTopLeft[1];
    },
    updateSvgDimensions(element, width, height) {
      if (!element.svgContent) return null;

      const parser = new DOMParser();
      const doc = parser.parseFromString(element.svgContent, "image/svg+xml");
      const svgElement = doc.documentElement;

      // Get the current viewBox values
      let [minX, minY, vWidth, vHeight] = (
        svgElement.getAttribute("viewBox") || "0 0 100 100"
      )
        .split(" ")
        .map(Number);

      // Maintain aspect ratio
      const aspectRatio = vWidth / vHeight;
      const newAspectRatio = width / height;

      if (Math.abs(aspectRatio - newAspectRatio) > 0.01) {
        // Adjust viewBox to maintain aspect ratio
        if (newAspectRatio > aspectRatio) {
          vWidth = vHeight * newAspectRatio;
        } else {
          vHeight = vWidth / newAspectRatio;
        }
      }

      // Update the viewBox with the new dimensions
      svgElement.setAttribute(
        "viewBox",
        `${minX} ${minY} ${vWidth} ${vHeight}`
      );

      // Update any shape-specific elements
      const shapeElement = svgElement.querySelector(
        "path, rect, circle, ellipse, polygon"
      );
      if (shapeElement) {
        // For circles, update radius and center
        if (element.shapeType === "circle") {
          const circle = svgElement.querySelector("circle");
          if (circle) {
            const r = Math.min(vWidth, vHeight) / 2;
            circle.setAttribute("cx", vWidth / 2);
            circle.setAttribute("cy", vHeight / 2);
            circle.setAttribute("r", r * 0.8); // 80% of possible radius for padding
          }
        }

        // For rectangles, update width and height
        else if (
          element.shapeType === "rectangle" ||
          element.shapeType === "roundedRectangle"
        ) {
          const rect = svgElement.querySelector("rect");
          if (rect) {
            rect.setAttribute("width", vWidth * 0.8);
            rect.setAttribute("height", vHeight * 0.8);
            rect.setAttribute("x", vWidth * 0.1);
            rect.setAttribute("y", vHeight * 0.1);
          }
        }

        // For other shapes using paths, scale the path data
        else if (shapeElement.tagName === "path") {
          const pathData = shapeElement.getAttribute("d");
          if (pathData) {
            const scaledPath = this.scalePathData(
              pathData,
              vWidth / 100,
              vHeight / 100
            );
            shapeElement.setAttribute("d", scaledPath);
          }
        }
      }

      return new XMLSerializer().serializeToString(svgElement);
    },
    scalePathData(pathData, scaleX, scaleY) {
      return pathData.replace(/([0-9]+(?:\.[0-9]*)?)/g, (match, p1) => {
        const num = parseFloat(p1);
        const scaled = num * (pathData.indexOf(match) % 2 ? scaleY : scaleX);
        return scaled.toFixed(2);
      });
    },

    stopResize(resizeHandler) {
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
              svgContent: this.element.svgContent,
              rotation: this.element.rotation,
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
      document.removeEventListener("mousemove", resizeHandler);
      document.removeEventListener("mouseup", this.stopResize);
    },

    startRotate(event) {
      // Prevent rotation if the element is locked
      if (this.element.locked) return;

      event.stopPropagation();

      if (this._rotateRAF) {
        cancelAnimationFrame(this._rotateRAF);
      }
      this.isRotating = true;
      this._rotateRAF = requestAnimationFrame(() => {
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
      });
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
      let deltaRotation = ((delta * 180) / Math.PI) * 0.9;
      let newRotation = this.initialRotation + deltaRotation;
      newRotation = ((newRotation % 360) + 360) % 360;

      // Apply angle snapping to all shapes
      // Define snap angles (in degrees)
      const snapAngles = [0, 90, 180, 270];
      
      // Use a more aggressive threshold for line/arrow shapes,
      // and a gentler threshold for other shapes
      const snapThreshold = 2
      // Check if we're close to a snap angle
      for (const snapAngle of snapAngles) {
        // Calculate the difference between current angle and snap angle
        let difference = Math.abs(newRotation - snapAngle);
        // Account for circular angles (e.g., difference between 355° and 0° should be 5°, not 355°)
        difference = Math.min(difference, 360 - difference);
        
        if (difference < snapThreshold) {
          newRotation = snapAngle;
          
          // Provide some visual feedback when snapping
          if (!this.$el.classList.contains('snapped-rotation')) {
            this.$el.classList.add('snapped-rotation');
            setTimeout(() => {
              this.$el.classList.remove('snapped-rotation');
            }, 100);
          }
          break; // Exit the loop once we've found a snap angle
        }
      }

      // Update element rotation
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

    handleGlobalClick(event) {
      // Only clear selection if clicking outside any shape element
      const clickedShape = event.target.closest(".shape-element");
      if (!clickedShape) {
        this.store.selectedElementIds = [];
        this.store.selectedElementId = null;
        this.store.selectedElement = {};
        this.isSelected = false;
      }
    },
    getHandleCursor(position) {
      return this.resizeHandleCursors[position] || "default";
    },
  },

  mounted() {
    // document.addEventListener("click", this.handleGlobalClick);
    this.rotationCache = {
      cos: Math.cos(this.element.rotation || 0),
      sin: Math.sin(this.element.rotation || 0),
    };
  },

  beforeUnmount() {
    if (this._transformRAF) {
      cancelAnimationFrame(this._transformRAF);
    }
    if (this._rotateRAF) {
      cancelAnimationFrame(this._rotateRAF);
    }
  },
};
</script>
<style scoped>
.shape-element {
  width: 100%;
  height: 100%;
  position: relative;
  user-select: none;
  touch-action: none;
  transform-origin: center center;
  will-change: transform;
  transform-style: preserve-3d;
}

.svg-wrapper {
  width: 100%;
  height: 100%;
  display: block;
  position: relative;
  overflow: visible;
  transform-style: preserve-3d;
}

.svg-wrapper :deep(svg) {
  width: 100%;
  height: 100%;
  display: block;
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  transform-style: preserve-3d;
  overflow: visible;
}

/* Selection state */
.shape-element.selected {
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

/* Show handles on hover/selection */
.shape-element:hover .resize-handle,
.shape-element.selected .resize-handle {
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

/* Special handles for arrows/lines */
.resize-handle.middle-left {
  top: 50%;
  left: -6px;
  transform: translateY(-50%);
}

.resize-handle.middle-right {
  top: 50%;
  right: -6px;
  transform: translateY(-50%);
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

.shape-element:hover .rotate-handle,
.shape-element.selected .rotate-handle {
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
.guide-line {
  background-color: transparent;
  border: 1px dashed #4a90e2;
  pointer-events: none;
  position: absolute;
  z-index: 1000;
}

/* Angle snapping indicator */
.snapped-rotation {
  box-shadow: 0 0 8px rgba(62, 87, 218, 0.5);
  transition: outline 0.15s ease-in, box-shadow 0.15s ease-in;
}

/* Display snap angles visually */
.snapped-rotation::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  border-radius: 4px;
  pointer-events: none;
  animation: snapFeedback 0.3s ease-out;
}

/* Add a snapping guide line */
.snapped-rotation::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  border-left: 1px dashed #3E57DA;
  animation: showSnapGuide 0.2s ease-out forwards;
  transform-origin: center;
  pointer-events: none;
  opacity: 0.7;
}

@keyframes showSnapGuide {
  0% { width: 0; height: 0; }
  100% { width: 300px; height: 2px; transform: translate(-50%, -50%); }
}

@keyframes snapFeedback {
  0% { transform: scale(1); opacity: 0.7; }
  100% { transform: scale(1.05); opacity: 0; }
}
</style>