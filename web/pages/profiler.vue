<template>
<main>
  <button class="btn-rnd btn-plus">+</button>
</main>
  
</template>
<script>

import { mapActions } from "vuex";

export default {  
  layout: "header_footer",

  created() {
    this.setActiveTabHeader("PROFILER");
  },
  
   methods: {
    ...mapActions("users", {
      setActiveTabHeader: "setActiveTabHeader"
    }),
   }

  
};
</script>

<style scoped>
main{
  width: 100%;
  height: 100%;
}
.btn-rnd {
  width: 60px;
  height: 60px;
  border: none;
  border-radius: 30px;
  background-color: hsl(160, 98%, 39%);
  outline: none;
  color: #fff;
  font-weight: 500;
  font-size: 66.4615px;
  line-height: 81px;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  text-transform: uppercase;

  position: absolute;
  bottom: 48px;
  right: 48px ;
}
.btn-rnd:hover{
  background-color: hsl(160, 98%, 36%);
}
</style>
