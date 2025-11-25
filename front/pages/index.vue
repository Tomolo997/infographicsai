<template>
  <div class="min-h-screen">
    <!-- Hero Section -->
    <section class="relative pt-32 pb-20 overflow-hidden">
      <!-- Background Effects -->
      <div
        class="absolute inset-0 bg-gradient-to-br from-sidebar-orange/5 via-background-primary to-sidebar-orange/10"
      ></div>
      <div class="absolute inset-0 opacity-20">
        <div
          class="absolute inset-0"
          style="
            background-image: radial-gradient(
              circle at 25px 25px,
              rgba(186, 116, 8, 0.1) 2px,
              transparent 0
            );
            background-size: 50px 50px;
          "
        ></div>
      </div>

      <div class="container-custom relative z-10">
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
          <!-- Left side: Text content -->
          <div>
            <h1 class="text-display-xl mb-6">
              Create Stunning
              <span class="text-sidebar-orange">Infographics</span>
              from your Blog Posts
            </h1>
            <p class="text-body-xl text-text-secondary mb-10 max-w-xl">
              Transform your content into beautiful, engaging infographics that
              capture attention and drive results.
              <span class="text-white bg-sidebar-orange px-2 py-1 rounded-md"
                >No design skills required.</span
              >
            </p>
            <div class="flex flex-col sm:flex-row gap-4">
              <NuxtLink to="/signup" class="btn-primary text-lg px-8 py-4">
                Start Creating
              </NuxtLink>
            </div>
            <div class="mt-8 flex items-center gap-4">
              <div class="flex -space-x-2">
                <div
                  class="w-10 h-10 rounded-full bg-sidebar-orange/20 border-2 border-background-primary"
                ></div>
                <div
                  class="w-10 h-10 rounded-full bg-sidebar-orange/40 border-2 border-background-primary"
                ></div>
                <div
                  class="w-10 h-10 rounded-full bg-sidebar-orange/60 border-2 border-background-primary"
                ></div>
              </div>
              <div class="text-sm">
                <div class="font-semibold text-text-primary">
                  Trusted by 10,000+ creators
                </div>
                <div class="text-text-secondary">⭐⭐⭐⭐⭐ 4.9/5 rating</div>
              </div>
            </div>
          </div>

          <!-- Right side: 3 Infographs with depth effect -->
          <div class="relative h-[600px] hidden lg:block">
            <!-- Back left infograph -->
            <div
              class="absolute top-0 left-0 w-64 transform rotate-[-8deg] translate-x-[-20px] translate-y-[40px] z-10 transition-transform duration-300 hover:scale-105"
            >
              <img
                src="https://images.ainfographic.com/template_1_landing_page.png"
                alt="Infograph 1"
                class="w-full h-full object-cover"
              />
            </div>

            <!-- Front center infograph (main focus) -->
            <div
              class="absolute top-20 left-1/2 transform -translate-x-1/2 w-72 z-30 transition-transform duration-300 hover:scale-105"
            >
              <img
                src="https://images.ainfographic.com/template_1_landing_page.png"
                alt="Infograph 1"
                class="w-full h-full object-cover"
              />
            </div>

            <!-- Back right infograph -->
            <div
              class="absolute top-0 right-0 w-64 transform rotate-[8deg] translate-x-[20px] translate-y-[40px] z-10 transition-transform duration-300 hover:scale-105"
            >
              <img
                src="https://images.ainfographic.com/template_1_landing_page.png"
                alt="Infograph 1"
                class="w-full h-full object-cover"
              />
            </div>

            <!-- Glow effects -->
            <div
              class="absolute top-20 left-1/2 -translate-x-1/2 w-96 h-96 bg-sidebar-orange/20 blur-3xl -z-10 rounded-full"
            ></div>
          </div>
        </div>
      </div>
    </section>

    <!-- Video Demo Section -->
    <section ref="videoSection" class="py-24 bg-background-secondary/30">
      <div class="container-custom">
        <div class="text-center mb-12">
          <h2 class="text-display-md mb-4">
            See How Easy It Is to Create Stunning Infographics
          </h2>
          <p class="text-body-lg text-text-secondary max-w-2xl mx-auto">
            Watch how our AI-powered platform transforms your content into
            beautiful, professional infographics in just minutes.
          </p>
        </div>

        <!-- Video Container -->
        <div class="max-w-5xl mx-auto">
          <div class="relative rounded-2xl overflow-hidden shadow-2xl">
            <!-- Video placeholder - Replace with your actual video -->
            <div
              class="relative bg-gradient-to-br from-sidebar-orange/10 to-purple-500/10 aspect-video"
            >
              <!-- Play button overlay -->
              <div
                class="absolute inset-0 flex items-center justify-center bg-black/20 backdrop-blur-sm cursor-pointer hover:bg-black/30 transition-colors group"
              >
                <div
                  class="w-20 h-20 rounded-full bg-sidebar-orange flex items-center justify-center transform group-hover:scale-110 transition-transform shadow-2xl"
                >
                  <svg
                    class="w-8 h-8 text-white ml-1"
                    fill="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path d="M8 5v14l11-7z" />
                  </svg>
                </div>
              </div>
              <!-- Placeholder content -->
              <div
                class="absolute inset-0 flex items-center justify-center text-text-secondary"
              >
                <div class="text-center p-8">
                  <div class="text-6xl mb-4">🎬</div>
                  <p class="text-lg">Demo Video Coming Soon</p>
                  <p class="text-sm mt-2 opacity-75">
                    Replace this with your actual video URL
                  </p>
                </div>
              </div>
            </div>
            <!-- Glow effect -->
            <div
              class="absolute -inset-4 bg-sidebar-orange/20 blur-3xl -z-10 rounded-[3rem]"
            ></div>
          </div>
        </div>
      </div>
    </section>

    <!-- Infographic Gallery Mosaic -->
    <section class="py-24">
      <div class="container-custom">
        <div class="text-center mb-12">
          <h2 class="text-display-md mb-4">
            Beautiful Infographics for Every Need
          </h2>
          <p class="text-body-lg text-text-secondary max-w-2xl mx-auto">
            From social media posts to detailed reports, create infographics in
            any format and style you need.
          </p>
        </div>

        <!-- Mosaic Grid -->
        <div class="grid grid-cols-12 gap-4 max-w-6xl mx-auto">
          <!-- Large square - Top left -->
          <div
            class="col-span-12 md:col-span-6 lg:col-span-5 row-span-2 aspect-square"
          >
            <div
              class="h-full bg-gradient-to-br from-blue-400 to-blue-600 rounded-xl overflow-hidden hover:scale-[1.02] transition-transform duration-300 shadow-lg cursor-pointer"
            >
              <div class="p-8 h-full flex flex-col justify-between">
                <div>
                  <h3 class="text-white font-bold text-3xl mb-4">
                    Market Analysis
                  </h3>
                  <p class="text-white/80">Q4 2024 Performance Report</p>
                </div>
                <div class="space-y-4">
                  <div class="bg-white/20 backdrop-blur-sm rounded-lg p-4">
                    <div class="text-white/60 text-sm mb-2">Revenue Growth</div>
                    <div class="text-white font-bold text-2xl">+127%</div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Tall rectangle - Top right -->
          <div
            class="col-span-6 md:col-span-3 lg:col-span-3 row-span-3 aspect-[9/16]"
          >
            <div
              class="h-full bg-gradient-to-br from-purple-400 to-purple-600 rounded-xl overflow-hidden hover:scale-[1.02] transition-transform duration-300 shadow-lg cursor-pointer"
            >
              <div class="p-6 h-full flex flex-col justify-between">
                <div>
                  <h3 class="text-white font-bold text-xl mb-3">
                    Social Stats
                  </h3>
                  <div class="space-y-3">
                    <div class="bg-white/20 backdrop-blur-sm rounded-lg p-3">
                      <div class="text-white/70 text-xs">Engagement</div>
                      <div class="text-white font-bold text-lg">8.4K</div>
                    </div>
                    <div class="bg-white/20 backdrop-blur-sm rounded-lg p-3">
                      <div class="text-white/70 text-xs">Reach</div>
                      <div class="text-white font-bold text-lg">124K</div>
                    </div>
                    <div class="bg-white/20 backdrop-blur-sm rounded-lg p-3">
                      <div class="text-white/70 text-xs">Shares</div>
                      <div class="text-white font-bold text-lg">2.1K</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Wide rectangle - Far right -->
          <div
            class="col-span-6 md:col-span-3 lg:col-span-4 row-span-2 aspect-[4/5]"
          >
            <div
              class="h-full bg-gradient-to-br from-sidebar-orange to-yellow-500 rounded-xl overflow-hidden hover:scale-[1.02] transition-transform duration-300 shadow-lg cursor-pointer"
            >
              <div class="p-6 h-full flex flex-col justify-between">
                <div>
                  <h3 class="text-white font-bold text-2xl mb-4">
                    Content Performance
                  </h3>
                  <div class="relative h-32">
                    <svg
                      viewBox="0 0 200 100"
                      class="w-full h-full"
                      preserveAspectRatio="none"
                    >
                      <path
                        d="M 0,80 L 50,60 L 100,40 L 150,30 L 200,20"
                        fill="none"
                        stroke="white"
                        stroke-width="3"
                        opacity="0.8"
                      />
                      <path
                        d="M 0,80 L 50,60 L 100,40 L 150,30 L 200,20 L 200,100 L 0,100 Z"
                        fill="white"
                        opacity="0.2"
                      />
                    </svg>
                  </div>
                </div>
                <div class="bg-white/20 backdrop-blur-sm rounded-lg p-4">
                  <div class="text-white/70 text-sm mb-1">Avg. Views</div>
                  <div class="text-white font-bold text-2xl">45.2K</div>
                </div>
              </div>
            </div>
          </div>

          <!-- Medium rectangle - Middle left -->
          <div
            class="col-span-6 md:col-span-3 lg:col-span-3 row-span-2 aspect-[3/2]"
          >
            <div
              class="h-full bg-gradient-to-br from-green-400 to-green-600 rounded-xl overflow-hidden hover:scale-[1.02] transition-transform duration-300 shadow-lg cursor-pointer"
            >
              <div class="p-6 h-full flex flex-col justify-between">
                <h3 class="text-white font-bold text-xl">Team Productivity</h3>
                <div class="relative w-32 h-32 mx-auto">
                  <svg viewBox="0 0 100 100" class="transform -rotate-90">
                    <circle
                      cx="50"
                      cy="50"
                      r="40"
                      fill="none"
                      stroke="white"
                      stroke-width="8"
                      opacity="0.2"
                    />
                    <circle
                      cx="50"
                      cy="50"
                      r="40"
                      fill="none"
                      stroke="white"
                      stroke-width="8"
                      stroke-dasharray="251.2"
                      stroke-dashoffset="50.24"
                    />
                  </svg>
                  <div
                    class="absolute inset-0 flex items-center justify-center text-white font-bold text-2xl"
                  >
                    80%
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Small square -->
          <div class="col-span-6 md:col-span-3 lg:col-span-2 aspect-square">
            <div
              class="h-full bg-gradient-to-br from-pink-400 to-pink-600 rounded-xl overflow-hidden hover:scale-[1.02] transition-transform duration-300 shadow-lg cursor-pointer p-4 flex items-center justify-center"
            >
              <div class="text-center text-white">
                <div class="text-4xl font-bold mb-2">92%</div>
                <div class="text-sm opacity-80">Satisfaction</div>
              </div>
            </div>
          </div>

          <!-- Wide landscape -->
          <div class="col-span-12 md:col-span-6 lg:col-span-7 aspect-[21/9]">
            <div
              class="h-full bg-gradient-to-r from-indigo-400 to-indigo-600 rounded-xl overflow-hidden hover:scale-[1.02] transition-transform duration-300 shadow-lg cursor-pointer"
            >
              <div class="p-6 h-full flex items-center justify-between">
                <div>
                  <h3 class="text-white font-bold text-2xl mb-2">
                    Annual Growth Metrics
                  </h3>
                  <p class="text-white/70">2024 Year-End Summary</p>
                </div>
                <div class="flex gap-6">
                  <div class="text-center">
                    <div class="text-white font-bold text-3xl">$2.4M</div>
                    <div class="text-white/70 text-sm">Revenue</div>
                  </div>
                  <div class="text-center">
                    <div class="text-white font-bold text-3xl">156%</div>
                    <div class="text-white/70 text-sm">Growth</div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Medium portrait -->
          <div
            class="col-span-6 md:col-span-3 lg:col-span-3 row-span-2 aspect-[2/3]"
          >
            <div
              class="h-full bg-gradient-to-br from-red-400 to-red-600 rounded-xl overflow-hidden hover:scale-[1.02] transition-transform duration-300 shadow-lg cursor-pointer"
            >
              <div class="p-6 h-full flex flex-col justify-between">
                <h3 class="text-white font-bold text-xl">Customer Insights</h3>
                <div class="space-y-3">
                  <div class="bg-white/20 backdrop-blur-sm rounded-lg p-3">
                    <div class="flex justify-between items-center">
                      <span class="text-white text-sm">Retention</span>
                      <span class="text-white font-bold">94%</span>
                    </div>
                    <div class="w-full bg-white/20 rounded-full h-2 mt-2">
                      <div
                        class="bg-white rounded-full h-2"
                        style="width: 94%"
                      ></div>
                    </div>
                  </div>
                  <div class="bg-white/20 backdrop-blur-sm rounded-lg p-3">
                    <div class="flex justify-between items-center">
                      <span class="text-white text-sm">NPS Score</span>
                      <span class="text-white font-bold">87</span>
                    </div>
                    <div class="w-full bg-white/20 rounded-full h-2 mt-2">
                      <div
                        class="bg-white rounded-full h-2"
                        style="width: 87%"
                      ></div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Small rectangle -->
          <div class="col-span-6 md:col-span-3 lg:col-span-2 aspect-[4/3]">
            <div
              class="h-full bg-gradient-to-br from-teal-400 to-teal-600 rounded-xl overflow-hidden hover:scale-[1.02] transition-transform duration-300 shadow-lg cursor-pointer p-4 flex flex-col justify-center"
            >
              <div class="text-white text-center">
                <div class="text-3xl font-bold mb-1">15K+</div>
                <div class="text-sm opacity-80">Active Users</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Benefits Section -->
    <section class="py-24 bg-background-secondary/30">
      <div class="container-custom">
        <div class="text-center mb-16">
          <h2 class="text-display-md mb-4">
            Why Choose Our Infographic Platform?
          </h2>
          <p class="text-body-lg text-text-secondary max-w-2xl mx-auto">
            Create visual content that captures attention and drives real
            results for your business.
          </p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          <!-- Benefit 1 -->
          <div
            class="card p-8 hover:border-sidebar-orange/50 transition-all duration-300 group"
          >
            <div
              class="w-14 h-14 rounded-xl bg-sidebar-orange/10 flex items-center justify-center mb-6 group-hover:bg-sidebar-orange/20 transition-colors"
            >
              <svg
                class="w-7 h-7 text-sidebar-orange"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
                />
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"
                />
              </svg>
            </div>
            <h3 class="text-2xl font-bold mb-4">10x More Views</h3>
            <p class="text-text-secondary leading-relaxed">
              Infographics get 3x more engagement than plain text content.
              Capture attention and increase your reach across all platforms.
            </p>
          </div>

          <!-- Benefit 2 -->
          <div
            class="card p-8 hover:border-sidebar-orange/50 transition-all duration-300 group"
          >
            <div
              class="w-14 h-14 rounded-xl bg-sidebar-orange/10 flex items-center justify-center mb-6 group-hover:bg-sidebar-orange/20 transition-colors"
            >
              <svg
                class="w-7 h-7 text-sidebar-orange"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"
                />
              </svg>
            </div>
            <h3 class="text-2xl font-bold mb-4">Boost Engagement</h3>
            <p class="text-text-secondary leading-relaxed">
              Visual content is processed 60,000x faster than text. Drive more
              likes, shares, and comments with compelling infographics.
            </p>
          </div>

          <!-- Benefit 3 -->
          <div
            class="card p-8 hover:border-sidebar-orange/50 transition-all duration-300 group"
          >
            <div
              class="w-14 h-14 rounded-xl bg-sidebar-orange/10 flex items-center justify-center mb-6 group-hover:bg-sidebar-orange/20 transition-colors"
            >
              <svg
                class="w-7 h-7 text-sidebar-orange"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                />
              </svg>
            </div>
            <h3 class="text-2xl font-bold mb-4">Simplify Complex Data</h3>
            <p class="text-text-secondary leading-relaxed">
              Transform complicated information into easy-to-understand visuals.
              Make your message clear and memorable.
            </p>
          </div>

          <!-- Benefit 4 -->
          <div
            class="card p-8 hover:border-sidebar-orange/50 transition-all duration-300 group"
          >
            <div
              class="w-14 h-14 rounded-xl bg-sidebar-orange/10 flex items-center justify-center mb-6 group-hover:bg-sidebar-orange/20 transition-colors"
            >
              <svg
                class="w-7 h-7 text-sidebar-orange"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.368 2.684 3 3 0 00-5.368-2.684z"
                />
              </svg>
            </div>
            <h3 class="text-2xl font-bold mb-4">Increase Shareability</h3>
            <p class="text-text-secondary leading-relaxed">
              Infographics are shared 3x more than any other content type. Grow
              your audience organically with viral-worthy visuals.
            </p>
          </div>

          <!-- Benefit 5 -->
          <div
            class="card p-8 hover:border-sidebar-orange/50 transition-all duration-300 group"
          >
            <div
              class="w-14 h-14 rounded-xl bg-sidebar-orange/10 flex items-center justify-center mb-6 group-hover:bg-sidebar-orange/20 transition-colors"
            >
              <svg
                class="w-7 h-7 text-sidebar-orange"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"
                />
              </svg>
            </div>
            <h3 class="text-2xl font-bold mb-4">Save Time & Money</h3>
            <p class="text-text-secondary leading-relaxed">
              Create professional infographics in minutes, not hours. No need
              for expensive designers or complex software.
            </p>
          </div>

          <!-- Benefit 6 -->
          <div
            class="card p-8 hover:border-sidebar-orange/50 transition-all duration-300 group"
          >
            <div
              class="w-14 h-14 rounded-xl bg-sidebar-orange/10 flex items-center justify-center mb-6 group-hover:bg-sidebar-orange/20 transition-colors"
            >
              <svg
                class="w-7 h-7 text-sidebar-orange"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"
                />
              </svg>
            </div>
            <h3 class="text-2xl font-bold mb-4">Build Brand Authority</h3>
            <p class="text-text-secondary leading-relaxed">
              Position yourself as an expert with high-quality visual content.
              Establish trust and credibility in your industry.
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- Features Section -->
    <section class="py-24">
      <div class="container-custom">
        <div class="text-center mb-16">
          <h2 class="text-display-md mb-4">Powerful Features, Simple to Use</h2>
          <p class="text-body-lg text-text-secondary max-w-2xl mx-auto">
            Everything you need to create stunning infographics in one
            easy-to-use platform.
          </p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          <!-- Feature 1 -->
          <div class="text-center group">
            <div
              class="relative mb-6 mx-auto w-20 h-20 rounded-2xl bg-gradient-to-br from-blue-500 to-blue-600 flex items-center justify-center transform group-hover:scale-110 transition-transform duration-300 shadow-lg"
            >
              <svg
                class="w-10 h-10 text-white"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1"
                />
              </svg>
            </div>
            <h3 class="text-xl font-bold mb-3">Create from Blog URL</h3>
            <p class="text-text-secondary text-sm leading-relaxed">
              Simply paste your blog URL and let our AI extract the key points
              and create a beautiful infographic automatically.
            </p>
          </div>

          <!-- Feature 2 -->
          <div class="text-center group">
            <div
              class="relative mb-6 mx-auto w-20 h-20 rounded-2xl bg-gradient-to-br from-purple-500 to-purple-600 flex items-center justify-center transform group-hover:scale-110 transition-transform duration-300 shadow-lg"
            >
              <svg
                class="w-10 h-10 text-white"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M4 5a1 1 0 011-1h4a1 1 0 011 1v7a1 1 0 01-1 1H5a1 1 0 01-1-1V5zM14 5a1 1 0 011-1h4a1 1 0 011 1v7a1 1 0 01-1 1h-4a1 1 0 01-1-1V5zM4 16a1 1 0 011-1h4a1 1 0 011 1v3a1 1 0 01-1 1H5a1 1 0 01-1-1v-3zM14 16a1 1 0 011-1h4a1 1 0 011 1v3a1 1 0 01-1 1h-4a1 1 0 01-1-1v-3z"
                />
              </svg>
            </div>
            <h3 class="text-xl font-bold mb-3">Choose from Templates</h3>
            <p class="text-text-secondary text-sm leading-relaxed">
              Browse our library of professional templates and customize them to
              match your brand and message perfectly.
            </p>
          </div>

          <!-- Feature 3 -->
          <div class="text-center group">
            <div
              class="relative mb-6 mx-auto w-20 h-20 rounded-2xl bg-gradient-to-br from-sidebar-orange to-yellow-500 flex items-center justify-center transform group-hover:scale-110 transition-transform duration-300 shadow-lg"
            >
              <svg
                class="w-10 h-10 text-white"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
                />
              </svg>
            </div>
            <h3 class="text-xl font-bold mb-3">Bring Your Own Design</h3>
            <p class="text-text-secondary text-sm leading-relaxed">
              Upload your existing infographic template and let our AI populate
              it with your content while maintaining your style.
            </p>
          </div>

          <!-- Feature 4 -->
          <div class="text-center group">
            <div
              class="relative mb-6 mx-auto w-20 h-20 rounded-2xl bg-gradient-to-br from-green-500 to-green-600 flex items-center justify-center transform group-hover:scale-110 transition-transform duration-300 shadow-lg"
            >
              <svg
                class="w-10 h-10 text-white"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"
                />
              </svg>
            </div>
            <h3 class="text-xl font-bold mb-3">Create from Your Content</h3>
            <p class="text-text-secondary text-sm leading-relaxed">
              Write or paste your content directly and watch as our AI designs a
              stunning infographic that tells your story.
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- Pricing & FAQ Section -->
    <section class="py-24 bg-background-secondary/30">
      <div class="container-custom">
        <!-- Pricing -->
        <div class="mb-24">
          <div class="text-center mb-12">
            <h2 class="text-display-md mb-4">Simple, Transparent Pricing</h2>
            <p class="text-body-lg text-text-secondary">
              Choose the plan that fits your needs. No hidden fees.
            </p>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-5xl mx-auto">
            <!-- Free Plan -->
            <div class="card p-8 hover:border-sidebar-orange/50 transition-all">
              <div class="mb-6">
                <h3 class="text-2xl font-bold mb-2">Free</h3>
                <div class="text-4xl font-bold mb-2">
                  $0<span class="text-lg text-text-secondary">/month</span>
                </div>
                <p class="text-text-secondary text-sm">
                  Perfect for trying out
                </p>
              </div>
              <ul class="space-y-3 mb-8">
                <li class="flex items-start gap-2">
                  <svg
                    class="w-5 h-5 text-green-500 mt-0.5 flex-shrink-0"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M5 13l4 4L19 7"
                    />
                  </svg>
                  <span class="text-sm">3 infographics per month</span>
                </li>
                <li class="flex items-start gap-2">
                  <svg
                    class="w-5 h-5 text-green-500 mt-0.5 flex-shrink-0"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M5 13l4 4L19 7"
                    />
                  </svg>
                  <span class="text-sm">Basic templates</span>
                </li>
                <li class="flex items-start gap-2">
                  <svg
                    class="w-5 h-5 text-green-500 mt-0.5 flex-shrink-0"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M5 13l4 4L19 7"
                    />
                  </svg>
                  <span class="text-sm">Standard resolution</span>
                </li>
                <li class="flex items-start gap-2">
                  <svg
                    class="w-5 h-5 text-green-500 mt-0.5 flex-shrink-0"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M5 13l4 4L19 7"
                    />
                  </svg>
                  <span class="text-sm">Watermark included</span>
                </li>
              </ul>
              <NuxtLink to="/signup" class="btn-outline w-full text-center">
                Get Started
              </NuxtLink>
            </div>

            <!-- Pro Plan - Featured -->
            <div
              class="card p-8 relative border-2 border-sidebar-orange shadow-xl"
            >
              <div
                class="absolute -top-4 left-1/2 -translate-x-1/2 bg-sidebar-orange text-white px-4 py-1 rounded-full text-sm font-semibold"
              >
                Most Popular
              </div>
              <div class="mb-6">
                <h3 class="text-2xl font-bold mb-2">Pro</h3>
                <div class="text-4xl font-bold mb-2">
                  $29<span class="text-lg text-text-secondary">/month</span>
                </div>
                <p class="text-text-secondary text-sm">For serious creators</p>
              </div>
              <ul class="space-y-3 mb-8">
                <li class="flex items-start gap-2">
                  <svg
                    class="w-5 h-5 text-green-500 mt-0.5 flex-shrink-0"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M5 13l4 4L19 7"
                    />
                  </svg>
                  <span class="text-sm font-medium"
                    >50 infographics per month</span
                  >
                </li>
                <li class="flex items-start gap-2">
                  <svg
                    class="w-5 h-5 text-green-500 mt-0.5 flex-shrink-0"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M5 13l4 4L19 7"
                    />
                  </svg>
                  <span class="text-sm">All premium templates</span>
                </li>
                <li class="flex items-start gap-2">
                  <svg
                    class="w-5 h-5 text-green-500 mt-0.5 flex-shrink-0"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M5 13l4 4L19 7"
                    />
                  </svg>
                  <span class="text-sm">4K resolution</span>
                </li>
                <li class="flex items-start gap-2">
                  <svg
                    class="w-5 h-5 text-green-500 mt-0.5 flex-shrink-0"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M5 13l4 4L19 7"
                    />
                  </svg>
                  <span class="text-sm">No watermark</span>
                </li>
                <li class="flex items-start gap-2">
                  <svg
                    class="w-5 h-5 text-green-500 mt-0.5 flex-shrink-0"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M5 13l4 4L19 7"
                    />
                  </svg>
                  <span class="text-sm">Custom branding</span>
                </li>
                <li class="flex items-start gap-2">
                  <svg
                    class="w-5 h-5 text-green-500 mt-0.5 flex-shrink-0"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M5 13l4 4L19 7"
                    />
                  </svg>
                  <span class="text-sm">Priority support</span>
                </li>
              </ul>
              <NuxtLink to="/signup" class="btn-primary w-full text-center">
                Start Free Trial
              </NuxtLink>
            </div>

            <!-- Business Plan -->
            <div class="card p-8 hover:border-sidebar-orange/50 transition-all">
              <div class="mb-6">
                <h3 class="text-2xl font-bold mb-2">Business</h3>
                <div class="text-4xl font-bold mb-2">
                  $99<span class="text-lg text-text-secondary">/month</span>
                </div>
                <p class="text-text-secondary text-sm">For teams & agencies</p>
              </div>
              <ul class="space-y-3 mb-8">
                <li class="flex items-start gap-2">
                  <svg
                    class="w-5 h-5 text-green-500 mt-0.5 flex-shrink-0"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M5 13l4 4L19 7"
                    />
                  </svg>
                  <span class="text-sm font-medium"
                    >Unlimited infographics</span
                  >
                </li>
                <li class="flex items-start gap-2">
                  <svg
                    class="w-5 h-5 text-green-500 mt-0.5 flex-shrink-0"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M5 13l4 4L19 7"
                    />
                  </svg>
                  <span class="text-sm">All Pro features</span>
                </li>
                <li class="flex items-start gap-2">
                  <svg
                    class="w-5 h-5 text-green-500 mt-0.5 flex-shrink-0"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M5 13l4 4L19 7"
                    />
                  </svg>
                  <span class="text-sm">Team collaboration</span>
                </li>
                <li class="flex items-start gap-2">
                  <svg
                    class="w-5 h-5 text-green-500 mt-0.5 flex-shrink-0"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M5 13l4 4L19 7"
                    />
                  </svg>
                  <span class="text-sm">API access</span>
                </li>
                <li class="flex items-start gap-2">
                  <svg
                    class="w-5 h-5 text-green-500 mt-0.5 flex-shrink-0"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M5 13l4 4L19 7"
                    />
                  </svg>
                  <span class="text-sm">Dedicated account manager</span>
                </li>
                <li class="flex items-start gap-2">
                  <svg
                    class="w-5 h-5 text-green-500 mt-0.5 flex-shrink-0"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M5 13l4 4L19 7"
                    />
                  </svg>
                  <span class="text-sm">Custom integrations</span>
                </li>
              </ul>
              <NuxtLink to="/signup" class="btn-outline w-full text-center">
                Contact Sales
              </NuxtLink>
            </div>
          </div>
        </div>

        <!-- FAQ -->
        <div class="max-w-3xl mx-auto">
          <div class="text-center mb-12">
            <h2 class="text-display-sm mb-4">Frequently Asked Questions</h2>
            <p class="text-text-secondary">
              Everything you need to know about our platform
            </p>
          </div>

          <div class="space-y-4">
            <div
              v-for="(faq, index) in faqs"
              :key="index"
              class="card p-0 overflow-hidden"
            >
              <button
                @click="toggleFaq(index)"
                class="w-full px-6 py-5 text-left flex justify-between items-center hover:bg-background-secondary/50 transition-colors"
              >
                <span class="font-semibold text-lg pr-4">{{
                  faq.question
                }}</span>
                <svg
                  class="w-5 h-5 text-sidebar-orange transform transition-transform duration-200 flex-shrink-0"
                  :class="{ 'rotate-180': faq.isOpen }"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M19 9l-7 7-7-7"
                  ></path>
                </svg>
              </button>
              <div
                v-show="faq.isOpen"
                class="px-6 pb-5 text-text-secondary leading-relaxed"
              >
                {{ faq.answer }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Final CTA -->
    <section class="py-24 relative overflow-hidden">
      <div
        class="absolute inset-0 bg-gradient-to-b from-sidebar-orange/5 to-sidebar-orange/20"
      ></div>
      <div
        class="absolute inset-0 opacity-10"
        style="
          background-image: radial-gradient(
            circle at 25px 25px,
            rgba(186, 116, 8, 0.3) 2px,
            transparent 0
          );
          background-size: 50px 50px;
        "
      ></div>

      <div class="container-custom relative z-10 text-center">
        <h2 class="text-display-md mb-6">
          Ready to Create Stunning Infographics?
        </h2>
        <p class="text-body-xl text-text-secondary mb-10 max-w-2xl mx-auto">
          Join thousands of creators, marketers, and businesses who are already
          creating engaging visual content with our platform.
        </p>
        <div class="flex flex-col sm:flex-row gap-4 justify-center">
          <NuxtLink to="/signup" class="btn-primary text-lg px-10 py-4">
            Start Creating for Free
          </NuxtLink>
          <button @click="scrollToVideo" class="btn-outline text-lg px-10 py-4">
            Watch Demo
          </button>
        </div>
        <p class="text-text-secondary text-sm mt-6">
          No credit card required • 3 free infographics • Cancel anytime
        </p>
      </div>
    </section>

    <!-- Footer -->
    <footer class="bg-background-secondary/50 border-t border-card-border">
      <div class="container-custom py-12">
        <div class="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
          <!-- Brand -->
          <div class="md:col-span-1">
            <div class="flex items-center gap-2 mb-4">
              <div
                class="w-8 h-8 rounded-lg bg-sidebar-orange flex items-center justify-center"
              >
                <span class="text-white font-bold text-lg">AI</span>
              </div>
              <span class="text-xl font-bold">InfoGraphics</span>
            </div>
            <p class="text-text-secondary text-sm leading-relaxed">
              Create beautiful infographics in minutes with AI-powered design.
            </p>
          </div>

          <!-- Product -->
          <div>
            <h3 class="font-semibold mb-4">Product</h3>
            <ul class="space-y-2 text-sm">
              <li>
                <NuxtLink
                  to="/dashboard/create"
                  class="text-text-secondary hover:text-sidebar-orange transition-colors"
                  >Create</NuxtLink
                >
              </li>
              <li>
                <NuxtLink
                  to="/dashboard/create/templates"
                  class="text-text-secondary hover:text-sidebar-orange transition-colors"
                  >Templates</NuxtLink
                >
              </li>
              <li>
                <a
                  href="#"
                  class="text-text-secondary hover:text-sidebar-orange transition-colors"
                  >Pricing</a
                >
              </li>
              <li>
                <a
                  href="#"
                  class="text-text-secondary hover:text-sidebar-orange transition-colors"
                  >Features</a
                >
              </li>
            </ul>
          </div>

          <!-- Company -->
          <div>
            <h3 class="font-semibold mb-4">Company</h3>
            <ul class="space-y-2 text-sm">
              <li>
                <a
                  href="#"
                  class="text-text-secondary hover:text-sidebar-orange transition-colors"
                  >About Us</a
                >
              </li>
              <li>
                <a
                  href="#"
                  class="text-text-secondary hover:text-sidebar-orange transition-colors"
                  >Blog</a
                >
              </li>
              <li>
                <a
                  href="#"
                  class="text-text-secondary hover:text-sidebar-orange transition-colors"
                  >Careers</a
                >
              </li>
              <li>
                <a
                  href="#"
                  class="text-text-secondary hover:text-sidebar-orange transition-colors"
                  >Contact</a
                >
              </li>
            </ul>
          </div>

          <!-- Legal -->
          <div>
            <h3 class="font-semibold mb-4">Legal</h3>
            <ul class="space-y-2 text-sm">
              <li>
                <NuxtLink
                  to="/privacy"
                  class="text-text-secondary hover:text-sidebar-orange transition-colors"
                  >Privacy Policy</NuxtLink
                >
              </li>
              <li>
                <NuxtLink
                  to="/terms"
                  class="text-text-secondary hover:text-sidebar-orange transition-colors"
                  >Terms of Service</NuxtLink
                >
              </li>
              <li>
                <a
                  href="#"
                  class="text-text-secondary hover:text-sidebar-orange transition-colors"
                  >Cookie Policy</a
                >
              </li>
              <li>
                <a
                  href="#"
                  class="text-text-secondary hover:text-sidebar-orange transition-colors"
                  >GDPR</a
                >
              </li>
            </ul>
          </div>
        </div>

        <!-- Bottom bar -->
        <div
          class="pt-8 border-t border-card-border flex flex-col md:flex-row justify-between items-center gap-4"
        >
          <p class="text-text-secondary text-sm">
            © 2024 AI Infographics. All rights reserved.
          </p>
          <div class="flex gap-6">
            <a
              href="#"
              class="text-text-secondary hover:text-sidebar-orange transition-colors"
            >
              <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                <path
                  d="M24 4.557c-.883.392-1.832.656-2.828.775 1.017-.609 1.798-1.574 2.165-2.724-.951.564-2.005.974-3.127 1.195-.897-.957-2.178-1.555-3.594-1.555-3.179 0-5.515 2.966-4.797 6.045-4.091-.205-7.719-2.165-10.148-5.144-1.29 2.213-.669 5.108 1.523 6.574-.806-.026-1.566-.247-2.229-.616-.054 2.281 1.581 4.415 3.949 4.89-.693.188-1.452.232-2.224.084.626 1.956 2.444 3.379 4.6 3.419-2.07 1.623-4.678 2.348-7.29 2.04 2.179 1.397 4.768 2.212 7.548 2.212 9.142 0 14.307-7.721 13.995-14.646.962-.695 1.797-1.562 2.457-2.549z"
                />
              </svg>
            </a>
            <a
              href="#"
              class="text-text-secondary hover:text-sidebar-orange transition-colors"
            >
              <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                <path
                  d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"
                />
              </svg>
            </a>
            <a
              href="#"
              class="text-text-secondary hover:text-sidebar-orange transition-colors"
            >
              <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                <path
                  d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z"
                />
              </svg>
            </a>
          </div>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref } from "vue";

definePageMeta({
  layout: "default",
});

useSeoMeta({
  title: "AI Infographics - Create Stunning Infographics in Minutes",
  description:
    "Transform your content into beautiful, engaging infographics with AI-powered design. No design skills required. Start creating for free.",
});

const videoSection = ref(null);

const faqs = ref([
  {
    question: "How does the AI infographic generator work?",
    answer:
      "Our AI analyzes your content, extracts key information, and automatically designs a professional infographic that matches your chosen template and brand style. You can customize colors, fonts, and layouts with just a few clicks.",
    isOpen: false,
  },
  {
    question: "Can I use my own templates and branding?",
    answer:
      "Yes! Pro and Business plans allow you to upload your own templates and add custom branding including logos, colors, and fonts. You can maintain complete brand consistency across all your infographics.",
    isOpen: false,
  },
  {
    question: "What formats can I export my infographics in?",
    answer:
      "You can export your infographics in PNG, JPG, PDF, and SVG formats. Pro users get access to 4K resolution exports perfect for print and high-quality digital displays.",
    isOpen: false,
  },
  {
    question: "Do I need design experience to use this?",
    answer:
      "Not at all! Our platform is designed for everyone, regardless of design experience. The AI handles the design work while you focus on your content. Simply choose a template, add your content, and let the AI do the rest.",
    isOpen: false,
  },
  {
    question: "Can I cancel my subscription anytime?",
    answer:
      "Yes, you can cancel your subscription at any time with no penalties. You'll continue to have access to your plan benefits until the end of your billing period.",
    isOpen: false,
  },
  {
    question: "Is there a free trial for paid plans?",
    answer:
      "Yes! We offer a 14-day free trial for our Pro plan. No credit card required to start. You can explore all Pro features and create unlimited infographics during your trial period.",
    isOpen: false,
  },
]);

const toggleFaq = (index) => {
  faqs.value[index].isOpen = !faqs.value[index].isOpen;
};

const scrollToVideo = () => {
  if (videoSection.value) {
    videoSection.value.scrollIntoView({ behavior: "smooth", block: "center" });
  }
};
</script>
