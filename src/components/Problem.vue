<template>
  <v-container>
    <v-breadcrumbs :items="breadcrumbsItems"></v-breadcrumbs>
    <v-row>
      <v-col>
        <v-card class="main-card mb-4">
          <v-row no-gutters>
            <v-col md="4" class="pa-4">
              <h1 v-text="title"></h1>
              <div>{{ content }}</div>
            </v-col>
            <v-col md="8">
              <codemirror
                ref="cm"
                v-model="code"
                :options="cmOption"
              ></codemirror>
            </v-col>
          </v-row>
        </v-card>
      </v-col>
    </v-row>
    <v-row>
      <v-spacer></v-spacer>
      <v-btn @click="runPython3Code">运行 Python3 代码</v-btn>
    </v-row>
  </v-container>
</template>

<script>
import { codemirror } from "vue-codemirror";
import "codemirror/mode/python/python";
import "codemirror/lib/codemirror.css";
import "codemirror/theme/idea.css";

export default {
  name: "Editor",

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
    breadcrumbsItems: [
      {
        text: "首页",
        disabled: false,
        href: "/",
      },
    ],
  }),

  methods: {
    async runPython3Code() {
      const pythonExecutorUrl = process.env.VUE_APP_PYTHON3_EXECUTOR;
      const response = await fetch(pythonExecutorUrl, {
        method: "POST",
        body: this.code,
      });
      const output = await response.text();
      console.log(output);
    },
  },

  components: { codemirror },
};
</script>

<style>
.CodeMirror {
  height: 60vh;
}
</style>