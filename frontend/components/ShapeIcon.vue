<template>
  <svg :viewBox="viewBox" :width="size" :height="size" class="shape-svg">
    <component :is="shapeComponent" />
  </svg>
</template>

<script>
import { h, computed } from "vue";

export default {
  name: "ShapeIcon",
  props: {
    type: {
      type: String,
      required: true,
    },
    size: {
      type: [Number, String],
      default: 24,
    },
    color: {
      type: String,
      default: "currentColor",
    },
    fillColor: {
      type: String,
      default: "none",
    },
    strokeWidth: {
      type: [String, Number],
      default: 2,
    },
    viewBox: {
      type: String,
      default: "0 0 24 24",
    },
    variant: {
      type: String,
      default: "outlined", // 'outlined' or 'filled'
      validator: (value) => ["outlined", "filled"].includes(value),
    },
  },
  setup(props) {
    const getShapeProps = (specificProps = {}) => ({
      stroke: props.color,
      "stroke-width": props.strokeWidth,
      fill: props.variant === "filled" ? props.color : props.fillColor,
      ...specificProps,
    });

    const shapes = {
      // Basic shapes - squares and rectangles
      Square: () =>
        h(
          "rect",
          getShapeProps({
            x: "4",
            y: "4",
            width: "16",
            height: "16",
            rx: "0",
          })
        ),
      RoundedSquare: () =>
        h(
          "rect",
          getShapeProps({
            x: "4",
            y: "4",
            width: "16",
            height: "16",
            rx: "4",
          })
        ),
      Rectangle: () =>
        h(
          "rect",
          getShapeProps({
            x: "2",
            y: "6",
            width: "20",
            height: "12",
            rx: "0",
          })
        ),
      RoundedRectangle: () =>
        h(
          "rect",
          getShapeProps({
            x: "2",
            y: "6",
            width: "20",
            height: "12",
            rx: "3",
          })
        ),

      // Circles and ovals
      Circle: () =>
        h(
          "circle",
          getShapeProps({
            cx: "12",
            cy: "12",
            r: "8",
          })
        ),
      Oval: () =>
        h(
          "ellipse",
          getShapeProps({
            cx: "12",
            cy: "12",
            rx: "10",
            ry: "6",
          })
        ),

      // Triangles
      Triangle: () =>
        h(
          "path",
          getShapeProps({
            d: "M12 4 L20 20 L4 20 Z",
          })
        ),
      RightTriangle: () =>
        h(
          "path",
          getShapeProps({
            d: "M4 4 L20 4 L4 20 Z",
          })
        ),

      // Polygons
      Pentagon: () =>
        h(
          "path",
          getShapeProps({
            d: "M12 3 L21 10 L17 21 L7 21 L3 10 Z",
          })
        ),
      Hexagon: () =>
        h(
          "path",
          getShapeProps({
            d: "M7 4 L17 4 L20 12 L17 20 L7 20 L4 12 Z",
          })
        ),
      Octagon: () =>
        h(
          "path",
          getShapeProps({
            d: "M8 3 L16 3 L21 8 L21 16 L16 21 L8 21 L3 16 L3 8 Z",
          })
        ),

      // Stars
      Star: () =>
        h(
          "path",
          getShapeProps({
            d: "M12 3 L14.5 8.5 L20 9.5 L16 14 L17 19.5 L12 17 L7 19.5 L8 14 L4 9.5 L9.5 8.5 Z",
          })
        ),
      StarOutline: () =>
        h(
          "path",
          getShapeProps({
            d: "M12 4 L14 9 L19 9.5 L15.5 13.5 L16.5 18.5 L12 16 L7.5 18.5 L8.5 13.5 L5 9.5 L10 9 Z",
          })
        ),

      // Lines
      Line: () =>
        h(
          "line",
          getShapeProps({
            x1: "4",
            y1: "12",
            x2: "20",
            y2: "12",
          })
        ),
      DiagonalLine: () =>
        h(
          "line",
          getShapeProps({
            x1: "4",
            y1: "4",
            x2: "20",
            y2: "20",
          })
        ),
      BackDiagonalLine: () =>
        h(
          "line",
          getShapeProps({
            x1: "20",
            y1: "4",
            x2: "4",
            y2: "20",
          })
        ),
      ArrowRight: () =>
        h("g", getShapeProps(), [
          h("line", {
            x1: "4",
            y1: "12",
            x2: "18",
            y2: "12",
            stroke: props.color,
            "stroke-width": props.strokeWidth,
          }),
          h("path", {
            d: "M14 8 L18 12 L14 16",
            fill: "none",
            stroke: props.color,
            "stroke-width": props.strokeWidth,
          }),
        ]),
    };

    const shapeComponent = computed(() => shapes[props.type] || null);

    return {
      shapeComponent,
    };
  },
};
</script>