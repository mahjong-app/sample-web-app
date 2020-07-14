<template>
<div>
    <img :src="makePiIconSrc(pi.name)" :alt="pi.name" class="rounded tile-item" width="25" />
    <ul>
        <li v-on:click.prevent="updateAgari(pi)" v-bind:class="{ active: isAgariActive }">上牌</li>
        <li
          v-for="num in [1, 2, 3, 4]"
          v-on:click.prevent="updateNaki(pi.id, num)"
          v-text="num"
          v-bind:class="{ active: isAgariActive }"
        >1</li>
        <li v-on:click.prevent="updateDra(pi.id)" v-bind:class="{ active: isDraActive }">ドラ</li>
        <li v-on:click.prevent="updateAka(pi.id)" v-bind:class="{ active: isAkaActive }">赤</li>
      </ul>
</div>
</template>

<script>
import store from "../store";
import { mapState } from "vuex";
export default {
  name: "Pi",
  computed: mapState({
    // pies: state => state.pies,
    pi: state => ({ id: "pi1", name: "2m", agari: false, naki: 1, dora: false, aka: false }),
    isAgariActive: (state, pi) => pi.agari,  //state.isAgariActive,
    // ここで、動的に状態を取ってきたいので関数化をする。
    isDraActive: state => state.isDraActive,
    isAkaActive: state => state.isAkaActive
  }),
  methods: {
    makePiIconSrc(name) {
      return require("@/assets/pi/" + name + ".png");
    },
    updateAgari(pi) {
      store.commit("updateAgari", pi);
      console.log(pi, pi.id);
      // pi.agari ? pi.set("agari", false) : pi.set("agari", true);
    },
    updateNaki(pi, num) {
      store.commit("updateNaki", pi, num);
    },
    updateDra(pi) {
      store.commit("updateDra", pi);
    },
    updateAka(pi) {
      store.commit("updateAka", pi);
    }
  }
}
</script>

<style scoped lang="scss">
#pi-buttons {
  li {
    width: 50px;
    height: 25px;
    display: inline-block;
    border: 1px solid;
    text-align: center;
    cursor: pointer;
  }
  .active {
    background-color: red;
    color: white;
  }
}
</style>