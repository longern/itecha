<template>
  <v-container>
    <v-row>
      <v-col>
        <v-breadcrumbs :items="breadcrumbsItems"></v-breadcrumbs>
      </v-col>
      <v-spacer></v-spacer>
      <v-col md="auto" class="pt-8">
        <v-btn
          class="mr-3"
          color="secondary"
          @click="isDebugPanelVisible ^= true"
          v-text="isDebugPanelVisible ? '隐藏' : '调试'"
        >
        </v-btn>
        <v-btn color="primary" @click="runPython3Code">提交</v-btn>
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <v-row>
          <v-col md="4">
            <v-card class="pa-4 fill-height">
              <h1 v-text="title" class="text-center mb-2"></h1>
              <div>{{ content }}</div>
            </v-card>
          </v-col>
          <v-col>
            <v-card class="fill-height">
              <codemirror
                ref="cm"
                v-model="code"
                :options="cmOption"
              ></codemirror>
            </v-card>
          </v-col>
          <v-col v-if="isDebugPanelVisible" md="3">
            <v-card class="pa-4 fill-height">
              <v-textarea v-model="debugInput" label="输入"></v-textarea>
              <pre><code v-text="debugOutput" ></code></pre>
            </v-card>
          </v-col>
        </v-row>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { codemirror } from "vue-codemirror";
import "codemirror/mode/python/python";
import "codemirror/lib/codemirror.css";
import "codemirror/theme/idea.css";

export default {
  name: "Problem",

  data: () => ({
    title: "A+B problem",
    content: "输入两个数a和b，输出他们的和",
    code: "",
    cmOption: {
      indentUnit: 4,
      lineNumbers: true,
      theme: "idea",
      viewportMargin: Infinity,
      extraKeys: {
        "Shift-Tab": "indentLess",
      },
    },
    debugInput: "",
    debugOutput: "",
    breadcrumbsItems: [
      {
        text: "首页",
        disabled: false,
        href: "/",
      },
    ],
    isDebugPanelVisible: false,
  }),

  methods: {
    async runPython3Code() {
      const pythonExecutorUrl = process.env.VUE_APP_PYTHON3_EXECUTOR;
      const response = await fetch(pythonExecutorUrl, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: this.code,
      });
      this.debugOutput = await response.text();
    },

    async submit() {},
  },

  components: { codemirror },
};
</script>

<style>
.CodeMirror {
  height: 60vh;
}

.CodeMirror-gutters {
  background: none;
}
</style>
