<template>
  <v-app-bar app>
    <slot name="back">
      <v-btn
        to="/"
        icon
      >
        <v-icon>mdi-arrow-left</v-icon>
      </v-btn>
    </slot>
    <v-spacer />
    <v-app-bar-title v-text="title" />
    <v-spacer />
    <v-btn
      icon
      @click="share"
    >
      <v-icon>mdi-share</v-icon>
    </v-btn>
  </v-app-bar>
</template>

<script>
export default {
  name: "MobileAppBar",

  props: {
    title: { type: String, default: "" },
  },

  methods: {
    share() {
      const url = window.location.href;
      const title = this.title;
      navigator.share({ title, url });
    },
  },
};
</script>
