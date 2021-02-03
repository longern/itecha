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
          :is-superuser="isSuperuser"
          @login="updateToken"
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
    isSuperuser:
      ["127.0.0.1", "localhost"].indexOf(document.location.hostname) >= 0,
    user: {},
  }),

  methods: {
    updateToken(token) {
      axios.defaults.headers.common["Authorization"] = `Bearer ${token}`;
      localStorage.setItem("rest_admin_auth", JSON.stringify({ token }));

      this.updateUser(token.replace(/,.*/, ""));
    },

    async updateUser(user_id) {
      const user_response = await axios.get(
        `${process.env.VUE_APP_API_BASE_URL}users/${user_id}`
      );
      this.user = user_response.data;
    },
  },

  created() {
    if (localStorage.getItem("rest_admin_auth")) {
      const { token } = JSON.parse(localStorage.getItem("rest_admin_auth"));
      this.updateToken(token);
    }
  },
};
</script>

<style>
.v-app-bar-title {
  font-family: Consolas, "Courier New", Courier, monospace;
  cursor: pointer;
}
</style>
