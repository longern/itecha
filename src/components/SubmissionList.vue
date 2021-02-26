<template>
  <v-container>
    <v-row class="align-center">
      <h1 class="ma-8">
        提交记录
      </h1>
      <v-spacer />
      <v-btn
        color="primary"
        @click="run"
      >
        测评
      </v-btn>
    </v-row>
    <v-row>
      <v-col>
        <v-card :loading="loading">
          <v-container>
            <v-data-table
              :headers="headers"
              :items="submissions"
              disable-sort
            >
              <template v-slot:item.problem="{ item }">
                <router-link
                  :to="`/problems/${item.problem.id}`"
                  v-text="item.problem.title"
                />
              </template>
              <template v-slot:item.creator="{ item }">
                <router-link
                  v-if="item.creator"
                  :to="`/users/${item.creator.id}`"
                  v-text="item.creator.username"
                />
                <span
                  v-if="item.creator_ip"
                  class="ml-1"
                  v-text="`(${item.creator_ip})`"
                />
              </template>
              <template v-slot:item.code="{ item }">
                <v-tooltip bottom>
                  <template v-slot:activator="{ on, attrs }">
                    <v-icon
                      v-bind="attrs"
                      v-on="on"
                    >
                      mdi-code-tags
                    </v-icon>
                  </template>
                  <pre v-text="item.code" />
                </v-tooltip>
              </template>
              <template v-slot:item.created="{ item }">
                <span v-text="new Date(item.created).toLocaleString()" />
              </template>
            </v-data-table>
          </v-container>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import axios from "axios";

export default {
  name: "SubmissionList",

  props: ["problem_id"],

  data: () => ({
    headers: [
      {
        text: "题目名称",
        value: "problem",
      },
      {
        text: "提交者",
        value: "creator",
      },
      {
        text: "代码",
        value: "code",
      },
      {
        text: "分数",
        value: "score",
      },
      {
        text: "提交时间",
        value: "created",
      },
    ],
    loading: true,
    submissions: [],
  }),

  async mounted() {
    this.submissions = (
      await axios.get(`${process.env.VUE_APP_API_BASE_URL}submissions`, {
        params: { problem: this.problem_id },
      })
    ).data;

    this.loading = false;
  },

  methods: {
    async run() {
      const pythonExecutorUrl = process.env.VUE_APP_PYTHON3_EXECUTOR;

      for (var i = 0; i < this.submissions.length; i++) {
        const submission = this.submissions[i];
        let submission_score = 0;

        const testcase_score = 100 / submission.problem.testcases.length;
        for (var j = 0; j < submission.problem.testcases.length; j++) {
          const testcase = submission.problem.testcases[j];
          const hidden_code = submission.problem.hidden_code || "";
          const response = await axios.post(
            pythonExecutorUrl,
            {
              source: `${submission.code}\n${hidden_code}`,
              input: testcase.input_data,
            },
            { transformResponse: [] }
          );
          const output = response.data;
          if (output.trim() == testcase.output_data.trim())
            submission_score += testcase_score;
        }

        this.$set(submission, "score", submission_score);
        axios.patch(
          `${process.env.VUE_APP_API_BASE_URL}submissions/${submission.id}`,
          { score: submission_score }
        );
      }
    },
  },
};
</script>

<style scoped>
a {
  text-decoration: none;
}
</style>
