<template>
  <div class="body">
        <nuxt />
 </div>
</template>

<script>


</script>

<style scoped>
html {
  font-family: "Montserrat", -apple-system, BlinkMacSystemFont, "Segoe UI",
    Roboto, "Helvetica Neue", Arial, sans-serif;
  font-size: 18px;
  word-spacing: 1px;
  -ms-text-size-adjust: 100%;
  -webkit-text-size-adjust: 100%;
  -moz-osx-font-smoothing: grayscale;
  -webkit-font-smoothing: antialiased;
  box-sizing: border-box;
}

*,
*:before,
*:after {
  box-sizing: border-box;
  margin: 0;
}

.body{
  display: flex;
  min-height: 100vh;
  flex-direction: column;
  background: #F7F8FA;
}
.Site-content {
  padding-left: 120px;
  width: 100%;
  flex: 1;
  }

</style>
