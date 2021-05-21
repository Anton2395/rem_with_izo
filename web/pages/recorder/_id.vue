<template>
  <div>
    <workSpace @changeworkspaces="workaspecesNew"></workSpace>
  </div>
</template>

<script>
import workSpace from "/components/workSpace.vue";

var nowDate = new Date();

export default {
    name: 'workSpaceId',
  components: {
    workSpace,
  },

  data() {
    return {
      tabs: [],
      visiable: false,
    };
  },
  methods:{
    workaspecesNew(data){
      this.$emit('workspaces',data);
    }
  }

  // setRange(sel) {
  //     this.range = 0;
  //     this.range = sel.period * 1000 * 3600;
  //     this.periodActive = this.periodActive.map((item) => false);
  //     this.periodActive.splice(sel.id, 1, true);

  //     // active
  //   },
  //   data(){
  //  return {

  //     periodActive: [false, true, false, false, false],

  //   };
  //   },
};
</script>