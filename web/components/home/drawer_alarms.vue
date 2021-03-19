<template>
    <div>
        <el-drawer
  title="I am the title"
  :visible.sync="drawer"
  direction="ltr"
  size="50%"
  :before-close="handleClose">
  <span>Hi, there!</span>
</el-drawer>
    </div>
</template>
<script>
  export default {
    data() {
      return {
        drawer: false,
      };
    },
    props:['show'],
    watch:{
        show(newVal){
            this.drawer = newVal;
        }
    },
    methods: {
      handleClose(done) {
          this.$parent.drowerAlarms = false;
            done();
      }
    }
  };
</script>