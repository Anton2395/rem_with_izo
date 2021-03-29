<template>
  <div class="body">
    <VHeaderMenu />
    <VSidebar />
    <!-- <VmsgBox /> -->
    <main class="Site-content">
          <nuxt />
    </main>
    <Vfooter />
  </div>
</template>

<script>
import VHeaderMenu from "@/components/Vheader";
import Vfooter from "@/components/Vfooter";
import VSidebar from "@/components/VSidebar";
import VmsgBox from "@/components/VmsgBox";

export default {
  components: {
    VHeaderMenu,
    VSidebar,
    Vfooter,
    VmsgBox
  }
};
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
  height: 100vh;
  flex-direction: column;
  /* background: #F7F8FA; */
}

.Site-content {
  padding-left: 120px;
  padding-right: 6px;
  height: calc(100vh - 72px);
  overflow: auto;
  width: 100%;
  flex: 1;
}
</style>
