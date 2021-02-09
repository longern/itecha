const CopyWebpackPlugin = require('copy-webpack-plugin');
const path = require('path');

module.exports = {
  "outputDir": "itecha/static",
  "transpileDependencies": [
    "vuetify"
  ],
};

process.env.VUE_APP_API_BASE_URL = process.env.VUE_APP_API_BASE_URL || "/";

process.env.VUE_APP_PYTHON3_EXECUTOR = process.env.VUE_APP_PYTHON3_EXECUTOR || "/python-executor";

process.env.VUE_APP_ENABLE_CDN = process.env.VUE_APP_ENABLE_CDN || "";

if (!process.env.VUE_APP_ENABLE_CDN)
  module.exports.configureWebpack = {
    plugins: [
      new CopyWebpackPlugin([{
        from: 'node_modules/mavon-editor/dist/markdown',
        to: path.resolve(module.exports.outputDir, 'markdown'),
      }, {
        from: 'node_modules/mavon-editor/dist/katex',
        to: path.resolve(module.exports.outputDir, 'katex')
      }, {
        from: 'node_modules/mavon-editor/dist/highlightjs',
        to: path.resolve(module.exports.outputDir, 'highlightjs')
      }]),
    ],
  };
