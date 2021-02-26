<template>
  <v-container class="playground">
    <v-row>
      <v-col>
        <v-row>
          <v-col
            cols="12"
            md="8"
          >
            <v-card class="fill-height">
              <codemirror
                ref="cm"
                v-model="code"
                :options="cmOption"
              />
            </v-card>
          </v-col>
          <v-col
            cols="12"
            md="4"
          >
            <v-card class="fill-height">
              <v-container>
                <v-textarea
                  v-model="debugInput"
                  label="输入"
                />
                <v-btn
                  color="secondary"
                  @click="runPython3Code"
                >
                  运行
                </v-btn>
                <pre class="mt-4"><code v-text="debugOutput" /></pre>
              </v-container>
            </v-card>
          </v-col>
        </v-row>
      </v-col>
    </v-row>
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
  },
};
</script>
