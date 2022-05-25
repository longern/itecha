<template>
  <!-- eslint-disable vue/no-v-html -->
  <div
    ref="mc"
    class="markdown-body"
  />
  <!-- Class markdown-body is required by github-markdown-css -->
</template>

<script>
import { mavonEditor } from "mavon-editor";
import { markdownItFancyListPlugin } from "markdown-it-fancy-lists";

const md = mavonEditor.getMarkdownIt();
md.use(markdownItFancyListPlugin);

export default {
  name: "Markdown",

  props: { source: { type: String, default: "" } },

  watch: {
    source() {
      this.$refs.mc.innerHTML = md.render(this.source || "");

      // Render ordered list with type=A as radio button
      for (const ol of this.$refs.mc.querySelectorAll("ol[type=A]")) {
        ol.setAttribute("value", 0);

        ol.addEventListener("input", function (event) {
          if (+this.getAttribute("value"))
            this.children[this.getAttribute("value") - 1].classList.remove(
              "checked"
            );
          this.setAttribute("value", event.detail);
          this.children[event.detail - 1].classList.add("checked");
        });

        for (let liIndex = 0; liIndex < ol.children.length; liIndex++) {
          const li = ol.children[liIndex];
          li.addEventListener("click", function () {
            this.parentElement.dispatchEvent(
              new CustomEvent("input", { detail: +liIndex + 1 })
            );
          });
        }
      }
    },
  },
};
</script>

<style>
.markdown-body ol[type=A] > li {
  border: 1px solid transparent;
}

.markdown-body ol[type=A] > li.checked {
  border: 1px solid #4caf50;
}
</style>
