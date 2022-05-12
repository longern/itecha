<template>
  <v-container class="problem-form">
    <v-card :loading="loading">
      <v-container>
        <h2 class="mb-4">
          <span v-if="$route.params.id">编辑：{{ original_title }}</span>
          <span v-else>创建题目</span>
        </h2>
        <v-form>
          <h3 class="mb-4">
            内容
          </h3>
          <v-text-field
            v-model="problem.title"
            label="标题"
            required
          />
          <v-label>描述</v-label>
          <mavon-editor
            v-model="problem.content"
            required
            class="mb-4"
            :external-link="false"
          />
          <v-expansion-panels>
            <v-expansion-panel>
              <v-expansion-panel-header>隐藏代码</v-expansion-panel-header>
              <v-expansion-panel-content>
                <codemirror
                  ref="cm"
                  v-model="problem.hidden_code"
                  :options="cmOption"
                />
              </v-expansion-panel-content>
            </v-expansion-panel>
          </v-expansion-panels>
          <editable-tags
            v-model="problem.tags"
            label="标签"
          />
          <h3 class="my-4">
            测评
          </h3>
          <v-btn
            icon
            @click="appendTestCase"
          >
            <v-icon>mdi-plus</v-icon>
          </v-btn>
          <v-row
            v-for="(testcase, index) in problem.testcases"
            :key="index"
          >
            <v-col>
              <v-textarea
                v-model="testcase.input_data"
                label="输入"
                required
              />
            </v-col>
            <v-col>
              <v-textarea
                v-model="testcase.output_data"
                label="输出"
                required
              />
            </v-col>
            <v-col md="1">
              <v-btn
                icon
                @click="deleteTestCase(index)"
              >
                <v-icon>mdi-delete</v-icon>
              </v-btn>
            </v-col>
          </v-row>
          <v-row>
            <v-col>
              <v-btn
                color="primary"
                :disabled="loading"
                @click="save"
              >
                保存
              </v-btn>
            </v-col>
          </v-row>
        </v-form>
      </v-container>
    </v-card>
  </v-container>
</template>

<script>
import axios from "axios";
import { codemirror } from "vue-codemirror";

import EditableTags from "./EditableTags.vue";

export default {
  name: "ProblemForm",

  components: { codemirror, EditableTags },

  data: () => ({
    loading: true,
    original_title: "题目",
    problem: { testcases: [], hidden_code: "", tags: [] },
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

  async mounted() {
    if (this.$route.params.id) {
      const problem_response = await axios.get(
        `${process.env.VUE_APP_API_BASE_URL}problems/${this.$route.params.id}`
      );
      this.problem = problem_response.data;
      this.original_title = this.problem.title;
      if (!Array.isArray(this.problem.testcases))
        this.$set(this.problem, "testcases", []);
    }
    this.loading = false;
  },

  methods: {
    appendTestCase() {
      this.problem.testcases.push({ input_data: "", output_data: "" });
    },

    deleteTestCase(index) {
      this.problem.testcases.splice(index, 1);
    },

    async save() {
      let response;
      if (this.$route.params.id) {
        response = await axios.put(
          `${process.env.VUE_APP_API_BASE_URL}problems/${this.problem.id}`,
          this.problem
        );
      } else {
        response = await axios.post(
          `${process.env.VUE_APP_API_BASE_URL}problems`,
          this.problem
        );
      }

      if (response.status <= 299) {
        this.$dialog.notify.success("保存成功", {
          position: "top-right",
          timeout: 5000,
        });
      } else {
        this.$dialog.notify.error(response.data.name, {
          position: "top-right",
          timeout: 5000,
        });
      }
    },
  },
};
</script>

<style>
.problem-form .v-textarea {
  font-family: Consolas, "Courier New", Courier, monospace;
}
</style>
