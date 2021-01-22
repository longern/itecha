<template>
  <v-container>
    <v-breadcrumbs :items="breadcrumbsItems"></v-breadcrumbs>
    <v-row
      v-for="problem in problems"
      :key="problem.id"
    >
      <v-col>
        <v-card class="pa-4">
          <router-link
            :to="`/problems/${problem.id}`"
            v-text="problem.title"
          >
          </router-link>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: "ProblemList",

  data: () => ({
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
