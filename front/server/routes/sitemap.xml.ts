import { readdir } from 'fs/promises'
import { join } from 'path'

export default defineEventHandler(async (event) => {
  const baseUrl = 'https://ainfographic.com'
  const currentDate = new Date().toISOString().split('T')[0]

  // Public pages that should be indexed
  const publicPages = [
    { url: '', priority: '1.0', changefreq: 'daily' },
    { url: '/login', priority: '0.8', changefreq: 'monthly' },
    { url: '/signup', priority: '0.8', changefreq: 'monthly' },
    { url: '/blog', priority: '0.9', changefreq: 'weekly' },
    { url: '/privacy', priority: '0.5', changefreq: 'yearly' },
    { url: '/terms', priority: '0.5', changefreq: 'yearly' },
  ]

  // Dynamically get all blog posts
  const blogPages: Array<{ url: string; priority: string; changefreq: string }> = []
  try {
    const blogDir = join(process.cwd(), 'pages', 'blog')
    const files = await readdir(blogDir)

    // Filter out index.vue and get all other .vue files
    const blogPosts = files.filter(file => file.endsWith('.vue') && file !== 'index.vue')

    blogPosts.forEach(file => {
      // Remove .vue extension to get the slug
      const slug = file.replace('.vue', '')
      blogPages.push({
        url: `/blog/${slug}`,
        priority: '0.8',
        changefreq: 'monthly'
      })
    })
  } catch (error) {
    console.error('Error reading blog directory:', error)
  }

  // Combine all pages
  const allPages = [...publicPages, ...blogPages]

  const sitemap = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${allPages
      .map(
        (page) => `  <url>
    <loc>${baseUrl}${page.url}</loc>
    <lastmod>${currentDate}</lastmod>
    <changefreq>${page.changefreq}</changefreq>
    <priority>${page.priority}</priority>
  </url>`
      )
      .join('\n')}
</urlset>`

  event.node.res.setHeader('Content-Type', 'application/xml')
  return sitemap
})