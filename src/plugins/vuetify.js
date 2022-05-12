import Vue from "vue";
import Vuetify from "vuetify";
import VuetifyDialog from "vuetify-dialog";
import zhHans from "vuetify/es5/locale/zh-Hans";

import "./notify.css";

Vue.use(Vuetify);

const vuetify = new Vuetify({
  breakpoint: {
    mobileBreakpoint: "sm",
  },
  lang: {
    locales: { zhHans },
    current: "zhHans",
  },
});

Vue.use(VuetifyDialog, {
  context: {
    vuetify,
  },
});

export default vuetify;
