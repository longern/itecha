<template>
  <v-container
    :class="{'mobile-container': true, 'pa-0': $vuetify.breakpoint.mobile || fluid}"
    :fluid="fluid"
  >
    <template v-if="$vuetify.breakpoint.mobile || fluid">
      <v-card
        flat
        tile
        :loading="loading"
        class="fill-height overflow-y-auto"
      >
        <slot />
      </v-card>
    </template>
    <template v-else>
      <v-card :loading="loading">
        <slot />
      </v-card>
    </template>
  </v-container>
</template>

<script>
export default {
  name: "MobileContainer",

  props: {
    fluid: {
      type: Boolean,
      default: false,
    },

    loading: {
      type: Boolean,
      default: false,
    },
  },
};
</script>

<style>
.mobile-container {
  width: 100%;
  height: 100%;
}
</style>
