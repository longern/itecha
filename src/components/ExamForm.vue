<template>
  <v-container class="exam-form">
    <v-card :loading="loading">
      <v-container>
        <h2 class="mb-4">
          <span v-if="$route.params.id">编辑：{{ original_title }}</span>
          <span v-else>创建考试</span>
        </h2>
        <v-form>
          <v-text-field
            v-model="exam.title"
            label="标题"
            required
          />
          <v-text-field
            v-model="exam.duration"
            label="考试时间（分钟）"
            required
          />
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

export default {
  name: "ExamForm",

  data: () => ({
    loading: true,
    original_title: "考试",
    exam: { questions: [] },
  }),

  async mounted() {
    if (this.$route.params.id) {
      const exam_response = await axios.get(
        `${process.env.VUE_APP_API_BASE_URL}exams/${this.$route.params.id}`
      );
      this.exam = exam_response.data;
      this.original_title = this.exam.title;
    }
    this.loading = false;
  },

  methods: {
    async save() {
      try {
        await axios({
          method: this.$route.params.id ? "PUT" : "POST",
          url: `${process.env.VUE_APP_API_BASE_URL}exams/${this.exam.id}`,
          data: this.exam,
        });

        this.$dialog.notify.success("保存成功");
      } catch (error) {
        this.$dialog.notify.error(error.response.data.name);
      }
    },
  },
};
</script>
