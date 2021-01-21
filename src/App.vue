<template>
  <v-app>
    <v-app-bar app>
      <v-app-bar-title>iTechA</v-app-bar-title>

      <v-spacer></v-spacer>

      <v-btn
        text
        to="/login"
      >登录
      </v-btn>
    </v-app-bar>

    <v-main>
      <div>
        <router-view></router-view>
      </div>
    </v-main>
  </v-app>
</template>

<script>
export default {
  name: "App",

  data: () => ({
    //
  }),
};
</script>

<style>
.v-app-bar-title {
  font-family: Consolas, "Courier New", Courier, monospace;
}
</style>
