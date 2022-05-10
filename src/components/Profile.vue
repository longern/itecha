<template>
  <!-- eslint-disable vue/no-v-html -->
  <v-container
    class="profile"
  >
    <v-row class="pa-4">
      <v-avatar
        size="56"
        color="grey lighten-2"
      >
        <img
          v-if="avatar"
          src="avatar"
        >
        <v-icon v-else>
          mdi-account
        </v-icon>
      </v-avatar>
      <span
        v-if="user.username"
        class="pa-4"
        v-text="user.username"
      />
      <span
        v-else
        class="pa-4"
        @click="login"
      >登录</span>
    </v-row>
    <v-list>
      <v-list-item
        @click="logout"
      >
        <v-list-item-title>注销</v-list-item-title>
      </v-list-item>
    </v-list>
  </v-container>
</template>

<script>
import axios from "axios";

export default {
  name: "Profile",

  props: { user: { type: Object, default: () => {} } },

  data: () => ({
    avatar: "",
  }),

  methods: {
    async login() {
      axios.options("/msal/login").then(() => {
        window.location = "/msal/login";
      }).catch(() => {});
    },

    async logout() {
      await axios.post(`${process.env.VUE_APP_API_BASE_URL}logout`);
      this.user = {};
    }
  },
};
</script>
