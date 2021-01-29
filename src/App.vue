<template>
  <v-app>
    <v-app-bar app absolute>
      <v-app-bar-title>
        <router-link to="/" tag="span">iTechA</router-link>
      </v-app-bar-title>

      <v-spacer></v-spacer>

      <v-btn text to="/login">登录</v-btn>
    </v-app-bar>

    <v-main>
      <div>
        <router-view :is-superuser="isSuperuser"></router-view>
      </div>
    </v-main>
  </v-app>
</template>

<script>
export default {
  name: "App",

  data: () => ({
    isSuperuser:
      ["127.0.0.1", "localhost"].indexOf(document.location.hostname) >= 0,
  }),
};
</script>

<style>
.v-app-bar-title {
  font-family: Consolas, "Courier New", Courier, monospace;
  cursor: pointer;
}
</style>
