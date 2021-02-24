<template>
  <v-container>
    <v-row class="align-center">
      <h1 class="ma-8">比赛列表</h1>
      <v-spacer></v-spacer>
      <v-btn v-if="isSuperuser" color="primary" to="/contests/create">
        创建比赛
      </v-btn>
    </v-row>
    <v-row>
      <v-col>
        <v-card :loading="loading">
          <v-container>
            <v-data-table :headers="headers" :items="contests">
              <template v-slot:item.name="{ item }">
                <router-link :to="`/contests/${item.id}`" v-text="item.name">
                </router-link>
              </template>
              <template v-slot:item.time="{ item }">
                <span
                  v-text="new Date(item.start_time).toLocaleString()"
                ></span>
                <span>~</span>
                <span v-text="new Date(item.end_time).toLocaleString()"></span>
              </template>
              <template v-slot:item.actions="{ item }" v-if="isSuperuser">
                <router-link :to="`/contests/${item.id}/edit`" title="编辑">
                  <v-icon>mdi-pencil</v-icon>
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
  name: "ContestList",

  props: ["isSuperuser"],

  data: () => ({
    headers: [
      {
        text: "比赛名称",
        value: "name",
        sortable: false,
      },
      {
        text: "时间",
        value: "time",
        sortable: false,
      },
      {
        text: "操作",
        value: "actions",
        sortable: false,
      },
    ],
    loading: true,
    contests: [],
  }),

  async mounted() {
    this.contests = (
      await axios.get(`${process.env.VUE_APP_API_BASE_URL}contests`)
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
