import Vue from "vue";
import VueRouter from "vue-router";
import vuetify from "./plugins/vuetify";
import VuetifyDialog from 'vuetify-dialog'
import 'vuetify-dialog/dist/vuetify-dialog.css'
import mavonEditor from 'mavon-editor'
import 'mavon-editor/dist/css/index.css'

import App from "./App.vue";
import router from "./router.js"

Vue.config.productionTip = false;

Vue.use(VueRouter);
Vue.use(VuetifyDialog, {
  context: {
    vuetify
  }
});
Vue.use(mavonEditor);

new Vue({
  vuetify,
  router,
  render: (h) => h(App),
}).$mount("#app");
