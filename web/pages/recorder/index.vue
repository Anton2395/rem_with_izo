<template>
  <div>
    <onlinePeriod :workspacesData.sync = "workspaces" />

    <workSpaceId @workspaces='workspacesUpd'></workSpaceId>
  </div>
</template>
<script>
import { mapActions } from "vuex";
import OnlineHeader from "/components/recorder/onlineHeader";
import RecorderChart from "/components/recorder/recorderChart";
import Chart from "/components/chart/chart.vue";

import workSpaceId from "/pages/recorder/_id.vue";
var nowDate = new Date();

export default {
  layout: "header_footer",

  components: {
    onlinePeriod: OnlineHeader,
    recorderChart: RecorderChart,
    highcharts: Chart,
   
    workSpaceId,
  },

  data() {
    return {
     workspaces:[],
    };
  },

  methods: {
    workspacesUpd(data){
      this.workspaces = data;
    },
    ...mapActions("users", {
      setActiveTabHeader: "setActiveTabHeader",
    }),
  },
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
<style scoped>
.titlepanel {
  display: flex;
  margin-left: 1800px;
  margin-right: auto;
}
.subMenu {
  width: 140px;
  height: 48px;
  font-weight: 500;
  font-size: 10px;
  line-height: 12px;
  display: flex;
  align-items: center;
  text-align: center;

  color: #49617b;

  /* position: relative; */
}
.subMenu_item {
  text-decoration: none;

  display: block;
  transition: 0.3s;
}

.subMenu_item:hover:before {
  content: "";
  width: 100%;
  border-bottom: 1px solid #2dc2fa;
  position: absolute;
  bottom: 0;
  left: 0;
}
.subMenu_item.actived:before {
  content: "";
  width: 100%;
  border-bottom: 1px solid #2dc2fa;
  position: absolute;
  bottom: 0;
  left: 0;
}

.btn_icon {
  background: none;
  border: none;

  display: flex;
  justify-content: baseline;
  outline: none;
}

.btn-submenu {
  color: #3f51b5;
}
.btn-submenu:hover {
  color: hsl(231, 48%, 45%);
}
.btn_icon btn-submenu {
  z-index: 10;
}
</style>
