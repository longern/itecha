<template>
  <v-container>
    <v-card :loading="loading" class="pa-4">
      <h2 class="mb-4">
        <span v-if="$route.params.id">编辑：{{ original_title }}</span>
        <span v-else>创建题目</span>
      </h2>
      <v-form>
        <v-text-field
          v-model="problem.title"
          label="标题"
          required
        ></v-text-field>
        <v-textarea
          label="描述"
          v-model="problem.content"
          required
        ></v-textarea>
        <v-btn color="primary" @click="save" :disabled="loading">保存</v-btn>
      </v-form>
    </v-card>
  </v-container>
</template>

<script>
export default {
  name: "ProblemForm",

  data: () => ({
    loading: true,
    original_title: "A+B problem",
    problem: {},
  }),

  methods: {
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
      this.problem = (await problem_response.json()).data;
    }
    this.loading = false;
  },
};
</script>
