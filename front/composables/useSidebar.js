import { ref } from 'vue'

const isCollapsed = ref(false)

export const useSidebar = () => {
  const toggleSidebar = () => {
    console.log('Toggle clicked! Current state:', isCollapsed.value)
    isCollapsed.value = !isCollapsed.value
    console.log('New state:', isCollapsed.value)
  }

  return {
    isCollapsed,
    toggleSidebar,
  }
}
