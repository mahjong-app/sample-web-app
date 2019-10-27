<template>
  <div id="app">
    <File />
    <Pies />
    <AddingSet />
    <Result />
  </div>
</template>

<script>
import File from "./components/File.vue";
import Pies from "./components/Pies.vue";
import Result from "./components/Result.vue";
import AddingSet from "./components/AddingSet.vue";

export default {
  name: "app",
  components: {
    File,
    Pies,
    Result,
    AddingSet
  }
};
</script>

<style lang="scss">
@import "~vue-material/dist/theme/engine"; // Import the theme engine

@include md-register-theme(
  "default",
  (
    primary: md-get-palette-color(blue, A200),
    // The primary color of your application
      accent: md-get-palette-color(red, A200) // The accent or secondary color
  )
);

@import "~vue-material/dist/theme/all"; // Apply the theme
</style>
