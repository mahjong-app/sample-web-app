<template>
  <div id="main-form" class="row">
    <form action="/upload" method="POST" enctype="multipart/form-data">
      <div class="form-group col">
        <label for="image">画像ファイルアップロード</label>
        <input type="file" class="form-control-file" id="image" name="image" />
      </div>
      <button type="submit" class="btn btn-primary col">Upload</button>
    </form>
  </div>
</template>

<script>
export default {
  name: "File"
};
</script>

<style scoped lang="scss">
</style>