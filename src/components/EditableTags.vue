<template>
  <v-input :label="label">
    <v-chip-group class="ml-4">
      <v-chip
        v-for="tag in value"
        :key="tag"
        close
        @click:close="removeTag(tag)"
      >
        <span v-text="tag" />
      </v-chip>
      <v-chip @click="activateEditor">
        <input
          v-if="newTagEditing"
          ref="editor"
          v-model.trim="newTag"
          @blur="addTag"
          @keydown.enter="addTag"
        >
        <v-icon v-else>
          mdi-plus
        </v-icon>
      </v-chip>
    </v-chip-group>
  </v-input>
</template>

<script>
export default {
  name: "EditableTags",

  props: {
    value: { type: Array, default: () => [] },
    label: { type: String, default: "" }
  },

  data: () => ({
    newTag: "",
    newTagEditing: false
  }),

  created() {
    if (!Array.isArray(this.value)) {
      this.$emit("input", []);
    }
  },

  methods: {
    async activateEditor() {
      this.newTagEditing = true;
      await this.$nextTick(); // Wait for creating editor
      this.$refs.editor.focus();
    },

    addTag() {
      if (this.newTag && this.value.indexOf(this.newTag) < 0)
        this.$emit("input", this.value.concat([this.newTag]));
      this.newTag = "";
      this.newTagEditing = false;
    },

    removeTag(tag) {
      this.$emit(
        "input",
        this.value.filter(t => t != tag)
      );
    }
  }
};
</script>
