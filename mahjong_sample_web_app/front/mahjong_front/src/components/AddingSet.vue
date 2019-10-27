<template>
  <div>
    <a href="#" class="btn btn-primary tile-item" role="button">牌追加</a>
    <div class="status-buttons row">
      <div class="btn-group btn-group-toggle tile-item" data-toggle="buttons">
        <label class="btn btn-secondary active">
          <input type="radio" name="ba" id="ton-ba" value="ton-ba" autocomplete="off" checked />東
        </label>
        <label class="btn btn-secondary">
          <input type="radio" name="ba" id="nan-ba" value="nan-ba" autocomplete="off" />南
        </label>
      </div>
      <div class="btn-group btn-group-toggle tile-item" data-toggle="buttons">
        <label class="btn btn-secondary active">
          <input type="radio" name="kaze" id="ton" value="ton" autocomplete="off" checked />東
        </label>
        <label class="btn btn-secondary">
          <input type="radio" name="kaze" id="nan" value="nan" autocomplete="off" />南
        </label>
        <label class="btn btn-secondary">
          <input type="radio" name="kaze" id="sha" value="sha" autocomplete="off" />西
        </label>
        <label class="btn btn-secondary">
          <input type="radio" name="kaze" id="pei" value="pei" autocomplete="off" />北
        </label>
      </div>
      <div class="btn-group btn-group-toggle tile-item" data-toggle="buttons">
        <label class="btn btn-secondary active">
          <input type="checkbox" autocomplete="off" name="riichi" value="1" checked />リーチ
        </label>
      </div>
    </div>
    <div class="submit-buttons">
      <button type="submit" class="btn btn-primary tile-item active" name="ron" value="1">ロン</button>
      <button type="submit" class="btn btn-primary tile-item active" name="tsumo" value="1">ツモ</button>
    </div>
  </div>
</template>
<script>
export default {
  name: "AddingSet"
};
</script>
<style scoped lang="scss">
</style>