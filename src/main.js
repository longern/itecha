import Vue from "vue";
import VueRouter from "vue-router";
import vuetify from "./plugins/vuetify";
import mavonEditor from "mavon-editor";

import App from "./App.vue";
import router from "./router.js";

Vue.config.productionTip = false;

Vue.use(VueRouter);
Vue.use(mavonEditor);

new Vue({
  vuetify,
  router,
  render: (h) => h(App),
}).$mount("#app");
