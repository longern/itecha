import Vue from "vue";
import VueRouter from "vue-router";
import vuetify from "./plugins/vuetify";

import App from "./App.vue";
import Login from "./components/Login.vue";
import Problem from "./components/Problem.vue";
import ProblemList from "./components/ProblemList.vue";
import ProblemForm from "./components/ProblemForm.vue";
import SubmissionList from "./components/SubmissionList.vue";

Vue.config.productionTip = false;

Vue.use(VueRouter);

const router = new VueRouter({
  routes: [
    {
      path: "/",
      component: ProblemList,
    },
    {
      path: "/login",
      component: Login,
    },
    {
      path: "/problems/create",
      component: ProblemForm,
    },
    {
      path: "/problems/:id",
      component: Problem,
    },
    {
      path: "/problems/:id/edit",
      component: ProblemForm,
    },
    {
      path: "/submissions",
      component: SubmissionList,
      props: (route) => ({ problem_id: route.query.problem_id }),
    },
  ],
});

new Vue({
  vuetify,
  router,
  render: (h) => h(App),
}).$mount("#app");
