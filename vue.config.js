const CopyWebpackPlugin = require('copy-webpack-plugin');
const path = require('path');

module.exports = {
  "outputDir": "itecha_backend/static",
  "transpileDependencies": [
    "vuetify"
  ],
};

module.exports.configureWebpack = {
  plugins: [
    new CopyWebpackPlugin([{
      from: 'node_modules/mavon-editor/dist/markdown',
      to: path.resolve(module.exports.outputDir, 'markdown'),
    }, {
      from: 'node_modules/mavon-editor/dist/katex',
      to: path.resolve(module.exports.outputDir, 'katex')
    }]),
  ],
};
