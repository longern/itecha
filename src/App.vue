<template>
  <v-app>
    <v-app-bar
      app
      absolute
    >
      <v-app-bar-title>
        <router-link
          to="/"
          tag="span"
        >
          iTechA
        </router-link>
      </v-app-bar-title>

      <v-spacer />

      <v-btn
        icon
        to="/playground"
      >
        <v-icon>mdi-language-python</v-icon>
      </v-btn>

      <v-menu
        left
        offset-y
        min-width="200"
      >
        <template v-slot:activator="{ on, attrs }">
          <v-btn
            icon
            v-bind="attrs"
            v-on="on"
          >
            <v-icon>mdi-account</v-icon>
          </v-btn>
        </template>

        <v-list dense>
          <template v-if="user.username">
            <v-list-item>
              <v-list-item-title v-text="user.username" />
            </v-list-item>
            <v-list-item to="/login">
              <v-list-item-title>注销</v-list-item-title>
            </v-list-item>
          </template>
          <template v-else>
            <v-list-item to="/login">
              <v-list-item-title>登录</v-list-item-title>
            </v-list-item>
          </template>
        </v-list>
      </v-menu>
    </v-app-bar>

    <v-main>
      <div>
        <router-view
          :is-superuser="user.is_superuser"
          @login="updateUser"
        />
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

  created() {
    axios.defaults.withCredentials = true;
    this.updateUser();
  },

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
