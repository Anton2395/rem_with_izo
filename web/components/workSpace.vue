<template>
  <div>
    <div class="sub-panel">
      <div class="subMenu" v-for="(tab, index) in workspaces" :key="tab.id">
        <button
          style="margin: auto"
          class="subMenu_item btn_icon"
          :class="{ actived: activeIdFix(tab)}"
          @click="redrawGraphics(index)"
        >
          {{ tab.name }}
        </button>
        <div style="width: 25px; z-index: 3">
          <button class="perecl" @click="modalRenameWorkspace(tab)"></button>
          <button
            class="removeWorkSpace"
            @click="deletedWorkspaceFunc(tab)"
          ></button>
        </div>
      </div>
    </div>
    <div style="margin-top: 100px; padding-bottom: 12px" v-if="actualWorkspace">
      <highcharts
        :workspaces.sync="workspaces"
        v-for="workareaId in actualWorkspace.workares"
        :key="workareaId.id"
        :baseUrl="'/recorder/chart/workarea/?id=' + workareaId.id"
        :dataWorkArea="workareaId"
        :id="workareaId.id"
      />
    </div>

    <RenameWorkSpace
      v-if="openRenameWorkSpace"
      @closeForm="openRenameWorkSpace = false"
      @changeNameInParent="changeNameInParent"
      :name.sync="clickRenameWorksape"
    />
    <WorkSpaceDel
      v-if="openWorkSpaceDel"
      @closeForm="openWorkSpaceDel = false"
      del="Удаление рабочего пространства"
      :whtdel="actualWorkspace.name"
      :deletedWorkspace="deletedWorkspace"
    />
  </div>
</template>
<script>
import { mapActions } from 'vuex'
import { mapGetters } from 'vuex'

// import OnlineHeader from "/components/recorder/onlineHeader";
import RecorderChart from '/components/recorder/recorderChart'
import Chart from '/components/chart/chart.vue'
import RenameWorkSpace from '/components/RenameWorkSpace.vue'
import WorkSpaceDel from '/components/WorkSpaceDel.vue'

var nowDate = new Date()

export default {
  layout: 'header_footer',

  data() {
    return {
      deletedWorkspace: {},
      result: [],
      workspaces: [],
      actualWorkspace: null,
      clickRenameWorksape: {},
      openRenameWorkSpace: false,
      openWorkSpaceDel: false,
    }
  },

  components: {
    // onlinePeriod: OnlineHeader,
    recorderChart: RecorderChart,
    highcharts: Chart,
    RenameWorkSpace,
    WorkSpaceDel,
  },

  computed: {
    ...mapGetters('recorder', {
      tabs: 'getTabs',
    }),
  },

  created() {
    this.setActiveTabHeader('RECORDER')

    this.setActiveTabSidebar('Online')
  },
  mounted() {
    this.getWorkspaces()
  },

  methods: {
    activeIdFix(tabs){
      try{
        if (this.actualWorkspace.id){
          return tabs.id == this.actualWorkspace.id;
        }
      }
      catch(e){
        // console.log(e);
        return false;
      }
    },
    changeNameInParent(name) {
     
      let indexFind = this.workspaces.findIndex((el) => {
        return el.id == this.clickRenameWorksape.id;
      })

      // this.workspaces[indexFind].name = name;
      this.$store.dispatch("selectedWorkarea/FixRenameWorkSpace",name);
      // this.$emit('changeworkspaces', this.workspaces);
    },
    modalRenameWorkspace(workspace) {
      this.clickRenameWorksape = workspace
      this.openRenameWorkSpace = !this.openRenameWorkSpace
    },
    async getWorkspaces() {
      let a = await this.$axios.get('/recorder/structure/Workspace/')
      this.workspaces = a.data.sort((a, b) => a.id - b.id)
      this.actualWorkspace = this.workspaces[0]
      this.$store.commit('selectedWorkarea/setWorkarea', this.actualWorkspace)
      this.$emit('changeworkspaces', this.workspaces)
    },
    deletedWorkspaceFunc(deletedWorkspace) {
      this.deletedWorkspace = deletedWorkspace
      this.openWorkSpaceDel = !this.openWorkSpaceDel
    },
    ...mapActions('users', {
      setActiveTabHeader: 'setActiveTabHeader',
      setActiveTabSidebar: 'setActiveTabSidebar',
    }),
    redrawGraphics(i) {
      this.actualWorkspace = this.workspaces[i]
      this.$store.commit('selectedWorkarea/setWorkarea', this.actualWorkspace)
    },
  },
}
</script>

<style lang="scss" scoped>
.chart {
  margin-top: 90px;
}
.headmenu {
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
    border: 1px solid #00b0ff;
    background: #ffffff;

    font-weight: 500;
    font-size: 10px;
    line-height: 10px;
    color: #00b0ff;
  }
  .btn-workspace-green {
    width: 148px;
    height: 26px;

    display: flex;
    align-items: center;
    text-align: center;

    margin-right: 24px;
    padding: 2px 12px;
    border: 1px solid #01c587;
    background: #ffffff;

    font-weight: normal;
    font-size: 10px;
    line-height: 10px;
    color: #01c587;
  }
}

.recorder-items {
  z-index: 100;
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
    content: '';
    width: 100%;
    border-bottom: 1px solid #2dc2fa;
    position: absolute;
    bottom: 0;
    left: 0;
  }
  .recorder-space.actived:before {
    content: '';
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
        background-image: url('~assets/svg/recorder/typeGraph.svg');
        background-position: center;
        background-repeat: no-repeat;
        background-size: contain;

        &:hover {
          background-image: url('~assets/svg/recorder/hovTypeGraph.svg');
        }
      }

      .online {
        background-image: url('~assets/svg/recorder/onlinePlay.svg');
        background-position: center;
        background-repeat: no-repeat;
        background-size: contain;

        &:hover {
          background-image: url('~assets/svg/recorder/hovOnlinePlay.svg');
        }
      }

      .gannt {
        background-image: url('~assets/svg/recorder/DiagrGannt.svg');
        background-position: center;
        background-repeat: no-repeat;
        background-size: contain;

        &:hover {
          background-image: url('~assets/svg/recorder/hovDiagrammGrannt.svg');
        }
      }

      .formule {
        background-image: url('~assets/svg/recorder/formule.svg');
        background-position: center;
        background-repeat: no-repeat;
        background-size: contain;

        &:hover {
          background-image: url('~assets/svg/recorder/hovFormule.svg');
        }
      }

      .resize {
        background-image: url('~assets/svg/recorder/resizeGraph.svg');
        background-position: center;
        background-repeat: no-repeat;
        background-size: contain;

        &:hover {
          background-image: url('~assets/svg/recorder/hovResizeGraph.svg');
        }
      }
      .bulity {
        background-image: url('~assets/svg/recorder/menu.svg');
        background-position: center;
        background-repeat: no-repeat;
        background-size: contain;

        &:hover {
          background-image: url('~assets/svg/recorder/hovAddicationMenu.svg');
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
  background: white;

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

  z-index: 3;
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
  content: '';
  width: 100%;
  border-bottom: 1px solid #2dc2fa;
  position: absolute;
  bottom: 0;
  left: 0;
}
.subMenu_item.actived:before {
  content: '';
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
.perecl {
  outline: none;
  width: 24px;
  height: 24px;
  padding: 0;
  border: none;
  background: none;
  margin: 4px 6px 0px 0px;
  background: center no-repeat url('~assets/svg/perecl.svg');
  /* background: center no-repeat url("~assets/svg/clear.svg"); */
}
.removeWorkSpace {
  outline: none;
  width: 24px;
  height: 24px;
  padding: 0;
  border: none;
  background: none;
  margin: -2px 6px 0px 0px;
  background: center no-repeat url('~assets/svg/recorder/remove.svg');
}
.perecl:hover {
  background: center no-repeat url('~assets/svg/hovRename.svg');
}
.removeWorkSpace:hover {
  background: center no-repeat url('~assets/svg/hovRemove.svg');
}
</style>

