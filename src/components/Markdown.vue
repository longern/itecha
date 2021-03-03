<template>
  <!-- eslint-disable vue/no-v-html -->
  <div
    class="markdown-body"
    v-html="renderedContent"
  />
</template>

<script>
import { mavonEditor } from "mavon-editor";

const md = mavonEditor.getMarkdownIt();

export default {
  name: "Markdown",

  props: { source: { type: String, default: "" } },

  computed: {
    renderedContent() {
      return md.render(this.source || "");
    }
  }
};
</script>
