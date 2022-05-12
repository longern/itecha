<template>
  <v-app>
    <v-app-bar
      v-if="!$vuetify.breakpoint.mobile"
      app
      absolute
      class="fill-height"
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
            <v-list-item to="/profile">
              <v-list-item-title v-text="user.username" />
            </v-list-item>
            <v-list-item
              v-if="user.is_superuser"
              href="/admin"
            >
              <v-list-item-title>控制台</v-list-item-title>
            </v-list-item>
            <v-list-item @click="logout">
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

    <v-main class="fill-height">
      <router-view
        :user="user"
        @login="updateUser"
      />
    </v-main>

    <v-footer
      v-if="$route.path !== '/playground' && $vuetify.breakpoint.mobile"
      app
      class="mobile-footer py-0"
    >
      <v-btn
        text
        to="/"
      >
        <v-icon>mdi-home</v-icon>
        <div>练习</div>
      </v-btn>
      <v-btn
        text
        to="/resources"
      >
        <v-icon>mdi-book</v-icon>
        <div>资源</div>
      </v-btn>
      <v-btn
        text
        to="/playground"
      >
        <v-icon>mdi-code-tags</v-icon>
        <div>编程</div>
      </v-btn>
      <v-btn
        text
        to="/profile"
      >
        <v-icon>mdi-account</v-icon>
        <div>我的</div>
      </v-btn>
    </v-footer>
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
      const msal_token_match = document.cookie.match(
        /(^| )msal_access_token=([^;]+)/
      );
      const refresh_token_match = document.cookie.match(
        /(^| )msal_refresh_token=([^;]+)/
      );
      if (refresh_token_match && !msal_token_match) {
        const refresh_token = refresh_token_match[2];
        axios.get("/msal/refresh", { params: { refresh_token } });
      }

      const user_response = await axios.get(
        `${process.env.VUE_APP_API_BASE_URL}users/current`
      );
      this.user = user_response.data;

      const csrf_token_match = document.cookie.match(/csrftoken=([^;]*)/);
      if (csrf_token_match)
        axios.defaults.headers["X-CSRFToken"] = csrf_token_match[1];
    },

    async logout() {
      await axios.post(`${process.env.VUE_APP_API_BASE_URL}logout`);
      this.user = {};
    },
  },
};
</script>

<style>
.v-application {
  max-height: 100vh;
}

.v-app-bar-title {
  font-family: Consolas, "Courier New", Courier, monospace;
  cursor: pointer;
}

.v-application .markdown-body pre code {
  background-color: transparent;
}

.fill-width {
  width: 100%;
}

.mobile-footer>.v-btn {
  margin: 0 auto;
  min-height: 48px;
  border-radius: 0;
}

.mobile-footer .v-btn__content {
  display: flex;
  flex-direction: column;
  font-size: 12px;
}
</style>
