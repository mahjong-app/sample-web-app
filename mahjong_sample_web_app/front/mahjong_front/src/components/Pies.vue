<template>
  <div id="main" class="row">
    <form action="/calc" method="GET">
      <!-- {{var tiles=[1, 2, 3]}} -->
      <div class="tile row" v-for="i in [1, 2, 3]">
        <!-- {{var tile="i"}} -->
        <!-- <div class="tile row"> -->
        <img src="static/img/pi/1m.png" alt="&#x1F007;" class="rounded tile-item" width="25" />
        <button
          type="radio"
          class="btn btn-secondary btn-sm tile-item"
          data-toggle="button"
          aria-pressed="false"
          autocomplete="off"
          name="tile-1-agari"
          value="1"
        >上牌</button>
        <div class="btn-group btn-group-toggle tile-item" data-toggle="buttons">
          <label class="btn btn-secondary btn-sm">
            <input type="radio" name="tile-1-naki" id="tile-1-naki-1" value="1" autocomplete="off" />明
          </label>
          <label class="btn btn-secondary btn-sm">
            <input type="radio" name="tile-1-naki" id="tile-1-naki-2" value="2" autocomplete="off" />明
          </label>
          <label class="btn btn-secondary btn-sm">
            <input type="radio" name="tile-1-naki" id="tile-1-naki-3" value="3" autocomplete="off" />明
          </label>
          <label class="btn btn-secondary btn-sm">
            <input type="radio" name="tile-1-naki" id="tile-1-naki-4" value="4" autocomplete="off" />明
          </label>
          <label class="btn btn-secondary btn-sm">
            <input type="radio" name="tile-1-naki" id="tile-1-naki-5" value="5" autocomplete="off" />槓
          </label>
        </div>
        <button
          type="radio"
          class="btn btn-secondary btn-sm tile-item"
          data-toggle="button"
          aria-pressed="false"
          autocomplete="off"
          name="tile-1-dora"
          value="1"
        >ドラ</button>
        <div class="btn-group btn-group-toggle tile-item" data-toggle="buttons">
          <label class="btn btn-secondary btn-sm">
            <input type="checkbox" autocomplete="off" name="aka-1" value="1" />赤
          </label>
        </div>
      </div>
    </form>
  </div>
</template>
<script>
export default {
  name: "Pies"
};
</script>

<style scoped lang="scss">
</style>