<template>
  <section id="faq" class="w-full max-w-4xl mx-auto py-16 px-4 mt-12 bg-white">
    <h3 class="text-center text-blue-600 font-medium mb-2">Got questions?</h3>
    <h2 class="text-center text-4xl font-bold mb-4">Frequently Asked Questions</h2>
    <p class="text-center text-gray-600 mb-12">Here are some of the questions you might have about DataGIF.io.</p>
    
    <div class="space-y-4">
      <div v-for="(item, index) in faqItems" :key="index" class="border-b border-gray-200">
        <button
          @click="toggleItem(index)"
          class="flex justify-between items-center w-full py-4 text-left"
        >
          <span class="text-lg font-medium text-gray-900">{{ item.question }}</span>
          <svg
            class="w-5 h-5 text-gray-500 transform transition-transform duration-200"
            :class="{ 'rotate-180': item.isOpen }"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
          </svg>
        </button>
        <div
          v-show="item.isOpen"
          class="pb-4 prose prose-sm max-w-none"
          v-html="item.answer"
        ></div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref } from 'vue'

const faqItems = ref([
  {
    question: 'How do I format the CSV, Excel files?',
    answer: `
    <span class="font-bold">Colmns </span><br/>
    <p class="ml-2"> Your CSV, Excel should have two columns: one for X (dates, numbers, strings), and another for Y (numbers or strings). The first row should contain column headers. </p><br/>
    <span class="font-bold">File name  </span><br/>
    <p class="ml-2"> Name your CSV, Excel file exactly as you want the chart title to appear. For example, if you want your chart to be titled "Global ChatGPT Usage 2023", save your CSV file as "Global ChatGPT Usage 2023.csv". The filename (without the .csv extension) will become your chart title automatically. </p> 
    `,
    isOpen: false
  },
  {
    question: 'What can I customise?',
    answer: 'You can customize colors, chart type, animation speed, gradient background. Detailed options are available in the chart editor.',
    isOpen: false
  },
  {
    question: 'Where can I use DataGIFs?',
    answer: 'DataGIFs can be used on social media platforms, in presentations, embedded in websites, or anywhere you can share animated images.',
    isOpen: false
  },
  {
    question: 'How do credits work?',
    answer: 'Each DataGIF creation uses one credit. Credits are purchased separately.',
    isOpen: false
  }
])

const toggleItem = (index) => {
  faqItems.value[index].isOpen = !faqItems.value[index].isOpen
}
</script>