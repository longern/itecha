<template>
  <mobile-container
    :loading="loading"
    fluid
  >
    <mobile-app-bar
      v-if="$vuetify.breakpoint.mobile"
      :title="verboseTitle"
    >
      <template v-slot:back>
        <v-btn
          v-if="$vuetify.breakpoint.mobile && displayEditor"
          icon
          @click="displayEditor = false"
        >
          <v-icon>mdi-chevron-down</v-icon>
        </v-btn>
        <v-btn
          v-else
          icon
          to="/"
        >
          <v-icon>mdi-chevron-left</v-icon>
        </v-btn>
      </template>
    </mobile-app-bar>
    <v-row class="flex-column ma-0 fill-height">
      <v-col
        class="grow pa-0"
        style="height: 0"
      >
        <v-container
          fluid
          class="fill-height py-0"
        >
          <v-row
            class="fill-height"
            style="overflow: auto"
          >
            <v-col
              v-show="!$vuetify.breakpoint.mobile || !displayEditor"
              cols="12"
              md="5"
              class="fill-height overflow-y-auto"
            >
              <h4
                v-if="!$vuetify.breakpoint.mobile"
                class="text-center mb-2"
                v-text="verboseTitle"
              />
              <markdown
                ref="problemText"
                :source="problem.content"
              />
              <v-btn
                v-show="$vuetify.breakpoint.mobile"
                ref="displayEditorButton"
                class="my-3"
                color="primary"
                @click="toggleDisplayEditor"
              >
                打开代码编辑器
              </v-btn>
            </v-col>
            <v-col
              v-show="!$vuetify.breakpoint.mobile || displayEditor"
              cols="12"
              md="7"
              class="fill-height pa-0"
            >
              <codemirror
                ref="cm"
                v-model="code"
                :options="cmOption"
                class="fill-height"
              />
            </v-col>
          </v-row>
        </v-container>
      </v-col>

      <v-col
        md="auto"
        class="shrink pa-0"
      >
        <v-card
          outlined
          tile
          class="pa-3"
        >
          <v-row>
            <v-spacer />
            <v-col cols="auto">
              <io-dialog
                ref="ioDialog"
                v-model="displayDebugPanel"
                @run="runPython3Code"
              >
                <v-btn
                  class="mr-3"
                  @click="displayDebugPanel = true"
                >
                  调试
                </v-btn>
              </io-dialog>
              <v-btn
                color="primary"
                :disabled="!user.username"
                :loading="submitLoading"
                @click="submit"
              >
                提交
              </v-btn>
            </v-col>
          </v-row>
        </v-card>
      </v-col>
    </v-row>
  </mobile-container>
</template>

<script>
import axios from "axios";
import { codemirror } from "vue-codemirror";

import IoDialog from "./IoDialog.vue";
import Markdown from "./Markdown.vue";
import MobileAppBar from "./MobileAppBar.vue";
import MobileContainer from "./MobileContainer.vue";

export default {
  name: "Problem",

  components: { codemirror, IoDialog, Markdown, MobileAppBar, MobileContainer },

  props: { user: { type: Object, default: () => {} } },

  data: () => ({
    problem: {},
    code: "",
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
    displayEditor: false,
    displayDebugPanel: false,
    loading: true,
    submitLoading: false,
  }),

  computed: {
    verboseTitle() {
      return (this.problem.title || "").replace(/.*\//, "");
    },
  },

  async created() {
    const problem_response = await axios.get(
      `${process.env.VUE_APP_API_BASE_URL}problems/${this.$route.params.id}`
    );
    this.problem = problem_response.data;

    await this.$nextTick();
    const problemTextElem = this.$refs.problemText.$el;
    for (const node of problemTextElem.querySelectorAll("code")) {
      if (node.innerText.match(/___\d+___/)) {
        this.code = node.innerText;
        await this.$nextTick();

        // Hide omitted code
        const patt = /[ \t]*#region hidden\n[\S\s]*?\n#endregion/g;
        const doc = this.$refs.cm.codemirror.doc;
        for (;;) {
          const match = patt.exec(this.code);
          if (match === null) break;
          const elem = document.createElement("span");
          elem.className = "cm-comment";
          elem.innerText = "# Omitted";
          doc.markText(
            doc.posFromIndex(match.index),
            doc.posFromIndex(patt.lastIndex),
            { replacedWith: elem }
          );
        }

        // Move display editor button
        if (this.$vuetify.breakpoint.mobile) {
          node
            .closest("pre")
            .insertAdjacentElement(
              "beforebegin",
              this.$refs.displayEditorButton.$el
            );
        }
        node.closest("pre").remove();
        break;
      }
    }

    const inputNode = problemTextElem.querySelector("code.lang-input");
    if (inputNode) {
      this.$refs.ioDialog.input = inputNode.innerText;
    }

    this.loading = false;
  },

  methods: {
    async runPython3Code(input) {
      const pythonExecutorUrl = process.env.VUE_APP_PYTHON3_EXECUTOR;
      const response = await axios.post(pythonExecutorUrl, {
        source: this.code,
        input: input,
      });
      this.$refs.ioDialog.receiveOutput(response.data);
    },

    async toggleDisplayEditor() {
      this.displayEditor = !this.displayEditor;
      if (this.displayEditor) {
        await this.$nextTick();
        this.$refs.cm.codemirror.refresh();
      }
    },

    async submit() {
      if (!this.code) {
        this.$dialog.notify.error("代码不能为空");
        return;
      }

      this.submitLoading = true;
      const response = await axios.post(
        `${process.env.VUE_APP_API_BASE_URL}submissions`,
        {
          problem_id: this.problem.id,
          code: this.code,
        }
      );
      this.submitLoading = false;

      const messageType = response.data.score === 100 ? "success" : "warning";
      this.$dialog.notify[messageType](
        `提交成功，得分：${response.data.score}`
      );

      const msal_token_match = document.cookie.match(
        /(^| )msal_access_token=([^;]+)/
      );
      if (msal_token_match && response.data.score === 100) {
        const msal_token = msal_token_match[2];
        await axios.put(
          `https://graph.microsoft.com/v1.0/me/drive/special/approot:/${this.problem.id}.py:/content`,
          this.code,
          {
            headers: { Authorization: `Bearer ${msal_token}` },
            withCredentials: false,
          }
        );
      }
    },
  },
};
</script>

<style>
@media (min-width: 960px) {
  .problem-card {
    overflow: hidden;
  }
}

div.CodeMirror {
  height: 100%;
  overflow: hidden;
}
</style>
