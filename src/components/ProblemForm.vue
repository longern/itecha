<template>
  <v-container>
    <v-card :loading="loading">
      <v-container>
        <h2 class="mb-4">
          <span v-if="$route.params.id">编辑：{{ original_title }}</span>
          <span v-else>创建题目</span>
        </h2>
        <v-form>
          <h3 class="mb-4">内容</h3>
          <v-text-field
            v-model="problem.title"
            label="标题"
            required
          ></v-text-field>
          <v-label>描述</v-label>
          <mavon-editor
            v-model="problem.content"
            required
            class="mb-4"
          ></mavon-editor>
          <v-expansion-panels>
            <v-expansion-panel>
              <v-expansion-panel-header>默认代码</v-expansion-panel-header>
              <v-expansion-panel-content>
                <codemirror
                  ref="cm"
                  v-model="problem.default_code"
                  :options="cmOption"
                ></codemirror>
              </v-expansion-panel-content>
            </v-expansion-panel>
          </v-expansion-panels>
          <h3 class="my-4">测评</h3>
          <v-btn icon @click="appendTestCase"><v-icon>mdi-plus</v-icon></v-btn>
          <v-row v-for="(testcase, index) in problem.testcases" :key="index">
            <v-col>
              <v-textarea
                label="输入"
                v-model="testcase.input_data"
                required
              ></v-textarea>
            </v-col>
            <v-col>
              <v-textarea
                label="输出"
                v-model="testcase.output_data"
                required
              ></v-textarea>
            </v-col>
            <v-col md="1">
              <v-btn icon @click="deleteTestCase(index)">
                <v-icon>mdi-delete</v-icon>
              </v-btn>
            </v-col>
          </v-row>
          <v-row>
            <v-col>
              <v-btn color="primary" @click="save" :disabled="loading">
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
import { mavonEditor } from "mavon-editor";
import { codemirror } from "vue-codemirror";
import "mavon-editor/dist/css/index.css";

export default {
  name: "ProblemForm",

  data: () => ({
    loading: true,
    original_title: "题目",
    problem: { testcases: [] },
    cmOption: {
      indentUnit: 4,
      lineNumbers: true,
      theme: "idea",
      viewportMargin: Infinity,
      extraKeys: {
        "Shift-Tab": "indentLess",
      },
    },
  }),

  methods: {
    appendTestCase() {
      this.problem.testcases.push({ input_data: "", output_data: "" });
    },

    deleteTestCase(index) {
      this.problem.testcases.splice(index, 1);
    },

    async save() {
      if (this.$route.params.id) {
        await fetch(
          `${process.env.VUE_APP_API_BASE_URL}problems/${this.problem.id}`,
          {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(this.problem),
          }
        );
      } else {
        await fetch(`${process.env.VUE_APP_API_BASE_URL}problems`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(this.problem),
        });
      }
    },
  },

  async mounted() {
    if (this.$route.params.id) {
      const problem_response = await fetch(
        `${process.env.VUE_APP_API_BASE_URL}problems/${this.$route.params.id}`,
        {
          method: "GET",
          headers: { "Content-Type": "application/json" },
        }
      );
      this.problem = await problem_response.json();
      this.original_title = this.problem.title;
    }
    this.loading = false;
  },

  components: { mavonEditor, codemirror },
};
</script>
