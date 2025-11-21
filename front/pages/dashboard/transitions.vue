<template>
  <ClientOnly>
    <div class="main-container">
      <div class="w-full max-w-7xl">
        <!-- Header -->
        <div class="mb-8">
          <h1 class="text-4xl font-bold mb-2">My Transitions</h1>
          <p class="text-text-secondary text-lg">
            View and manage all your created transitions
          </p>
        </div>

        <!-- Loading State -->
        <div v-if="loading" class="flex justify-center items-center py-20">
          <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
        </div>

        <!-- Error State -->
        <div v-else-if="error" class="bg-red-500/10 border border-red-500/20 rounded-lg p-6 text-center">
          <p class="text-red-500 text-lg">{{ error }}</p>
          <button @click="fetchTransitions" class="btn-primary mt-4">
            Try Again
          </button>
        </div>

        <!-- Empty State -->
        <div v-else-if="transitions.length === 0" class="bg-card-bg border border-card-border rounded-lg p-12 text-center">
          <div class="mb-6">
            <svg
              class="w-24 h-24 mx-auto text-text-secondary opacity-50"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z"
              />
            </svg>
          </div>
          <h2 class="text-2xl font-semibold mb-2">No transitions yet</h2>
          <p class="text-text-secondary mb-6">
            Create your first evolution video to get started
          </p>
          <button @click="navigateTo('/dashboard/create/evolution')" class="btn-primary">
            Create Transition
          </button>
        </div>

        <!-- Transitions Grid -->
        <div v-else class="space-y-6">
          <!-- Filter and Sort -->
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-4">
              <span class="text-text-secondary">
                {{ transitions.length }} transition{{ transitions.length === 1 ? '' : 's' }}
              </span>
            </div>
            <div class="flex items-center gap-2">
              <button 
                @click="viewMode = 'grid'" 
                :class="[
                  'p-2 rounded-lg transition-colors',
                  viewMode === 'grid' ? 'bg-primary text-white' : 'bg-card-bg text-text-secondary hover:bg-card-border'
                ]"
              >
                <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M3 3h8v8H3V3zm10 0h8v8h-8V3zM3 13h8v8H3v-8zm10 0h8v8h-8v-8z"/>
                </svg>
              </button>
              <button 
                @click="viewMode = 'list'" 
                :class="[
                  'p-2 rounded-lg transition-colors',
                  viewMode === 'list' ? 'bg-primary text-white' : 'bg-card-bg text-text-secondary hover:bg-card-border'
                ]"
              >
                <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M3 4h18v2H3V4zm0 7h18v2H3v-2zm0 7h18v2H3v-2z"/>
                </svg>
              </button>
            </div>
          </div>

          <!-- Grid View -->
          <div v-if="viewMode === 'grid'" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div
              v-for="transition in transitions"
              :key="transition.id"
              class="bg-card-bg border border-card-border rounded-lg overflow-hidden hover:shadow-lg transition-all duration-300 group"
            >
              <!-- Video/Image Preview -->
              <div class="relative aspect-video bg-background-secondary overflow-hidden">
                <video
                  v-if="transition.video_url"
                  :src="transition.video_url"
                  class="w-full h-full object-cover"
                  controls
                  preload="metadata"
                ></video>
                <div v-else-if="transition.front_image" class="relative w-full h-full">
                  <img
                    :src="transition.front_image"
                    :alt="transition.name || 'Transition'"
                    class="w-full h-full object-cover"
                  />
                  <div class="absolute inset-0 bg-black/40 flex items-center justify-center">
                    <span class="text-white text-sm font-medium">No Video Generated</span>
                  </div>
                </div>
                <div v-else class="w-full h-full flex items-center justify-center text-text-secondary">
                  <svg class="w-16 h-16 opacity-50" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z"
                    />
                  </svg>
                </div>

                <!-- Status Badge -->
                <div class="absolute top-2 right-2">
                  <span
                    :class="[
                      'px-2 py-1 text-xs font-medium rounded-full',
                      transition.video_url
                        ? 'bg-green-500/20 text-green-400 border border-green-500/30'
                        : 'bg-yellow-500/20 text-yellow-400 border border-yellow-500/30'
                    ]"
                  >
                    {{ transition.video_url ? 'Complete' : 'Pending' }}
                  </span>
                </div>
              </div>

              <!-- Card Content -->
              <div class="p-4">
                <h3 class="font-semibold text-lg mb-2 line-clamp-1">
                  {{ transition.name || `Transition #${transition.id}` }}
                </h3>
                
                <div class="space-y-2 mb-4">
                  <div class="flex items-center text-sm text-text-secondary">
                    <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
                    </svg>
                    <span class="capitalize">{{ formatTransitionType(transition.transition_type) }}</span>
                  </div>
                  
                  <div class="flex items-center text-sm text-text-secondary">
                    <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    <span>{{ transition.duration }}s duration</span>
                  </div>

                  <div class="flex items-center text-sm text-text-secondary">
                    <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                    </svg>
                    <span>{{ formatDate(transition.created_at) }}</span>
                  </div>
                </div>

                <!-- Action Buttons -->
                <div class="flex items-center gap-2">
                  <button
                    v-if="!transition.video_url"
                    @click="regenerateVideo(transition.id)"
                    :disabled="regenerating[transition.id]"
                    class="flex-1 px-3 py-2 bg-primary text-white rounded-lg text-sm font-medium hover:bg-primary/90 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    {{ regenerating[transition.id] ? 'Generating...' : 'Generate Video' }}
                  </button>
                  <button
                    v-if="transition.video_url"
                    @click="downloadVideo(transition.video_url, transition.name)"
                    class="flex-1 px-3 py-2 bg-primary text-white rounded-lg text-sm font-medium hover:bg-primary/90 transition-colors"
                  >
                    Download
                  </button>
                  <button
                    @click="openDeleteModal(transition)"
                    class="px-3 py-2 bg-red-500/10 text-red-500 rounded-lg text-sm font-medium hover:bg-red-500/20 transition-colors border border-red-500/20"
                  >
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                    </svg>
                  </button>
                </div>
              </div>
            </div>
          </div>

          <!-- List View -->
          <div v-else class="space-y-4">
            <div
              v-for="transition in transitions"
              :key="transition.id"
              class="bg-card-bg border border-card-border rounded-lg p-4 hover:shadow-lg transition-all duration-300 flex items-center gap-4"
            >
              <!-- Thumbnail -->
              <div class="w-32 h-20 bg-background-secondary rounded overflow-hidden flex-shrink-0">
                <video
                  v-if="transition.video_url"
                  :src="transition.video_url"
                  class="w-full h-full object-cover"
                  preload="metadata"
                ></video>
                <img
                  v-else-if="transition.front_image"
                  :src="transition.front_image"
                  :alt="transition.name || 'Transition'"
                  class="w-full h-full object-cover"
                />
                <div v-else class="w-full h-full flex items-center justify-center">
                  <svg class="w-8 h-8 text-text-secondary opacity-50" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
                  </svg>
                </div>
              </div>

              <!-- Info -->
              <div class="flex-1 min-w-0">
                <h3 class="font-semibold text-lg mb-1">
                  {{ transition.name || `Transition #${transition.id}` }}
                </h3>
                <div class="flex items-center gap-4 text-sm text-text-secondary flex-wrap">
                  <span class="capitalize">{{ formatTransitionType(transition.transition_type) }}</span>
                  <span>{{ transition.duration }}s</span>
                  <span>{{ formatDate(transition.created_at) }}</span>
                  <span
                    :class="[
                      'px-2 py-0.5 text-xs font-medium rounded-full',
                      transition.video_url
                        ? 'bg-green-500/20 text-green-400'
                        : 'bg-yellow-500/20 text-yellow-400'
                    ]"
                  >
                    {{ transition.video_url ? 'Complete' : 'Pending' }}
                  </span>
                </div>
              </div>

              <!-- Actions -->
              <div class="flex items-center gap-2 flex-shrink-0">
                <button
                  v-if="!transition.video_url"
                  @click="regenerateVideo(transition.id)"
                  :disabled="regenerating[transition.id]"
                  class="px-4 py-2 bg-primary text-white rounded-lg text-sm font-medium hover:bg-primary/90 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {{ regenerating[transition.id] ? 'Generating...' : 'Generate Video' }}
                </button>
                <button
                  v-if="transition.video_url"
                  @click="downloadVideo(transition.video_url, transition.name)"
                  class="px-4 py-2 bg-primary text-white rounded-lg text-sm font-medium hover:bg-primary/90 transition-colors"
                >
                  Download
                </button>
                <button
                  @click="openDeleteModal(transition)"
                  class="px-3 py-2 bg-red-500/10 text-red-500 rounded-lg text-sm font-medium hover:bg-red-500/20 transition-colors border border-red-500/20"
                >
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                  </svg>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Delete Confirmation Modal -->
    <Modal
      :isOpen="deleteModal.show"
      title="Delete Transition"
      subtitle="Are you sure you want to delete this transition?"
      layout="single-column"
      @close="closeDeleteModal"
    >
      <template #body>
        <div class="space-y-4">
          <p class="text-text-secondary">
            This action cannot be undone. The transition "{{ deleteModal.transition?.name || `Transition #${deleteModal.transition?.id}` }}" will be permanently deleted.
          </p>
        </div>
      </template>

      <template #cta>
        <div class="flex gap-3">
          <button
            @click="closeDeleteModal"
            class="flex-1 px-4 py-2 bg-card-bg border border-card-border text-text-primary rounded-lg hover:bg-card-border transition-colors"
          >
            Cancel
          </button>
          <button
            @click="confirmDelete"
            :disabled="deleting"
            class="flex-1 px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {{ deleting ? 'Deleting...' : 'Delete' }}
          </button>
        </div>
      </template>
    </Modal>
  </ClientOnly>
</template>

<script setup>
import { ref, onMounted, reactive } from 'vue'
import { getTransitions, deleteTransition, generateVideoWithPolling } from '~/client/videoGenerationApi'

definePageMeta({
  layout: 'dashboard',
  middleware: 'auth',
})

const transitions = ref([])
const loading = ref(true)
const error = ref(null)
const viewMode = ref('grid') // 'grid' or 'list'
const regenerating = reactive({})
const deleting = ref(false)

const deleteModal = reactive({
  show: false,
  transition: null
})

// Fetch transitions on mount
onMounted(async () => {
  await fetchTransitions()
})

async function fetchTransitions() {
  loading.value = true
  error.value = null
  
  try {
    transitions.value = await getTransitions()
  } catch (err) {
    console.error('Failed to fetch transitions:', err)
    error.value = 'Failed to load transitions. Please try again.'
  } finally {
    loading.value = false
  }
}

function formatTransitionType(type) {
  if (!type) return 'Unknown'
  return type.toLowerCase().replace(/_/g, ' ')
}

function formatDate(dateString) {
  if (!dateString) return 'Unknown'
  
  const date = new Date(dateString)
  const now = new Date()
  const diffInMs = now - date
  const diffInDays = Math.floor(diffInMs / (1000 * 60 * 60 * 24))
  
  if (diffInDays === 0) {
    return 'Today'
  } else if (diffInDays === 1) {
    return 'Yesterday'
  } else if (diffInDays < 7) {
    return `${diffInDays} days ago`
  } else {
    return date.toLocaleDateString('en-US', { 
      month: 'short', 
      day: 'numeric', 
      year: 'numeric' 
    })
  }
}

async function regenerateVideo(transitionId) {
  regenerating[transitionId] = true
  
  try {
    const result = await generateVideoWithPolling(transitionId, (status) => {
      console.log('Video generation progress:', status)
    })
    
    console.log('Video generated successfully:', result)
    
    // Refresh transitions to get the updated video URL
    await fetchTransitions()
  } catch (err) {
    console.error('Failed to generate video:', err)
    error.value = 'Failed to generate video. Please try again.'
  } finally {
    regenerating[transitionId] = false
  }
}

function downloadVideo(videoUrl, name) {
  const link = document.createElement('a')
  link.href = videoUrl
  link.download = `${name || 'transition'}.mp4`
  link.target = '_blank'
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
}

function openDeleteModal(transition) {
  deleteModal.show = true
  deleteModal.transition = transition
}

function closeDeleteModal() {
  deleteModal.show = false
  deleteModal.transition = null
}

async function confirmDelete() {
  if (!deleteModal.transition) return
  
  deleting.value = true
  
  try {
    await deleteTransition(deleteModal.transition.id)
    
    // Remove from local list
    transitions.value = transitions.value.filter(t => t.id !== deleteModal.transition.id)
    
    closeDeleteModal()
  } catch (err) {
    console.error('Failed to delete transition:', err)
    error.value = 'Failed to delete transition. Please try again.'
  } finally {
    deleting.value = false
  }
}
</script>

<style scoped>
.main-container {
  display: flex;
  justify-content: center;
  align-items: start;
  min-height: calc(100vh - 100px);
  overflow: auto;
  padding: 40px 20px;
}

.line-clamp-1 {
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>

