import VueRouter from "vue-router";

import ContestList from "./components/ContestList.vue";
import Login from "./components/Login.vue";
import Playground from "./components/Playground.vue";
import Problem from "./components/Problem.vue";
import ProblemList from "./components/ProblemList.vue";
import ProblemForm from "./components/ProblemForm.vue";
import Profile from "./components/Profile.vue";
import Resources from "./components/Resources.vue"
import SubmissionList from "./components/SubmissionList.vue";

const router = new VueRouter({
  routes: [
    {
      path: "/",
      component: ProblemList,
    },
    {
      path: "/resources",
      component: Resources,
    },
    {
      path: "/contests",
      component: ContestList,
    },
    {
      path: "/login",
      component: Login,
    },
    {
      path: "/playground",
      component: Playground,
    },
    {
      path: "/profile",
      component: Profile,
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
      props: (route) => ({ problemId: route.query.problem_id }),
    },
  ],
});

export default router;
