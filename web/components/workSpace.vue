<template>
  <div>
    <!-- <div>
        <button v-on:click="hideCharts" class="btn_icon btn-submenu">
          <IconifyIcon
            icon="baselineViewHeadline"
            :style="{ fontSize: '30px' }"
          />
        </button>
      </div>
      <div>
        <button v-on:click="showedCharts" class="btn_icon btn-submenu">
          <IconifyIcon
            icon="baselineViewStream"
            :style="{ fontSize: '30px' }"
          />
        </button>
      </div>
      <div class="select-showing">
        <button v-on:click="showVchartBoxVisible" class="btn_icon btn-submenu">
          <IconifyIcon icon="baselineExtension" :style="{ fontSize: '30px' }" />
        </button>
      </div> -->
<!-- вкладки с рабочими областями -->
    <!-- <div class="recorder-items">
      <div v-for="(tab, index) in workspaces" :key="tab.name">
        <div class="recorder-space">
          <button @click="redrawGraphics(index)">
            <span>{{ tab.name }}</span>
          </button>
        </div>
      </div>
    </div> -->
    <div class="sub-panel">
      <div class="subMenu" v-for="(tab, index) in workspaces" :key="tab.id">
        <button
        style="margin: auto;"
          class="subMenu_item btn_icon"
          :class="{ actived: tab.id == actualWorkspace.id}"
          @click="redrawGraphics(index)"
        >
          {{ tab.name }}
        </button>
      </div>
    </div>
    <div style="margin-top: 100px;padding-bottom:12px;" v-if="actualWorkspace">
      <highcharts
        v-for="workareaId in actualWorkspace.workares"
        :key="workareaId.id"
        :baseUrl="'/recorder/chart/workarea/?id=' + workareaId.id"
        :dataWorkArea="workareaId"
        :id="workareaId.id"
      />
    </div>
    
    
    <!-- <menuTypeLine></menuTypeLine> -->
  </div>
</template>
<script>
import { mapActions } from "vuex";
import { mapGetters } from "vuex";

// import OnlineHeader from "/components/recorder/onlineHeader";
import RecorderChart from "/components/recorder/recorderChart";
import Chart from "/components/chart/chart.vue";
import menuTypeLine from "/components/menuTypeLine/menuTypeLine.vue";

var nowDate = new Date();

export default {
  layout: "header_footer",

  data() {
    return {
      result: [],
      workspaces: [],
      actualWorkspace: null,
    };
  },
  components: {
    // onlinePeriod: OnlineHeader,
    recorderChart: RecorderChart,
    highcharts: Chart,
    menuTypeLine,
  },

  computed: {
    ...mapGetters("recorder", {
      tabs: "getTabs",
    }),
  },

  created() {
    this.setActiveTabHeader("RECORDER");

    this.setActiveTabSidebar("Online");
  },
  async mounted() {
    let a = await this.$axios.get("/recorder/structure/Workspace/");
    this.workspaces = a.data;
    this.actualWorkspace = this.workspaces[0];
    // debugger;
    console.log(this.workspaces);
    console.log(this.result);
  },

  methods: {
    ...mapActions("users", {
      setActiveTabHeader: "setActiveTabHeader",
      setActiveTabSidebar: "setActiveTabSidebar",
    }),
    redrawGraphics(i) {
      this.actualWorkspace = this.workspaces[i];
    },
  },
};
</script>

<style lang="scss" scoped>

.chart {
  margin-top: 90px;
}
.headmenu{
    display: flex;
    margin-left: 150px;
    margin-right: auto;
    .btn-workspace-blue {
      width: 148px;
      height: 26px;

      display: flex;
      align-items: center;
      text-align: center;

      padding: 2px 12px;
      border: 1px solid #00B0FF;
      background: #FFFFFF;

      font-weight: 500;
      font-size: 10px;
      line-height: 10px;
      color: #00B0FF;
    }
    .btn-workspace-green {
      width: 148px;
      height: 26px;

      display: flex;
      align-items: center;
      text-align: center;

      margin-right: 24px;
      padding: 2px 12px;
      border: 1px solid #01C587;
      background: #FFFFFF;

      font-weight: normal;
      font-size: 10px;
      line-height: 10px;
      color: #01C587;
    }

}

.recorder-items {
  z-index: 10000;
  padding-top: 96px;
  padding-left: 12px;
  padding-right: 24px;
  .recorder-space {
    font-size: 14px;
    margin-top: -37px;
    margin-left: 5px;
    text-align: center;
    width: 140px;
    height: 38px;
    float: left;
  }
  .recorder-space:hover:before {
    content: "";
    width: 100%;
    border-bottom: 1px solid #2dc2fa;
    position: absolute;
    bottom: 0;
    left: 0;
  }
  .recorder-space.actived:before {
    content: "";
    width: 100%;
    border-bottom: 1px solid #2dc2fa;
    position: absolute;
    bottom: 0;
    left: 0;
  }

  .recorder-menu {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding-top: 24px;
    margin-bottom: 12px;

    .recorder-spease {
      font-weight: 500;
      font-size: 14px;
      line-height: 17px;
      letter-spacing: 0.05em;
      color: #46627d;
    }

    .menu {
      display: flex;
      align-items: center;
      justify-content: center;
      z-index: 500;

      .menu-svg {
        cursor: pointer;
        width: 24px;
        height: 24px;
        display: flex;
        align-items: center;
        margin-left: 12px;
      }

      .type {
        background-image: url("~assets/svg/recorder/typeGraph.svg");
        background-position: center;
        background-repeat: no-repeat;
        background-size: contain;

        &:hover {
          background-image: url("~assets/svg/recorder/hovTypeGraph.svg");
        }
      }

      .online {
        background-image: url("~assets/svg/recorder/onlinePlay.svg");
        background-position: center;
        background-repeat: no-repeat;
        background-size: contain;

        &:hover {
          background-image: url("~assets/svg/recorder/hovOnlinePlay.svg");
        }
      }

      .gannt {
        background-image: url("~assets/svg/recorder/DiagrGannt.svg");
        background-position: center;
        background-repeat: no-repeat;
        background-size: contain;

        &:hover {
          background-image: url("~assets/svg/recorder/hovDiagrammGrannt.svg");
        }
      }

      .formule {
        background-image: url("~assets/svg/recorder/formule.svg");
        background-position: center;
        background-repeat: no-repeat;
        background-size: contain;

        &:hover {
          background-image: url("~assets/svg/recorder/hovFormule.svg");
        }
      }

      .resize {
        background-image: url("~assets/svg/recorder/resizeGraph.svg");
        background-position: center;
        background-repeat: no-repeat;
        background-size: contain;

        &:hover {
          background-image: url("~assets/svg/recorder/hovResizeGraph.svg");
        }
      }
      .bulity {
        background-image: url("~assets/svg/recorder/menu.svg");
        background-position: center;
        background-repeat: no-repeat;
        background-size: contain;

        &:hover {
          background-image: url("~assets/svg/recorder/hovAddicationMenu.svg");
        }
      }
    }

    .addGraph {
      width: 724px;
      height: 400px;
      background: #f7f8fa;
      box-shadow: 0px 2px 6px rgba(0, 0, 0, 0.25);
    }
  }
}
.sub-panel {
  background-repeat: no-repeat;
  border-bottom: 1px solid hsl(220, 33%, 88%);
  background: #f9fafc; 

  font-weight: 500;
  font-size: 14px;
  line-height: 17px;

  align-items: center;

  display: flex;
  flex-direction: row;
  flex-wrap: wrap;

  justify-content: flex-start;
  /* width: 1640px; */
  /* left: 260px; */
  margin-left: 15%;

  width: 85%;
  height: 48px;

  position: absolute;
  top: 96px;
  left: 0;

  z-index: 80;
}
.subMenu {
  width: 140px;
  height: 48px;
  font-weight: 500;
  font-size: 12px;
  line-height: 12px;
  display: flex;
  align-items: center;
  text-align: center;
  
  color: #49617b;

  position: relative;
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
</style>

