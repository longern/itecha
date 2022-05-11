<template>
  <mobile-container :loading="loading">
    <v-row
      v-if="user.isSuperuser"
      class="align-center"
    >
      <v-btn
        color="primary"
        to="/problems/create"
      >
        创建题目
      </v-btn>
    </v-row>
    <v-data-table
      :headers="headers"
      :items="problems"
      mobile-breakpoint="0"
    >
      <template v-slot:item.status="{ item }">
        <v-icon
          v-if="item.status === 'AC'"
          color="green"
        >
          mdi-check
        </v-icon>
      </template>
      <template v-slot:item.title="{ item }">
        <router-link
          :to="`/problems/${item.id}`"
          v-text="item.title"
        />
      </template>
      <template v-slot:item.tags="{ item }">
        <v-chip-group v-if="item.tags">
          <v-chip
            v-for="tag in item.tags"
            :key="tag"
            small
            v-text="tag"
          />
        </v-chip-group>
      </template>
      <template
        v-if="user.isSuperuser"
        v-slot:item.actions="{ item }"
      >
        <router-link
          :to="`/problems/${item.id}/edit`"
          title="编辑"
        >
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
  </mobile-container>
</template>

<script>
import axios from "axios";

import MobileContainer from "./MobileContainer.vue";

export default {
  name: "ProblemList",

  components: { MobileContainer },

  props: { user: { type: Object, default: () => {} } },

  data: () => ({
    headers: [
      {
        text: "状态",
        value: "status",
        sortable: false,
      },
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

  async created() {
    this.problems = (
      await axios.get(`${process.env.VUE_APP_API_BASE_URL}problems`, {
        params: { fields: "id,title,tags" },
      })
    ).data;

    const msal_token_match = document.cookie.match(/(^| )msal_access_token=([^;]+)/);
    if (msal_token_match) {
      const msal_token = msal_token_match[2];
      const approot_response = await axios.get(
        "https://graph.microsoft.com/v1.0/me/drive/special/approot/children",
        {
          headers: { Authorization: `Bearer ${msal_token}` },
          withCredentials: false,
        }
      )

      const files = approot_response.data.value;
      const filenames = files.map(file => file.name);

      // If filename starts with problem id, then mark the problem as solved.
      for (const problem of this.problems) {
        if (filenames.includes(`${problem.id}.py`)) {
          problem.status = "AC";
        }
      }
    }

    this.loading = false;
  },
};
</script>

<style scoped>
a {
  text-decoration: none;
}
</style>
