<template>
  <v-container>
    <v-row class="align-center">
      <h1 class="ma-8">提交记录</h1>
      <v-spacer></v-spacer>
      <v-btn color="primary" @click="run">测评</v-btn>
    </v-row>
    <v-row>
      <v-col>
        <v-card :loading="loading">
          <v-container>
            <v-data-table
              :headers="headers"
              :items="submissions"
              disable-sort
              hide-default-footer
            >
              <template v-slot:item.title>
                <router-link
                  :to="`/problems/${problem.id}`"
                  v-text="problem.title"
                >
                </router-link>
              </template>
              <template v-slot:item.creator="{ item }">
                <router-link
                  v-if="item.creator"
                  :to="`/users/${item.creator.id}`"
                  v-text="item.creator.username"
                >
                </router-link>
              </template>
              <template v-slot:item.code="{ item }">
                <v-tooltip bottom>
                  <template v-slot:activator="{ on, attrs }">
                    <v-icon v-bind="attrs" v-on="on">mdi-code-tags</v-icon>
                  </template>
                  <pre v-text="item.code"></pre>
                </v-tooltip>
              </template>
              <template v-slot:item.create_time="{ item }">
                <span
                  v-text="new Date(item.create_time).toLocaleString()"
                ></span>
              </template>
            </v-data-table>
          </v-container>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: "SubmissionList",

  props: ["problem_id"],

  data: () => ({
    headers: [
      {
        text: "题目名称",
        value: "title",
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
        value: "create_time",
      },
    ],
    loading: true,
    problem: {},
    submissions: [],
  }),

  methods: {
    async run() {
      const pythonExecutorUrl = process.env.VUE_APP_PYTHON3_EXECUTOR;

      for (var i = 0; i < this.submissions.length; i++) {
        const submission = this.submissions[i];
        let submission_score = 0;

        const testcase_score = 100 / this.problem.testcases.length;
        for (var j = 0; j < this.problem.testcases.length; j++) {
          const testcase = this.problem.testcases[j];
          const response = await fetch(pythonExecutorUrl, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              source: `${submission.code}\n${this.problem.hidden_code || ""}`,
              input: testcase.input_data,
            }),
          });
          const output = await response.text();
          if (output.trim() == testcase.output_data)
            submission_score += testcase_score;
        }

        this.$set(submission, "score", submission_score);
      }
    },
  },

  async mounted() {
    const submissions = (
      await (
        await fetch(`${process.env.VUE_APP_API_BASE_URL}submissions`)
      ).json()
    ).data;

    this.problem = await (
      await fetch(
        `${process.env.VUE_APP_API_BASE_URL}problems/${this.problem_id}`
      )
    ).json();

    this.submissions = submissions.filter(
      (submission) => submission.problem_id == this.problem_id
    );

    this.loading = false;
  },
};
</script>

<style scoped>
a {
  text-decoration: none;
}
</style>
