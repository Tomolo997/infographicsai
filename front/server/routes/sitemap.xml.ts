export default defineEventHandler((event) => {
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

  // Blog posts - add new posts here when you create them
  const blogPosts = [
    'instagram-post-sizes-complete-guide-2025',
    // Add more blog post slugs here as you create them
  ]

  const blogPages = blogPosts.map(slug => ({
    url: `/blog/${slug}`,
    priority: '0.8',
    changefreq: 'monthly'
  }))

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