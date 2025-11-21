/**
 * Image Upload API Service
 *
 * Handles uploading images to R2 storage via the backend API
 */

import apiClient from './apiClient'

/**
 * Upload a single image
 * @param {File} imageFile - The image file to upload
 * @param {string} imageType - Type of image ('front' or 'tail')
 * @returns {Promise<{url: string, filename: string, size: number}>}
 */
export async function uploadImage(imageFile, imageType = 'unknown') {
  // Create FormData for multipart upload
  const formData = new FormData()
  formData.append('image', imageFile)
  formData.append('image_type', imageType)

  // Upload with multipart/form-data
  const response = await apiClient.post('/transitions/upload-image/', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  })

  return response.data
}

/**
 * Upload both front and tail images at once
 * @param {File|null} frontImage - The front image file
 * @param {File|null} tailImage - The tail image file
 * @returns {Promise<{front_image?: object, tail_image?: object, errors?: object}>}
 */
export async function uploadImages(frontImage, tailImage) {
  const formData = new FormData()

  if (frontImage) {
    formData.append('front_image', frontImage)
  }

  if (tailImage) {
    formData.append('tail_image', tailImage)
  }

  if (!frontImage && !tailImage) {
    throw new Error('At least one image must be provided')
  }

  const response = await apiClient.post('/transitions/upload-images/', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  })

  return response.data
}

/**
 * Delete an image from storage
 * @param {string} filename - The filename to delete
 * @returns {Promise<{success: boolean, message: string}>}
 */
export async function deleteImage(filename) {
  const response = await apiClient.post('/transitions/delete-image/', {
    filename: filename,
  })

  return response.data
}

/**
 * Convert base64 data URL to File object
 * @param {string} dataUrl - Base64 data URL (e.g., from FileReader)
 * @param {string} filename - Desired filename
 * @returns {File}
 */
export function dataURLtoFile(dataUrl, filename) {
  const arr = dataUrl.split(',')
  const mime = arr[0].match(/:(.*?);/)[1]
  const bstr = atob(arr[1])
  let n = bstr.length
  const u8arr = new Uint8Array(n)

  while (n--) {
    u8arr[n] = bstr.charCodeAt(n)
  }

  return new File([u8arr], filename, { type: mime })
}

/**
 * Upload image from base64 data URL
 * @param {string} dataUrl - Base64 data URL
 * @param {string} imageType - Type of image ('front' or 'tail')
 * @param {string} filename - Optional filename (default: auto-generated)
 * @returns {Promise<{url: string, filename: string, size: number}>}
 */
export async function uploadImageFromDataURL(dataUrl, imageType = 'unknown', filename = null) {
  // Auto-generate filename if not provided
  if (!filename) {
    const extension = dataUrl.split(';')[0].split('/')[1] // Extract extension from mime type
    filename = `${imageType}_${Date.now()}.${extension}`
  }

  // Convert data URL to File
  const file = dataURLtoFile(dataUrl, filename)

  // Upload the file
  return await uploadImage(file, imageType)
}

/**
 * Validate image file before upload
 * @param {File} file - The file to validate
 * @param {number} maxSizeMB - Maximum file size in MB (default: 10)
 * @returns {{valid: boolean, error?: string}}
 */
export function validateImageFile(file, maxSizeMB = 10) {
  // Check if file exists
  if (!file) {
    return { valid: false, error: 'No file provided' }
  }

  // Check file type
  const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp', 'image/gif']
  if (!allowedTypes.includes(file.type)) {
    return {
      valid: false,
      error: `Invalid file type. Allowed types: ${allowedTypes.join(', ')}`,
    }
  }

  // Check file size
  const maxSize = maxSizeMB * 1024 * 1024 // Convert to bytes
  if (file.size > maxSize) {
    return {
      valid: false,
      error: `File size exceeds ${maxSizeMB}MB limit`,
    }
  }

  return { valid: true }
}

/**
 * Upload image with progress tracking
 * @param {File} imageFile - The image file to upload
 * @param {string} imageType - Type of image ('front' or 'tail')
 * @param {Function} onProgress - Progress callback (receives percentage)
 * @returns {Promise<{url: string, filename: string, size: number}>}
 */
export async function uploadImageWithProgress(imageFile, imageType = 'unknown', onProgress = null) {
  const formData = new FormData()
  formData.append('image', imageFile)
  formData.append('image_type', imageType)

  const response = await apiClient.post('/transitions/upload-image/', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
    onUploadProgress: (progressEvent) => {
      if (onProgress && progressEvent.total) {
        const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total)
        onProgress(percentCompleted)
      }
    },
  })

  return response.data
}

export default {
  uploadImage,
  uploadImages,
  deleteImage,
  dataURLtoFile,
  uploadImageFromDataURL,
  validateImageFile,
  uploadImageWithProgress,
}
