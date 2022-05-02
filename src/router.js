import VueRouter from "vue-router";

import ContestList from "./components/ContestList.vue";
import ExamForm from "./components/ExamForm.vue";
import Login from "./components/Login.vue";
import Playground from "./components/Playground.vue";
import Problem from "./components/Problem.vue";
import ProblemList from "./components/ProblemList.vue";
import ProblemForm from "./components/ProblemForm.vue";
import SubmissionList from "./components/SubmissionList.vue";

const router = new VueRouter({
  routes: [
    {
      path: "/",
      component: ProblemList,
    },
    {
      path: "/contests",
      component: ContestList,
    },
    {
      path: "/exams/create",
      component: ExamForm,
    },
    {
      path: "/exams/:id/edit",
      component: ExamForm,
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
