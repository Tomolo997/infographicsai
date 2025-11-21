<template>
  <div class="container mx-auto mt-12 px-16 w-full xl:w-[1000px] py-16 rounded-md bg-white">
    <div class="flex flex-col md:flex-row">
      <div class="md:w-1/2 mb-6 flex flex-col justify-center md:mb-0">
        <h2 class="text-5xl font-bold mb-4">Engage your audience across platforms</h2>
        <p class="text-2xl text-left w-[300px]">
          Increase engagement on <span class="font-bold">socials</span>, bring your  <span class="font-bold">website</span> to life, or make your  <span class="font-bold">presentation</span> sing.
        </p>
      </div>
      <div class="md:w-1/2 md:pl-8">
        <div v-for="(item, index) in items" :key="index" class="mb-12">
          <div class="flex items-center mb-2">
            <div class="">
             <LightningBoldCircleIcon class="text-purple-500 mr-4"  size="50" fill="bg-purple-400"/>
            </div>
            <h3 v-html="item.title" class="text-2xl font-semibold"></h3>
          </div>
          <p v-html="item.description" class="text-gray-600 pl-16"></p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'GraphsSellStory',
  data() {
    return {
      items: [
        {
          title: 'Capture attention on <br> social media',
          description: 'Turn data into scroll-stopping content that resonates. Watch your <span class="font-bold">engagement</span> soar with informative, eye-catching animations.'
        },
        {
          title: 'Bring your website <br> to life',
          description: 'Breathe life into your web pages with dynamic data visualizations. Keep visitors <span class="font-bold">hooked</span> and boost time-on-site.'
        },
        {
          title: 'Captivating presentations',
          description: 'Say goodbye to boring slides. Our animated graphs make complex data accessible and <span class="font-bold">memorable</span>.'
        }
      ]
    }
  }
}
</script>

<style scoped>
.container{
}
/* Add any additional styles here if needed */
</style>