<template>
  <div
    v-if="selectedElementType"
    class="w-[300px] min-h-[600px] text-sm p-4 border z-20 border-grayBackground rounded-md"
  >
    <div v-if="selectedElementType === 'text'">
      <h2 class="font-semibold">Text</h2>
      <Dropdown
        v-model="selectedFont"
        :items="dropdownItemsFont"
        position-top="100%"
        position-left=""
        placeholder="Select a size"
      >
        <template #trigger>
          <div
            class="border gap-4 flex justify-between w-[150px] cursor-pointer border-lineColor rounded-md px-1 py-2 outline-primary text-sm"
          >
            <span class="font-light" :style="{ fontFamily: selectedFont }">
              {{ selectedFont }}
            </span>
            <ChewronDownIcon size="20"></ChewronDownIcon>
          </div>
        </template>
      </Dropdown>
      <div class="w-full flex gap-5 justify-center mt-4">
        <div
          class="w-[210px] bg-grayBackgroundLight px-1 rounded-md flex gap-2 justify-center items-center h-[34px]"
        >
          <div
            class="w-6 h-6 p-[1px] rounded-md cursor-pointer flex justify-center items-center"
            @click="selectTextType('bold')"
            :class="selectedTextTypes.includes('bold') ? 'bg-blue-200' : 'bg-white '"
          >
            <BoldIcon></BoldIcon>
          </div>
          <div
            class="w-6 h-6 p-[1px] rounded-md flex justify-center cursor-pointer items-center"
            @click="selectTextType('italic')"
            :class="selectedTextTypes.includes('italic') ?  'bg-blue-200': 'bg-white '"
          >
            <ItalicIcon></ItalicIcon>
          </div>
          <div
            class="w-6 h-6 p-[1px] rounded-md flex justify-center cursor-pointer items-center"
            @click="selectTextType('underline')"
            :class="selectedTextTypes.includes('underline') ?  'bg-blue-200': 'bg-white '"
          >
            <UnderlineIcon></UnderlineIcon>
          </div>
          <div
            class="w-6 h-6 p-[1px] rounded-md flex justify-center cursor-pointer items-center"
            @click="selectTextType('strikethrough')"
            :class="selectedTextTypes.includes('strikethrough') ?  'bg-blue-200':'bg-white '"
          >
            <StrikethroughIcon></StrikethroughIcon>
          </div>
        </div>
        <div
          class="w-[120px] bg-grayBackgroundLight px-1 rounded-md flex gap-3 justify-center items-center h-[34px]"
        >
          <div
            class="w-6 h-6 p-[1px] rounded-md flex justify-center cursor-pointer items-center"
            @click="selectTextAlign('left')"
            :class="selectedTextAlign === 'left' ? 'bg-blue-200' : 'bg-white'"
          >
            <LeftAlignText></LeftAlignText>
          </div>
          <div
            class="w-6 h-6 p-[1px] rounded-md flex justify-center cursor-pointer items-center"
            @click="selectTextAlign('center')"
            :class="selectedTextAlign === 'center' ? 'bg-blue-200' : 'bg-white'"
          >
            <CenterAlignText></CenterAlignText>
          </div>
          <div
            class="w-6 h-6 p-[1px] rounded-md flex justify-center cursor-pointer items-center"
            @click="selectTextAlign('right')"
            :class="selectedTextAlign === 'right' ? 'bg-blue-200' : 'bg-white'"
          >
            <RightAlignText></RightAlignText>
          </div>
        </div>
      </div>
      <div class="w-full flex gap-5 justify-center mt-4">
        <div
          class="w-[120px] bg-grayBackgroundLight px-3 rounded-md flex gap-1 justify-between items-center h-[34px]"
        >
          <ColorPicker v-model="backgroundPicked" />
        </div>
        <Dropdown
          v-model="selectedFontSize"
          :items="dropdownItemsFontSize"
          position-top="100%"
          position-left=""
          placeholder="Select a size"
          class="fontsize-dropdown"
        >
          <template #trigger>
            <div
              class="border gap-4 flex justify-between cursor-pointer border-lineColor rounded-md px-1 py-2 outline-primary text-sm"
            >
              <span>{{ selectedFontSize }}</span>

              <ChewronDownIcon size="20"></ChewronDownIcon>
            </div>
          </template>
        </Dropdown>
      </div>
      <div class="w-full flex gap-5 justify-center mt-4">
        <div
          class="w-[120px] bg-grayBackgroundLight px-3 rounded-md flex gap-1 justify-between items-center h-[34px]"
        >
          <div class="w-12">
            <svg
              width="24"
              height="24"
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 24 24"
            >
              <path
                fill="currentColor"
                d="M10 13h12v-2H10m0 8h12v-2H10m0-10h12V5H10M6 7h2.5L5 3.5L1.5 7H4v10H1.5L5 20.5L8.5 17H6V7Z"
              />
            </svg>
          </div>
          <Dropdown
            v-model="selectedLineHeight"
            :items="lineHeightOptions"
            position-top="100%"
            position-left=""
            placeholder="Select a size"
            class="lenghtsize-dropdown"
          >
            <template #trigger>
              <div
                class="border gap-4 flex justify-between cursor-pointer border-lineColor rounded-md px-1 py-2 outline-primary text-sm"
              >
                <span>{{ selectedLineHeight }}</span>

                <ChewronDownIcon size="20"></ChewronDownIcon>
              </div>
            </template>
          </Dropdown>
        </div>
        <div
          class="w-[120px] bg-grayBackgroundLight px-3 rounded-md flex gap-1 justify-between items-center h-[34px]"
        >
          <div class="w-12">
            <svg
              width="24"
              height="24"
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 24 24"
            >
              <path
                fill="currentColor"
                d="M22 3v18h-2V3h2M4 3v18H2V3h2m6 10.7h4l-2-5.4l-2 5.4M11.2 6h1.7l4.7 12h-2l-.9-2.6H9.4L8.5 18h-2l4.7-12Z"
              />
            </svg>
          </div>
          <Dropdown
            v-model="selectedLetterSpacing"
            :items="letterSpacingOptions"
            position-top="100%"
            position-left=""
            placeholder="Select a size"
            class="lenghtsize-dropdown"
          >
            <template #trigger>
              <div
                class="border gap-4 flex justify-between cursor-pointer border-lineColor rounded-md px-1 py-2 outline-primary text-sm"
              >
                <span>{{ selectedLetterSpacing }}</span>

                <ChewronDownIcon size="20"></ChewronDownIcon>
              </div>
            </template>
          </Dropdown>
        </div>
      </div>

      <div class="w-full h-[1px] bg-grayBackground mt-4"></div>
      <div class="w-full flex gap-1 justify-center flex-col mt-4">
        <h2 class="font-semibold">Layer</h2>
        <div class="w-full mt-2">
          <label
            for="border-radius"
            class="block text-sm font-light text-gray-700 mb-1"
            >Text Opacity</label
          >
          <div class="flex items-center gap-5">
            <input
              id="border-radius"
              type="range"
              min="0"
              max="1"
              step="0.01"
              v-model="opacity"
              class="w-[210px] h-1.5 bg-[#BEBFC5] rounded-full appearance-none cursor-pointer"
            />
            <div class="font-light w-[15px]">
              {{ parseFloat(opacity * 100).toFixed(0) }}%
            </div>
          </div>
        </div>
      </div>
      <div class="w-full h-[1px] bg-grayBackground mt-4"></div>
      <div class="w-full flex gap-1 justify-start flex-col mt-1">
        <div class="w-full flex justify-between items-center mt-4">
          <h2 class="font-semibold">Shadow</h2>
          <label class="relative inline-flex items-center cursor-pointer">
            <input
              type="checkbox"
              v-model="shadowEnabled"
              class="sr-only peer"
            />
            <div
              class="w-9 h-5 bg-gray-200 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full rtl:peer-checked:after:-translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:start-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-4 after:w-4 after:transition-all peer-checked:bg-primary"
            ></div>
          </label>
        </div>
        <div class="flex flex-wrap gap-5 mt-2">
          <div>
            <label class="block text-sm font-light text-gray-700 mb-1"
              >Offset X</label
            >
            <div class="relative">
              <input
                type="number"
                v-model="offsetX"
                :disabled="!shadowEnabled"
                step="1"
                min="0"
                class="w-[120px] h-[34px] text-sm font-light px-3 py-2 bg-grayBackgroundLight rounded-md text-gray-900"
                @input="validateInputOffsetX"
              />
              <div
                class="absolute right-2 top-0 h-full flex flex-col justify-center"
              >
                <button
                  @click="decrementOffsetX"
                  class="text-gray-500 hover:text-gray-700"
                >
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="16"
                    height="16"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                  >
                    <path d="M6 9l6 6 6-6" />
                  </svg>
                </button>
              </div>
            </div>
          </div>
          <div>
            <label class="block text-sm font-light text-gray-700 mb-1"
              >Offset Y</label
            >
            <div class="relative">
              <input
                type="number"
                v-model="offsetY"
                :disabled="!shadowEnabled"
                step="1"
                min="0"
                class="w-[120px] h-[34px] text-sm font-light px-3 py-2 bg-grayBackgroundLight rounded-md text-gray-900"
                @input="validateInputOffsetY"
              />
              <div
                class="absolute right-2 top-0 h-full flex flex-col justify-center"
              >
                <button
                  @click="incrementOffsetY"
                  class="text-gray-500 hover:text-gray-700"
                >
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="16"
                    height="16"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                  >
                    <path d="M18 15l-6-6-6 6" />
                  </svg>
                </button>
                <button
                  @click="decrementOffsetY"
                  class="text-gray-500 hover:text-gray-700"
                >
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="16"
                    height="16"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                  >
                    <path d="M6 9l6 6 6-6" />
                  </svg>
                </button>
              </div>
            </div>
          </div>
          <div>
            <label class="block text-sm font-light text-gray-700 mb-1"
              >Blur</label
            >
            <div class="relative">
              <input
                type="number"
                v-model="blur"
                :disabled="!shadowEnabled"
                step="0.1"
                min="0"
                class="w-[120px] h-[34px] text-sm font-light px-3 py-2 bg-grayBackgroundLight rounded-md text-gray-900"
                @input="validateInputBlur"
              />
              <div
                class="absolute right-2 top-0 h-full flex flex-col justify-center"
              >
                <button
                  @click="incrementBlur"
                  class="text-gray-500 hover:text-gray-700"
                >
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="16"
                    height="16"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                  >
                    <path d="M18 15l-6-6-6 6" />
                  </svg>
                </button>
                <button
                  @click="decrementBlur"
                  class="text-gray-500 hover:text-gray-700"
                >
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="16"
                    height="16"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                  >
                    <path d="M6 9l6 6 6-6" />
                  </svg>
                </button>
              </div>
            </div>
          </div>
        </div>
        <label class="block text-sm font-light mt-2 text-gray-700 mb-1"
          >Color</label
        >
        <div
          class="w-[120px] bg-grayBackgroundLight px-3 rounded-md flex gap-1 justify-between items-center h-[34px]"
        >
          <input
            type="color"
            v-model="shadowBackgroundPicked"
            class="w-6 h-6 rounded-md border-none color-input-no-border outline-none cursor-pointer bg-gradient-to-br appearance-none"
            :style="{ backgroundColor: shadowBackgroundPicked }"
          />
          <div class="font-extralight">{{ shadowBackgroundPicked }}</div>
        </div>
      </div>
    </div>
    <div v-if="selectedElementType === 'shape'">
      <h2 class="font-semibold">Shape</h2>
      <div class="mt-4 flex flex-col">
        <label class="block text-sm font-light text-gray-700 mb-1">Fill</label>
        <div class="flex items-center justify-between">
          <Dropdown
            v-model="selectedFillOptions"
            :items="dropdownItemsFill"
            position-top="100%"
            position-left=""
            placeholder="Select a size"
            class="fillshape-dropdown"
          >
            <template #trigger>
              <div
                class="border gap-4 flex justify-between w-[300px] h-[34px] cursor-pointer border-lineColor rounded-md px-1 py-2 outline-primary text-sm"
              >
                <span class="font-light">{{ selectedFillOptions }}</span>

                <ChewronDownIcon size="20"></ChewronDownIcon>
              </div>
            </template>
          </Dropdown>
          <div>
            <div
              class="w-[120px] bg-grayBackgroundLight px-3 rounded-md flex gap-1 justify-between items-center h-[34px]"
            >
              <ColorPicker v-model="backgroundPickedElement" />
            </div>
          </div>
        </div>
      </div>
      <div class="mt-4 flex flex-col">
        <label  v-if="store.selectedElement.shapeType !== 'line'" class="block text-sm font-light text-gray-700 mb-1"
          >Border</label
        >
        <div  v-if="store.selectedElement.shapeType !== 'line'" class="flex items-center justify-between">
          <Dropdown
            v-model="selectedBorderOption"
            :items="dropdownItemsBorder"
            position-top="100%"
            position-left=""
            placeholder="Select a size"
            class="bordershape-dropdown"
          >
            <template #trigger>
              <div
                class="border gap-4 flex justify-between w-[10px] h-[34px] cursor-pointer border-lineColor rounded-md px-1 py-2 outline-primary text-sm"
              >
                <span class="font-light">{{ selectedBorderOption }}</span>

                <ChewronDownIcon size="20"></ChewronDownIcon>
              </div>
            </template>
          </Dropdown>
          <div>
            <div
              class="w-[120px] bg-grayBackgroundLight px-3 rounded-md flex gap-1 justify-between items-center h-[34px]"
            >
              <ColorPicker
                :is-color-disabled="selectedBorderOption === 'None'"
                v-model="fillBackgroundBorder"
              />
            </div>
          </div>
        </div>
        <div class="relative mt-3">
          <input
           v-if="store.selectedElement.shapeType !== 'line'"
            type="number"
            v-model="borderThickness"
            step="0.1"
            min="0"
            class="w-full h-[34px] text-sm font-light px-3 py-2 bg-grayBackgroundLight rounded-md text-gray-900"
            @input="validateInputBorderThickness"
          />
          <div
            class="absolute right-2 top-0 h-full flex flex-col justify-center"
             v-if="store.selectedElement.shapeType !== 'line'"
          >
            <button
              @click="incrementBorderThickness"
              class="text-gray-500 hover:text-gray-700"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="16"
                height="16"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
                stroke-linecap="round"
                stroke-linejoin="round"
              >
                <path d="M18 15l-6-6-6 6" />
              </svg>
            </button>
            <button
              @click="decrementBorderThickness"
              class="text-gray-500 hover:text-gray-700"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="16"
                height="16"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
                stroke-linecap="round"
                stroke-linejoin="round"
              >
                <path d="M6 9l6 6 6-6" />
              </svg>
            </button>
          </div>
        </div>
        <div class="mt-3" v-if="isElementForRoundedCorners">
          <label class="block text-sm font-light text-gray-700 mb-1"
            >Rounded Corners</label
          >
          <div class="relative">
            <input
              type="number"
              v-model="roundedBorder"
              step="1"
              min="0"
              class="w-full h-[34px] text-sm font-light px-3 py-2 bg-grayBackgroundLight rounded-md text-gray-900"
              @input="validateInputRoundedBorder"
            />
            <div
              class="absolute right-2 top-0 h-full flex flex-col justify-center"
            >
              <button
                @click="incrementRoundedBorder"
                class="text-gray-500 hover:text-gray-700"
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  width="16"
                  height="16"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                >
                  <path d="M18 15l-6-6-6 6" />
                </svg>
              </button>
              <button
                @click="decrementRoundedBorder"
                class="text-gray-500 hover:text-gray-700"
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  width="16"
                  height="16"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                >
                  <path d="M6 9l6 6 6-6" />
                </svg>
              </button>
            </div>
          </div>
        </div>
        <div class="w-full mt-3">
          <label
            for="border-radius"
            class="block text-sm font-light text-gray-700 mb-1"
            >Shape Opacity</label
          >
          <div class="flex items-center gap-5">
            <input
              id="border-radius"
              type="range"
              min="0"
              max="100"
              step="1"
              v-model="shapeOpacity"
              class="w-[210px] h-1.5 bg-[#BEBFC5] rounded-full appearance-none cursor-pointer"
            />
            <div class="font-light w-[15px]">
              {{ parseFloat(shapeOpacity).toFixed(0) }}%
            </div>
          </div>
        </div>
        
        <!-- Shadow Controls -->
        <div class="w-full h-[1px] bg-grayBackground mt-4"></div>
        <div class="w-full flex gap-1 justify-start flex-col mt-1">
          <div class="w-full flex justify-between items-center mt-4">
            <h2 class="font-semibold">Shadow</h2>
            <label class="relative inline-flex items-center cursor-pointer">
              <input
                type="checkbox"
                v-model="shapeShadowEnabled"
                class="sr-only peer"
              />
              <div
                class="w-9 h-5 bg-gray-200 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full rtl:peer-checked:after:-translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:start-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-4 after:w-4 after:transition-all peer-checked:bg-primary"
              ></div>
            </label>
          </div>
          <div class="flex flex-wrap gap-5 mt-2">
            <div>
              <label class="block text-sm font-light text-gray-700 mb-1"
                >Offset X</label
              >
              <div class="relative">
                <input
                  type="number"
                  v-model="shapeShadowOffsetX"
                  :disabled="!shapeShadowEnabled"
                  step="1"
                  class="w-[120px] h-[34px] text-sm font-light px-3 py-2 bg-grayBackgroundLight rounded-md text-gray-900"
                  @input="validateShapeShadowOffsetX"
                />
                <div
                  class="absolute right-2 top-0 h-full flex flex-col justify-center"
                >
                  <button
                    @click="incrementShapeShadowOffsetX"
                    class="text-gray-500 hover:text-gray-700"
                  >
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      width="16"
                      height="16"
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      stroke-width="2"
                      stroke-linecap="round"
                      stroke-linejoin="round"
                    >
                      <path d="M18 15l-6-6-6 6" />
                    </svg>
                  </button>
                  <button
                    @click="decrementShapeShadowOffsetX"
                    class="text-gray-500 hover:text-gray-700"
                  >
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      width="16"
                      height="16"
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      stroke-width="2"
                      stroke-linecap="round"
                      stroke-linejoin="round"
                    >
                      <path d="M6 9l6 6 6-6" />
                    </svg>
                  </button>
                </div>
              </div>
            </div>
            <div>
              <label class="block text-sm font-light text-gray-700 mb-1"
                >Offset Y</label
              >
              <div class="relative">
                <input
                  type="number"
                  v-model="shapeShadowOffsetY"
                  :disabled="!shapeShadowEnabled"
                  step="1"
                  class="w-[120px] h-[34px] text-sm font-light px-3 py-2 bg-grayBackgroundLight rounded-md text-gray-900"
                  @input="validateShapeShadowOffsetY"
                />
                <div
                  class="absolute right-2 top-0 h-full flex flex-col justify-center"
                >
                  <button
                    @click="incrementShapeShadowOffsetY"
                    class="text-gray-500 hover:text-gray-700"
                  >
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      width="16"
                      height="16"
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      stroke-width="2"
                      stroke-linecap="round"
                      stroke-linejoin="round"
                    >
                      <path d="M18 15l-6-6-6 6" />
                    </svg>
                  </button>
                  <button
                    @click="decrementShapeShadowOffsetY"
                    class="text-gray-500 hover:text-gray-700"
                  >
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      width="16"
                      height="16"
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      stroke-width="2"
                      stroke-linecap="round"
                      stroke-linejoin="round"
                    >
                      <path d="M6 9l6 6 6-6" />
                    </svg>
                  </button>
                </div>
              </div>
            </div>
            <div>
              <label class="block text-sm font-light text-gray-700 mb-1"
                >Blur</label
              >
              <div class="relative">
                <input
                  type="number"
                  v-model="shapeShadowBlur"
                  :disabled="!shapeShadowEnabled"
                  step="1"
                  min="0"
                  class="w-[120px] h-[34px] text-sm font-light px-3 py-2 bg-grayBackgroundLight rounded-md text-gray-900"
                  @input="validateShapeShadowBlur"
                />
                <div
                  class="absolute right-2 top-0 h-full flex flex-col justify-center"
                >
                  <button
                    @click="incrementShapeShadowBlur"
                    class="text-gray-500 hover:text-gray-700"
                  >
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      width="16"
                      height="16"
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      stroke-width="2"
                      stroke-linecap="round"
                      stroke-linejoin="round"
                    >
                      <path d="M18 15l-6-6-6 6" />
                    </svg>
                  </button>
                  <button
                    @click="decrementShapeShadowBlur"
                    class="text-gray-500 hover:text-gray-700"
                  >
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      width="16"
                      height="16"
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      stroke-width="2"
                      stroke-linecap="round"
                      stroke-linejoin="round"
                    >
                      <path d="M6 9l6 6 6-6" />
                    </svg>
                  </button>
                </div>
              </div>
            </div>
          </div>
          <label class="block text-sm font-light mt-2 text-gray-700 mb-1"
            >Color</label
          >
          <div
            class="w-[120px] bg-grayBackgroundLight px-3 rounded-md flex gap-1 justify-between items-center h-[34px]"
          >
            <ColorPicker
              :is-color-disabled="!shapeShadowEnabled"
              v-model="shapeShadowColor"
            />
          </div>
        </div>
      </div>
    </div>

    <div v-if="selectedElementType === 'graphic'">
      <h2 class="font-semibold">Graphic</h2>
      <div class="mt-4 flex flex-col">
        <label class="block text-sm font-light text-gray-700 mb-1"
          >Flip & Rotate</label
        >
        <div class="flex gap-6 mt-2 justify-center items-center">
          <div class="flex gap-1 w-1/4 justify-between items-center">
            <div
              class="bg-grayBackgroundLight w-full items-center justify-center flex h-9 p-1 rounded-md cursor-pointer"
              @click="handleFlipHorizontal"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                height="28"
                width="28"
                viewBox="0 0 28 28"
              >
                <path
                  fill="#3E57DA"
                  d="M25.882 23.654a.75.75 0 0 1-.632.346h-9.5a.75.75 0 0 1-.75-.75V2.75a.75.75 0 0 1 1.43-.315l9.5 20.5a.75.75 0 0 1-.048.719M16.5 6.152V22.5h7.576zM2.75 24a.75.75 0 0 1-.68-1.065l9.5-20.5A.75.75 0 0 1 13 2.75v20.5a.75.75 0 0 1-.75.75z"
                />
              </svg>
            </div>
          </div>
          <div class="flex gap-1 w-1/4 justify-between items-center">
            <div
              class="bg-grayBackgroundLight w-full flex justify-center items-center h-9 p-1 rounded-md cursor-pointer"
              @click="handleFlipVertical"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                style="margin-top: 4px"
                height="30"
                width="30"
                viewBox="0 0 28 28"
              >
                <path
                  fill="#3E57DA"
                  d="M19.656 2.12a.75.75 0 0 1 .344.63v7.5a.75.75 0 0 1-.75.75H2.75a.75.75 0 0 1-.31-1.433l16.5-7.5a.75.75 0 0 1 .716.052M6.213 9.5H18.5V3.915zM20 21.5a.5.5 0 0 1-.713.452l-17-8A.5.5 0 0 1 2.5 13h17a.5.5 0 0 1 .5.5z"
                />
              </svg>
            </div>
          </div>
          <div class="flex gap-1 w-1/4 justify-between items-center">
            <div
              class="bg-grayBackgroundLight w-full flex justify-center h-9 p-1 items-center rounded-md cursor-pointer"
              @click="handleRotateCounterclockwise"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                height="28"
                width="28"
                viewBox="0 0 24 24"
              >
                <path
                  fill="#3E57DA"
                  d="M12 3a9 9 0 0 0-9 9a9 9 0 0 0 4.873 8.001L6 20a1 1 0 0 0-.117 1.993L6 22h4a1 1 0 0 0 .993-.883L11 21v-4a1 1 0 0 0-1.993-.117L9 17l-.001 1.327A7.01 7.01 0 0 1 5 12a7 7 0 0 1 14 0a1 1 0 1 0 2 0a9 9 0 0 0-9-9m0 6a3 3 0 1 0 0 6a3 3 0 0 0 0-6m0 2a1 1 0 1 1 0 2a1 1 0 0 1 0-2"
                />
              </svg>
            </div>
          </div>
          <div class="flex gap-1 w-1/4 justify-between items-center">
            <div
              class="bg-grayBackgroundLight w-full flex justify-center items-center h-9 p-1 rounded-md cursor-pointer"
              @click="handleRotateClockwise"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 24 24"
                height="28"
                width="28"
              >
                <path
                  fill="#3E57DA"
                  d="M12 3a9 9 0 0 1 9 9a9 9 0 0 1-4.873 8.001L18 20a1 1 0 0 1 .117 1.993L18 22h-4a1 1 0 0 1-.993-.883L13 21v-4a1 1 0 0 1 1.993-.117L15 17l.001 1.327A7.01 7.01 0 0 0 19 12a7 7 0 1 0-14 0a1 1 0 1 1-2 0a9 9 0 0 1 9-9m0 6a3 3 0 1 1 0 6a3 3 0 0 1 0-6m0 2a1 1 0 1 0 0 2a1 1 0 0 0 0-2"
                />
              </svg>
            </div>
          </div>
        </div>
        <div class="w-full mt-4">
          <label
            for="border-radius"
            class="block text-sm font-light text-gray-700 mb-1"
            >Opacity</label
          >
          <div class="flex items-center gap-5">
            <input
              id="border-radius"
              type="range"
              min="0"
              max="100"
              v-model="graphicOpacity"
              class="w-[210px] h-1.5 bg-[#BEBFC5] rounded-full appearance-none cursor-pointer"
            />
            <div class="font-light w-[15px]">{{ graphicOpacity }}%</div>
          </div>
        </div>
        <div class="mt-4 flex flex-col">
          <label class="block text-sm font-light text-gray-700 mb-1"
            >Fill</label
          >
          <div
            class="w-[120px] bg-grayBackgroundLight px-3 rounded-md flex gap-1 justify-between items-center h-[34px]"
            :class="{'opacity-50 cursor-not-allowed': store.selectedElement?.iconType === 'flat'}"
          >
            <ColorPicker 
              v-model="graphicFill" 
              :disabled="store.selectedElement?.iconType === 'flat'"
            />
          </div>
          <span v-if="store.selectedElement?.iconType === 'flat'" class="text-xs text-gray-500 mt-1">
            Color changes are not available for flat icons
          </span>
        </div>
      </div>
    </div>
    <div v-if="selectedElementType === 'media'">
      <h2 class="font-semibold">Media</h2>
      <div class="mt-4 flex flex-col">
        <label class="block text-sm font-light text-gray-700 mb-1"
          >Flip & Rotate</label
        >
        <div class="flex gap-6 mt-2 justify-center items-center">
          <div class="flex gap-1 w-1/4 justify-between items-center">
            <div
              class="bg-grayBackgroundLight w-full items-center justify-center flex h-9 p-1 rounded-md cursor-pointer"
              @click="handleFlipHorizontal"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                height="28"
                width="28"
                viewBox="0 0 28 28"
              >
                <path
                  fill="#3E57DA"
                  d="M25.882 23.654a.75.75 0 0 1-.632.346h-9.5a.75.75 0 0 1-.75-.75V2.75a.75.75 0 0 1 1.43-.315l9.5 20.5a.75.75 0 0 1-.048.719M16.5 6.152V22.5h7.576zM2.75 24a.75.75 0 0 1-.68-1.065l9.5-20.5A.75.75 0 0 1 13 2.75v20.5a.75.75 0 0 1-.75.75z"
                />
              </svg>
            </div>
          </div>
          <div class="flex gap-1 w-1/4 justify-between items-center">
            <div
              class="bg-grayBackgroundLight w-full flex justify-center items-center h-9 p-1 rounded-md cursor-pointer"
              @click="handleFlipVertical"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                style="margin-top: 4px"
                height="30"
                width="30"
                viewBox="0 0 28 28"
              >
                <path
                  fill="#3E57DA"
                  d="M19.656 2.12a.75.75 0 0 1 .344.63v7.5a.75.75 0 0 1-.75.75H2.75a.75.75 0 0 1-.31-1.433l16.5-7.5a.75.75 0 0 1 .716.052M6.213 9.5H18.5V3.915zM20 21.5a.5.5 0 0 1-.713.452l-17-8A.5.5 0 0 1 2.5 13h17a.5.5 0 0 1 .5.5z"
                />
              </svg>
            </div>
          </div>
          <div class="flex gap-1 w-1/4 justify-between items-center">
            <div
              class="bg-grayBackgroundLight w-full flex justify-center h-9 p-1 items-center rounded-md cursor-pointer"
              @click="handleRotateCounterclockwise"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                height="28"
                width="28"
                viewBox="0 0 24 24"
              >
                <path
                  fill="#3E57DA"
                  d="M12 3a9 9 0 0 0-9 9a9 9 0 0 0 4.873 8.001L6 20a1 1 0 0 0-.117 1.993L6 22h4a1 1 0 0 0 .993-.883L11 21v-4a1 1 0 0 0-1.993-.117L9 17l-.001 1.327A7.01 7.01 0 0 1 5 12a7 7 0 0 1 14 0a1 1 0 1 0 2 0a9 9 0 0 0-9-9m0 6a3 3 0 1 0 0 6a3 3 0 0 0 0-6m0 2a1 1 0 1 1 0 2a1 1 0 0 1 0-2"
                />
              </svg>
            </div>
          </div>
          <div class="flex gap-1 w-1/4 justify-between items-center">
            <div
              class="bg-grayBackgroundLight w-full flex justify-center items-center h-9 p-1 rounded-md cursor-pointer"
              @click="handleRotateClockwise"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 24 24"
                height="28"
                width="28"
              >
                <path
                  fill="#3E57DA"
                  d="M12 3a9 9 0 0 1 9 9a9 9 0 0 1-4.873 8.001L18 20a1 1 0 0 1 .117 1.993L18 22h-4a1 1 0 0 1-.993-.883L13 21v-4a1 1 0 0 1 1.993-.117L15 17l.001 1.327A7.01 7.01 0 0 0 19 12a7 7 0 1 0-14 0a1 1 0 1 1-2 0a9 9 0 0 1 9-9m0 6a3 3 0 1 1 0 6a3 3 0 0 1 0-6m0 2a1 1 0 1 0 0 2a1 1 0 0 0 0-2"
                />
              </svg>
            </div>
          </div>
        </div>
        <div class="w-full mt-4">
          <label
            for="border-radius"
            class="block text-sm font-light text-gray-700 mb-1"
            >Opacity</label
          >
          <div class="flex items-center gap-5">
            <input
              id="border-radius"
              type="range"
              min="0"
              max="100"
              v-model="mediaOpacity"
              class="w-[210px] h-1.5 bg-[#BEBFC5] rounded-full appearance-none cursor-pointer"
            />
            <div class="font-light w-[15px]">{{ mediaOpacity }}%</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useEditorStore } from "@/stores/editorStore";
import { useFontStore } from "@/stores/fontStore";

export default {
  name: "SideEditor",
  setup() {
    const store = useEditorStore();

    // Access store state through computed properties
    const elementType = computed(() => store.elementType);
    const shapeProps = computed(() => store.shapeProperties);
    const textProps = computed(() => store.textProperties);
    const graphicProps = computed(() => store.graphicProperties);
    const fontStore = useFontStore();
    return {
      elementType,
      shapeProps,
      textProps,
      graphicProps,
      store,
      fontStore,
    };
  },
  data() {
    // Line height options (unitless values for best practice)
    return {
      selectedTextAlign: "center",
      editorStore: useEditorStore(),
      mediaOpacity: 100,
      selectedElementType: null,
      borderThickness: 1,
      selectedElement: {},
      dropdownItemsBorder: [
        {
          label: "None",
          value: "None",
        },
        {
          label: "Solid",
          value: "Solid",
        },
        {
          label: "Dashed",
          value: "Dashed",
        },
      ],
      dropdownItemsFill: [
        {
          label: "Solid Color",
          value: "Solid Color",
        },
        {
          label: "No Fill", // More user-friendly than "Transparent"
          value: "No Fill",
        },
      ],
      lineHeightOptions: [
        {
          label: "0.75",
          value: "0.75",
        },
        {
          label: "1",
          value: "1",
        },
        {
          label: "1.25",
          value: "1.25",
        },
        {
          label: "1.5",
          value: "1.5",
        },
        {
          label: "1.75",
          value: "1.75",
        },
        {
          label: "2",
          value: "2",
        },
        {
          label: "2.25",
          value: "2.25",
        },
        {
          label: "2.5",
          value: "2.5",
        },
      ], // TEXT
      letterSpacingOptions: [
        {
          label: "-5px",
          value: "-5px",
        },
        {
          label: "-4px",
          value: "-4px",
        },
        {
          label: "-3px",
          value: "-3px",
        },
        {
          label: "-2px",
          value: "-2px",
        },
        {
          label: "-1px",
          value: "-1px",
        },
        {
          label: "0",
          value: "0",
        },
        {
          label: "1px",
          value: "1px",
        },
        {
          label: "2px",
          value: "2px",
        },
        {
          label: "3px",
          value: "3px",
        },
        {
          label: "4px",
          value: "4px",
        },
        {
          label: "5px",
          value: "5px",
        },
        {
          label: "6px",
          value: "6px",
        },
        {
          label: "7px",
          value: "7px",
        },
        {
          label: "8px",
          value: "8px",
        },
        {
          label: "9px",
          value: "9px",
        },
        {
          label: "10px",
          value: "10px",
        },
        {
          label: "11px",
          value: "11px",
        },
        {
          label: "12px",
          value: "12px",
        },
      ], // TEXT
      dropdownItemsFontSize: [
        {
          label: "12",
          value: "12",
        },
        {
          label: "14",
          value: "14",
        },
        {
          label: "16",
          value: "16",
        },
        {
          label: "18",
          value: "18",
        },
        {
          label: "20",
          value: "20",
        },
        {
          label: "22",
          value: "22",
        },
        {
          label: "24",
          value: "24",
        },
        {
          label: "26",
          value: "26",
        },
        {
          label: "28",
          value: "28",
        },
        {
          label: "30",
          value: "30",
        },
        {
          label: "32",
          value: "32",
        },
        {
          label: "34",
          value: "34",
        },
        {
          label: "36",
          value: "36",
        },
        {
          label: "42",
          value: "42",
        },
        {
          label: "48",
          value: "48",
        },
        {
          label: "54",
          value: "54",
        },
        {
          label: "60",
          value: "60",
        },
        {
          label: "66",
          value: "66",
        },
        {
          label: "72",
          value: "72",
        },
        {
          label: "84",
          value: "84",
        },
        {
          label: "96",
          value: "96",
        },
        {
          label: "112",
          value: "112",
        },
        {
          label: "128",
          value: "128",
        },
        {
          label: "136",
          value: "136",
        },
        {
          label: "144",
          value: "144",
        },
        {
          label: "152",
          value: "152",
        },
        {
          label: "160",
          value: "160",
        },
        {
          label: "170",
          value: "170",
        },
        {
          label: "180",
          value: "180",
        },
        {
          label: "190",
          value: "190",
        },
        {
          label: "200",
          value: "200",
        },
      ], // TEXT
      selectedTextTypes: [],
    };
  },
  computed: {
    dropdownItemsFont() {
      // Get font options from the fontStore
      const fontOptions = this.fontStore.getFontOptions;

      // Return the options with styled labels
      return fontOptions.map((font) => ({
        label: font.value,
        value: font.value,
        // Add custom style for the dropdown item
        customStyle: {
          fontFamily: font.value,
          // Optional: add some padding and full width to make it look better
          padding: "8px",
          width: "100%",
          // Optional: add minimum height to ensure consistent sizing
          minHeight: "24px",
        },
      }));
    },

    isElementForRoundedCorners() {
      return (
        this.editorStore.selectedElement.shapeType === "rectangle" ||
        this.editorStore.selectedElement.shapeType === "square" ||
        this.editorStore.selectedElement.shapeType === "roundedSquare" ||
        this.editorStore.selectedElement.shapeType === "roundedRectangle"
      );
    },
    roundedBorder: {
      get() {
        return this.shapeProps?.roundedCorners;
      },
      set(value) {
        this.store.updateShapeProperties({ rx: value, ry: value });
      },
    },
    shadowBackgroundPicked: {
      get() {
        return this.textProps?.shadowColor;
      },
      set(value) {
        this.store.updateTextProperties({ shadowColor: value });
      },
    },
    blur: {
      get() {
        return this.textProps?.shadowBlur;
      },
      set(value) {
        this.store.updateTextProperties({ shadowBlur: value });
      },
    },
    graphicFill: {
      get() {
        // Check if it's a FLAT icon type
        if (this.store.selectedElement.svgType === "icon" && 
            this.store.selectedElement.iconType === "flat") {
          return null; // Return null to indicate color changes not allowed
        }
        
        if (this.store.selectedElement.svgType === "icon") {
          return this.graphicProps?.stroke || "#3E57DA";
        } else if (this.store.selectedElement.svgType === "vector") {
          return this.store.selectedElement.currentColor;
        }
        return this.graphicProps?.fill || "#000000";
      },
      set(value) {
        // Don't allow color changes for FLAT icons
        if (this.store.selectedElement.iconType === "flat") {
          return;
        }

        const finalChange = value && typeof value === 'object' && value.finalChange;
        const colorValue = value && typeof value === 'object' && value.color ? value.color : value;

        let props = {};
        if (this.store.selectedElement.svgType === "icon") {
          if (this.store.selectedElement.iconType === "outline" || 
              this.store.selectedElement.iconType === "all") {
            props["stroke"] = colorValue;
          } else {
            props["stroke"] = colorValue;
            props["fill"] = colorValue;
          }
          if (finalChange) {
            props["finalChange"] = finalChange;
          }
          this.store.updateIconProperties(props);
        }
        if (this.store.selectedElement.svgType === "vector") {
          this.store.selectedElement.currentColor = colorValue;
          if (finalChange) {
            this.store.saveToHistory('colorChange', true);
          }
        }
      }
    },
    graphicOpacity: {
      get() {
        return this.graphicProps?.opacity;
      },
      set(value) {
        this.store.updateIconProperties({ opacity: value });
      },
    },
    offsetY: {
      get() {
        return this.textProps?.shadowOffsetY;
      },
      set(value) {
        this.store.updateTextProperties({ shadowOffsetY: value });
      },
    },
    offsetX: {
      get() {
        return this.textProps?.shadowOffsetX;
      },
      set(value) {
        this.store.updateTextProperties({ shadowOffsetX: value });
      },
    },
    shapeOpacity: {
      get() {
        return this.shapeProps?.opacity;
      },
      set(value) {
        this.store.updateShapeProperties({ opacity: value / 100 });
      },
    },
    opacity: {
      get() {
        return this.textProps?.opacity;
      },
      set(value) {
        this.store.updateTextProperties({ opacity: value });
      },
    },
    shadowEnabled: {
      get() {
        return this.textProps?.hasShadow || false;
      },
      set(value) {
        this.store.updateTextProperties({ hasShadow: value });
      },
    },
    selectedLetterSpacing: {
      get() {
        return this.textProps?.letterSpacing || "1";
      },
      set(value) {
        console.log("value", value)
        this.store.updateTextProperties({ letterSpacing: value });
      },
    },
    selectedLineHeight: {
      get() {
        return this.textProps?.lineHeight || "1";
      },
      set(value) {
        this.store.updateTextProperties({ lineHeight: value });
      },
    },
    backgroundPicked: {
      get() {
        return this.textProps?.color || "transparent";
      },
      set(value) {
        // Check if value is an object with color and finalChange properties
        if (value && typeof value === 'object' && value.color) {
          this.store.updateTextProperties({
            color: value.color,
            finalChange: value.finalChange
          });
        } else {
          // Otherwise treat as a direct color value
          this.store.updateTextProperties({ color: value });
        }
      },
    },

    selectedFont: {
      get() {
        return this.textProps?.font || "transparent";
      },
      set(value) {
        this.store.updateTextProperties({ fontFamily: value });
      },
    },

    selectedFontSize: {
      get() {
        return this.textProps?.fontSize || "transparent";
      },
      set(value) {
        this.store.updateTextProperties({ fontSize: value });
      },
    },
    backgroundPickedElement: {
      get() {
        if (this.shapeProps?.shapeType === "line") {
          return this.shapeProps?.backgroundColor || "transparent";
        }
        return this.shapeProps?.fillColor || "transparent";
      },
      set(value) {
        // Handle object value from color picker
        if (value && typeof value === 'object' && value.color) {
          if (this.shapeProps.shapeType === "line") {
            this.store.updateShapeProperties({ 
              backgroundColor: value.color,
              finalChange: value.finalChange 
            });
          } else {
            this.store.updateShapeProperties({ 
              fill: value.color,
              finalChange: value.finalChange 
            });
          }
        } else {
          // Original behavior for direct values
          if (this.shapeProps.shapeType === "line") {
            this.store.updateShapeProperties({ backgroundColor: value });
          } else {
            this.store.updateShapeProperties({ fill: value });
          }
        }
      },
    },
    fillBackgroundBorder: {
      get() {
        return this.shapeProps?.borderColor || "transparent";
      },
      set(value) {
        this.store.updateShapeProperties({ stroke: value });
      },
    },
    selectedBorderOption: {
      get() {
        return this.shapeProps?.borderType || "transparent";
      },
      set(value) {
        this.store.updateShapeProperties({
          borderType: value,
        });
      },
    },
    selectedFillOptions: {
      get() {
        return this.shapeProps?.fillType || "Solid color";
      },
      set(value) {
        if (value === "Solid Color") {
          this.store.updateShapeProperties({
            fillColor: "#3E57DA",
            fillType: "Solid Color",
          });
        } else {
          this.store.updateShapeProperties({
            fillColor: "transparent",
            fillType: "No Fill",
          });
        }
      },
    },
    shapeShadowEnabled: {
      get() {
        return this.shapeProps?.hasShadow || false;
      },
      set(value) {
        // When shadow is enabled, set default shadow values for better visibility
        if (value === true) {

          this.store.updateShapeProperties({
            hasShadow: true,
            shadowOffsetX: 5,
            shadowOffsetY: 5,
            shadowBlur: 0,
            shadowColor: "#000000"
          });
          return;
        }
        this.store.updateShapeProperties({ hasShadow: value });
      }
    },
    shapeShadowOffsetX: {
      get() {
        return this.shapeProps?.shadowOffsetX || 0;
      },
      set(value) {
        this.store.updateShapeProperties({ shadowOffsetX: value });
      }
    },
    shapeShadowOffsetY: {
      get() {
        return this.shapeProps?.shadowOffsetY || 0;
      },
      set(value) {
        this.store.updateShapeProperties({ shadowOffsetY: value });
      }
    },
    shapeShadowBlur: {
      get() {
        return this.shapeProps?.shadowBlur || 0;
      },
      set(value) {
        this.store.updateShapeProperties({ shadowBlur: value });
      }
    },
    shapeShadowColor: {
      get() {
        return this.shapeProps?.shadowColor || "#000000";
      },
      set(value) {
        if (value && typeof value === 'object' && value.color) {
          this.store.updateShapeProperties({
            shadowColor: value.color,
            finalChange: value.finalChange
          });
        } else {
          this.store.updateShapeProperties({ shadowColor: value });
        }
      }
    },
  },
  watch: {
    // Element type watcher
    "editorStore.selectedElement": function (newStatus) {
      this.selectedElementType = newStatus.type;
    },

    // Shape-related watchers
    borderThickness(thickness) {
      this.updateShape({ strokeWidth: thickness });
    },

    fillBackground(color) {
      this.updateShape({ fill: color });
    },

    fillBackgroundBorder(color) {
      this.updateShape({ stroke: color });
    },

    shapeOpacity(value) {
      this.updateShape({ opacity: value / 100 });
    },

    roundedBorder(value) {
      this.updateShape({
        rx: value,
        ry: value,
      });
    },

    // Text-related watchers
    backgroundPicked(color) {
      this.updateText({ color });
    },

    selectedLetterSpacing(size) {
      this.updateText({ letterSpacing: size });
    },

    selectedLineHeight(size) {
      this.updateText({ lineHeight: size });
    },

    selectedFont(font) {
      this.updateText({ fontFamily: font });
    },
  },

  methods: {
    // ... existing methods ...

    handleRotateClockwise() {
      if (!this.store.selectedElement?.id) return;
      const currentRotation = this.editorStore.selectedElement.rotation || 0;
      this.store.updateGraphicTransform(this.store.selectedElement.id, {
        rotation: currentRotation + 90,
      });
    },

    handleRotateCounterclockwise() {
      if (!this.store.selectedElement?.id) return;
      const currentRotation = this.editorStore.selectedElement.rotation || 0;
      this.store.updateGraphicTransform(this.store.selectedElement.id, {
        rotation: currentRotation - 90,
      });
    },

    handleFlipHorizontal() {
      if (!this.store.selectedElement?.id) return;
      const currentScaleX = this.editorStore.selectedElement.scaleX || 1;
      this.store.updateGraphicTransform(this.store.selectedElement.id, {
        scaleX: currentScaleX * -1,
      });
    },

    handleFlipVertical() {
      if (!this.store.selectedElement?.id) return;
      const currentScaleY = this.editorStore.selectedElement.scaleY || 1;
      this.store.updateGraphicTransform(this.store.selectedElement.id, {
        scaleY: currentScaleY * -1,
      });
    },
    // In your selectTextType method:
    bringElementToFront() {
      if (this.editorStore.selectedElement?.id) {
        this.editorStore.bringToFront(this.editorStore.selectedElement.id);
      }
    },
    bringElementToBack() {
      if (this.editorStore.selectedElement?.id) {
        this.editorStore.bringToBack(this.editorStore.selectedElement.id);
      }
    },
    updateShape(properties) {
      if (!this.editorStore.selectedElement?.id) return;
      this.editorStore.updateShapeElement(
        this.editorStore.selectedElement.id,
        properties
      );
    },

    updateText(properties) {
      console.log("SideEditor - updating text:", properties);
      if (!this.editorStore.selectedElement?.id) return;
      this.editorStore.updateElement(
        this.editorStore.selectedElement.id,
        properties
      );
    },
    selectTextType(textType) {
      if (textType === "bold") {
        this.editorStore.updateElement(this.editorStore.selectedElement.id, {
          fontWeight: this.selectedTextTypes.includes("bold") ? "normal" : "bold",
        });
      } else if (textType === "italic") {
        this.editorStore.updateElement(this.editorStore.selectedElement.id, {
          fontStyle: this.selectedTextTypes.includes("italic") ? "normal" : "italic",
        });
      }
      // Handle multiple text decorations
      else if (textType === "underline" || textType === "strikethrough") {
        // Get current decorations
        const currentDecoration =
          this.editorStore.selectedElement.textDecoration || "none";
        let newDecoration;

        // Convert decoration string to array
        const decorations =
          currentDecoration === "none" ? [] : currentDecoration.split(" ");

        if (textType === "underline") {
          if (decorations.includes("underline")) {
            // Remove underline if it exists
            decorations.splice(decorations.indexOf("underline"), 1);
          } else {
            // Add underline
            decorations.push("underline");
          }
        }

        if (textType === "strikethrough") {
          if (decorations.includes("line-through")) {
            // Remove line-through if it exists
            decorations.splice(decorations.indexOf("line-through"), 1);
          } else {
            // Add line-through
            decorations.push("line-through");
          }
        }

        // Convert back to string or set to 'none' if empty
        newDecoration = decorations.length > 0 ? decorations.join(" ") : "none";

        this.editorStore.updateElement(this.editorStore.selectedElement.id, {
          textDecoration: newDecoration,
        });
      }

      // Toggle the selected state in the array
      const index = this.selectedTextTypes.indexOf(textType);
      if (index === -1) {
        // Add to array if not present
        this.selectedTextTypes.push(textType);
      } else {
        // Remove from array if already present
        this.selectedTextTypes.splice(index, 1);
      }
    },
    selectTextAlign(textAlign) {
      this.selectedTextAlign = textAlign;
      this.editorStore.updateElement(this.editorStore.selectedElement.id, {
        textAlign: textAlign,
      });
    },
    incrementOffsetX() {
      if (this.shadowEnabled) {
        this.offsetX = parseFloat((this.offsetX + 0.1).toFixed(1));
      }
    },
    incrementOffsetY() {
      if (this.shadowEnabled) {
        this.offsetY = parseFloat((this.offsetY + 0.1).toFixed(1));
      }
    },
    decrementOffsetX() {
      if (this.offsetX > 0 && this.shadowEnabled) {
        this.offsetX = parseFloat((this.offsetX - 0.1).toFixed(1));
      }
    },
    decrementOffsetY() {
      if (this.offsetY > 0 && this.shadowEnabled) {
        this.offsetY = parseFloat((this.offsetY - 0.1).toFixed(1));
      }
    },
    incrementBlur() {
      if (this.shadowEnabled) {
        this.blur = parseFloat((this.blur + 0.1).toFixed(1));
      }
    },
    decrementBlur() {
      if (this.blur > 0 && this.shadowEnabled) {
        this.blur = parseFloat((this.blur - 0.1).toFixed(1));
      }
    },
    incrementBorderThickness() {
      this.borderThickness = parseFloat(
        (this.borderThickness + 0.1).toFixed(1)
      );
    },
    decrementBorderThickness() {
      if (this.borderThickness > 0) {
        this.borderThickness = parseFloat(
          (this.borderThickness - 0.1).toFixed(1)
        );
      }
    },
    validateInputBorderThickness(event) {
      const value = parseFloat(event.target.value);
      if (value < 0) {
        this.borderThickness = 0;
      } else {
        this.borderThickness = parseFloat(value.toFixed(1));
      }
    },

    incrementRoundedBorder() {
      this.roundedBorder = parseFloat((this.roundedBorder + 0.1).toFixed(1));
    },
    decrementRoundedBorder() {
      if (this.roundedBorder > 0) {
        this.roundedBorder = parseFloat((this.roundedBorder - 0.1).toFixed(1));
      }
    },
    validateInputRoundedBorder(event) {
      const value = parseFloat(event.target.value);
      if (value < 0) {
        this.roundedBorder = 0;
      } else {
        this.roundedBorder = parseFloat(value.toFixed(1));
      }
    },
    validateInputOffsetX(event) {
      const value = parseFloat(event.target.value);
      if (value < 0) {
        this.offsetX = 0;
      } else {
        this.offsetX = parseFloat(value.toFixed(1));
      }
    },
    validateInputOffsetY(event) {
      const value = parseFloat(event.target.value);
      if (value < 0) {
        this.offsetY = 0;
      } else {
        this.offsetY = parseFloat(value.toFixed(1));
      }
    },
    validateInputBlur(event) {
      const value = parseFloat(event.target.value);
      if (value < 0) {
        this.blur = 0;
      } else {
        this.blur = parseFloat(value.toFixed(1));
      }
    },
    incrementShapeShadowOffsetX() {
      if (this.shapeShadowEnabled) {
        this.shapeShadowOffsetX = parseFloat((this.shapeShadowOffsetX + 1).toFixed(0));
      }
    },
    decrementShapeShadowOffsetX() {
      if (this.shapeShadowEnabled) {
        this.shapeShadowOffsetX = parseFloat((this.shapeShadowOffsetX - 1).toFixed(0));
      }
    },
    incrementShapeShadowOffsetY() {
      if (this.shapeShadowEnabled) {
        this.shapeShadowOffsetY = parseFloat((this.shapeShadowOffsetY + 1).toFixed(0));
      }
    },
    decrementShapeShadowOffsetY() {
      if (this.shapeShadowEnabled) {
        this.shapeShadowOffsetY = parseFloat((this.shapeShadowOffsetY - 1).toFixed(0));
      }
    },
    incrementShapeShadowBlur() {
      if (this.shapeShadowEnabled) {
        this.shapeShadowBlur = parseFloat((this.shapeShadowBlur + 1).toFixed(0));
      }
    },
    decrementShapeShadowBlur() {
      if (this.shapeShadowEnabled && this.shapeShadowBlur > 0) {
        this.shapeShadowBlur = parseFloat((this.shapeShadowBlur - 1).toFixed(0));
      }
    },
    validateShapeShadowOffsetX(event) {
      const value = parseFloat(event.target.value);
      this.shapeShadowOffsetX = parseFloat(value.toFixed(0));
    },
    validateShapeShadowOffsetY(event) {
      const value = parseFloat(event.target.value);
      this.shapeShadowOffsetY = parseFloat(value.toFixed(0));
    },
    validateShapeShadowBlur(event) {
      const value = parseFloat(event.target.value);
      if (value < 0) {
        this.shapeShadowBlur = 0;
      } else {
        this.shapeShadowBlur = parseFloat(value.toFixed(0));
      }
    },
  },
};
</script>

<style scoped>
.dropdown-wrapper {
  margin-top: 1rem;
}
.fontsize-dropdown {
  margin-top: 0;
  width: 120px;
}
.dropdown-trigger div {
  width: 100%;
  padding: 10px;
  background-color: #2b2e400e;
  border: none;
}

.fontsize-dropdown div {
  width: 100%;
  padding: 8px;
  background-color: #2b2e400e;
  border: none;
  height: 100%;
  font-weight: 300;
}
.dropdown {
  width: 100%;
  background-color: red;
}
.color-input-no-border::-webkit-color-swatch-wrapper {
  padding: 0;
}
.color-input-no-border::-webkit-color-swatch {
  border: none;
}
.color-input-no-border::-moz-color-swatch {
  border: none;
}
.lenghtsize-dropdown {
  margin-top: 0;
}
.lenghtsize-dropdown div {
  padding: 0px;
  width: 60px;
  gap: 2px;
  border: none;
  background-color: transparent;
  height: 100%;
  font-weight: 300;
}

.fillshape-dropdown {
  margin-top: 0;
}
.fillshape-dropdown div {
  padding: 0px;
  height: 34px;
  font-weight: 300;
  padding: 8px;
  width: 130px;
}

.bordershape-dropdown {
  margin-top: 0;
}
.bordershape-dropdown div {
  padding: 0px;
  height: 34px;
  font-weight: 300;
  padding: 8px;
  width: 130px;
}

input[type="range"]::-webkit-slider-thumb {
  -webkit-appearance: none;
  @apply w-4 h-4 bg-[#3E57DA] rounded-full cursor-pointer;
}
input[type="range"]::-moz-range-thumb {
  @apply w-4 h-4 bg-[#3E57DA] border-none rounded-full cursor-pointer;
}
/* Hide number input spinners */
input[type="number"]::-webkit-inner-spin-button,
input[type="number"]::-webkit-outer-spin-button {
  -webkit-appearance: none;
  margin: 0;
}
input[type="number"] {
  -moz-appearance: textfield;
}
</style>