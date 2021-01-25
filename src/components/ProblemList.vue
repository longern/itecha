<template>
  <v-container>
    <v-row>
      <h1 class="ma-8">题目列表</h1>
    </v-row>
    <v-row>
      <v-col>
        <v-card class="pa-4">
          <v-data-table
            :headers="headers"
            :items="problems"
            hide-default-footer
          >
            <template v-slot:item.title="{ item }">
              <router-link :to="`/problems/${item.id}`" v-text="item.title">
              </router-link>
            </template>
          </v-data-table>
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
    ],
    problems: [],
  }),

  async mounted() {
    this.problems = (
      await (await fetch(`${process.env.VUE_APP_API_BASE_URL}problems`)).json()
    ).data;
  },
};
</script>

<style scoped>
a {
  text-decoration: none;
}
</style>
