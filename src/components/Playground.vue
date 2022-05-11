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
        to="/"
      >
        <v-icon>mdi-home</v-icon>
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
      <v-btn
        icon
        @click="indentMore"
      >
        <v-icon>mdi-keyboard-tab</v-icon>
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
            @input="uploadImage"
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
      lineWrapping: true,
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

    indentMore() {
      this.$refs.cm.codemirror.execCommand("indentMore");
    },

    async uploadImage() {
      this.isUploadingImage = true;
      try {
        let imageFile = this.$refs.capture.files[0];
        const SIZE_LIMIT = 10 ** 5;
        if (imageFile.size >= SIZE_LIMIT) {
          const imageFileContent = await new Promise(resolve => {
            const reader = new FileReader();
            reader.onload = (e) => resolve(e.target.result);
            reader.readAsDataURL(imageFile);
          });

          const img = await new Promise(resolve => {
            const img = document.createElement("img");
            img.onload = () => resolve(img);
            img.src = imageFileContent;
          });

          const canvas = document.createElement("canvas");
          const resizeRatio = Math.sqrt(SIZE_LIMIT / imageFile.size) * 0.95;
          canvas.width = resizeRatio * img.width;
          canvas.height = resizeRatio * img.height;
          const ctx = canvas.getContext("2d");
          ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
          imageFile = await new Promise(resolve => {
            canvas.toBlob(blob => {
              const resizedFile = new File([blob], "image.png");
              resolve(resizedFile);
            });
          });
        }

        const orcUrl = "https://1945724074264704.cn-hongkong.fc.aliyuncs.com/2016-08-15/proxy/executors.LATEST/tesseract/";
        const response = await axios.post(orcUrl, imageFile);
        let code = response.data;

        let codeLines = code.split("\n");
        for (let i = 1; i < codeLines.length; i++) {
          if (codeLines[i - 1].search(/:$/) >= 0) {
            const numLeadingSpaces = codeLines[i - 1].match(/^ */)[0].length;
            codeLines[i] = " ".repeat(numLeadingSpaces + 4) + codeLines[i];
          }
        }
        code = codeLines.join("\n");

        this.code = code;
      } catch(err) {
        console.log(err);
      }

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
