<template>
  <v-app-bar
    :class="{ 'd-none': !$vuetify.breakpoint.mobile }"
    app
  >
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
    <v-btn icon>
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
};
</script>
