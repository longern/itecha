const CopyWebpackPlugin = require("copy-webpack-plugin");
const path = require("path");

module.exports = {
  outputDir: "itecha/static",
  transpileDependencies: ["vuetify"],

  configureWebpack: {
    externals: {
      axios: "axios",
      codemirror: "CodeMirror",
      "mavon-editor": "MavonEditor",
      vue: "Vue",
      "vue-codemirror": "VueCodemirror",
      "vue-router": "VueRouter",
      vuetify: "Vuetify",
      "vuetify-dialog": "VuetifyDialog",
    },
  },

  pluginOptions: {
    compression: {
      gzip: {
        filename: "[path].gz[query]",
        algorithm: "gzip",
        include: /\.(js|css|html|svg|json)(\?.*)?$/i,
        minRatio: 0.8,
      },
    },
  },

  css: {
    extract: false,
  },
};

process.env.VUE_APP_API_BASE_URL = process.env.VUE_APP_API_BASE_URL || "/";

process.env.VUE_APP_PYTHON3_EXECUTOR =
  process.env.VUE_APP_PYTHON3_EXECUTOR || "/python-executor";

process.env.VUE_APP_ENABLE_CDN = process.env.VUE_APP_ENABLE_CDN || "";

if (!process.env.VUE_APP_ENABLE_CDN)
  module.exports.configureWebpack.plugins = [
    new CopyWebpackPlugin([
      {
        from: "node_modules/axios/dist",
        to: path.resolve(module.exports.outputDir, "axios"),
      },
      {
        from: "node_modules/codemirror",
        to: path.resolve(module.exports.outputDir, "codemirror"),
      },
      {
        from: "node_modules/mavon-editor/dist",
        to: path.resolve(module.exports.outputDir, "mavon-editor"),
      },
      {
        from: "node_modules/vue/dist",
        to: path.resolve(module.exports.outputDir, "vue"),
      },
      {
        from: "node_modules/vue-codemirror/dist",
        to: path.resolve(module.exports.outputDir, "vue-codemirror"),
      },
      {
        from: "node_modules/vue-router/dist",
        to: path.resolve(module.exports.outputDir, "vue-router"),
      },
      {
        from: "node_modules/vuetify/dist",
        to: path.resolve(module.exports.outputDir, "vuetify"),
      },
      {
        from: "node_modules/vuetify-dialog/dist",
        to: path.resolve(module.exports.outputDir, "vuetify-dialog"),
      },
    ]),
  ];
