<template>
  <div class="cover-letters-container">
    <div class="visual-view">
      <div class="template-wrapper">
        <div class="template" :style="{ backgroundColor: backgroundColor }">
          <div class="title-container">
            <EditableTitle
              v-model="localMainTitle"
              @input="updateMainTitle"
              placeholder="Enter main title"
            />
          </div>

          <div class="letter-types">
            <div
              v-for="(letter, index) in modifiedContent"
              :key="index"
              class="letter-type"
              :style="{ backgroundColor: letter.color }"
            >
              <div class="number-wrapper">
                <div class="number" contenteditable="">
                  {{ index + 1 }}
                </div>
              </div>
              <div class="content">
                <EditableSubTitle
                  v-model="letter.title"
                  @input="updateTitle($event, index)"
                  placeholder="Enter main title"
                ></EditableSubTitle>
                <TextEditor
                  v-model="letter.content"
                  @input="updateContent($event, index)"
                />
              </div>
            </div>
            <Signature></Signature>
          </div>
        </div>
        <div class="text-editor">
          <div class="editor-section">
            <label>Main Title:</label>
            <TextEditor
              :indirect-edit="true"
              v-model="localMainTitle"
              @input="updateMainTitle"
              placeholder="Enter main title"
            />
          </div>
          <div
            v-for="(letter, index) in localContent"
            :key="index"
            class="editor-section"
          >
            <label>Title {{ index + 1 }}:</label>
            <TextEditor
              :indirect-edit="true"
              v-model="letter.title"
              @input="updateTitle($event, index)"
            />

            <label>Paragraph {{ index + 1 }}:</label>
            <TextEditor
              :indirect-edit="true"
              v-model="letter.content"
              @input="updateContent($event, index)"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    content: {
      type: Array,
      required: false,
      validator: function (value) {
        return value.every(
          (item) =>
            item.hasOwnProperty("title") && item.hasOwnProperty("content")
        );
      },
    },
    mainTitle: {
      type: String,
      required: true,
      default: "title",
    },
  },
  data() {
    return {
      backgroundColor: "#ffffff",
      currentColor: "#ffffff",
      colorsList: [
        "#FFB3BA",
        "#FFDFBA",
        "#BAFFC9",
        "#BAE1FF",
        "#FFD1DC",
        "#E6E6FA",
        "#C1FFC1",
      ],
      localContent: [],
      localMainTitle: this.mainTitle,
      isDropdownVisible: false,
    };
  },
  computed: {
    modifiedContent() {
      return this.localContent.map((letterType, index) => ({
        ...letterType,
        color: this.colorsList[index % this.colorsList.length],
        index: index + 1,
      }));
    },
  },
  methods: {
    updateMainTitle(newValue) {
      this.localMainTitle = newValue;
      this.$emit("update:mainTitle", this.localMainTitle);
    },
    handleColorChange(newColor) {
      this.currentColor = newColor;
      // Do something with the new color, e.g., change background
      document.body.style.backgroundColor = newColor;
    },

    showDropdown() {
      this.isDropdownVisible = true;
      document.addEventListener("click", this.hideDropdown);
    },
    hideDropdown(event) {
      if (!this.$refs.mainTitleElement.contains(event.target)) {
        this.isDropdownVisible = false;
        document.removeEventListener("click", this.hideDropdown);
      }
    },
    applyFormatting(format) {
      document.execCommand(format, false, null);
      this.$refs.mainTitleElement.focus();
      this.updateMainTitleDirect({ target: this.$refs.mainTitleElement });
    },
    updateTitle(event, index) {
      if (!event.target) {
        this.localContent[index].title = event;
      } else {
        this.localContent[index].title =
          event.target.value || event.target.textContent;
      }
      this.$emit("update:title", this.localContent);
    },
    updateContent(event, index) {
      if (!event.target) {
        this.localContent[index].content = event;
      } else {
        this.localContent[index].content =
          event.target.value || event.target.textContent;
      }

      this.$emit("update:content", this.localContent);
    },
    updateBackgroundColor(color) {
      this.backgroundColor = color;
    },
  },
  created() {
    this.localContent = JSON.parse(JSON.stringify(this.content));
  },
  beforeUnmount() {
    document.removeEventListener("click", this.hideDropdown);
  },
};
</script>

<style scoped>
.cover-letters-container {
  display: flex;
  font-family: Arial, sans-serif;
  margin: 0 auto;
  height: 100%;
  flex: 1;
}

.visual-view {
  flex: 1;
  display: flex;
  justify-content: center;
  width: 100%;
  margin-bottom: 50px;
}

.template {
  width: 600px;
  margin-top: 30px;
  padding: 2rem;
  background-color: white;
  height: fit-content;
}

.template-wrapper {
  display: flex;
  justify-content: center;
  gap: 10px;
}

.text-editor {
  margin-left: auto;
  border: 1px solid #ccc;
  background-color: white;
  padding: 10px;
  width: 300px;
  border-radius: 4px;
  margin-top: 60px;
}

.editor-section {
  margin-bottom: 5px;
}

.editor-section label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
  font-size: var(--font-size-smaller);
}

.editor-section textarea {
  width: 100%;
  padding: 5px;
  resize: vertical;
  font-size: var(--font-size-smaller);
  border: 1px solid #ccc;
  background-color: #f8f8f8;
  border-radius: 4px;
}
.editor-section input {
  width: 100%;
  padding: 5px;
  resize: vertical;
  font-size: var(--font-size-smaller);
  border: 1px solid #ccc;
  background-color: #f8f8f8;
  border-radius: 4px;
}

.title {
  font-size: 24px;
  text-align: center;
  margin-bottom: 5px;
  color: #333;
}

.letter-types {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.letter-type {
  display: flex;
  align-items: center;
  padding: 15px;
  border-radius: 5px;
  gap: 15px;
}

.number {
  font-size: 24px;
  font-weight: bold;
  color: #fff;
  background-color: rgba(0, 0, 0, 0.1);
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
}

.content {
  flex-grow: 1;
}

.content h3 {
  margin: 0 0 5px 0;
  font-size: 18px;
}

.content p {
  margin: 0;
  font-size: 14px;
}

.icon {
  width: 40px;
  height: 40px;
  margin-left: 15px;
}

.icon svg {
  width: 100%;
  height: 100%;
}

.title-container {
  margin-bottom: 10px;
  padding: 1rem;
}
</style>