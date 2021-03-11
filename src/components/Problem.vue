<template>
  <v-container>
    <v-row>
      <v-col>
        <v-breadcrumbs :items="breadcrumbsItems" />
      </v-col>
      <v-spacer v-if="!$vuetify.breakpoint.mobile" />
      <v-col
        cols="auto"
        class="pt-8"
      >
        <v-btn
          class="mr-3"
          @click="isDebugPanelVisible ^= true"
          v-text="isDebugPanelVisible ? '隐藏' : '调试'"
        />
        <v-btn
          color="primary"
          @click="submit"
        >
          提交
        </v-btn>
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <v-row>
          <v-col
            cols="12"
            md="5"
          >
            <v-card
              class="problem-card fill-height"
              :loading="loading"
            >
              <v-container class="problem-container">
                <h1
                  class="text-center mb-2"
                  v-text="problem.title"
                />
                <markdown :source="problem.content" />
              </v-container>
            </v-card>
          </v-col>
          <v-col
            cols="12"
            :md="isDebugPanelVisible ? 5 : 7"
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
            v-if="isDebugPanelVisible"
            cols="12"
            md="2"
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

import Markdown from "./Markdown.vue";

export default {
  name: "Problem",

  components: { codemirror, Markdown },

  data: () => ({
    problem: {},
    code: "",
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
    debugInput: "",
    debugOutput: "",
    isDebugPanelVisible: false,
    loading: true,
  }),

  computed: {
    breadcrumbsItems() {
      return [
        {
          text: "首页",
          disabled: false,
          to: "/",
        },
        {
          text: this.problem.title,
          disabled: true,
          to: "/",
        },
      ];
    },
  },

  async mounted() {
    const problem_response = await axios.get(
      `${process.env.VUE_APP_API_BASE_URL}problems/${this.$route.params.id}`
    );
    this.problem = problem_response.data;
    this.code = this.problem.default_code || "";
    this.loading = false;
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

    async submit() {
      if (!this.code) {
        this.$dialog.notify.error("代码不能为空");
        return;
      }

      await axios.post(`${process.env.VUE_APP_API_BASE_URL}submissions`, {
        problem_id: this.problem.id,
        code: this.code,
      });

      this.$dialog.notify.success("提交成功");
    },
  },
};
</script>

<style>
@media (min-width: 960px) {
  .problem-card {
    overflow: hidden;
  }

  .problem-container {
    height: 72vh;
    overflow-y: auto;
  }
}

div.CodeMirror {
  height: 72vh;
}
</style>
