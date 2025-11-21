<template>
  <div class="flex justify-center items-center gap-1 color-picker">
    <!-- Color Preview Button -->
    <div 
      class="w-6 h-6 rounded-md border cursor-pointer"
      :style="{ backgroundColor: modelValue }"
      @click="togglePicker"
    ></div>


    <!-- Dropdown Panel -->
    <div 
      v-if="isOpen"
      class="fixed mt-2 z-50 bg-white rounded-lg shadow-lg border w-[300px]"
      :style="dropdownStyle"
      @click.stop
    >
      <div class="p-4">
        <!-- Color Picker Area -->
        <div 
          ref="colorPanel"
          class="relative w-full h-32 mb-4 rounded-lg cursor-crosshair overflow-hidden"
          @mousedown="startPicking"
          @touchstart.prevent="startPicking"
        >
          <!-- Base gradient -->
          <div class="w-full h-full" :style="baseGradient"></div>
          
          <!-- Brightness/Saturation overlay -->
          <div class="w-full h-full bg-gradient-to-r from-white to-transparent" style="transform: translateY(-100%)"></div>
          <div class="w-full h-full bg-gradient-to-b from-transparent to-black" style="transform: translateY(-200%)"></div>
          
          <!-- Color picker indicator -->
          <div 
            class="w-4 h-4 rounded-full border-2 border-white shadow-md"
            :style="{
              transform: `translate(${pickerPosition.x}%, ${pickerPosition.y}%) translate(-50%, -50%)`,
              backgroundColor: selectedColor
            }"
          ></div>
        </div>

        <!-- Color Input Section -->
        <div class="flex items-center gap-2">
          <div class="text-sm font-medium text-gray-700">Hex</div>
          <div class="flex-1 flex items-center gap-1 px-2 py-1 bg-gray-50 rounded">
            <span class="text-gray-400">#</span>
            <input 
              type="text"
              v-model="hexInput"
              class="w-16 bg-transparent border-none outline-none uppercase text-sm"
              @input="updateFromHex"
            />
          </div>
          <button 
            @click="clearColor"
            class="px-2 py-1 text-sm text-red-500 hover:text-red-600 font-medium"
          >
            Clear
          </button>
        </div>
      </div>
    </div>
    <div>{{ modelValue }}</div>

  </div>
</template>

<script>
export default {
  name: 'ModernColorPicker',
  
  props: {
    modelValue: {
      type: String,
      default: '#000000'
    }
  },

  emits: ['update:modelValue'],

  data() {
    return {
      isOpen: false,
      hue: 0,
      saturation: 100,
      value: 100,
      isDragging: false,
      pickerPosition: { x: 100, y: 0 },
      dropdownStyle: {
        left: '0px',
        top: '0px'
      }
    }
  },

  computed: {
    baseGradient() {
      const colors = []
      for (let i = 0; i <= 360; i += 60) {
        colors.push(`hsl(${i}, 100%, 50%) ${i / 3.6}%`)
      }
      return {
        background: `linear-gradient(to right, ${colors.join(', ')})`
      }
    },

    selectedColor() {
      return this.hsvToHex(this.hue, this.saturation, this.value)
    },

    hexInput: {
      get() {
        return this.selectedColor.slice(1).toUpperCase()
      },
      set(value) {
        // Handled by updateFromHex method
      }
    }
  },

  created() {
    this.handleClickOutside = (event) => {
      if (!event.target.closest('.color-picker')) {
        this.isOpen = false
      }
    }
  },

  mounted() {
    window.addEventListener('mousemove', this.handleMouseMove)
    window.addEventListener('mouseup', this.stopPicking)
    window.addEventListener('touchmove', this.handleTouchMove)
    window.addEventListener('touchend', this.stopPicking)
    window.addEventListener('click', this.handleClickOutside)
    window.addEventListener('scroll', this.updateDropdownPosition)
    window.addEventListener('resize', this.updateDropdownPosition)

    // Initialize from prop
    if (this.modelValue && this.isValidHex(this.modelValue)) {
      const hsv = this.hexToHsv(this.modelValue)
      this.updateHSV(hsv)
    }
  },

  beforeUnmount() {
    window.removeEventListener('mousemove', this.handleMouseMove)
    window.removeEventListener('mouseup', this.stopPicking)
    window.removeEventListener('touchmove', this.handleTouchMove)
    window.removeEventListener('touchend', this.stopPicking)
    window.removeEventListener('click', this.handleClickOutside)
    window.removeEventListener('scroll', this.updateDropdownPosition)
    window.removeEventListener('resize', this.updateDropdownPosition)
  },

  methods: {
    togglePicker() {
      this.isOpen = !this.isOpen
      if (this.isOpen) {
        this.$nextTick(() => {
          this.updateDropdownPosition()
        })
      }
    },

    updateDropdownPosition() {
      const button = this.$el.querySelector('.w-6')
      if (button && this.isOpen) {
        const rect = button.getBoundingClientRect()
        const spaceBelow = window.innerHeight - rect.bottom
        
        // Position horizontally
        let left = rect.left
        if (left + 300 > window.innerWidth) {
          left = window.innerWidth - 300
        }
        
        // Position vertically
        let top = rect.bottom + window.scrollY
        if (spaceBelow < 300) {
          top = rect.top - 300 + window.scrollY
        }
        
        this.dropdownStyle = {
          left: `${Math.max(0, left)}px`,
          top: `${Math.max(0, top)}px`
        }
      }
    },

    startPicking(event) {
      this.isDragging = true
      this.updateColorFromEvent(event)
    },

    stopPicking() {
      this.isDragging = false
    },

    handleMouseMove(event) {
      if (this.isDragging) {
        this.updateColorFromEvent(event)
      }
    },

    handleTouchMove(event) {
      if (this.isDragging && event.touches?.[0]) {
        this.updateColorFromEvent(event.touches[0])
      }
    },

    updateColorFromEvent(event) {
      const rect = this.$refs.colorPanel.getBoundingClientRect()
      const x = Math.max(0, Math.min(100, ((event.clientX - rect.left) / rect.width) * 100))
      const y = Math.max(0, Math.min(100, ((event.clientY - rect.top) / rect.height) * 100))

      this.pickerPosition = { x, y }
      
      // Convert position to HSV
      this.hue = x * 3.6 // 360 degrees across width
      this.saturation = x // Horizontal is saturation
      this.value = 100 - y // Vertical is value

      this.$emit('update:modelValue', this.selectedColor)
    },

    updateFromHex(event) {
      const value = event.target.value
      const hex = `#${value}`
      if (this.isValidHex(hex)) {
        const hsv = this.hexToHsv(hex)
        this.updateHSV(hsv)
        this.$emit('update:modelValue', hex)
      }
    },

    updateHSV(hsv) {
      this.hue = hsv.h
      this.saturation = hsv.s
      this.value = hsv.v
      
      // Update picker position
      this.pickerPosition = {
        x: this.saturation,
        y: 100 - this.value
      }
    },

    clearColor() {
      this.updateHSV({ h: 0, s: 0, v: 100 })
      this.$emit('update:modelValue', '#FFFFFF')
    },

    isValidHex(color) {
      return /^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$/.test(color)
    },

    hsvToHex(h, s, v) {
      s = s / 100
      v = v / 100
      
      const hi = Math.floor(h / 60) % 6
      const f = (h / 60) - Math.floor(h / 60)
      const p = v * (1 - s)
      const q = v * (1 - f * s)
      const t = v * (1 - (1 - f) * s)
      
      let r, g, b
      
      switch (hi) {
        case 0: [r, g, b] = [v, t, p]; break
        case 1: [r, g, b] = [q, v, p]; break
        case 2: [r, g, b] = [p, v, t]; break
        case 3: [r, g, b] = [p, q, v]; break
        case 4: [r, g, b] = [t, p, v]; break
        case 5: [r, g, b] = [v, p, q]; break
      }
      
      const toHex = (x) => {
        const hex = Math.round(x * 255).toString(16)
        return hex.length === 1 ? '0' + hex : hex
      }
      
      return `#${toHex(r)}${toHex(g)}${toHex(b)}`
    },

    hexToHsv(hex) {
      hex = hex.replace('#', '')
      
      if (hex.length === 3) {
        hex = hex.split('').map(char => char + char).join('')
      }
      
      const r = parseInt(hex.substring(0, 2), 16) / 255
      const g = parseInt(hex.substring(2, 4), 16) / 255
      const b = parseInt(hex.substring(4, 6), 16) / 255
      
      const max = Math.max(r, g, b)
      const min = Math.min(r, g, b)
      const diff = max - min
      
      let h = 0
      const s = max === 0 ? 0 : (diff / max) * 100
      const v = max * 100
      
      if (diff !== 0) {
        switch (max) {
          case r: h = 60 * ((g - b) / diff + (g < b ? 6 : 0)); break
          case g: h = 60 * ((b - r) / diff + 2); break
          case b: h = 60 * ((r - g) / diff + 4); break
        }
      }
      
      return { h, s, v }
    }
  }
}
</script>