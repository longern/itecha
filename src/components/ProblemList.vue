<template>
  <v-container>
    <v-row class="align-center">
      <h1 class="ma-8">题目列表</h1>
      <v-spacer></v-spacer>
      <v-btn v-if="isSuperuser" color="primary" to="/problems/create">
        创建题目
      </v-btn>
    </v-row>
    <v-row>
      <v-col>
        <v-card :loading="loading">
          <v-container>
            <v-data-table
              :headers="headers"
              :items="problems"
              hide-default-footer
            >
              <template v-slot:item.title="{ item }">
                <router-link :to="`/problems/${item.id}`" v-text="item.title">
                </router-link>
              </template>
              <template v-slot:item.tags="{ item }">
                <v-chip-group v-if="item.tags">
                  <v-chip
                    v-for="tag in item.tags"
                    :key="tag"
                    v-text="tag"
                  ></v-chip>
                </v-chip-group>
              </template>
              <template v-slot:item.actions="{ item }" v-if="isSuperuser">
                <router-link :to="`/problems/${item.id}/edit`" title="编辑">
                  <v-icon>mdi-pencil</v-icon>
                </router-link>
                <router-link
                  :to="`/submissions?problem_id=${item.id}`"
                  title="提交记录"
                >
                  <v-icon>mdi-clock</v-icon>
                </router-link>
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
  name: "ProblemList",

  props: ["isSuperuser"],

  data: () => ({
    headers: [
      {
        text: "题目名称",
        value: "title",
        sortable: false,
      },
      {
        text: "标签",
        value: "tags",
        sortable: false,
      },
      {
        text: "操作",
        value: "actions",
        sortable: false,
      },
    ],
    loading: true,
    problems: [],
  }),

  async mounted() {
    this.problems = (
      await axios.get(`${process.env.VUE_APP_API_BASE_URL}problems`)
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
