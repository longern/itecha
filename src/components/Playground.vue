<template>
  <v-container
    class="playground pa-0 fill-height"
    fluid
  >
    <codemirror
      v-if="!showIO"
      ref="cm"
      v-model="code"
      :options="cmOption"
      class="fill-height fill-width"
    />
    <v-container v-else>
      <v-textarea
        v-model="debugInput"
        label="输入"
      />
      <v-btn
        color="primary"
        @click="runPython3Code"
      >
        运行
      </v-btn>
      <pre><code
        v-if="debugOutput !== ''"
        class="d-block mt-4"
        v-text="debugOutput"
      /></pre>
    </v-container>
    <v-footer app>
      <v-btn
        icon
        @click="showIO = !showIO"
      >
        <v-icon>mdi-play</v-icon>
      </v-btn>
      <v-btn
        icon
        @click="undo"
      >
        <v-icon>mdi-undo</v-icon>
      </v-btn>
      <v-btn
        icon
        @click="redo"
      >
        <v-icon>mdi-redo</v-icon>
      </v-btn>
    </v-footer>
  </v-container>
</template>

<script>
import axios from "axios";
import { codemirror } from "vue-codemirror";

export default {
  name: "Playground",

  components: { codemirror },

  data: () => ({
    code: "",
    showIO: false,
    debugInput: "",
    debugOutput: "",
    cmOption: {
      mode: "text/x-python",
      indentUnit: 4,
      lineNumbers: true,
      theme: "idea",
      viewportMargin: Infinity,
      extraKeys: {
        "Shift-Tab": "indentLess",
      },
    },
  }),

  async mounted() {},

  methods: {
    async runPython3Code() {
      const pythonExecutorUrl = process.env.VUE_APP_PYTHON3_EXECUTOR;
      const response = await axios.post(pythonExecutorUrl, {
        source: this.code,
        input: this.debugInput,
      });
      this.debugOutput = response.data;
    },

    undo() {
      this.$refs.cm.codemirror.doc.undo();
    },

    redo() {
      this.$refs.cm.codemirror.doc.redo();
    }
  },
};
</script>

<style>
.vue-codemirror > div.CodeMirror {
  height: 100%;
  width: 100%;
}
</style>
