// server/api/user.js
export default defineEventHandler(async (event) => {
  try {
    const response = await $fetch("http://127.0.0.1:8000/api/account/me/") // Replace with your actual API endpoint
    return response
  } catch (error) {
    console.error("Error fetching user:", error)
    throw createError({
      statusCode: 500,
      statusMessage: "Failed to fetch user",
    })
  }
})
