<template>
  <div class="w-full">
    <Header />

    <!-- Hero Section -->

    <div class="hero-section mt-[70px]">
      <div class="hero-container">
        <div class="hero-content">
          <h1 class="hero-title font-sans">
            Turn blog posts into <br />
            <span class="highlight-text">scroll-stopping</span> <br />
            infographics.
          </h1>
          <div></div>
          <div class="ai-form-container mt-[40px]">
            <div class="form-card">
              <!-- Tabs -->
              <div class="form-tabs">
                <button
                  class="form-tab"
                  :class="{ active: activeTab === 'infographic' }"
                  @click="setActiveTab('infographic')"
                >
                  <div
                    v-if="isGenerating"
                    class="absolute inset-0 flex items-center justify-center bg-white bg-opacity-80 z-10 rounded-t-lg"
                  >
                    <div
                      class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"
                    ></div>
                  </div>
                  <span v-else class="tab-icon">
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      class="h-5 w-5"
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke="currentColor"
                    >
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"
                      />
                    </svg>
                  </span>
                  Infographic
                </button>
              </div>

              <!-- Form Input -->
              <div class="form-input-container">
                <!-- Show input field for URL or textarea for content based on currentTopic -->
                <input
                  v-if="currentTopic === 'URL'"
                  type="text"
                  class="form-input"
                  v-model="inputText"
                  placeholder="Enter your blog post URL"
                />
                <textarea
                  v-else
                  class="form-input"
                  v-model="inputText"
                  placeholder="Enter your content here"
                />
                <!-- Hide the default textarea since we're conditionally rendering input elements -->
              </div>

              <!-- Form Actions -->
              <div class="form-actions">
                <div class="form-dropdown relative" ref="topicDropdownRef">
                  <button
                    class="dropdown-button"
                    :class="{ active: showTopicDropdown }"
                    @click.stop="toggleTopicDropdown"
                  >
                    {{ currentTopic }}
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      class="h-4 w-4 ml-2"
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke="currentColor"
                    >
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M19 9l-7 7-7-7"
                      />
                    </svg>
                  </button>
                  <!-- Topic Dropdown Menu -->
                  <div v-if="showTopicDropdown" class="dropdown-menu">
                    <button
                      v-for="topic in topics"
                      :key="topic"
                      class="dropdown-item"
                      :class="{ 'selected-item': currentTopic === topic }"
                      @click.stop="selectTopic(topic)"
                    >
                      <span v-if="currentTopic === topic" class="check-icon"
                        >✓</span
                      >
                      {{ topic }}
                    </button>
                  </div>
                </div>
                <div class="form-dropdown relative" ref="languageDropdownRef">
                  <button
                    class="dropdown-button"
                    :class="{ active: showLanguageDropdown }"
                    @click.stop="toggleLanguageDropdown"
                  >
                    {{ currentLanguage }}
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      class="h-4 w-4 ml-2"
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke="currentColor"
                    >
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M19 9l-7 7-7-7"
                      />
                    </svg>
                  </button>
                  <!-- Language Dropdown Menu -->
                  <div v-if="showLanguageDropdown" class="dropdown-menu">
                    <button
                      v-for="language in languages"
                      :key="language"
                      class="dropdown-item"
                      :class="{ 'selected-item': currentLanguage === language }"
                      @click.stop="selectLanguage(language)"
                    >
                      <span
                        v-if="currentLanguage === language"
                        class="check-icon"
                        >✓</span
                      >
                      {{ language }}
                    </button>
                  </div>
                </div>
                <button
                  class="form-submit-button"
                  :disabled="isGenerating || !inputText"
                  @click="handleGenerateClick"
                >
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    class="h-5 w-5"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M5 10l7-7m0 0l7 7m-7-7v18"
                    />
                  </svg>
                </button>
              </div>
            </div>

            <!-- Quick Topics -->
            <div class="quick-topics">
              <NuxtLink
                href="/"
                class="premium-tag cursor-pointer"
                @click="subscribe(12)"
              >
                <span class="flex items-center">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    class="h-4 w-4 mr-1"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z"
                    />
                  </svg>
                  Get Lifetime Access
                </span>
              </NuxtLink>
            </div>
          </div>
        </div>

        <!-- AI Loading Animation -->
        <div class="ai-loading-container" v-if="isGenerating">
          <div class="loading-animation">
            <div class="loading-spinner">
              <div class="spinner-ring"></div>
            </div>
            <div class="loading-text">
              {{ generationStatus }}
            </div>
          </div>
        </div>

        <!-- Generated Infographics Results -->
        <div
          v-if="generatedInfographics.length > 0"
          class="generated-infographics-container"
        >
          <h1 class="results-title">Your Generated Infographics</h1>
          <div class="results-grid">
            <ListTemplatePublicInfographCard
              v-for="infograph in generatedInfographics"
              :key="infograph.id"
              :infograph="infograph"
            ></ListTemplatePublicInfographCard>
          </div>
        </div>

        <div class="hero-image">
          <div class="video-container">
            <video
              autoplay
              muted
              loop
              playsinline
              class="video-player"
              controls
              preload="metadata"
            >
              <source
                src="https://images.ainfographic.com/dashboard_movie.mov"
                type="video/mp4"
                autoplay
              />
              Your browser does not support the video tag.
            </video>
          </div>
        </div>
      </div>
    </div>

    <!-- Signup Modal -->
    <SignupModal :isOpen="showSignupModal" @close="closeSignupModal" />

    <!-- Benefits Section -->
    <div class="benefits-section" id="features">
      <div class="section-container">
        <div class="section-header">
          <h2 class="section-title">Benefits of Ainfographic</h2>
          <p class="section-subtitle">
            Create beautiful infographics easily with our powerful features
          </p>
        </div>

        <div class="benefits-grid">
          <div class="benefit-card">
            <div class="benefit-icon">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                class="h-8 w-8"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M13 10V3L4 14h7v7l9-11h-7z"
                />
              </svg>
            </div>
            <h3 class="benefit-title">Instant Generation</h3>
            <p class="benefit-description">
              Turn any blog post or content into a beautiful infographic in
              seconds with AI
            </p>
          </div>

          <div class="benefit-card">
            <div class="benefit-icon">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                class="h-8 w-8"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M4 5a1 1 0 011-1h14a1 1 0 011 1v2a1 1 0 01-1 1H5a1 1 0 01-1-1V5zM4 13a1 1 0 011-1h6a1 1 0 011 1v6a1 1 0 01-1 1H5a1 1 0 01-1-1v-6zM16 13a1 1 0 011-1h2a1 1 0 011 1v6a1 1 0 01-1 1h-2a1 1 0 01-1-1v-6z"
                />
              </svg>
            </div>
            <h3 class="benefit-title">Customizable Templates</h3>
            <p class="benefit-description">
              Choose from dozens of professionally designed templates that fit
              your brand
            </p>
          </div>

          <div class="benefit-card">
            <div class="benefit-icon">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                class="h-8 w-8"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"
                />
              </svg>
            </div>
            <h3 class="benefit-title">Social Media Ready</h3>
            <p class="benefit-description">
              Export in perfect sizes for all social platforms with one click
            </p>
          </div>

          <div class="benefit-card">
            <div class="benefit-icon">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                class="h-8 w-8"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"
                />
              </svg>
            </div>
            <h3 class="benefit-title">World class editor</h3>
            <p class="benefit-description">
              Create infographics with our world class editor
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- Templates Section -->
    <div class="templates-section" id="templates">
      <div class="section-container">
        <div class="section-header">
          <h2 class="section-title">Beautiful Templates</h2>
          <p class="section-subtitle">
            Choose from a variety of professionally designed templates, sneak
            peak of some of them:
          </p>
        </div>

        <div class="templates-grid">
          <div class="template-card">
            <div class="template-image">
              <img
                src="https://images.ainfographic.com/template_1.jpg"
                alt="Infographic Template"
                class="template-img"
              />
            </div>
            <div class="template-info">
              <h3 class="template-title">Marcus Aurelius</h3>
              <p class="template-description">
                Infographic about Marcus Aurelius from this link
                <a
                  class="text-primary"
                  href="https://en.wikipedia.org/wiki/Marcus_Aurelius"
                  target="_blank"
                  >Link</a
                >
              </p>
            </div>
          </div>

          <div class="template-card">
            <div class="template-image">
              <img
                src="https://images.ainfographic.com/template_2.jpg"
                alt="Infographic Template"
                class="template-img"
              />
            </div>
            <div class="template-info">
              <h3 class="template-title">Understanding Masculinity</h3>
              <p class="template-description">
                https://en.wikipedia.org/wiki/Masculinity Infographic about
                Understanding Masculinity from this link
                <a
                  class="text-primary"
                  href="https://en.wikipedia.org/wiki/Marcus_Aurelius"
                  target="_blank"
                  >Link</a
                >
              </p>
            </div>
          </div>

          <div class="template-card">
            <div class="template-image">
              <img
                src="https://images.ainfographic.com/template_3.jpg"
                alt="Infographic Template"
                class="template-img"
              />
            </div>
            <div class="template-info">
              <h3 class="template-title">
                Using LLMs to Write Code Effectively
              </h3>
              <p class="template-description">
                Infographic about Using LLMs to Write Code Effectively from this
                link
                <a
                  class="text-primary"
                  href="https://simonwillison.net/2025/Mar/11/using-llms-for-code/?fbclid=IwY2xjawI-lBNleHRuA2FlbQIxMAABHcKnyfxc68Tlc8DuAuC4OATwqMTwprBrzDRAYf8Z9R0TOXsGuDYOfiFOVw_aem_-BJPyA1CReSE8c1ya3IXHA"
                  target="_blank"
                  >Link</a
                >
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Editor Video Section -->
    <div class="editor-video-section">
      <div class="section-container">
        <div class="section-header">
          <h2 class="section-title">Easy-to-use Editor</h2>
          <p class="section-subtitle">
            Create stunning infographics with our intuitive editor
          </p>
        </div>

        <div class="editor-video-container">
          <video
            autoplay
            muted
            loop
            playsinline
            class="video-player"
            controls
            preload="metadata"
          >
            <source
              src="https://images.ainfographic.com/editor.mov"
              type="video/mp4"
            />
            Your browser does not support the video tag.
          </video>
        </div>
      </div>
    </div>

    <!-- Pricing Section -->
    <div id="pricing" class="pricing-section">
      <div class="section-container">
        <div class="section-header">
          <h2 class="section-title">Choose Your Plan</h2>
          <p class="section-subtitle">Find the perfect plan for your needs</p>
        </div>

        <div v-if="loading" class="loading-container">
          <div class="loading-spinner"></div>
          <p>Loading subscription plans...</p>
        </div>

        <div v-else-if="error" class="error-container">
          <p>{{ error }}</p>
        </div>

        <div v-else class="pricing-grid">
          <!-- Free Tier -->
          <div v-for="tier in freeTiers" :key="tier.id" class="pricing-card">
            <div class="pricing-header">
              <h3 class="pricing-title">{{ tier.name }}</h3>
              <div class="pricing-price">
                <span class="price">${{ tier.price }}</span>
                <span class="period" v-if="!isLifetime(tier)">/month</span>
              </div>
            </div>
            <ul class="pricing-features">
              <li class="pricing-feature">
                {{ tier.monthly_download_limit }} downloads per month
              </li>
              <li class="pricing-feature">
                {{ tier.ai_credits }} AI credits monthly
              </li>
              <li class="pricing-feature">Basic support</li>
              <li class="pricing-feature">All templates</li>
            </ul>
            <div class="pricing-action">
              <button
                :disabled="isProcessing"
                @click="subscribe(tier.id)"
                class="pricing-button"
              >
                Get Started
              </button>
            </div>
          </div>

          <!-- Monthly Tiers -->
          <div
            v-for="tier in monthlyTiers"
            :key="tier.id"
            class="pricing-card"
            :class="{ popular: isPopular(tier) }"
          >
            <div v-if="isPopular(tier)" class="popular-badge">Most Popular</div>
            <div class="pricing-header">
              <h3 class="pricing-title">{{ tier.name }}</h3>
              <div class="pricing-price">
                <span class="price">${{ tier.price }}</span>
                <span class="period">/month</span>
              </div>
            </div>
            <ul class="pricing-features">
              <li class="pricing-feature">
                {{ tier.monthly_download_limit }} downloads per month
              </li>
              <li class="pricing-feature">
                {{ tier.ai_credits }} AI credits monthly
              </li>
              <li class="pricing-feature">All templates</li>
              <li class="pricing-feature">Priority support</li>
              <!-- <li class="pricing-feature">Brand kit integration</li> -->
              <!-- <li v-if="isPremium(tier)" class="pricing-feature">
                Advanced analytics
              </li>
              <li v-if="isPremium(tier)" class="pricing-feature">
                Team collaboration
              </li>
              <li v-if="isPremium(tier)" class="pricing-feature">API access</li> -->
            </ul>
            <div class="pricing-action">
              <button
                :disabled="isProcessing"
                @click="subscribe(tier.id)"
                class="pricing-button"
                :class="{ primary: isPopular(tier) }"
              >
                Get Started
              </button>
            </div>
          </div>

          <!-- Lifetime Tiers -->
          <div
            v-for="tier in lifetimeTiers"
            :key="tier.id"
            class="pricing-card"
          >
            <div class="pricing-header">
              <h3 class="pricing-title">
                {{ tier.name }}
                <span class="discount-badge">50% off</span>
              </h3>
              <div class="flex flex-col justify-center items-center">
                <span class="old-price">${{ tier.price }}</span>
              </div>
              <div class="pricing-price">
                <span class="price flex flex-col">${{ tier.price / 2 }}</span>
                <span class="period"></span>
              </div>
            </div>
            <ul class="pricing-features">
              <li class="pricing-feature">
                {{
                  tier.monthly_download_limit === 999999
                    ? "Unlimited"
                    : tier.monthly_download_limit
                }}
                downloads per month
              </li>
              <li class="pricing-feature">
                {{ tier.ai_credits }} AI credits monthly
              </li>
              <li class="pricing-feature">Premium templates</li>
              <!-- <li class="pricing-feature">Advanced analytics</li> -->
              <!-- <li class="pricing-feature">Team collaboration</li> -->
              <!-- <li class="pricing-feature">Custom branding</li> -->
              <!-- <li class="pricing-feature">API access</li> -->
              <li class="pricing-feature">Lifetime access</li>
            </ul>
            <div class="pricing-action">
              <button
                :disabled="isProcessing"
                @click="subscribe(tier.id)"
                class="pricing-button"
                :class="{ primary: isPopular(tier) }"
              >
                Get Started
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- FAQ Section -->
    <div id="faq" class="faq-section">
      <div class="section-container">
        <div class="section-header">
          <h2 class="section-title">Frequently Asked Questions</h2>
          <p class="section-subtitle">
            Find answers to common questions about Ainfographic
          </p>
        </div>

        <div class="faq-container">
          <div class="faq-item" v-for="(item, index) in faqItems" :key="index">
            <div class="faq-question" @click="toggleFaq(index)">
              <h3 class="faq-question-text">{{ item.question }}</h3>
              <div class="faq-icon">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  class="h-6 w-6"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                  :class="{ 'rotate-180': item.isOpen }"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M19 9l-7 7-7-7"
                  />
                </svg>
              </div>
            </div>
            <div class="faq-answer" v-show="item.isOpen">
              <p>{{ item.answer }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
    <button @click="test">Test</button>
    <!-- Footer Section -->
    <footer class="footer-section">
      <div class="footer-container">
        <div class="footer-left">
          <div class="footer-logo">
            <Logo></Logo>
            <span class="footer-logo-text">Ainfographic</span>
          </div>
          <p class="footer-description">
            Turn any URL or content into shareable infographics for social
            media, blogs, and marketing.
          </p>
        </div>

        <div class="footer-right">
          <div class="footer-column">
            <h4 class="footer-column-title">Product</h4>
            <ul class="footer-links">
              <li>
                <NuxtLink to="/#features" class="footer-link"
                  >Features</NuxtLink
                >
              </li>
              <li>
                <NuxtLink to="/#templates" class="footer-link"
                  >Templates</NuxtLink
                >
              </li>
              <li>
                <NuxtLink to="/#pricing" class="footer-link">Pricing</NuxtLink>
              </li>
            </ul>
          </div>

          <div class="footer-column">
            <h4 class="footer-column-title">Company</h4>
            <ul class="footer-links">
              <li>
                <a href="mailto:tomazovsenjak7@gmail.com" class="footer-link"
                  >Contact</a
                >
              </li>
            </ul>
          </div>

          <div class="footer-column">
            <h4 class="footer-column-title">Legal</h4>
            <ul class="footer-links">
              <li>
                <NuxtLink to="/terms-and-conditions" class="footer-link"
                  >Terms of Service</NuxtLink
                >
              </li>
              <li>
                <NuxtLink to="/privacy" class="footer-link"
                  >Privacy Policy</NuxtLink
                >
              </li>
              <li><NuxtLink to="/#faq" class="footer-link">FAQ</NuxtLink></li>
            </ul>
          </div>
        </div>
      </div>

      <div class="footer-bottom">
        <p class="footer-copyright">
          © {{ new Date().getFullYear() }} Ainfographic. All rights reserved.
        </p>
        <div class="footer-legal">
          <NuxtLink to="/terms-and-conditions" class="footer-legal-link"
            >Terms of Service</NuxtLink
          >
          <NuxtLink to="/privacy" class="footer-legal-link"
            >Privacy Policy</NuxtLink
          >
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import apiClient, { getProxyUrl } from "~/services/apiClient";
import ListTemplateCard from "~/components/ListTemplateCard.vue";
import ListTemplateInfographCard from "~/components/ListTemplateInfographCard.vue";
import ListTemplatePublicInfographCard from "~/components/ListTemplatePublicInfographCard.vue";
import SignupModal from "~/components/SignupModal.vue";
import { useAuthStore } from "~/stores/auth";
import { useToastStore } from "~/stores/toast";

// Set up the page metadata including favicon
useHead({
  title: "Ainfographic - Turn blog posts into scroll-stopping infographics",
  htmlAttrs: {
    lang: "en",
  },
  meta: [
    {
      name: "description",
      content:
        "Turn any URL or content into shareable infographics for social media, blogs, and marketing — AI does the design work for you.",
    },
    {
      property: "og:title",
      content:
        "Ainfographic - Turn blog posts into scroll-stopping infographics",
    },
    {
      property: "og:description",
      content:
        "Turn any URL or content into shareable infographics for social media, blogs, and marketing — AI does the design work for you.",
    },
    { property: "og:type", content: "website" },
    { name: "twitter:card", content: "summary_large_image" },
    {
      name: "twitter:title",
      content:
        "Ainfographic - Turn blog posts into scroll-stopping infographics",
    },
    {
      name: "twitter:description",
      content:
        "Turn any URL or content into shareable infographics for social media, blogs, and marketing — AI does the design work for you.",
    },
  ],
  link: [{ rel: "icon", type: "image/svg+xml", href: "/favicon.svg" }],
});

const mobileMenuOpen = ref(false);
const loading = ref(true);
const error = ref(null);
const allTiers = ref([]);
const freeTiers = ref([]);
const monthlyTiers = ref([]);
const lifetimeTiers = ref([]);
const otherTiers = ref([]);
const isProcessing = ref(false);

// Auth store
const authStore = useAuthStore();
const toastStore = useToastStore();
const isAuthenticated = computed(() => authStore.isAuthenticated());

// AI Form reactive state
const activeTab = ref("infographic"); // Options: 'infographic', 'timeline'
const inputText = ref("");
const currentTopic = ref("URL");
const currentLanguage = ref("English");
const showTopicDropdown = ref(false);
const showLanguageDropdown = ref(false);
const showSignupModal = ref(false);

// Loading state
const isGenerating = ref(false);
const generationStatus = ref("Generating infographics...");
const generatedInfographics = ref([]);

// Refs for dropdown elements
const topicDropdownRef = ref(null);
const languageDropdownRef = ref(null);

// Handle clicks outside dropdowns
const handleClickOutside = (event) => {
  if (
    topicDropdownRef.value &&
    !topicDropdownRef.value.contains(event.target) &&
    showTopicDropdown.value
  ) {
    showTopicDropdown.value = false;
  }

  if (
    languageDropdownRef.value &&
    !languageDropdownRef.value.contains(event.target) &&
    showLanguageDropdown.value
  ) {
    showLanguageDropdown.value = false;
  }
};
const test = async () => {
  console.log("arsena");
};
// Set up click outside listener
onMounted(async () => {
  document.addEventListener("click", handleClickOutside);
  // Check for token in URL
  const route = useRoute();
  const token = route.query.token;
  const tokenFromQuery = route.query?.token;

  if (tokenFromQuery) {
    authStore.setToken(tokenFromQuery);
    await authStore.fetchUser();
  } else {
    const token = localStorage.getItem("token");
    if (token) {
      await authStore.fetchUser();
      fetchSubscriptionStatus();
    }
  }
  fetchSubscriptionTiers();
});

onUnmounted(() => {
  document.removeEventListener("click", handleClickOutside);
});

// Available topics for dropdown
const topics = ref(["URL", "Content"]);

// Available languages for dropdown
const languages = ref([
  "English",
  "Spanish",
  "French",
  "German",
  "Chinese",
  "Japanese",
  "Russian",
  "Arabic",
]);

// Form interaction methods
const setActiveTab = (tab) => {
  activeTab.value = tab;
};

const toggleTopicDropdown = () => {
  showTopicDropdown.value = !showTopicDropdown.value;
  if (showTopicDropdown.value) {
    showLanguageDropdown.value = false;
  }
};

const toggleLanguageDropdown = () => {
  showLanguageDropdown.value = !showLanguageDropdown.value;
  if (showLanguageDropdown.value) {
    showTopicDropdown.value = false;
  }
};

const subscriptionInfo = ref(null);

const selectTopic = (topic) => {
  currentTopic.value = topic;
  showTopicDropdown.value = false;
};

const selectLanguage = (language) => {
  currentLanguage.value = language;
  showLanguageDropdown.value = false;
};

// Handle generate infographic click
const handleGenerateClick = () => {
  // Check if user is authenticated
  if (!isAuthenticated.value) {
    // Show signup modal if not authenticated
    showSignupModal.value = true;
  } else {
    // Generate infographic if authenticated
    generateInfographic();
  }
};

// Close signup modal
const closeSignupModal = () => {
  showSignupModal.value = false;
};

const generateInfographic = async () => {
  // Get the form values
  const payload = {
    content: inputText.value,
    language: currentLanguage.value,
  };

  // If the input looks like a URL, use the url field instead of content
  if (
    inputText.value.startsWith("http://") ||
    inputText.value.startsWith("https://")
  ) {
    payload.url = inputText.value;
    delete payload.content;
  }
  // Call the public API endpoint to generate infographics
  isGenerating.value = true;
  const response = await apiClient.post(
    "infos/generate-infographics/",
    payload
  );

  try {
    const data = await response.data;
    // Store the generated infographics
    generatedInfographics.value = data.infographics.map((infographic) => ({
      ...infographic,
      uuid:
        infographic.id ||
        `temp-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
      preview_image_url: infographic.preview,
    }));
  } catch (error) {
    isGenerating.value = false;
  } finally {
    isGenerating.value = false;
  }
};

// Helper functions for tiers
const isPopular = (tier) => {
  return tier.name.toLowerCase().includes("premium");
};

const isPremium = (tier) => {
  return tier.name.toLowerCase().includes("premium");
};

const isLifetime = (tier) => {
  return tier.name.toLowerCase().includes("lifetime");
};

// FAQ items data
const faqItems = ref([
  {
    question: "How does Ainfographic work?",
    answer:
      "Ainfographic uses AI to analyze your content and automatically generate professional infographics. Simply paste a URL or your content, choose a template, customize if needed, and download your infographic.",
    isOpen: false,
  },
  {
    question: "Can I customize the generated infographics?",
    answer:
      "Yes, all infographics can be fully customized. You can change colors, fonts, layouts, add your brand elements, and adjust the content as needed.",
    isOpen: false,
  },
  {
    question: "What formats can I export my infographics in?",
    answer:
      "You can export your infographics in PNG, JPG, and WEBP formats. We also provide optimized sizes for different social media platforms.",
    isOpen: false,
  },
  {
    question: "Do I need design skills to use Ainfographic?",
    answer:
      "No design skills required! Our AI handles the design work for you, creating professional-looking infographics based on your content and selected template.",
    isOpen: false,
  },
  {
    question: "Can I use Ainfographic for commercial purposes?",
    answer:
      "Yes, all plans include commercial usage rights. The Premium plan includes extended commercial licenses for team usage and client work.",
    isOpen: false,
  },
  {
    question: "Do you offer refunds?",
    answer:
      "Yes, we offer a 30-day money-back guarantee. If you're not satisfied with the service, you can contact us within 30 days of purchase for a full refund.",
    isOpen: false,
  },
]);

// Toggle FAQ accordion
const toggleFaq = (index) => {
  faqItems.value[index].isOpen = !faqItems.value[index].isOpen;
};

const subscribe = async (planId) => {
  console.log("Subscribing to plan:", planId);
  isProcessing.value = true;
  try {
    const response = await apiClient.post("/account/public-checkout-session/", {
      tier_id: planId,
      coupon_code: true,
    });
    window.location.href = response.data.url;
  } catch (error) {
    console.error("Error subscribing:", error);
  } finally {
    isProcessing.value = false;
  }
};

const fetchSubscriptionStatus = async () => {
  try {
    const response = await apiClient.get("/account/subscription-status/");
    authStore.subscriptionInfo = response.data.subscription;
  } catch (error) {}
};

// Fetch subscription tiers from API
const fetchSubscriptionTiers = () => {
  apiClient
    .get(`/account/subscription-tiers/`)
    .then((response) => {
      const data = response.data;
      allTiers.value = data.all_tiers;
      freeTiers.value = data.categories.free;
      monthlyTiers.value = data.categories.monthly;
      lifetimeTiers.value = data.categories.lifetime;
      otherTiers.value = data.categories.other;
    })
    .catch((err) => {
      console.error("Error fetching subscription tiers:", err);
      error.value =
        "Unable to load subscription plans. Please try again later.";

      // Fallback data if API fails
      freeTiers.value = [
        {
          id: 1,
          name: "Free",
          price: 0,
          monthly_download_limit: 5,
          ai_credits: 10,
        },
      ];

      monthlyTiers.value = [
        {
          id: 2,
          name: "Basic Monthly",
          price: 9,
          monthly_download_limit: 25,
          ai_credits: 100,
        },
        {
          id: 3,
          name: "Premium Monthly",
          price: 19,
          monthly_download_limit: 100,
          ai_credits: 200,
        },
      ];

      lifetimeTiers.value = [
        {
          id: 4,
          name: "Lifetime",
          price: 99,
          monthly_download_limit: 999999,
          ai_credits: 500,
        },
      ];
    })
    .finally(() => {
      loading.value = false;
    });
};
</script>

<style scoped>
.navigation-wrapper {
  width: 100%;
  transition: box-shadow 0.3s ease;
  background-color: #f9fafb;
}

.navigation {
  max-width: 1024px;
  width: 100%;
  height: 70px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 16px;
  margin: 0 auto;
}
.navigation-left {
  display: flex;
  justify-content: start;
  align-items: center;
  gap: 32px;
}
.navigation-left-links {
  display: flex;
  justify-content: center;
  gap: 24px;
  font-size: 16px;
}

.logo {
  display: flex;
  align-items: center;
  gap: 10px;
}

.logo-text {
  font-size: 18px;
  font-weight: 700;
  color: #111827;
}

.nav-link {
  color: #4b5563;
  font-weight: 400;
  padding: 8px 12px;
  border-radius: 6px;
  transition: all 0.2s ease;
}

.nav-link:hover {
  background-color: #f3f4f6;
}

.nav-button {
  padding: 10px 20px;
  border-radius: 6px;
  font-weight: 500;
  font-size: 16px;
  transition: all 0.2s ease;
  text-align: center;
}

.nav-button.primary {
  background-color: #0d6efd;
  color: white;
  border: 1px solid #0d6efd;
}

.nav-button.primary:hover {
  background-color: #0b5ed7;
}

.nav-button.secondary {
  background-color: white;
  color: #111827;
  border: 1px solid #e5e7eb;
}

.nav-button.secondary:hover {
  background-color: #f9fafb;
}

/* Hero Section Styles */
.hero-section {
  background-color: #f9fafb;
  width: 100%;
  padding: 80px 0;
  display: flex;
  justify-content: center;
}

.hero-container {
  width: 1200px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-direction: column;
  gap: 40px;
}

.hero-content {
  flex: 1;
  max-width: 900px;
  display: flex;
  gap: 5px;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  opacity: 1;
}

.hero-title {
  font-size: 64px;
  font-weight: 700;
  color: #111827;
  line-height: 1.1;
  margin-bottom: 24px;
  text-align: center;
  letter-spacing: 0.01em; /* Increases vertical space between letters */
  line-height: 1.5; /* Increases vertical space between lines of text */
}

.hero-subtitle {
  font-size: 20px;
  color: #4b5563;
  line-height: 1.6;
  margin-bottom: 12px;
  text-align: center;
}

.hero-cta {
  display: flex;
  gap: 16px;
  flex-direction: column;
  align-items: center;
  gap: 30px;
  margin-bottom: 40px;
}

.cta-button {
  padding: 12px 24px;
  border-radius: 8px;
  font-weight: 600;
  font-size: 16px;
  transition: all 0.2s ease;
  text-align: center;
}

.cta-button.primary {
  background-color: var(--primary-color, #4f46e5);
  color: white;
  border: 2px solid var(--primary-color, #4f46e5);
}

.cta-button.primary:hover {
  background-color: var(--primary-hover, #4338ca);
  border-color: var(--primary-hover, #4338ca);
}

.cta-button.secondary {
  background-color: white;
  color: var(--primary-color, #4f46e5);
  border: 2px solid #d1d5db;
}

.cta-button.secondary:hover {
  border-color: var(--primary-color, #4f46e5);
  background-color: #f9fafb;
}

.hero-stats {
  display: flex;
  align-items: center;
  gap: 24px;
}

.stat-item {
  display: flex;
  flex-direction: column;
}

.stat-number {
  font-size: 24px;
  font-weight: 700;
  color: #111827;
}

.stat-label {
  font-size: 14px;
  color: #6b7280;
}

.stat-divider {
  width: 1px;
  height: 40px;
  background-color: #e5e7eb;
}

.hero-image {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  opacity: 1;
  margin-top: 200px;
}

/* Video Player Styles */
.video-container {
  width: 100%;
  max-width: 900px;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1),
    0 10px 10px -5px rgba(0, 0, 0, 0.04);
  position: relative;
}

.video-player {
  width: 100%;
  height: auto;
  display: block;
  background-color: #000;
}

/* Common Section Styles */
.section-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 80px 16px;
}

.section-header {
  text-align: center;
  margin-bottom: 60px;
}

.section-title {
  font-size: 36px;
  font-weight: 700;
  color: #111827;
  margin-bottom: 16px;
}

.section-subtitle {
  font-size: 18px;
  color: #6b7280;
  max-width: 600px;
  margin: 0 auto;
}

/* Benefits Section */
.benefits-section {
  background-color: white;
}

.benefits-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 30px;
}

.benefit-card {
  background-color: #f9fafb;
  border-radius: 12px;
  padding: 30px;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.benefit-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1);
}

.benefit-icon {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 60px;
  height: 60px;
  border-radius: 12px;
  background-color: #eef2ff;
  margin-bottom: 20px;
  color: var(--primary-color, #4f46e5);
}

.benefit-title {
  font-size: 20px;
  font-weight: 600;
  color: #111827;
  margin-bottom: 12px;
}

.benefit-description {
  font-size: 16px;
  color: #6b7280;
  line-height: 1.5;
}

/* Templates Section */
.templates-section {
  background-color: #f9fafb;
}

.templates-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 30px;
}

.template-card {
  background-color: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.template-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1);
}
.template-image {
  height: 1000px;
  overflow: hidden;
}

.template-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.template-card:hover .template-img {
  transform: scale(1.05);
}

.template-info {
  padding: 20px;
}

.template-title {
  font-size: 18px;
  font-weight: 600;
  color: #111827;
  margin-bottom: 8px;
}

.template-description {
  font-size: 14px;
  color: #6b7280;
}

/* Editor Video Section */
.editor-video-section {
  background-color: white;
}

.editor-video-container {
  max-width: 800px;
  margin: 0 auto;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1);
}

/* Pricing Section */
.pricing-section {
  background-color: #f9fafb;
}

.pricing-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 30px;
  margin-top: 40px;
}

.pricing-card {
  background-color: white;
  border-radius: 12px;
  padding: 40px 30px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  position: relative;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  display: flex;
  flex-direction: column;
}

.pricing-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1);
}

.pricing-card.popular {
  border: 2px solid var(--primary-color, #4f46e5);
  transform: scale(1.05);
  z-index: 1;
}

.pricing-card.popular:hover {
  transform: scale(1.05) translateY(-5px);
}

.popular-badge {
  position: absolute;
  top: -12px;
  left: 50%;
  transform: translateX(-50%);
  background-color: var(--primary-color, #4f46e5);
  color: white;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 14px;
  font-weight: 500;
}

.pricing-header {
  text-align: center;
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 1px solid #e5e7eb;
}

.pricing-title {
  font-size: 24px;
  font-weight: 600;
  color: #111827;
  margin-bottom: 16px;
}

.pricing-price {
  display: flex;
  justify-content: center;
  align-items: baseline;
}

.price {
  font-size: 48px;
  font-weight: 700;
  color: #111827;
}

.period {
  font-size: 16px;
  color: #6b7280;
  margin-left: 4px;
}

.pricing-features {
  list-style-type: none;
  padding: 0;
  margin: 0 0 30px 0;
  flex-grow: 1;
}

.pricing-feature {
  font-size: 16px;
  color: #4b5563;
  padding: 8px 0;
  display: flex;
  align-items: center;
}

.pricing-feature::before {
  content: "✓";
  color: var(--primary-color, #4f46e5);
  font-weight: bold;
  margin-right: 10px;
}

.pricing-action {
  text-align: center;
}

.pricing-button {
  display: inline-block;
  width: 100%;
  padding: 12px 24px;
  border-radius: 8px;
  font-weight: 500;
  font-size: 16px;
  transition: all 0.2s ease;
  text-align: center;
  background-color: white;
  color: var(--primary-color, #4f46e5);
  border: 1px solid #e5e7eb;
}

.pricing-button:hover {
  border-color: var(--primary-color, #4f46e5);
  background-color: #f9fafb;
}

.pricing-button.primary {
  background-color: var(--primary-color, #4f46e5);
  color: white;
  border: 1px solid var(--primary-color, #4f46e5);
}

.pricing-button.primary:hover {
  background-color: var(--primary-hover, #4338ca);
  border-color: var(--primary-hover, #4338ca);
}

/* FAQ Section */
.faq-section {
  background-color: white;
}

.faq-container {
  max-width: 800px;
  margin: 0 auto;
}

.faq-item {
  border-bottom: 1px solid #e5e7eb;
}

.faq-question {
  padding: 24px 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
}

.faq-question-text {
  font-size: 18px;
  font-weight: 500;
  color: #111827;
  margin: 0;
}

.faq-icon {
  color: #6b7280;
  transition: transform 0.3s ease;
}

.faq-icon .rotate-180 {
  transform: rotate(180deg);
}

.faq-answer {
  padding: 0 0 24px 0;
  font-size: 16px;
  color: #6b7280;
  line-height: 1.6;
}

/* Footer Section */
.footer-section {
  background-color: #f9fafb;
  padding-top: 80px;
}

.footer-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 16px;
  display: flex;
  flex-wrap: wrap;
  gap: 60px;
}

.footer-left {
  flex: 1 1 300px;
}

.footer-logo {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 20px;
}

.footer-logo-text {
  font-size: 18px;
  font-weight: 700;
  color: #111827;
}

.footer-description {
  font-size: 16px;
  color: #6b7280;
  line-height: 1.6;
}

.footer-right {
  flex: 2 1 600px;
  display: flex;
  justify-content: space-between;
  gap: 40px;
}

.footer-column {
  flex: 1;
}

.footer-column-title {
  font-size: 16px;
  font-weight: 600;
  color: #111827;
  margin-bottom: 20px;
}

.footer-links {
  list-style-type: none;
  padding: 0;
  margin: 0;
}

.footer-link {
  display: block;
  font-size: 14px;
  color: #6b7280;
  margin-bottom: 12px;
  transition: color 0.2s ease;
}

.footer-link:hover {
  color: var(--primary-color, #4f46e5);
}

.footer-bottom {
  max-width: 1200px;
  margin: 60px auto 0;
  padding: 20px 16px;
  border-top: 1px solid #e5e7eb;
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  align-items: center;
  gap: 20px;
}

.footer-copyright {
  font-size: 14px;
  color: #9ca3af;
  margin: 0;
}

.footer-legal {
  display: flex;
  gap: 20px;
}

.footer-legal-link {
  font-size: 14px;
  color: #6b7280;
  transition: color 0.2s ease;
}

.footer-legal-link:hover {
  color: var(--primary-color, #4f46e5);
}

/* Responsive Video Sizing */
@media (max-width: 768px) {
  .video-container,
  .editor-video-container {
    max-width: 100%;
  }
}

/* Responsive Media Queries */
/* Large Desktops */
@media (min-width: 1200px) {
  .hero-container,
  .navigation,
  .section-container {
    width: 1200px;
  }
}

/* Medium Desktops */
@media (max-width: 1199px) and (min-width: 992px) {
  .hero-container,
  .navigation,
  .section-container {
    width: 960px;
  }
  .hero-title {
    font-size: 52px;
  }
  .video-container {
    max-width: 450px;
  }
}

/* Tablets and Small Desktops */
@media (max-width: 991px) and (min-width: 768px) {
  .hero-container,
  .navigation,
  .section-container {
    width: 720px;
  }
  .hero-container {
    flex-direction: column;
    text-align: center;
  }
  .hero-content {
    max-width: 100%;
  }
  .hero-title {
    font-size: 54px;
  }
  .hero-subtitle {
    font-size: 16px;
  }
  .hero-cta {
    justify-content: center;
  }
  .hero-stats {
    justify-content: center;
  }
  .navigation-left-links {
    margin-left: 2rem;
  }
  .pricing-grid {
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  }
  .footer-right {
    gap: 20px;
  }
}

/* Large Mobile Devices */
@media (max-width: 767px) and (min-width: 576px) {
  .hero-container,
  .navigation,
  .section-container {
    width: 540px;
  }
  .hero-container {
    flex-direction: column;
    text-align: center;
  }
  .hero-content {
    max-width: 100%;
  }
  .hero-title {
    font-size: 48px;
  }
  .hero-subtitle {
    font-size: 16px;
  }
  .hero-cta {
    justify-content: center;
    flex-direction: column;
    gap: 12px;
  }
  .hero-stats {
    justify-content: center;
    flex-wrap: wrap;
  }
  .stat-divider {
    display: none;
  }
  .navigation-left-links {
    margin-left: 1rem;
    gap: 8px;
  }
  .benefits-grid,
  .templates-grid,
  .pricing-grid {
    grid-template-columns: 1fr;
    gap: 20px;
  }
  .section-container {
    padding: 60px 16px;
  }
  .section-title {
    font-size: 28px;
  }
  .footer-container {
    flex-direction: column;
    gap: 40px;
  }
  .footer-right {
    flex-direction: column;
    gap: 30px;
  }
}
.curly-arrow-container {
  width: 200px;
  height: 200px;
  position: relative;
  top: 0;
  left: 0px;
  rotate: 260deg;
}

.curly-arrow-container svg {
  width: 100%;
  height: 100%;
}

/* Small Mobile Devices */
@media (max-width: 575px) {
  .hero-container,
  .navigation,
  .section-container {
    width: 100%;
    padding: 0 16px;
  }
  .section-container {
    padding: 50px 16px;
  }
  .hero-container {
    flex-direction: column;
    text-align: center;
  }
  .hero-content {
    max-width: 100%;
  }
  .hero-title {
    font-size: 38px;
  }
  .hero-subtitle {
    font-size: 16px;
  }
  .hero-cta {
    justify-content: center;
    flex-direction: column;
    gap: 12px;
  }
  .hero-stats {
    justify-content: center;
    flex-wrap: wrap;
    gap: 16px;
  }
  .stat-divider {
    display: none;
  }
  .navigation-left-links {
    display: none;
  }
  .benefits-grid,
  .templates-grid,
  .pricing-grid {
    grid-template-columns: 1fr;
    gap: 20px;
  }
  .pricing-card.popular {
    transform: scale(1);
  }
  .pricing-card.popular:hover {
    transform: translateY(-5px);
  }
  .section-title {
    font-size: 24px;
  }
  .section-subtitle {
    font-size: 16px;
  }
  .footer-container {
    flex-direction: column;
    gap: 40px;
  }
  .footer-right {
    flex-direction: column;
    gap: 30px;
  }
  .footer-bottom {
    flex-direction: column;
    align-items: flex-start;
  }
  .video-container {
    height: 300px;
  }
  .video-container {
    max-width: 100%;
  }
}

/* Mobile Menu Toggle (for very small screens where you might want a hamburger menu) */
@media (max-width: 480px) {
  .hero-section {
    padding: 40px 0;
  }
}

.read-docs-link {
  display: inline-flex;
  align-items: center;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
    "Helvetica Neue", Arial, sans-serif;
  font-size: 14px;
  font-weight: 500;
  color: var(--primary-color);
  text-decoration: none;
  padding: 6px 0;
  transition: color 0.2s ease;
}

.read-docs-link:hover {
  color: var(--primary-color);
}

.arrow {
  margin-left: 6px;
  font-size: 14px;
  display: inline-block;
  transition: transform 0.3s ease;
  position: relative;
}

.read-docs-link:hover .arrow {
  transform: translateX(5px);
}

.highlight-text {
  background-color: #3e57da;
  color: white;
  padding: 2px 8px;
  border-radius: 4px;
  font-weight: 800;
  display: inline-block;
}

/* Mobile Menu Styles */
.mobile-menu {
  display: flex;
  flex-direction: column;
  width: 100%;
  background-color: white;
}

.mobile-nav-link {
  padding: 12px 16px;
  font-size: 16px;
  color: #4b5563;
  border-bottom: 1px solid #f3f4f6;
  transition: background-color 0.2s ease;
}

.mobile-nav-link:hover {
  background-color: #f9fafb;
}

.loading-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 40px 0;
  width: 100%;
}

.loading-spinner {
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 0 auto 24px;
}

.spinner-ring {
  position: relative;
  width: 64px;
  height: 64px;
}

.spinner-ring:after {
  content: "";
  display: block;
  width: 46px;
  height: 46px;
  margin: 8px;
  border-radius: 50%;
  border: 3px solid var(--primary-color, #3e57da);
  border-color: var(--primary-color, #3e57da) transparent
    var(--primary-color, #3e57da) transparent;
  animation: spin 1.2s linear infinite;
}

.loading-text {
  text-align: center;
  font-size: 16px;
  color: #4b5563;
  font-weight: 500;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

.error-container {
  text-align: center;
  padding: 40px 0;
  color: #ef4444;
  background-color: #fee2e2;
  border-radius: 8px;
  max-width: 600px;
  margin: 0 auto;
}

.old-price {
  width: fit-content;
  text-decoration: line-through;
  color: #6b7280;
  font-size: 18px;
  margin-bottom: 4px;
}
.discount-badge {
  background-color: #3e57da;
  color: white;
  padding: 2px 8px;
  border-radius: 4px;
  font-weight: 800;
  width: fit-content;
}

/* AI Infographic Generator Form Styles */
.ai-form-container {
  width: 100%;
  max-width: 660px;
  margin: 50px auto;
  opacity: 1;
}

.form-card {
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1);
  border: 1px solid #e5e7eb;
  position: relative;
  z-index: 10;
}

.form-tabs {
  display: flex;
  border-bottom: 1px solid #e5e7eb;
}

.form-tab {
  padding: 12px 16px;
  color: #6b7280;
  font-size: 14px;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.2s ease;
  background: transparent;
  border: none;
  cursor: pointer;
}

.form-tab.active {
  color: var(--primary-color, #3e57da);
  border-bottom: 2px solid var(--primary-color, #3e57da);
}

.tab-icon {
  display: flex;
  align-items: center;
  justify-content: center;
}

.form-input-container {
  padding: 16px 20px;
}

.form-input {
  width: 100%;
  background-color: transparent;
  border: none;
  color: #111827;
  font-size: 16px;
  padding: 8px 0;
  outline: none;
  caret-color: var(--primary-color, #3e57da);
}

.form-input::placeholder {
  color: #9ca3af;
}

.form-actions {
  display: flex;
  padding: 12px 20px;
  border-top: 1px solid #e5e7eb;
  align-items: center;
  gap: 10px;
  background-color: #f9fafb;
}

.form-dropdown {
  position: relative;
  z-index: 100;
}

.dropdown-button {
  display: flex;
  align-items: center;
  background-color: white;
  border: 1px solid #e5e7eb;
  color: #4b5563;
  font-size: 14px;
  padding: 8px 16px;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.dropdown-button:hover,
.dropdown-button.active {
  border-color: var(--primary-color, #3e57da);
}

.dropdown-button.active {
  background-color: rgba(62, 87, 218, 0.05);
  color: var(--primary-color, #3e57da);
}

.dropdown-menu {
  position: absolute;
  top: 100%;
  left: 0;
  z-index: 999;
  margin-top: 8px;
  background-color: white;
  border-radius: 8px;
  min-width: 180px;
  max-height: 220px;
  overflow-y: auto;
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1),
    0 4px 6px -2px rgba(0, 0, 0, 0.05);
  border: 1px solid #e5e7eb;
  display: block;
}

.dropdown-item {
  display: block;
  width: 100%;
  text-align: left;
  padding: 10px 16px;
  color: #4b5563;
  font-size: 14px;
  background-color: white;
  border: none;
  cursor: pointer;
  transition: all 0.1s ease;
  border-bottom: 1px solid #f3f4f6;
}

.dropdown-item:last-child {
  border-bottom: none;
}

.dropdown-item:hover {
  background-color: #f9fafb;
  color: var(--primary-color, #3e57da);
}

.form-submit-button {
  background-color: var(--primary-color, #3e57da);
  border: none;
  color: white;
  width: 40px;
  height: 40px;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
  margin-left: auto;
}

.form-submit-button:hover {
  background-color: var(--primary-hover, #4338ca);
}

.quick-topics {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-top: 16px;
  justify-content: center;
}

.topic-tag {
  display: flex;
  align-items: center;
  background-color: white;
  color: #4b5563;
  font-size: 14px;
  font-weight: 500;
  padding: 6px 12px;
  border-radius: 9999px;
  border: 1px solid #e5e7eb;
  transition: all 0.2s ease;
  text-decoration: none;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.topic-tag:hover {
  border-color: var(--primary-color, #3e57da);
  color: var(--primary-color, #3e57da);
  background-color: rgba(62, 87, 218, 0.05);
  transform: translateY(-2px);
}

.premium-tag {
  display: flex;
  align-items: center;
  background-color: var(--primary-color, #3e57da);
  color: white;
  font-size: 14px;
  font-weight: 500;
  padding: 6px 12px;
  border-radius: 9999px;
  transition: all 0.2s ease;
  text-decoration: none;
  box-shadow: 0 2px 4px rgba(62, 87, 218, 0.3);
}

.premium-tag:hover {
  background-color: var(--primary-hover, #4338ca);
  transform: translateY(-2px);
  box-shadow: 0 4px 6px rgba(62, 87, 218, 0.4);
}

/* Responsive styles for the form */
@media (max-width: 767px) {
  .ai-form-container {
    max-width: 100%;
    padding: 0 16px;
  }

  .form-actions {
    flex-wrap: wrap;
    gap: 1px;
  }

  .form-dropdown {
    flex: 1;
    min-width: 120px;
  }

  .quick-topics {
    justify-content: center;
  }
}

.selected-item {
  color: var(--primary-color, #3e57da) !important;
  font-weight: 500;
}

.check-icon {
  display: inline-block;
  margin-right: 8px;
  color: var(--primary-color, #3e57da);
  font-weight: bold;
}

/* Loading Animation Styles */
.ai-loading-container {
  margin: 40px auto;
  max-width: 500px;
  width: 100%;
  opacity: 1;
  animation: fadeIn 0.5s ease-out;
}

.loading-animation {
  background-color: white;
  border-radius: 16px;
  padding: 30px;
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1);
  border: 1px solid #e5e7eb;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  text-align: center;
}

.loading-spinner {
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 0 auto 24px;
}

.spinner-ring {
  position: relative;
  width: 64px;
  height: 64px;
}

.spinner-ring:after {
  content: "";
  display: block;
  width: 46px;
  height: 46px;
  margin: 8px;
  border-radius: 50%;
  border: 3px solid var(--primary-color, #3e57da);
  border-color: var(--primary-color, #3e57da) transparent
    var(--primary-color, #3e57da) transparent;
  animation: spin 1.2s linear infinite;
}

.loading-text {
  text-align: center;
  font-size: 16px;
  color: #4b5563;
  font-weight: 500;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

/* Generated Infographics Results Styles */
.generated-infographics-container {
  width: 100%;
  max-width: 1200px;
  margin: 60px auto 0;
  opacity: 1;
  animation: fadeIn 0.5s ease-out;
}

.results-title {
  font-size: 24px;
  font-weight: 600;
  color: #111827;
  margin-bottom: 24px;
  text-align: center;
}

.results-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  justify-content: center;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@media (max-width: 767px) {
  .results-grid {
    grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  }
}
</style>