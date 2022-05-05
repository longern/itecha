<template>
  <v-container
    class="playground pa-0 fill-height"
    fluid
  >
    <codemirror
      ref="cm"
      v-model="code"
      :options="cmOption"
      class="fill-height fill-width"
    />
    <v-card
      v-if="showIO"
      class="io-card"
      outlined
    >
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
    </v-card>
    <v-footer app>
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
      <v-spacer />
      <v-btn
        icon
        :loading="isUploadingImage"
        @click="
          () => {
            $refs.capture.click();
          }
        "
      >
        <form ref="captureForm">
          <input
            ref="capture"
            type="file"
            accept="image/*"
            capture
            hidden
            @change="uploadImage"
          >
        </form>
        <v-icon>mdi-camera</v-icon>
      </v-btn>
      <v-btn
        fab
        small
        color="primary"
        class="ml-2"
        @click="showIO = !showIO"
      >
        <v-icon>mdi-play</v-icon>
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
    isUploadingImage: false,
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

  watch: {
    code(newCode) {
      localStorage.playgroundCode = newCode;
    },
  },

  async mounted() {
    if (localStorage.playgroundCode) {
      this.code = localStorage.playgroundCode;
    }
  },

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
    },

    async uploadImage() {
      this.isUploadingImage = true;
      const orcUrl = "https://1945724074264704.cn-hongkong.fc.aliyuncs.com/2016-08-15/proxy/executors.LATEST/tesseract/";
      const response = await axios.post(orcUrl, this.$refs.capture.files[0]);
      this.code = response.data;
      this.isUploadingImage = false;
    },
  },
};
</script>

<style>
.playground > .vue-codemirror > div.CodeMirror {
  height: 100%;
  width: 100%;
}

.io-card {
  position: absolute;
  bottom: 0;
  z-index: 5;
  width: 100%;
  padding: 16px;
}
</style>
