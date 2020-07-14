<template>
  <div id="main" class="row">

    <!-- <form action="/calc" method="GET"> -->
    <!-- {{var tiles=[1, 2, 3]}} -->
    <div class="tile row" v-for="pi in pies" id="pi-buttons">
      <Pi />
    </div>
    <!-- </form> -->
  </div>
</template>
<script>
import store from "../store";
import Pi from "./Pi.vue";
import { mapState } from "vuex";
export default {
  name: "Pies",
  components: {
    Pi
  },
  computed: mapState({
    pies: state => state.pies,
    isAgariActive: (state, pi) => state.isAgariActive,
    // ここで、動的に状態を取ってきたいので関数化をする。
    isDraActive: state => state.isDraActive,
    isAkaActive: state => state.isAkaActive
  }),
  methods: {
  }
};
</script>

<style scoped lang="scss">

</style>