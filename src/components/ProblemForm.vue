<template>
  <v-container>
    <v-card :loading="loading" class="pa-4">
      <h2 class="mb-4">编辑：{{ original_title }}</h2>
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
    problem: {
      id: 1,
      title: "A+B problem",
      content: "输入两个数a和b，输出他们的和",
    },
  }),

  methods: {
    async save() {
      await fetch(
        `${process.env.VUE_APP_API_BASE_URL}problems/${this.problem.id}`,
        {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(this.problem),
        }
      );
    },
  },

  async mounted() {
    this.loading = false;
  },
};
</script>
