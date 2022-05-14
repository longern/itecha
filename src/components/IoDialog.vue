<template>
  <v-dialog
    :value="value"
    class="io-dialog"
    width="500"
    @input="$emit('input', $event)"
  >
    <template v-slot:activator="{ on, attrs }">
      <slot
        v-bind="attrs"
        v-on="on"
      />
    </template>

    <v-card :loading="loading">
      <v-tabs
        v-model="tab"
        align-with-title
      >
        <v-tabs-slider color="black" />

        <v-tab :key="0">
          输入
        </v-tab>
        <v-tab :key="1">
          输出
        </v-tab>
      </v-tabs>
      <v-container v-if="tab === 0">
        <v-textarea
          v-model="input"
          label="用户输入"
        />
        <v-card-actions>
          <v-spacer />
          <v-btn
            color="secondary"
            @click="run"
          >
            运行
          </v-btn>
        </v-card-actions>
      </v-container>
      <v-card-text
        v-else
        class="overflow-auto"
      >
        <pre
          v-if="output"
          class="mt-4"
        ><code v-text="output" /></pre>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  name: "IoDialog",

  props: {
    value: {
      type: Boolean,
      default: false,
    },
    loading: {
      type: Boolean,
      default: false,
    },
  },

  data: () => ({
    input: "",
    output: "",
    tab: 0,
  }),

  methods: {
    receiveOutput(output) {
      console.log(output, this.output);
      this.output = output;
      this.loading = false;
    },

    run() {
      this.$emit("run", this.input);
      this.loading = true;
      this.tab = 1;
    },
  }
};
</script>

<style>
.v-dialog .v-textarea, .v-dialog code {
  font-family: Consolas, monospace;
}
</style>
