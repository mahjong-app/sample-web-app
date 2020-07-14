import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);

// function toggleActive(state, attr) {
//   attrObj = state[attr];
//   console.log(attrObj);
//   if (attrObj) {
//     attrObj = false;
//   } else {
//     attrObj = true;
//   }
//   console.log(attrObj);
// }

export default new Vuex.Store({
  state: {
    pies: [
      { id: "pi1", name: "2m", agari: false, naki: 1, dora: false, aka: false },
      { id: "pi2", name: "3m", agari: false, naki: 1, dora: false, aka: false }
    ], // [{id: "pi1", name: "2m", agari: false, naki: 1, dora: false, aka: false}]
    // agari: null, // id of pi
    // nakipies: { naki1: [], naki2: [], naki3: [], naki4: [] },
    ba: "ton",
    kaze: "ton",
    reach: false,
    ron: false,
    tsumo: false,
    isAgariActive: {},
    isDraActive: false,
    isAkaActive: false
  },
  mutations: {
    updateAgari(state, pi) {
      // toggleActive(state, state.isAgariActive);
      // この部分のforを作る。
      // プロパティへの保存が伝播するのか？
      for (let p of state.pies) {
        if (pi === p.index) {
          p.agari = true
        } else if (p.agari) {
          p.agari = false
        }
      }
      // state.pies[pi]["agari"] = true;

      // state.agari = pi;

      if (state.isAgariActive) {
        state.isAgariActive = false;
      } else {
        state.isAgariActive = true;
      }
    },
    updateNaki(state, pi, num) {},
    updateDra(state, pi) {
      if (state.isDraActive) {
        state.isDraActive = false;
      } else {
        state.isDraActive = true;
      }
    },
    updateAka(state, pi) {
      if (state.isAkaActive) {
        state.isAkaActive = false;
      } else {
        state.isAkaActive = true;
      }
    }
  },
  actions: {},
  modules: {}
});
