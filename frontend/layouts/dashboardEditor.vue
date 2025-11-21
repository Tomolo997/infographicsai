<template>
    <div class="app-layout w-full">
    <LeftSideBar></LeftSideBar>
    <div class="w-full">
      <Navigation></Navigation>
      <slot></slot>
    </div>
  </div>
</template>

<script>
export default {
  setup() {
    useHead({
      title: 'Dashboard | Ainfographic',
      meta: [
        { name: 'description', content: 'This is the dashboard of Ainfographic.' },
        { property: 'og:title', content: 'Dashboard | Ainfographic' },
        { property: 'og:description', content: 'This is the dashboard of Ainfographic.' },
        { property: 'og:image', content: 'https://images.ainfographic.com/opengraph.png' },
        { property: 'og:url', content: 'https://yourdomain.com/dashboard' },
        { name: 'twitter:card', content: 'summary_large_image' },
        { name: 'twitter:title', content: 'Dashboard | Ainfographic' },
        { name: 'twitter:description', content: 'This is the dashboard of Ainfographic.' },
        { name: 'twitter:image', content: 'https://images.ainfographic.com/opengraph.png' }
      ],
      link: [
        { rel: 'icon', type: 'image/x-icon', href: '/favicon.svg' }
      ]
    });
  }
};



</script>

<style scoped>
.app-layout {
    display: flex;
    flex-direction: row;
    height: 100vh;
    background-repeat: repeat;
    background-size: 100px 100px; /* Adjust this value to match the size of your SVG */
}

.page-content {
    flex: 1;
    overflow-y: auto;
    max-height: 100vh;
}

</style>
