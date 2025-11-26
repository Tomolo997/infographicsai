<template>
  <div class="min-h-screen">
    <!-- Hero Section -->
    <section class="relative pt-12 pb-20 overflow-hidden">
      <!-- Background Effects -->
      <div class="absolute inset-0 bg-sidebar-orange-bg"></div>
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
            <h1 class="text-display-xl mb-2">
              Create Stunning
              <span class="text-sidebar-orange">Infographics</span>
              from your Blog Posts
            </h1>
            <p
              class="text-body-xl text-gray-600 mb-10 max-w-xl leading-relaxed"
            >
              Transform your content into beautiful, engaging infographics that
              capture attention and drive results.
              <br />
              <span class="text-white bg-sidebar-orange px-2 py-1 rounded-md"
                >No design skills required.</span
              >
            </p>
            <div class="flex flex-col sm:flex-row gap-4">
              <NuxtLink to="/signup" class="btn-primary text-lg px-8 py-4">
                Start Creating
              </NuxtLink>
            </div>
            <!-- <div class="mt-8 flex items-center gap-4">
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
                  Trusted by 100+ creators
                </div>
                <div class="text-text-secondary">⭐⭐⭐⭐⭐ 4.9/5 rating</div>
              </div>
            </div> -->
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
                src="https://images.ainfographic.com/template_2_landing_page.png"
                alt="Infograph 1"
                class="w-full h-full object-cover"
              />
            </div>

            <!-- Back right infograph -->
            <div
              class="absolute top-0 right-0 w-64 transform rotate-[8deg] translate-x-[20px] translate-y-[40px] z-10 transition-transform duration-300 hover:scale-105"
            >
              <img
                src="https://images.ainfographic.com/infographs_3_landing_page.png"
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

    <!-- Features Section -->
    <section id="features" class="py-24 bg-sidebar-orange-bg">
      <div class="container-custom">
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-12 items-start">
          <!-- Left Side: Title, Subtitle, and Feature Cards -->
          <div>
            <h2 class="text-display-md mb-4">
              Powerful Features,
              <span class="text-sidebar-orange">Simple</span> to Use
            </h2>
            <p class="text-body-lg text-gray-600 mb-10 max-w-xl">
              Everything you need to create stunning infographics in one
              easy-to-use platform.
            </p>

            <!-- Feature Cards -->
            <div class="grid grid-cols-2 gap-4">
              <div
                v-for="(feature, index) in features"
                :key="index"
                @click="selectFeature(index)"
                :class="[
                  'flex items-start gap-4 p-4 rounded-xl cursor-pointer transition-all duration-300 border-2',
                  selectedFeatureIndex === index
                    ? 'bg-card-bg border-sidebar-orange shadow-lg'
                    : 'bg-card-bg/50 border-transparent hover:bg-card-bg hover:border-card-border',
                ]"
              >
                <!-- Icon -->
                <div
                  :class="[
                    'flex-shrink-0 w-12 h-12 rounded-xl flex items-center justify-center transition-all duration-300',
                    selectedFeatureIndex === index
                      ? feature.gradientClass
                      : 'bg-background-secondary',
                  ]"
                >
                  <component
                    :is="feature.icon"
                    :class="[
                      'w-6 h-6 transition-colors duration-300',
                      selectedFeatureIndex === index
                        ? 'text-white'
                        : 'text-text-secondary',
                    ]"
                  />
                </div>

                <!-- Content -->
                <div class="flex-1 min-w-0">
                  <h3
                    :class="[
                      'font-semibold mb-1 text-sm transition-colors duration-300',
                      selectedFeatureIndex === index
                        ? 'text-text-primary'
                        : 'text-text-primary',
                    ]"
                  >
                    {{ feature.title }}
                  </h3>
                  <p
                    class="text-xs text-text-secondary leading-relaxed line-clamp-2"
                  >
                    {{ feature.subtitle }}
                  </p>
                </div>

                <!-- Arrow indicator -->
                <div
                  :class="[
                    'flex-shrink-0 w-6 h-6 rounded-full flex items-center justify-center transition-all duration-300',
                    selectedFeatureIndex === index
                      ? 'bg-sidebar-orange text-white'
                      : 'bg-transparent',
                  ]"
                >
                  <svg
                    v-if="selectedFeatureIndex === index"
                    class="w-4 h-4"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                    stroke-width="2"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      d="M9 5l7 7-7 7"
                    />
                  </svg>
                </div>
              </div>
            </div>
          </div>

          <!-- Right Side: Video/Demo Area -->
          <div class="lg:sticky lg:top-48">
            <div
              class="relative bg-card-bg rounded-2xl border border-card-border overflow-hidden shadow-2xl"
            >
              <!-- Browser-like header -->
              <div
                class="flex items-center gap-2 px-4 py-3 bg-background-secondary border-b border-card-border"
              >
                <div class="flex gap-1.5">
                  <div class="w-3 h-3 rounded-full bg-red-500"></div>
                  <div class="w-3 h-3 rounded-full bg-yellow-500"></div>
                  <div class="w-3 h-3 rounded-full bg-green-500"></div>
                </div>
                <div
                  class="flex-1 mx-4 px-3 py-1 bg-background-primary rounded-md text-xs text-text-secondary text-center"
                >
                  ainfographic.com/dashboard
                </div>
              </div>

              <!-- Video/Image Content Area -->
              <div class="relative aspect-[16/9] bg-background-secondary">
                <!-- Placeholder for video - shows current feature demo -->
                <transition name="fade" mode="out-in">
                  <div
                    :key="selectedFeatureIndex"
                    class="absolute inset-0 flex items-center justify-center"
                  >
                    <!-- Video element -->
                    <video
                      v-if="features[selectedFeatureIndex].videoUrl"
                      :src="features[selectedFeatureIndex].videoUrl"
                      class="w-full object-contain"
                      autoplay
                      loop
                      muted
                      playsinline
                    ></video>

                    <!-- Fallback placeholder if no video -->
                    <div
                      v-else
                      class="w-full h-full flex flex-col items-center justify-center p-8"
                    >
                      <div
                        :class="[
                          'w-20 h-20 rounded-2xl flex items-center justify-center mb-6',
                          features[selectedFeatureIndex].gradientClass,
                        ]"
                      >
                        <component
                          :is="features[selectedFeatureIndex].icon"
                          class="w-10 h-10 text-white"
                        />
                      </div>
                      <h4 class="text-xl font-bold text-text-primary mb-2">
                        {{ features[selectedFeatureIndex].title }}
                      </h4>
                      <p
                        class="text-text-secondary text-center text-sm max-w-sm"
                      >
                        {{ features[selectedFeatureIndex].subtitle }}
                      </p>
                    </div>
                  </div>
                </transition>

                <!-- Feature indicator dots -->
                <div
                  class="absolute bottom-4 left-1/2 -translate-x-1/2 flex gap-2"
                >
                  <button
                    v-for="(_, index) in features"
                    :key="index"
                    @click="selectFeature(index)"
                    :class="[
                      'w-2 h-2 rounded-full transition-all duration-300',
                      selectedFeatureIndex === index
                        ? 'bg-sidebar-orange w-6'
                        : 'bg-text-secondary/30 hover:bg-text-secondary/50',
                    ]"
                  ></button>
                </div>
              </div>
            </div>

            <!-- Quick stats below video -->
          </div>
        </div>
      </div>
    </section>
    <!-- Video Demo Section -->
    <section
      ref="templateGallerySection"
      id="gallery"
      class="py-24 px-12 bg-sidebar-orange-bg"
    >
      <div class="container-custom">
        <div class="text-center mb-12">
          <h2 class="text-display-md mb-4">
            Our Beautiful Infographics Gallery
          </h2>
          <p class="text-body-lg text-gray-600 max-w-3xl mx-auto">
            Explore our collection of beautiful infographics created for our
            users.
          </p>
        </div>
        <div
          class="grid grid-cols-1 justify-center md:grid-cols-2 lg:grid-cols-3 gap-4"
        >
          <div class="w-full flex justify-center items-center">
            <img
              src="https://images.ainfographic.com/template_1_landing_page.png"
              alt="Infograph 1"
              class="w-full h-full object-cover"
            />
          </div>
          <div class="w-full flex justify-center items-center">
            <img
              src="https://images.ainfographic.com/template_2_landing_page.png"
              alt="Infograph 2"
              class="w-full h-full object-cover"
            />
          </div>
          <div class="w-full flex justify-center items-center">
            <img
              src="https://images.ainfographic.com/infographs_3_landing_page.png"
              alt="Infograph 3"
              class="w-full h-full object-cover"
            />
          </div>
          <div class="w-full flex justify-center items-center">
            <img
              src="https://images.ainfographic.com/templates/app_templates/template_3.webp"
              alt="Infograph 3"
              class="w-full h-full object-cover"
            />
          </div>
          <div class="w-full flex justify-center items-center">
            <img
              src="https://images.ainfographic.com/templates/app_templates/template_5.webp"
              alt="Infograph 3"
              class="w-full h-full object-cover"
            />
          </div>
          <div class="w-full flex justify-center items-center">
            <img
              src="https://images.ainfographic.com/templates/app_templates/template_6.webp"
              alt="Infograph 3"
              class="w-full h-full object-cover"
            />
          </div>
        </div>
      </div>
    </section>

    <!-- Why Use AI Infographic Section -->
    <section class="py-24 bg-sidebar-orange-bg">
      <div class="container-custom">
        <!-- Header -->
        <div class="text-center mb-12">
          <h2 class="text-display-md mb-4">
            Why use an
            <span class="text-sidebar-orange italic">AInfographic</span>
            Generator?
          </h2>
          <p class="text-body-lg text-gray-600 max-w-3xl mx-auto">
            Transform complex information into stunning visuals
            <span class="text-green-600 font-semibold"
              >in minutes, not hours</span
            >. Skip the learning curve and
            <span class="font-semibold">save 99% on design costs</span>.
          </p>
        </div>

        <!-- Benefit Tags -->
        <div class="flex flex-wrap justify-center gap-3 mb-16">
          <span
            class="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-white border border-gray-200 text-sm font-medium text-text-primary shadow-sm"
          >
            2-minute creation
          </span>
          <span
            class="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-white border border-gray-200 text-sm font-medium text-text-primary shadow-sm"
          >
            Fraction of the cost
          </span>
          <span
            class="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-white border border-gray-200 text-sm font-medium text-text-primary shadow-sm"
          >
            Professional quality
          </span>
          <span
            class="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-white border border-gray-200 text-sm font-medium text-text-primary shadow-sm"
          >
            AI-powered design
          </span>
        </div>

        <!-- Comparison Cards -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 max-w-6xl mx-auto">
          <!-- Traditional Design Card -->
          <div
            class="bg-white rounded-2xl border border-gray-200 p-8 shadow-lg"
          >
            <!-- Card Header -->
            <div class="flex items-center justify-between mb-8">
              <div class="flex items-center gap-3">
                <div
                  class="w-10 h-10 rounded-full bg-red-100 flex items-center justify-center"
                >
                  <svg
                    class="w-5 h-5 text-red-500"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                    stroke-width="2"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"
                    />
                  </svg>
                </div>
                <h3 class="text-xl font-bold text-text-primary">
                  Traditional Design Process
                </h3>
              </div>
              <span
                class="px-3 py-1 rounded-full bg-red-100 text-red-600 text-sm font-semibold"
              >
                9 hours
              </span>
            </div>

            <!-- Steps -->
            <div class="space-y-5">
              <div class="flex items-start gap-4">
                <div
                  class="flex-shrink-0 w-8 h-8 rounded-full bg-red-100 text-red-600 flex items-center justify-center text-sm font-bold"
                >
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="18"
                    height="18"
                    viewBox="0 0 24 24"
                  >
                    <!-- Icon from Lucide by Lucide Contributors - https://github.com/lucide-icons/lucide/blob/main/LICENSE -->
                    <g
                      fill="none"
                      stroke="currentColor"
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                    >
                      <path
                        d="M14 18a2 2 0 0 0-4 0m9-7l-2.11-6.657a2 2 0 0 0-2.752-1.148l-1.276.61A2 2 0 0 1 12 4H8.5a2 2 0 0 0-1.925 1.456L5 11m-3 0h20"
                      />
                      <circle cx="17" cy="18" r="3" />
                      <circle cx="7" cy="18" r="3" />
                    </g>
                  </svg>
                </div>
                <div class="flex-1">
                  <div class="flex justify-between items-start">
                    <div>
                      <h4 class="font-semibold text-text-primary">Research</h4>
                      <p class="text-sm text-text-secondary">
                        Understanding the topic and gathering relevant data
                      </p>
                    </div>
                    <span class="text-sm text-red-500 font-medium"
                      >2 hours</span
                    >
                  </div>
                </div>
              </div>

              <div class="flex items-start gap-4">
                <div
                  class="flex-shrink-0 w-8 h-8 rounded-full bg-red-100 text-red-600 flex items-center justify-center text-sm font-bold"
                >
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="18"
                    height="18"
                    viewBox="0 0 24 24"
                  >
                    <!-- Icon from Lucide by Lucide Contributors - https://github.com/lucide-icons/lucide/blob/main/LICENSE -->
                    <g
                      fill="none"
                      stroke="currentColor"
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                    >
                      <path
                        d="M12 3H5a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"
                      />
                      <path
                        d="M18.375 2.625a1 1 0 0 1 3 3l-9.013 9.014a2 2 0 0 1-.853.505l-2.873.84a.5.5 0 0 1-.62-.62l.84-2.873a2 2 0 0 1 .506-.852z"
                      />
                    </g>
                  </svg>
                </div>
                <div class="flex-1">
                  <div class="flex justify-between items-start">
                    <div>
                      <h4 class="font-semibold text-text-primary">
                        Conceptualization
                      </h4>
                      <p class="text-sm text-text-secondary">
                        Sketching ideas and planning the layout
                      </p>
                    </div>
                    <span class="text-sm text-red-500 font-medium"
                      >1.5 hours</span
                    >
                  </div>
                </div>
              </div>

              <div class="flex items-start gap-4">
                <div
                  class="flex-shrink-0 w-8 h-8 rounded-full bg-red-100 text-red-600 flex items-center justify-center text-sm font-bold"
                >
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="18"
                    height="18"
                    viewBox="0 0 24 24"
                  >
                    <!-- Icon from Lucide by Lucide Contributors - https://github.com/lucide-icons/lucide/blob/main/LICENSE -->
                    <g
                      fill="none"
                      stroke="currentColor"
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                    >
                      <path
                        d="M12.5 22H18a2 2 0 0 0 2-2V7l-5-5H6a2 2 0 0 0-2 2v9.5"
                      />
                      <path
                        d="M14 2v4a2 2 0 0 0 2 2h4m-6.622 7.626a1 1 0 1 0-3.004-3.004l-5.01 5.012a2 2 0 0 0-.506.854l-.837 2.87a.5.5 0 0 0 .62.62l2.87-.837a2 2 0 0 0 .854-.506z"
                      />
                    </g>
                  </svg>
                </div>
                <div class="flex-1">
                  <div class="flex justify-between items-start">
                    <div>
                      <h4 class="font-semibold text-text-primary">Design</h4>
                      <p class="text-sm text-text-secondary">
                        Creating and assembling visual elements
                      </p>
                    </div>
                    <span class="text-sm text-red-500 font-medium"
                      >4 hours</span
                    >
                  </div>
                </div>
              </div>

              <div class="flex items-start gap-4">
                <div
                  class="flex-shrink-0 w-8 h-8 rounded-full bg-red-100 text-red-600 flex items-center justify-center text-sm font-bold"
                >
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="18"
                    height="18"
                    viewBox="0 0 24 24"
                  >
                    <!-- Icon from Lucide by Lucide Contributors - https://github.com/lucide-icons/lucide/blob/main/LICENSE -->
                    <g
                      fill="none"
                      stroke="currentColor"
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                    >
                      <path
                        d="M2.062 12.348a1 1 0 0 1 0-.696a10.75 10.75 0 0 1 19.876 0a1 1 0 0 1 0 .696a10.75 10.75 0 0 1-19.876 0"
                      />
                      <circle cx="12" cy="12" r="3" />
                    </g>
                  </svg>
                </div>
                <div class="flex-1">
                  <div class="flex justify-between items-start">
                    <div>
                      <h4 class="font-semibold text-text-primary">Review</h4>
                      <p class="text-sm text-text-secondary">
                        Checking accuracy and visual appeal
                      </p>
                    </div>
                    <span class="text-sm text-red-500 font-medium">1 hour</span>
                  </div>
                </div>
              </div>

              <div class="flex items-start gap-4">
                <div
                  class="flex-shrink-0 w-8 h-8 rounded-full bg-red-100 text-red-600 flex items-center justify-center text-sm font-bold"
                >
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="18"
                    height="18"
                    viewBox="0 0 24 24"
                  >
                    <!-- Icon from Lucide by Lucide Contributors - https://github.com/lucide-icons/lucide/blob/main/LICENSE -->
                    <g
                      fill="none"
                      stroke="currentColor"
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                    >
                      <path
                        d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"
                      />
                      <path d="M14 2v4a2 2 0 0 0 2 2h4M8 16l2-2l-2-2m4 6h4" />
                    </g>
                  </svg>
                </div>
                <div class="flex-1">
                  <div class="flex justify-between items-start">
                    <div>
                      <h4 class="font-semibold text-text-primary">
                        Finalization
                      </h4>
                      <p class="text-sm text-text-secondary">
                        Final adjustments and export
                      </p>
                    </div>
                    <span class="text-sm text-red-500 font-medium"
                      >0.5 hours</span
                    >
                  </div>
                </div>
              </div>
            </div>

            <!-- Cost Footer -->
            <div
              class="mt-8 pt-6 border-t border-gray-200 flex justify-between items-end"
            >
              <div>
                <p class="text-sm text-text-secondary">Designer Cost</p>
                <p class="text-3xl font-bold text-text-primary">$315</p>
              </div>
              <p class="text-sm text-text-secondary">$35/hour × 9 hours</p>
            </div>
          </div>

          <!-- AI-Powered Design Card -->
          <div
            class="bg-gradient-to-br from-green-50 to-emerald-50 rounded-2xl border-2 border-green-200 p-8 shadow-lg relative overflow-hidden"
          >
            <!-- Decorative glow -->
            <div
              class="absolute top-0 right-0 w-32 h-32 rounded-full blur-3xl"
            ></div>

            <!-- Card Header -->
            <div class="flex items-center justify-between mb-8 relative">
              <div class="flex items-center gap-3">
                <div
                  class="w-10 h-10 rounded-full bg-green-100 flex items-center justify-center"
                >
                  <svg
                    class="w-5 h-5 text-green-600"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                    stroke-width="2"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      d="M13 10V3L4 14h7v7l9-11h-7z"
                    />
                  </svg>
                </div>
                <h3 class="text-xl font-bold text-text-primary">
                  AI-Powered Design
                </h3>
              </div>
              <span
                class="px-3 py-1 rounded-full bg-green-100 text-green-600 text-sm font-semibold"
              >
                2 minutes
              </span>
            </div>

            <!-- AI Features -->
            <div class="space-y-5 relative">
              <div class="flex items-start gap-4">
                <div
                  class="flex-shrink-0 w-8 h-8 rounded-full bg-green-100 flex items-center justify-center"
                >
                  <svg
                    class="w-4 h-4 text-green-600"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                    stroke-width="2"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
                    />
                  </svg>
                </div>
                <div class="flex-1">
                  <h4 class="font-semibold text-text-primary">
                    Instant research
                  </h4>
                  <p class="text-sm text-green-600">
                    AI analyzes and summarizes content in seconds
                  </p>
                </div>
              </div>

              <div class="flex items-start gap-4">
                <div
                  class="flex-shrink-0 w-8 h-8 rounded-full bg-green-100 flex items-center justify-center"
                >
                  <svg
                    class="w-4 h-4 text-green-600"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                    stroke-width="2"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"
                    />
                  </svg>
                </div>
                <div class="flex-1">
                  <h4 class="font-semibold text-text-primary">
                    Beautiful Templates
                  </h4>
                  <p class="text-sm text-green-600">
                    Perfect visuals, zero effort
                  </p>
                </div>
              </div>

              <div class="flex items-start gap-4">
                <div
                  class="flex-shrink-0 w-8 h-8 rounded-full bg-green-100 flex items-center justify-center"
                >
                  <svg
                    class="w-4 h-4 text-green-600"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                    stroke-width="2"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"
                    />
                  </svg>
                </div>
                <div class="flex-1">
                  <h4 class="font-semibold text-text-primary">Smart design</h4>
                  <p class="text-sm text-green-600">
                    Professional layouts automagically
                  </p>
                </div>
              </div>

              <div class="flex items-start gap-4">
                <div
                  class="flex-shrink-0 w-8 h-8 rounded-full bg-green-100 flex items-center justify-center"
                >
                  <svg
                    class="w-4 h-4 text-green-600"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                    stroke-width="2"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12"
                    />
                  </svg>
                </div>
                <div class="flex-1">
                  <h4 class="font-semibold text-text-primary">
                    One-click export
                  </h4>
                  <p class="text-sm text-green-600">
                    Download in any format instantly
                  </p>
                </div>
              </div>
            </div>

            <!-- Cost Footer -->
            <div
              class="mt-8 pt-6 border-t border-green-200 flex justify-between items-end relative"
            >
              <div>
                <p class="text-sm text-text-secondary">Cost Per Design</p>
                <p class="text-3xl font-bold text-green-600">
                  $0.50<span class="text-lg font-normal text-text-secondary">
                    or less</span
                  >
                </p>
              </div>
              <div class="text-right">
                <p class="text-4xl font-bold text-green-600">99%</p>
                <p class="text-sm text-text-secondary">cost savings</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Pricing & FAQ Section -->
    <section id="pricing" class="py-24 bg-sidebar-orange-bg">
      <div class="container-custom">
        <!-- Pricing -->
        <div class="mb-24">
          <div class="text-center mb-12">
            <h2 class="text-display-md mb-4">Simple, Credit based pricing</h2>
            <p class="text-body-lg text-gray-600 max-w-3xl mx-auto">
              Choose the plan that fits your needs.
            </p>
          </div>

          <div
            class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 max-w-7xl mx-auto"
          >
            <!-- 10 Credits -->
            <div
              class="card p-6 bg-card-bg hover:border-sidebar-orange/50 transition-all flex flex-col"
            >
              <div class="mb-4">
                <div class="text-3xl font-bold mb-1 text-text-primary">
                  10 Credits
                </div>
                <div class="text-3xl font-bold mb-2 text-sidebar-orange">
                  $5
                </div>
                <p class="text-text-secondary text-xs">$0.50 per credit</p>
              </div>
              <div class="flex-1"></div>
              <NuxtLink
                to="/dashboard"
                class="btn-outline w-full text-center mt-4"
              >
                Buy Credits
              </NuxtLink>
            </div>

            <!-- 50 Credits -->
            <div
              class="card p-6 bg-card-bg hover:border-sidebar-orange/50 transition-all flex flex-col"
            >
              <div class="mb-4">
                <div class="text-3xl font-bold mb-1 text-text-primary">
                  50 Credits
                </div>
                <div class="text-3xl font-bold mb-2 text-sidebar-orange">
                  $25
                </div>
                <p class="text-text-secondary text-xs">$0.50 per credit</p>
              </div>
              <div class="flex-1"></div>
              <NuxtLink
                to="/dashboard"
                class="btn-outline w-full text-center mt-4"
              >
                Buy Credits
              </NuxtLink>
            </div>

            <!-- 100 Credits - Featured -->
            <div
              class="card p-6 bg-card-bg relative border-2 border-sidebar-orange shadow-xl flex flex-col"
            >
              <div
                class="absolute -top-3 left-1/2 -translate-x-1/2 bg-sidebar-orange text-white px-3 py-1 rounded-full text-xs font-semibold"
              >
                Best Value
              </div>
              <div class="mb-4 mt-2">
                <div class="text-3xl font-bold mb-1 text-text-primary">
                  100 Credits
                </div>
                <div class="text-3xl font-bold mb-2 text-sidebar-orange">
                  $45
                </div>
                <p class="text-text-secondary text-xs">$0.45 per credit</p>
              </div>
              <div class="flex-1"></div>
              <NuxtLink
                to="/dashboard"
                class="btn-primary w-full text-center mt-4"
              >
                Buy Credits
              </NuxtLink>
            </div>

            <!-- 200 Credits -->
            <div
              class="card p-6 bg-card-bg hover:border-sidebar-orange/50 transition-all flex flex-col"
            >
              <div class="mb-4">
                <div class="text-3xl font-bold mb-1 text-text-primary">
                  200 Credits
                </div>
                <div class="text-3xl font-bold mb-2 text-sidebar-orange">
                  $89
                </div>
                <p class="text-text-secondary text-xs">$0.45 per credit</p>
              </div>
              <div class="flex-1"></div>
              <NuxtLink
                to="/dashboard"
                class="btn-outline w-full text-center mt-4"
              >
                Buy Credits
              </NuxtLink>
            </div>
          </div>
        </div>

        <!-- FAQ -->
        <div class="max-w-3xl mx-auto">
          <div class="text-center mb-12">
            <h2 class="text-display-sm mb-4">Frequently Asked Questions</h2>
            <p class="text-gray-600 text-body-lg">
              Everything you need to know about our platform
            </p>
          </div>

          <div class="space-y-4">
            <div
              v-for="(faq, index) in faqs"
              :key="index"
              class="card bg-card-bg p-0 overflow-hidden"
            >
              <button
                @click="toggleFaq(index)"
                class="w-full px-6 py-5 text-left flex justify-between items-center transition-colors"
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
                class="px-6 pb-5 text-gray-600 leading-relaxed"
              >
                {{ faq.answer }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Final CTA -->
  </div>
</template>

<script setup>
import { ref, shallowRef, h } from "vue";

definePageMeta({
  layout: "default",
});

useSeoMeta({
  title: "AI Infographics - Create Stunning Infographics in Minutes",
  description:
    "Transform your content into beautiful, engaging infographics with AI-powered design. No design skills required. Start creating for free.",
});

const videoSection = ref(null);
const selectedFeatureIndex = ref(0);

// Icon components as render functions
const LinkIcon = {
  render() {
    return h(
      "svg",
      {
        fill: "none",
        stroke: "currentColor",
        viewBox: "0 0 24 24",
        strokeWidth: "2",
      },
      [
        h("path", {
          strokeLinecap: "round",
          strokeLinejoin: "round",
          d: "M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1",
        }),
      ]
    );
  },
};

const DocumentIcon = {
  render() {
    return h(
      "svg",
      {
        fill: "none",
        stroke: "currentColor",
        viewBox: "0 0 24 24",
        strokeWidth: "2",
      },
      [
        h("path", {
          strokeLinecap: "round",
          strokeLinejoin: "round",
          d: "M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z",
        }),
      ]
    );
  },
};

const ImageIcon = {
  render() {
    return h(
      "svg",
      {
        fill: "none",
        stroke: "currentColor",
        viewBox: "0 0 24 24",
        strokeWidth: "2",
      },
      [
        h("path", {
          strokeLinecap: "round",
          strokeLinejoin: "round",
          d: "M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z",
        }),
      ]
    );
  },
};

const ChartIcon = {
  render() {
    return h(
      "svg",
      {
        fill: "none",
        stroke: "currentColor",
        viewBox: "0 0 24 24",
        strokeWidth: "2",
      },
      [
        h("path", {
          strokeLinecap: "round",
          strokeLinejoin: "round",
          d: "M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z",
        }),
      ]
    );
  },
};

const AspectRatioIcon = {
  render() {
    return h(
      "svg",
      {
        fill: "none",
        stroke: "currentColor",
        viewBox: "0 0 24 24",
        strokeWidth: "2",
      },
      [
        h("path", {
          strokeLinecap: "round",
          strokeLinejoin: "round",
          d: "M4 5a1 1 0 011-1h4a1 1 0 011 1v4a1 1 0 01-1 1H5a1 1 0 01-1-1V5zM14 5a1 1 0 011-1h4a1 1 0 011 1v4a1 1 0 01-1 1h-4a1 1 0 01-1-1V5zM4 15a1 1 0 011-1h4a1 1 0 011 1v4a1 1 0 01-1 1H5a1 1 0 01-1-1v-4zM14 15a1 1 0 011-1h4a1 1 0 011 1v4a1 1 0 01-1 1h-4a1 1 0 01-1-1v-4z",
        }),
      ]
    );
  },
};

const ResolutionIcon = {
  render() {
    return h(
      "svg",
      {
        fill: "none",
        stroke: "currentColor",
        viewBox: "0 0 24 24",
        strokeWidth: "2",
      },
      [
        h("path", {
          strokeLinecap: "round",
          strokeLinejoin: "round",
          d: "M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z",
        }),
      ]
    );
  },
};

const features = shallowRef([
  {
    title: "Create from Blog URL",
    subtitle:
      "Simply paste your blog URL and let our AI extract the key points and create a beautiful infographic automatically.",
    icon: LinkIcon,
    gradientClass: "bg-gradient-to-br from-blue-500 to-blue-600",
    videoUrl: "https://images.ainfographic.com/video_presentation.mp4", // Add video URL when available
  },
  {
    title: "Create from PDF",
    subtitle:
      "Upload any PDF document and transform it into a visually stunning infographic. Perfect for reports, whitepapers, and presentations.",
    icon: DocumentIcon,
    gradientClass: "bg-gradient-to-br from-red-500 to-pink-600",
    videoUrl: "https://images.ainfographic.com/pdf_presentation.mp4",
  },
  {
    title: "Use Your Own Template",
    subtitle:
      "Upload your existing infographic template image and let our AI populate it with your content while maintaining your unique style.",
    icon: ImageIcon,
    gradientClass: "bg-gradient-to-br from-sidebar-orange to-yellow-500",
    videoUrl: "https://images.ainfographic.com/own_template_presentation.mp4",
  },
  {
    title: "Multiple Visual Types",
    subtitle:
      "Create infographics, mindmaps, roadmaps, timelines, flowcharts, and organization charts. Choose the perfect format for your content.",
    icon: ChartIcon,
    gradientClass: "bg-gradient-to-br from-purple-500 to-purple-600",
    videoUrl: null,
  },
  {
    title: "Flexible Aspect Ratios",
    subtitle:
      "Choose from 8+ aspect ratios optimized for Instagram, TikTok, LinkedIn, Twitter, Pinterest, and more. Perfect for any platform.",
    icon: AspectRatioIcon,
    gradientClass: "bg-gradient-to-br from-green-500 to-emerald-600",
    videoUrl: null,
  },
  {
    title: "High Resolution Export",
    subtitle:
      "Export your infographics in 1K, 2K, or stunning 4K resolution. Perfect for print, presentations, and high-quality digital displays.",
    icon: ResolutionIcon,
    gradientClass: "bg-gradient-to-br from-cyan-500 to-blue-600",
    videoUrl: null,
  },
]);

const selectFeature = (index) => {
  selectedFeatureIndex.value = index;
};

const faqs = ref([
  {
    question: "How does the AI infographic generator work?",
    answer:
      "Our AI analyzes your content, extracts key information, and automatically designs a professional infographic that matches your chosen template and brand style.",
    isOpen: false,
  },
  {
    question: "Can I use my own templates and branding?",
    answer:
      "Yes! You can upload your own templates. You can maintain complete brand consistency across all your infographics.",
    isOpen: false,
  },
  {
    question: "What formats can I export my infographics in?",
    answer:
      "You can export your infographics in PNG, in the future we will support also JPEG. You get access to 4K resolution exports perfect for print and high-quality digital displays.",
    isOpen: false,
  },
  {
    question: "Do I need design experience to use this?",
    answer:
      "Not at all! Our platform is designed for everyone, regardless of design experience. The AI handles the design work while you focus on your content. Simply choose a template, add your content, and let the AI do the rest. We also provide a lot of templates to choose from.",
    isOpen: false,
  },
  {
    question: "Can I cancel my credits anytime?",
    answer:
      "Yes, you can cancel your credits at any time. You'll continue to have access to your credits until you use them all.",
    isOpen: false,
  },
  {
    question: "Is there a free trial for paid plans?",
    answer:
      "No, we offer credit based pricing. You can buy credits and use them to create infographics.",
    isOpen: false,
  },
]);

const toggleFaq = (index) => {
  faqs.value[index].isOpen = !faqs.value[index].isOpen;
};

const templateGallerySection = ref(null);

const scrollToVideo = () => {
  if (templateGallerySection.value) {
    templateGallerySection.value.scrollIntoView({
      behavior: "smooth",
      block: "center",
    });
  }
};
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
