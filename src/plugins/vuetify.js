import Vue from "vue";
import Vuetify from "vuetify";
import zhHans from "vuetify/es5/locale/zh-Hans";

Vue.use(Vuetify);

export default new Vuetify({
  lang: {
    locales: { zhHans },
    current: "zhHans",
  },
});
