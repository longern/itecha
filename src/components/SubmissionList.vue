<template>
  <v-container>
    <v-row>
      <h1 class="ma-8">提交记录</h1>
    </v-row>
    <v-row>
      <v-col>
        <v-card :loading="loading">
          <v-container>
            <v-data-table
              :headers="headers"
              :items="submissions"
              hide-default-footer
            >
              <template v-slot:item.title="{ item }">
                <router-link
                  :to="`/submissions/${item.id}`"
                  v-text="item.title"
                >
                </router-link>
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
  name: "ProblemList",

  data: () => ({
    headers: [
      {
        text: "题目名称",
        value: "title",
        sortable: false,
      },
      {
        text: "提交者",
        value: "creator",
        sortable: false,
      },
      {
        text: "提交IP",
        value: "creator_ip",
      },
      {
        text: "提交时间",
        value: "create_time",
      },
    ],
    loading: true,
    submissions: [],
  }),

  async mounted() {
    this.submissions = (
      await (
        await fetch(`${process.env.VUE_APP_API_BASE_URL}submissions`)
      ).json()
    ).data;
    this.loading = false;
  },
};
</script>

<style scoped>
a {
  text-decoration: none;
}
</style>
