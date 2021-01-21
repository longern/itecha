import Vue from "vue";
import VueRouter from "vue-router";
import vuetify from "./plugins/vuetify";

import App from "./App.vue";
import Login from "./components/Login.vue";
import Problem from "./components/Problem.vue";

Vue.config.productionTip = false;

Vue.use(VueRouter);

const router = new VueRouter({
  routes: [
    {
      path: "/login",
      component: Login,
    },
    {
      path: "/problem",
      component: Problem,
    },
  ],
});

new Vue({
  vuetify,
  router,
  render: (h) => h(App),
}).$mount("#app");
