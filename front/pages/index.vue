<template>
  <div class="min-h-screen">
    <!-- Hero Section -->
    <section class="relative pt-32 pb-20 overflow-hidden">
      <!-- Background Effects -->
      <div
        class="absolute inset-0 bg-gradient-to-br from-primary-950/50 via-background-primary to-primary-900/20"
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
        <div class="text-center max-w-4xl mx-auto">
          <h1 class="text-display-xl mb-6">
            Get traffic that converts from
            <span class="gradient-text">ChatGPT, Claude, Gemini</span>, and
            other AI platforms
          </h1>
          <p class="text-body-xl text-text-secondary mb-10 max-w-2xl mx-auto">
            Track and optimize visibility in ChatGPT, Gemini and other AI Search
            engines to drive traffic to your website that converts.
          </p>
          <div class="flex flex-col sm:flex-row gap-4 justify-center mb-16">
            <button class="btn-primary text-lg px-8 py-4">Book a Demo</button>
            <button class="btn-outline text-lg px-8 py-4">
              Start a Free Trial
            </button>
          </div>
        </div>

        <!-- Dashboard Preview -->
        <div class="relative mx-auto max-w-5xl mt-12">
          <div class="card-glass p-4 rounded-xl border border-border-primary">
            <div class="bg-background-primary rounded-lg p-6 min-h-[400px]">
              <!-- Mockup Header -->
              <div class="flex justify-between items-center mb-8">
                <div class="flex gap-4">
                  <div class="h-8 w-32 bg-background-secondary rounded"></div>
                  <div class="h-8 w-24 bg-background-secondary rounded"></div>
                </div>
                <div class="h-8 w-40 bg-background-secondary rounded"></div>
              </div>
              <!-- Mockup Content -->
              <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div class="col-span-2 space-y-4">
                  <div class="h-64 bg-background-secondary/50 rounded-lg flex items-end p-4 gap-2">
                    <div class="w-full bg-primary-500/20 h-[40%] rounded-t"></div>
                    <div class="w-full bg-primary-500/40 h-[60%] rounded-t"></div>
                    <div class="w-full bg-primary-500/60 h-[30%] rounded-t"></div>
                    <div class="w-full bg-primary-500/80 h-[80%] rounded-t"></div>
                    <div class="w-full bg-primary-500 h-[50%] rounded-t"></div>
                  </div>
                </div>
                <div class="space-y-4">
                  <div class="h-20 bg-background-secondary/50 rounded-lg p-4">
                    <div class="text-sm text-text-secondary mb-2">ChatGPT</div>
                    <div class="text-2xl font-bold text-text-primary">189,423</div>
                    <div class="text-green-500 text-sm">+18%</div>
                  </div>
                  <div class="h-20 bg-background-secondary/50 rounded-lg p-4">
                    <div class="text-sm text-text-secondary mb-2">Perplexity</div>
                    <div class="text-2xl font-bold text-text-primary">128,754</div>
                    <div class="text-green-500 text-sm">+22%</div>
                  </div>
                  <div class="h-20 bg-background-secondary/50 rounded-lg p-4">
                    <div class="text-sm text-text-secondary mb-2">Gemini</div>
                    <div class="text-2xl font-bold text-text-primary">110,480</div>
                    <div class="text-red-500 text-sm">-7%</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <!-- Glow effect behind dashboard -->
          <div
            class="absolute -inset-4 bg-primary-500/20 blur-3xl -z-10 rounded-[3rem]"
          ></div>
        </div>
      </div>
    </section>

    <!-- 3 Step Process -->
    <section class="py-24 bg-background-secondary/20">
      <div class="container-custom">
        <div class="text-center mb-16">
          <h2 class="text-display-md mb-4">Control your AI search visibility</h2>
          <p class="text-text-secondary text-lg max-w-2xl mx-auto">
            Understand how and when AI is recommending your brand and what you
            can do about it.
          </p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <!-- Step 1 -->
          <div class="card p-8 relative overflow-hidden group hover:border-primary-500/50 transition-colors">
            <div class="absolute top-0 right-0 p-4 opacity-10 text-6xl font-bold">1</div>
            <h3 class="text-2xl font-bold mb-4">Track</h3>
            <p class="text-text-secondary mb-6">
              Track specific prompts to see when AI mentions your brand in its
              responses.
            </p>
            <div class="bg-background-primary p-4 rounded-lg border border-border-primary text-sm">
              <div class="text-text-secondary mb-2">User Prompt:</div>
              <div class="text-text-primary italic">
                "What is the best CRM for a startup?"
              </div>
            </div>
          </div>

          <!-- Step 2 -->
          <div class="card p-8 relative overflow-hidden group hover:border-primary-500/50 transition-colors">
            <div class="absolute top-0 right-0 p-4 opacity-10 text-6xl font-bold">2</div>
            <h3 class="text-2xl font-bold mb-4">Analyze</h3>
            <p class="text-text-secondary mb-6">
              See when these responses mention your brand or competitors.
            </p>
            <div class="bg-background-primary p-4 rounded-lg border border-border-primary">
              <div class="flex justify-between items-center mb-2">
                <span class="text-sm text-text-secondary">Answer Gap</span>
                <span class="text-red-500 text-sm">40% Missing</span>
              </div>
              <div class="w-full bg-background-secondary h-2 rounded-full overflow-hidden">
                <div class="bg-red-500 h-full w-[40%]"></div>
              </div>
            </div>
          </div>

          <!-- Step 3 -->
          <div class="card p-8 relative overflow-hidden group hover:border-primary-500/50 transition-colors">
            <div class="absolute top-0 right-0 p-4 opacity-10 text-6xl font-bold">3</div>
            <h3 class="text-2xl font-bold mb-4">Optimize</h3>
            <p class="text-text-secondary mb-6">
              Know where to publish content to boost your search visibility.
            </p>
            <div class="space-y-2">
              <div class="flex items-center gap-2 text-sm text-green-500">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
                <span>Content Gaps Analyzed</span>
              </div>
              <div class="flex items-center gap-2 text-sm text-green-500">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
                <span>Crawlers Indexing</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Detailed Features -->
    <section class="py-24">
      <div class="container-custom space-y-32">
        <!-- Feature 1 -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
          <div>
            <h3 class="text-display-sm mb-6">Track Prompts</h3>
            <p class="text-body-lg text-text-secondary mb-8">
              Track real user prompts, identify high-value prompts to target and
              optimize. See exactly what users are asking and how AI models are responding.
            </p>
            <ul class="space-y-4">
              <li class="flex items-center gap-3">
                <div class="w-6 h-6 rounded-full bg-primary-500/20 flex items-center justify-center text-primary-500">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
                </div>
                <span>Real-time prompt tracking</span>
              </li>
              <li class="flex items-center gap-3">
                <div class="w-6 h-6 rounded-full bg-primary-500/20 flex items-center justify-center text-primary-500">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
                </div>
                <span>Sentiment analysis</span>
              </li>
            </ul>
          </div>
          <div class="card-glass p-8 relative">
            <div class="absolute -inset-4 bg-primary-500/10 blur-2xl -z-10 rounded-full"></div>
            <!-- Mockup -->
            <div class="space-y-4">
              <div class="bg-background-primary p-4 rounded-lg border border-border-primary">
                <div class="text-xs text-text-secondary mb-1">Prompt</div>
                <div class="font-medium">"Best running shoes for 5k?"</div>
              </div>
              <div class="bg-background-primary p-4 rounded-lg border border-border-primary ml-8">
                <div class="text-xs text-text-secondary mb-1">AI Response</div>
                <div class="text-sm text-text-secondary">
                  "For a 5k run, you want lightweight and responsive shoes. Top picks include Nike Pegasus 40 and Hoka Mach 5..."
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Feature 2 -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center lg:flex-row-reverse">
          <div class="order-last lg:order-first card-glass p-8 relative">
             <div class="absolute -inset-4 bg-blue-500/10 blur-2xl -z-10 rounded-full"></div>
             <div class="grid grid-cols-2 gap-4">
               <div class="bg-background-primary p-4 rounded-lg border border-border-primary text-center">
                 <div class="font-bold text-xl mb-1">ChatGPT</div>
                 <div class="text-green-500 text-sm">Connected</div>
               </div>
               <div class="bg-background-primary p-4 rounded-lg border border-border-primary text-center">
                 <div class="font-bold text-xl mb-1">Claude</div>
                 <div class="text-green-500 text-sm">Connected</div>
               </div>
               <div class="bg-background-primary p-4 rounded-lg border border-border-primary text-center">
                 <div class="font-bold text-xl mb-1">Gemini</div>
                 <div class="text-green-500 text-sm">Connected</div>
               </div>
               <div class="bg-background-primary p-4 rounded-lg border border-border-primary text-center">
                 <div class="font-bold text-xl mb-1">Perplexity</div>
                 <div class="text-green-500 text-sm">Connected</div>
               </div>
             </div>
          </div>
          <div>
            <h3 class="text-display-sm mb-6">Every AI Model</h3>
            <p class="text-body-lg text-text-secondary mb-8">
              Monitor ChatGPT, Claude, Perplexity, Gemini, DeepSeek, and
              emerging AI search engines all in one place.
            </p>
            <button class="btn-outline">View Integrations</button>
          </div>
        </div>
      </div>
    </section>

    <!-- Testimonials -->
    <section class="py-24 bg-background-secondary/20">
      <div class="container-custom">
        <div class="text-center mb-16">
          <h2 class="text-display-md mb-4">Trusted by industry leaders</h2>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          <div class="card p-8">
            <div class="flex items-center gap-4 mb-6">
              <div class="w-12 h-12 bg-primary-500 rounded-full flex items-center justify-center text-white font-bold">JP</div>
              <div>
                <div class="font-bold">Jimmy Park</div>
                <div class="text-sm text-text-secondary">Head of Search at Opascope</div>
              </div>
            </div>
            <p class="text-text-secondary">
              "We needed GEO visibility insights for our clients. Now we
              understand what LLM platforms want and how they use our content."
            </p>
          </div>
          <div class="card p-8">
            <div class="flex items-center gap-4 mb-6">
              <div class="w-12 h-12 bg-blue-500 rounded-full flex items-center justify-center text-white font-bold">RJ</div>
              <div>
                <div class="font-bold">Rens de Jonge</div>
                <div class="text-sm text-text-secondary">Owner at Revisto Marketing</div>
              </div>
            </div>
            <p class="text-text-secondary">
              "We get clients discovered on AI platforms like ChatGPT by
              tracking AI-generated answers and optimizing with real data."
            </p>
          </div>
          <div class="card p-8">
            <div class="flex items-center gap-4 mb-6">
              <div class="w-12 h-12 bg-green-500 rounded-full flex items-center justify-center text-white font-bold">MK</div>
              <div>
                <div class="font-bold">Mohs Klunder</div>
                <div class="text-sm text-text-secondary">Owner at Goochem Media</div>
              </div>
            </div>
            <p class="text-text-secondary">
              "Monitoring AI platforms with data-driven recommendations helps us
              demonstrate clear ROI - essential for our AI SEO offering."
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- FAQ Section -->
    <section class="py-24">
      <div class="container-narrow">
        <div class="text-center mb-16">
          <h2 class="text-display-md mb-4">Frequently Asked Questions</h2>
          <p class="text-text-secondary">
            Learn about AI visibility monitoring and how we help your brand succeed.
          </p>
        </div>
        
        <div class="space-y-4">
          <div v-for="(faq, index) in faqs" :key="index" class="card p-0 overflow-hidden">
            <button 
              @click="toggleFaq(index)"
              class="w-full px-6 py-4 text-left flex justify-between items-center hover:bg-background-secondary/50 transition-colors"
            >
              <span class="font-medium text-lg">{{ faq.question }}</span>
              <svg 
                class="w-5 h-5 transform transition-transform duration-200"
                :class="{ 'rotate-180': faq.isOpen }"
                fill="none" 
                stroke="currentColor" 
                viewBox="0 0 24 24"
              >
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
              </svg>
            </button>
            <div 
              v-show="faq.isOpen"
              class="px-6 pb-4 text-text-secondary"
            >
              {{ faq.answer }}
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Bottom CTA -->
    <section class="py-24 relative overflow-hidden">
      <div class="absolute inset-0 bg-gradient-to-b from-background-primary to-primary-900/20"></div>
      <div class="container-custom relative z-10 text-center">
        <h2 class="text-display-md mb-6">Monitor Your AI Search Performance</h2>
        <p class="text-body-xl text-text-secondary mb-10 max-w-2xl mx-auto">
          Track how ChatGPT, Claude, Perplexity, and Gemini mention your brand
          in real-time. Get alerts when AI assistants recommend competitors
          instead of you.
        </p>
        <div class="flex flex-col sm:flex-row gap-4 justify-center">
          <button class="btn-primary text-lg px-8 py-4">Book a Demo</button>
          <button class="btn-outline text-lg px-8 py-4">Get Started</button>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref } from 'vue';

definePageMeta({
  layout: "default",
});

useSeoMeta({
  title: "Promptwatch - AI Search Visibility & Optimization",
  description:
    "Track and optimize visibility in ChatGPT, Gemini and other AI Search engines to drive traffic to your website that converts.",
});

const faqs = ref([
  {
    question: "What is Promptwatch and how does it work?",
    answer: "Promptwatch monitors AI search engines like ChatGPT, Claude, and Perplexity to track when and how your brand is mentioned. It provides analytics and insights to help you optimize your visibility in AI-generated responses.",
    isOpen: false
  },
  {
    question: "What is Generative Engine Optimization (GEO)?",
    answer: "GEO is the process of optimizing your online content to increase visibility and favorable mentions in generative AI outputs. Similar to SEO, but focused on AI models.",
    isOpen: false
  },
  {
    question: "Which AI platforms does Promptwatch monitor?",
    answer: "We currently monitor OpenAI (ChatGPT), Anthropic (Claude), Google (Gemini), Perplexity, Microsoft (Copilot), and other emerging AI search engines.",
    isOpen: false
  },
  {
    question: "How can Promptwatch help improve my brand's AI visibility?",
    answer: "By identifying content gaps, tracking competitor mentions, and analyzing sentiment, we provide actionable recommendations on what content to create or optimize to get better AI citations.",
    isOpen: false
  }
]);

const toggleFaq = (index) => {
  faqs.value[index].isOpen = !faqs.value[index].isOpen;
};
</script>