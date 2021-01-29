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
          @click="isDebugPanelVisible ^= true"
          v-text="isDebugPanelVisible ? '隐藏' : '调试'"
        >
        </v-btn>
        <v-btn color="primary" @click="submit">提交</v-btn>
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <v-row>
          <v-col md="4">
            <v-card class="fill-height" :loading="loading">
              <v-container>
                <h1 v-text="problem.title" class="text-center mb-2"></h1>
                <div v-html="renderedContent"></div>
              </v-container>
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
            <v-card class="fill-height">
              <v-container>
                <v-textarea v-model="debugInput" label="输入"></v-textarea>
                <v-btn color="secondary" @click="runPython3Code">运行</v-btn>
                <pre class="mt-4"><code v-text="debugOutput" ></code></pre>
              </v-container>
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
import MarkdownIt from "markdown-it";

const md = new MarkdownIt();

export default {
  name: "Problem",

  data: () => ({
    problem: {},
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
    loading: true,
  }),

  computed: {
    renderedContent() {
      return md.render(this.problem.content);
    },
  },

  methods: {
    async runPython3Code() {
      const pythonExecutorUrl = process.env.VUE_APP_PYTHON3_EXECUTOR;
      const response = await fetch(pythonExecutorUrl, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          source: this.code,
          input: this.debugInput,
        }),
      });
      this.debugOutput = await response.text();
    },

    async submit() {
      await fetch(`${process.env.VUE_APP_API_BASE_URL}submissions`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ problem_id: this.problem.id, code: this.code }),
      });
    },
  },

  async mounted() {
    const problem_response = await fetch(
      `${process.env.VUE_APP_API_BASE_URL}problems/${this.$route.params.id}`,
      { headers: { "Content-Type": "application/json" } }
    );
    this.problem = await problem_response.json();
    this.loading = false;
  },

  components: { codemirror },
};
</script>

<style>
.CodeMirror {
  height: 60vh;
}
</style>
