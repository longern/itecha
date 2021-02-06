<template>
  <v-app>
    <v-app-bar app absolute>
      <v-app-bar-title>
        <router-link to="/" tag="span">iTechA</router-link>
      </v-app-bar-title>

      <v-spacer></v-spacer>

      <v-btn v-if="user.username" text v-text="user.username"></v-btn>
      <v-btn v-else text to="/login">登录</v-btn>
    </v-app-bar>

    <v-main>
      <div>
        <router-view
          :is-superuser="user.is_superuser"
          @login="updateUser"
        ></router-view>
      </div>
    </v-main>
  </v-app>
</template>

<script>
import axios from "axios";

export default {
  name: "App",

  data: () => ({
    user: {},
  }),

  methods: {
    async updateUser() {
      const user_response = await axios.get(
        `${process.env.VUE_APP_API_BASE_URL}users/current`
      );
      this.user = user_response.data;

      const csrf_token_match = document.cookie.match(/csrftoken=([^;]*)/);
      if (csrf_token_match)
        axios.defaults.headers["X-CSRFToken"] = csrf_token_match[1];
    },
  },

  created() {
    axios.defaults.withCredentials = true;
    this.updateUser();
  },
};
</script>

<style>
.v-app-bar-title {
  font-family: Consolas, "Courier New", Courier, monospace;
  cursor: pointer;
}

.v-application .markdown-body pre code {
  background-color: transparent;
}
</style>
