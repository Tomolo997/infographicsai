<template>
  <div class="line-animation">
    <svg ref="svg" :width="width" :height="height"></svg>
    <button @click="startAnimation" :disabled="isAnimating">
      {{ isAnimating ? 'Animating...' : 'Start Animation' }}
    </button>
  </div>
</template>

<script>
import * as d3 from 'd3';

export default {
  name: 'GrowingLineAnimation',
  data() {
    return {
      width: 600,
      height: 400,
      isAnimating: false,
      startPoint: { x: 100, y: 200 },
      endPoint: { x: 500, y: 200 },
      duration: 2000, // Animation duration in milliseconds
    };
  },
  mounted() {
    this.initializeSVG();
  },
  methods: {
    initializeSVG() {
      this.svg = d3.select(this.$refs.svg);
      this.line = this.svg.append('line')
        .attr('x1', this.startPoint.x)
        .attr('y1', this.startPoint.y)
        .attr('x2', this.startPoint.x)
        .attr('y2', this.startPoint.y)
        .attr('stroke', 'black')
        .attr('stroke-width', 2);
    },
    startAnimation() {
      if (this.isAnimating) return;
      this.isAnimating = true;

      this.line
        .attr('x1', this.startPoint.x)
        .attr('y1', this.startPoint.y)
        .attr('x2', this.startPoint.x)
        .attr('y2', this.startPoint.y)
        .transition()
        .duration(this.duration)
        .attr('x2', this.endPoint.x)
        .attr('y2', this.endPoint.y)
        .on('end', () => {
          this.isAnimating = false;
        });
    }
  }
};
</script>

<style scoped>
.line-animation {
  display: flex;
  flex-direction: column;
  align-items: center;
}

button {
  margin-top: 20px;
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
}

button:disabled {
  cursor: not-allowed;
}
</style>