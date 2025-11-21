<template>
  <div class="p-8 space-y-4">
    <!-- Button to open single column modal -->
    <button
      @click="isSingleColumnModalOpen = true"
      class="px-6 py-3 bg-primary-600 hover:bg-primary-700 text-white rounded-lg transition-colors font-medium mr-4"
    >
      Open Single Column Modal
    </button>

    <!-- Button to open two column modal -->
    <button
      @click="isTwoColumnModalOpen = true"
      class="px-6 py-3 bg-primary-600 hover:bg-primary-700 text-white rounded-lg transition-colors font-medium"
    >
      Open Two Column Modal
    </button>

    <!-- Single Column Modal -->
    <Modal
      :is-open="isSingleColumnModalOpen"
      layout="single-column"
      title="Single Column Modal"
      subtitle="This modal has a single column layout"
      @close="isSingleColumnModalOpen = false"
    >
      <template #body>
        <p class="text-text-secondary mb-4">
          This is the body content of the modal. You can put any content here,
          including forms, text, images, or other components.
        </p>
        <p class="text-text-secondary">
          The modal uses card colors from your Tailwind config and has a blurred
          background for a modern look.
        </p>
      </template>

      <template #cta>
        <div class="flex gap-3 justify-end">
          <button
            @click="isSingleColumnModalOpen = false"
            class="px-4 py-2 border border-card-border text-text-primary hover:bg-white/5 rounded-lg transition-colors"
          >
            Cancel
          </button>
          <button
            @click="handleSingleConfirm"
            class="px-4 py-2 bg-primary-600 hover:bg-primary-700 text-white rounded-lg transition-colors"
          >
            Confirm
          </button>
        </div>
      </template>
    </Modal>

    <!-- Two Column Modal -->
    <Modal
      :is-open="isTwoColumnModalOpen"
      layout="two-column"
      title="Two Column Modal"
      subtitle="This modal has a two column layout"
      @close="isTwoColumnModalOpen = false"
    >
      <template #left>
        <h3 class="text-lg font-semibold mb-3">Left Column</h3>
        <p class="text-text-secondary mb-4">
          This is the left side of the modal. You can put forms, descriptions,
          or any other content here.
        </p>
        <div class="space-y-3">
          <div>
            <label class="block text-sm font-medium mb-1">Name</label>
            <input
              type="text"
              class="w-full px-3 py-2 bg-background-primary border border-card-border rounded-lg text-text-primary focus:outline-none focus:ring-2 focus:ring-primary-600"
              placeholder="Enter name"
            />
          </div>
          <div>
            <label class="block text-sm font-medium mb-1">Email</label>
            <input
              type="email"
              class="w-full px-3 py-2 bg-background-primary border border-card-border rounded-lg text-text-primary focus:outline-none focus:ring-2 focus:ring-primary-600"
              placeholder="Enter email"
            />
          </div>
        </div>
      </template>

      <template #right>
        <h3 class="text-lg font-semibold mb-3">Right Column</h3>
        <p class="text-text-secondary mb-4">
          This is the right side of the modal. Perfect for previews, additional
          information, or contextual help.
        </p>
        <div class="bg-background-primary border border-card-border rounded-lg p-4">
          <h4 class="font-medium mb-2">Preview</h4>
          <p class="text-sm text-text-secondary">
            Your content preview will appear here. The two-column layout is
            great for forms with live previews or side-by-side comparisons.
          </p>
        </div>
      </template>

      <template #cta>
        <div class="flex gap-3 justify-end">
          <button
            @click="isTwoColumnModalOpen = false"
            class="px-4 py-2 border border-card-border text-text-primary hover:bg-white/5 rounded-lg transition-colors"
          >
            Cancel
          </button>
          <button
            @click="handleTwoColumnConfirm"
            class="px-4 py-2 bg-primary-600 hover:bg-primary-700 text-white rounded-lg transition-colors"
          >
            Confirm
          </button>
        </div>
      </template>
    </Modal>
  </div>
</template>

<script>
export default {
  data() {
    return {
      isSingleColumnModalOpen: false,
      isTwoColumnModalOpen: false,
    }
  },
  methods: {
    handleSingleConfirm() {
      console.log('Single column modal confirmed!')
      this.isSingleColumnModalOpen = false
    },
    handleTwoColumnConfirm() {
      console.log('Two column modal confirmed!')
      this.isTwoColumnModalOpen = false
    },
  },
}
</script>

