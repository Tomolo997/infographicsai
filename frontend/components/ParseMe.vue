<template>
  <div>
    <h1>CSV File Uploader</h1>
    <input type="file" @change="handleFileUpload" accept=".csv">
    <div v-if="csvData.length > 0">
      <h2>CSV Data:</h2>
      <pre>{{ csvData }}</pre>
    </div>
  </div>
</template>

<script>
import Papa from 'papaparse'

export default {
  data() {
    return {
      csvData: []
    }
  },
  methods: {
    handleFileUpload(event) {
      const file = event.target.files[0]
      if (file) {
        this.parseCSV(file)
      }
    },
    parseCSV(file) {
      Papa.parse(file, {
        complete: (result) => {
          this.csvData = result.data
        },
        header: true,
        error: (error) => {
          console.error('Error parsing CSV:', error)
        }
      })
    }
  }
}
</script>