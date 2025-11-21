<template>
  <NuxtLink
    :to="to"
    :class="['custom-link', `link-${type}`, { 'is-square': square }]"
    :target="external ? '_blank' : undefined"
    :rel="external ? 'noopener noreferrer' : undefined"
  >
    <span v-if="icon" class="icon" :class="icon"></span>
    <span class="link-text"><slot></slot></span>
  </NuxtLink>
</template>

<script>
export default {
  name: 'CustomLink',
  props: {
    to: {
      type: [String, Object],
      required: true
    },
    type: {
      type: String,
      default: 'primary',
      validator: value => ['primary', 'secondary', 'secondary-light', 'secondary-white', 'new'].includes(value)
    },
    icon: String,
    square: Boolean,
    external: Boolean
  }
}
</script>

<style scoped>
.custom-link {
  font-family: "Basier Square Regular", sans-serif;
  font-size: 13px;
  border-radius: 8px;
  cursor: pointer;
  padding: 8px 16px;
  transition: all 0.3s ease;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  text-decoration: none;
}

.link-primary {
  background-color: #2B2E400F;
  color: #050506F5;
  font-weight: 600;
}

.link-primary:hover {
  background-color: #0404061E;
}

.link-secondary {
  background-color: #3E57DA;
  color: white;
}

.link-secondary:hover {
  background-color: #3A4FBB;
}

.link-secondary-light {
  background-color: #3D5BFB21;
  color: #3E57DA;
}

.link-secondary-light:hover {
  background-color: #3D5BFB40;
}

.link-secondary-white {
  background-color: white;
  color: #3E57DA;
  border: 1px solid #3E57DA;
}

.link-secondary-white:hover {
  background-color: #F0F0FF;
}

.link-new {
  background-color: #FF6B6B;
  color: white;
  font-weight: bold;
  text-transform: uppercase;
  letter-spacing: 1px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.link-new:hover {
  background-color: #FF8787;
  transform: translateY(-2px);
  box-shadow: 0 6px 8px rgba(0, 0, 0, 0.15);
}

.link-new:active {
  transform: translateY(0);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.is-square {
  width: 45px;
  height: 45px;
  padding: 0;
}

.icon {
  margin-right: 8px;
}

@media (min-width: 768px) {
  .custom-link {
    font-size: 15px;
  }
}
</style>