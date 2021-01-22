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
    problems: [
      {
        id: 1,
        title: "A+B problem",
        content: "输入两个数a和b，输出他们的和",
      },
      {
        id: 2,
        title: "A*B problem",
        content: "输入两个数a和b，输出他们的乘积",
      },
    ],
  }),
};
</script>

<style scoped>
a {
  text-decoration: none;
}
</style>
