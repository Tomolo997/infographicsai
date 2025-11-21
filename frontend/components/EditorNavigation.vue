<template>
  <nav
    class="navigation w-full bg-white items-center flex gap-6 justify-between p-3"
  >
    <div class="flex gap-4">
      <!-- Create  -->
      <div class="relative flex w-[200px]">
        <input
          v-model="templateName"
          class="border w-[200px] border-lineColor rounded-md px-1 py-2 outline-primary text-sm"
          placeholder="My Template Name"
        />
        <svg
          class="absolute top-2 right-2"
          xmlns="http://www.w3.org/2000/svg"
          width="20"
          height="20"
          viewBox="0 0 24 24"
        >
          <path
            fill="currentColor"
            d="M3 21v-4.25L16.2 3.575q.3-.275.663-.425t.762-.15t.775.15t.65.45L20.425 5q.3.275.438.65T21 6.4q0 .4-.137.763t-.438.662L7.25 21zM17.6 7.8L19 6.4L17.6 5l-1.4 1.4z"
          />
        </svg>
      </div>
      <div>
        <ResizeDropdown
          ref="dropdown"
          v-model="selectedSize"
          :items="dropdownItemsSize"
          placeholder="Select a size"
        >
          <template #trigger>
            <div
              class="border gap-4 flex justify-between w-[150px] cursor-pointer border-lineColor rounded-md px-1 py-2 outline-primary text-sm"
              @click="$refs.dropdown.toggleDropdown()"
            >
              <span>{{ editorStore.canvasHeight }}x{{ editorStore.canvasWidth }}</span>
              <ChewronDownIcon size="20" />
            </div>
          </template>
        </ResizeDropdown>
      </div>
    </div>

    <div class="flex gap-4 mr-24">
      <TextDropdown
        v-model="selectedTextInput"
        :items="dropdownTextSize"
        position-top="100%"
        position-left=""
        placeholder="Select a size"
        @titleSizeSelected="handleTitleSizeChange"
      >
        <template #trigger>
          <button
            class="flex flex-col justify-center rounded-md py-1.5 px-4 hover:bg-grayBackground items-center"
            :class="{
              'bg-primaryLight':
                editorStore.selectedNavigationDesign === 'text',
            }"
            @click="selectElementType('text')"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="24"
              height="24"
              viewBox="0 0 32 32"
              :class="{
                'text-primary': editorStore.selectedNavigationDesign === 'text',
              }"
            >
              <path
                fill="currentColor"
                d="M6 4.5a.5.5 0 0 1 .5-.5h19a.5.5 0 0 1 .5.5v4a.5.5 0 0 1-1 0V5h-8.5v22h3a.5.5 0 0 1 0 1h-7a.5.5 0 0 1 0-1h3V5H7v3.5a.5.5 0 0 1-1 0z"
              />
            </svg>
            <span
              class="font-extralight text-sm"
              :class="{
                'text-primary': editorStore.selectedNavigationDesign === 'text',
              }"
              >Text</span
            >
          </button>
        </template>
      </TextDropdown>
      <ShapesDropdown
        v-model="selectedShape"
        :items="dropdownTextSize"
        position-top="100%"
        position-left="-125px"
        placeholder="Select a size"
      >
        <template #trigger>
          <button
            class="flex flex-col justify-center rounded-md w-14 h-14 hover:bg-grayBackground items-center"
            :class="{
              'bg-primaryLight':
                editorStore.selectedNavigationDesign === 'shapes',
            }"
            @click="selectElementType('shapes')"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="24"
              height="24"
              viewBox="0 0 24 24"
              :class="{
                'text-primary':
                  editorStore.selectedNavigationDesign === 'shapes',
              }"
            >
              <path
                fill="currentColor"
                d="m8.77 17.989l.224.008q.11.003.237.003q.148 0 .276-.003l.262-.008v1.78h10v-10h-1.78l.008-.262Q18 9.379 18 9.23q0-.127-.003-.237l-.008-.225h2.78v12h-12zm.464-2.758q-2.505 0-4.254-1.746q-1.75-1.745-1.75-4.25T4.977 4.98q1.745-1.75 4.251-1.75t4.255 1.746t1.749 4.251t-1.745 4.255t-4.251 1.749m-.004-1q2.075 0 3.537-1.463t1.463-3.537t-1.463-3.538t-3.537-1.462t-3.538 1.462t-1.462 3.538t1.462 3.537t3.538 1.463m0-5"
              />
            </svg>
            <span
              class="font-extralight text-sm"
              :class="{
                'text-primary':
                  editorStore.selectedNavigationDesign === 'shapes',
              }"
              >Shapes</span
            >
          </button>
        </template>
      </ShapesDropdown>
      <MediaDropdown
        v-model="selectedMedia"
        position-left=""
        placeholder="Select a size"
      >
        <template #trigger>
          <button
            class="flex flex-col justify-center rounded-md w-14 h-14 hover:bg-grayBackground items-center"
            :class="{
              'bg-primaryLight':
                editorStore.selectedNavigationDesign === 'media',
            }"
            @click="selectElementType('media')"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              :class="{
                'text-primary':
                  editorStore.selectedNavigationDesign === 'media',
              }"
              width="24"
              height="24"
              viewBox="0 0 24 24"
            >
              <path
                fill="currentColor"
                d="M10.864 16.867L8.37 18.43q-.211.13-.416.016t-.205-.364v-3.123q0-.25.205-.365t.416.016l2.492 1.562q.193.121.193.344t-.192.352M13 9.616q-1.122 0-1.907-.784t-.785-1.905t.785-1.908T13 4.231h.5q.192 0 .317.125t.125.316t-.125.318t-.317.125H13q-.753 0-1.28.529t-.528 1.284t.527 1.279T13 8.73h.5q.192 0 .317.125t.125.316t-.125.317t-.317.126zm4 0h-.5q-.192 0-.317-.126q-.125-.125-.125-.316t.125-.317t.317-.126h.5q.753 0 1.28-.529t.528-1.283t-.528-1.28T17 5.117h-.5q-.192 0-.317-.126q-.125-.125-.125-.316t.125-.317t.317-.126h.5q1.122 0 1.907.784t.785 1.904t-.785 1.908T17 9.616m-.75-2.25h-2.5q-.192 0-.317-.126q-.125-.125-.125-.316t.125-.317t.317-.126h2.5q.192 0 .317.125t.125.316t-.125.318t-.317.125m-.708 5.731v-1h4.842q.27 0 .443-.173t.173-.442V3.71q0-.269-.173-.442t-.442-.173H9.615q-.269 0-.442.173T9 3.712v7.807H8V3.712q0-.667.475-1.141t1.14-.475h10.77q.666 0 1.14.475T22 3.71v7.77q0 .666-.475 1.14q-.474.475-1.14.475zM3.616 21.904q-.667 0-1.142-.475T2 20.29v-7.54q0-.666.475-1.14q.474-.476 1.14-.476h10.77q.666 0 1.14.475q.475.475.475 1.141v7.539q0 .666-.475 1.14t-1.14.475zm0-1h10.769q.269 0 .442-.173t.173-.442V12.75q0-.27-.173-.442q-.173-.173-.442-.173H3.615q-.269 0-.442.173T3 12.75v7.539q0 .269.173.442t.443.173M9 16.519"
              />
            </svg>

            <span
              class="font-extralight text-sm"
              :class="{
                'text-primary':
                  editorStore.selectedNavigationDesign === 'media',
              }"
              >Media</span
            >
          </button>
        </template>
      </MediaDropdown>
      <GraphicDropdown
        position-left=""
        placeholder="Select a size"
        v-model="selectedGraphic"
      >
        <template #trigger>
          <button
            class="flex flex-col justify-center rounded-md w-14 h-14 hover:bg-grayBackground items-center"
            :class="{
              'bg-primaryLight':
                editorStore.selectedNavigationDesign === 'graphic',
            }"
            @click="selectElementType('graphic')"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="24"
              height="24"
              viewBox="0 0 256 256"
              :class="{
                'text-primary':
                  editorStore.selectedNavigationDesign === 'graphic',
              }"
            >
              <path
                fill="currentColor"
                d="M173.19 155c-9.92 17.16-26.39 27-45.19 27s-35.27-9.84-45.19-27a6 6 0 0 1 10.38-6c7.84 13.54 20.2 21 34.81 21s27-7.46 34.81-21a6 6 0 1 1 10.38 6M230 128A102 102 0 1 1 128 26a102.12 102.12 0 0 1 102 102m-12 0a90 90 0 1 0-90 90a90.1 90.1 0 0 0 90-90M92 118a10 10 0 1 0-10-10a10 10 0 0 0 10 10m72-20a10 10 0 1 0 10 10a10 10 0 0 0-10-10"
              />
            </svg>
            <span
              class="font-extralight text-sm"
              :class="{
                'text-primary':
                  editorStore.selectedNavigationDesign === 'graphic',
              }"
              >Graphic</span
            >
          </button>
        </template>
      </GraphicDropdown>
      <BackgroundDropdown
        position-left=""
        placeholder="Select a size"
        v-model="selectedBackground"
        title="Add Background"
      >
        <template #trigger>
          <button
            class="flex flex-col justify-center rounded-md px-1 h-14 hover:bg-grayBackground items-center"
            :class="{
              'bg-primaryLight':
                editorStore.selectedNavigationDesign === 'background',
            }"
            @click="selectElementType('background')"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="24"
              height="24"
              viewBox="0 0 24 24"
              :class="{
                'text-primary':
                  editorStore.selectedNavigationDesign === 'background',
              }"
            >
              <path
                fill="currentColor"
                d="M5 3h13a3 3 0 0 1 3 3v13a3 3 0 0 1-3 3H5a3 3 0 0 1-3-3V6a3 3 0 0 1 3-3Zm0 1a2 2 0 0 0-2 2v11.586l4.293-4.293l2.5 2.5l5-5L20 16V6a2 2 0 0 0-2-2H5Zm4.793 13.207l-2.5-2.5L3 19a2 2 0 0 0 2 2h13a2 2 0 0 0 2-2v-1.586l-5.207-5.207l-5 5ZM7.5 6a2.5 2.5 0 1 1 0 5a2.5 2.5 0 0 1 0-5Zm0 1a1.5 1.5 0 1 0 0 3a1.5 1.5 0 0 0 0-3Z"
              />
            </svg>

            <span
              class="font-extralight text-sm"
              :class="{
                'text-primary':
                  editorStore.selectedNavigationDesign === 'background',
              }"
              >Background</span
            >
          </button>
        </template>
      </BackgroundDropdown>
    </div>
    <div class="flex gap-5 items-center">
      <div class="w-[32px] h-[32px] rounded-sm relative">
        <!-- this should be an profile picture -->
        <Dropdown
          :items="dropdownItems"
          position-top="110%"
          position-left="-80px"
        >
          <template #trigger>
            <img
              class="rounded-md"
              src="../assets/images/logo.svg"
              @click="accountModalOpen = true"
              alt=""
            />
          </template>
        </Dropdown>
      </div>
      <div class="h-[24px] w-[1px] bg-grayBackgroundLight"></div>
      <div>
         <DownloadDropdown />
      </div>
    </div>
  </nav>
</template>
<script>
import { markRaw } from "vue";
import CogOutlineIcon from "./CogOutlineIcon.vue";
import LogoutIcon from "./LogoutIcon.vue";
import AccountIcon from "./AccountIcon.vue";
import { useEditorStore } from "@/stores/editorStore";
import { useCanvasRef } from "~/composables/useCanvasRef";

export default {
  setup() {
    const { canvasEditor } = useCanvasRef();

    const handleDownload = () => {
      canvasEditor.value?.downloadCanvas();
    };

    const editorStore = useEditorStore();
    return {
      editorStore,
      handleDownload,
    };
  },
  name: "Navigation",
  data() {
    return {
      accountModalOpen: false,
      selectedNavigationDesign: null,
      selectedTextInput: null,
      selectedSize: `${this.editorStore.canvasHeight}x${this.editorStore.canvasWidth}`,
      selectedMedia: null,
      selectedBackground: null,
      selectedShape: null,
      selectedGraphic: null,
      dropdownItems: [
        // {
        //   label: "Account",
        //   icon: markRaw(AccountIcon),
        //   href: "/dashboard/account",
        // },
        {
          label: "Settings",
          icon: markRaw(CogOutlineIcon),
          href: "/dashboard/settings",
        },
        { label: "Logout", icon: markRaw(LogoutIcon), action: "logout" },
      ],
      dropdownItemsSize: [
        {
          category: "Social Media Posts",
          items: [
            {
              label: "Facebook Post",
              value: "1200x900",
              width: 1200,
              height: 900,
              icon: "facebook",
            },
            {
              label: "Instagram Post",
              value: "1080x1080",
              width: 1080,
              height: 1080,
              icon: "instagram",
            },
            {
              label: "Instagram Story",
              value: "1080x1920",
              width: 1080,
              height: 1920,
              icon: "instagram",
            },
            {
              label: "LinkedIn Post",
              value: "1200x628",
              width: 1200,
              height: 628,
              icon: "linkedin",
            },
            {
              label: "X Post",
              value: "1024x512",
              width: 1024,
              height: 512,
              icon: "twitter",
            },
            {
              label: "YouTube Thumbnail",
              value: "1280x720",
              width: 1280,
              height: 720,
              icon: "youtube",
            },
          ],
        },
        {
          category: "Infographics",
          items: [
            {
              label: "Infographic",
              value: "800x2000",
              width: 800,
              height: 2000,
            },
            {
              label: "Infographic",
              value: "1000x500",
              width: 1000,
              height: 500,
            },
          ],
        },
        // {
        //   category: "Headers and Banners",
        //   items: [
        //     {
        //       label: "YouTube Banner",
        //       value: "2560x1440",
        //       width: 2560,
        //       height: 1440,
        //       icon: "youtube",
        //     },
        //     {
        //       label: "Twitch Cover",
        //       value: "1200x480",
        //       width: 1200,
        //       height: 480,
        //       icon: "twitch",
        //     },
        //   ],
        // },
        // {
        //   category: "Advertising",
        //   items: [
        //     {
        //       label: "Facebook Carousel",
        //       value: "1080x1080",
        //       width: 1080,
        //       height: 1080,
        //       icon: "facebook",
        //     },
        //     {
        //       label: "Medium Rectangle",
        //       value: "300x250",
        //       width: 300,
        //       height: 250,
        //     },
        //     { label: "Leaderboard", value: "728x90", width: 728, height: 90 },
        //     {
        //       label: "Wide Skyscraper",
        //       value: "160x600",
        //       width: 160,
        //       height: 600,
        //     },
        //     { label: "Billboard", value: "970x250", width: 970, height: 250 },
        //   ],
        // },
      ],
      dropdownTextSize: [
        {
          label: "Title 1",
          value: "Title1",
          class: "text-2xl font-extrabold",
        },
        {
          label: "Title 2",
          value: "Title2",
          class: "text-xl font-extrabold",
        },
        {
          label: "Subtitle",
          value: "subTitle",
          class: "text-lg font-bold",
        },
        {
          label: "Body",
          value: "body",
          class: "text-sm font-normal",
        },
        {
          label: "Caption",
          value: "Caption",
          class: "text-sm font-extralight",
        },
      ],
    };
  },
  computed: {
    templateName: {
      get() {
        return this.editorStore?.templateName;
      },
      set(value) {
        this.editorStore.templateName = value;
      },
    },
    height() {
      return this.editorStore.canvasHeight
    }
  },
  methods: {
    handleConfirm() {
      this.isModalCsvOpen = false;
    },
    selectElementType(element) {
      this.editorStore.selectedNavigationDesign = element;
      this.editorStore.selectedElementType = element;
    },
    handleTitleSizeChange(fontSize) {
      // If you have a selected element
      this.editorStore.addTextElement(fontSize);
    },
  },
  watch: {
    selectedText: {
      handler(newValue) {
        this.editorStore.selectedNavigationDesign = null;
      },
    },
    selectedTextInput: {
      handler(newValue, oldValue) {},
    },
    "editorStore.selectedNavigationDesign": function (newStatus) {
      this.selectedNavigationDesign = newStatus;
    },
    selectedSize: {
      handler(newValue) {
        // Search through all categories and their items
        const selectedOption = this.dropdownItemsSize.reduce(
          (found, category) => {
            if (found) return found; // If already found, return it
            return category.items.find((item) => item.value === newValue);
          },
          null
        );

        if (selectedOption) {
          this.editorStore.$patch({
            canvasWidth: selectedOption.width,
            canvasHeight: selectedOption.height,
          });
        }
      },
      immediate: true,
    },
  },
};
</script>

<style scoped>
.navigation {
  height: 80px;
}

.user-menu {
  display: flex;
  gap: 5px;
}

.logo-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 5px;
}

.logo-wrapper img {
  width: 120px;
}

.logo-wrapper h1 {
  font-size: var(--font-size-large);
  color: var(--primary-color);
  margin: 0;
  font-weight: bold;
}
</style>