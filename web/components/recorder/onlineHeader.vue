<template>
  <div>
    <div class="title-panel">
      <div class="headMenu">
        <button class="btn-workspace-green" @click="addWorkSpace">
          Добавить рабочее пространство
        </button>
        <button @click="addWorkArea" class="btn-workspace-blue">
          Добавить рабочую область
        </button>

        <!-- <select v-model="selectedfactory" class="headMenu_item btn_icon">
          <option
            v-for="factory in factories"
            :key="factory.factoryid"
            :value="factory"
          >
            {{ factory.name }}
          </option>
        </select> -->
      </div>

      <div>
        <button @click="openHideChart(false)" class="btn_icon btn-submenu">
          <img class="hideCharts" src="~assets/svg/hideCharts.svg" />
        </button>
      </div>
      <div>
        <button @click="openHideChart(true)" class="btn_icon btn-submenu">
          <img class="rollCharts" src="~assets/svg/rollCharts.svg" />
        </button>
      </div>
      <div class="select-showing">
        <button class="btn_icon btn-submenu" @click="visibleVBox = true">
          <img class="moreCharts" src="~assets/svg/puzzle.svg" />

          <!-- <IconifyIcon icon="baselineExtension" :style="{ fontSize: '30px' }" /> -->
        </button>
      </div>
    </div>

    <VchartBox
      v-show="visibleVBox"
      @changeShow="visibleVBox = false"
      :content="content"
    ></VchartBox>
  </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'
import VchartBox from '@/components/VchartBox'

export default {
  name: 'onlineHeader',
  data() {
    return {
      visibleVBox: false,
      periodActive: [false, false, false, false, false],
    }
  },
  props: ['workspacesData'],
  components: {
    VchartBox: VchartBox,
  },

  computed: {
    // ...mapGetters('oeecharts', {
    //   selectedshops: 'selectedshops',
    //   factories: 'factories',
    //   shops: 'shops',
    //   activeshop: 'activeshop',
    // }),

    // selectedfactory: {
    //   get() {
    //     let item = this.$store.getters['oeecharts/selectedfactory']
    //     return item
    //   },
    //   set(value) {
    //     console.log(value)
    //     this.$store.dispatch('oeecharts/setSelectedfactory', value)
    //   },
    // },
    content: function () {
      return {
        // fist: this.fistDate,
        // // last: this.lastDate,
        // title: 'Настройка отображения графиков',
        // btnLeft: 'Экспорт',
        // btnRight: 'Обновить',
        // selectLeft: 'Графики - все подряд',
        // selectRight: 'Графики - группировать по группам',
      }
    },
  },

  getters: {
    factories(state) {
      return state.factories
    },
  },

  methods: {
      addWorkSpace() {
      this.$axios
        .post('/recorder/structure/Workspace/', {
          name: 'Новое рабочее пространство',
        })
        .then((data) => {
          // console.log(this.$parent);
          this.workspacesData.push(data.data)
          this.$emit('closeForm')
        })
        .catch((e) => {
          console.log(e)
        })
    },
    addWorkArea() {
      try{let id = this.$store.state.selectedWorkarea.workarea.id
      // console.log(this.$store.state.selectedWorkarea.workarea)
      this.$axios
        .post(`/recorder/structure/Workarea/`, {
          name: 'Новая рабочая область',
          parent: id,
          data: [],
        })
        .then((data) => {
          // this.workspacesData.find(function (x) {
          //   if (x.id == id) {
          //     x.workares.push(data.data);
          //   }
          // });
          // console.log(data);
          
          this.$store.dispatch('selectedWorkarea/AddEmptyWorkArea', {
            id: data.data.id,
            name: data.data.name,
          })
          // this.$emit("closeForm");
        })
        .catch((e) => {})
      }
      catch(e){
        // console.log(e);
      }
    },
  
    ...mapActions('recorder', {
      addTab: 'addTabs',
    }),

    ...mapActions('oeecharts', {
      setSelectedfactory: 'setSelectedfactory',
      setActiveshop: 'setActiveshop',
      setChart: 'setChart',
      setshowCharts: 'setshowCharts',
    }),
    ...mapActions('users', {
      setActiveTabHeader: 'setActiveTabHeader',
      setActiveTabSidebar: 'setActiveTabSidebar',
    }),

    setRange(sel) {
      this.periodActive = this.periodActive.map((item) => false)
      this.periodActive.splice(sel.id, 1, true)
      // debugger;
      this.periodActive[sel.id] = true

      for (let el of this.$parent.$children[1].$children[0].$children) {
        el.setRange(sel)
      }
    },

    openHideChart(status) {
      for (let el of this.$parent.$children[1].$children[0].$children) {
        el.openedAccordion = status
      }
    },

    hideCharts() {
      let arrShow = this.showCharts.map((item) => false)
      this.setshowCharts(arrShow)
    },
  },
}
</script>

<style lang="scss" scoped>
.title-panel {
  background-repeat: no-repeat;
  border-bottom: 1px solid hsl(220, 33%, 88%);
  background: #f9fafc;
  z-index: 4;
  font-weight: 500;
  font-size: 14px;
  line-height: 17px;

  align-items: center;

  display: flex;
  flex-direction: row;
  flex-wrap: wrap;

  justify-content: space-between;
  width: 100%;
  /* width: 1780px; */
  /* left: 120px; */
  left: 0;
  height: 48px;

  position: absolute;
  top: 49px;

  .headMenu {
    display: flex;
    margin-left: 150px;
    margin-right: auto;

    .btn_icon {
      display: none;
    }

    .btn-workspace-green {
      width: 148px;
      height: 26px;

      display: flex;
      align-items: center;
      text-align: center;
      outline: none;
      margin-right: 24px;
      padding: 2px 12px;
      border: 1px solid #01c587;
      background: #ffffff;

      font-weight: normal;
      font-size: 10px;
      line-height: 10px;
      color: #01c587;
    }
    .btn-workspace-green:hover {
      width: 148px;
      height: 26px;

      display: flex;
      align-items: center;
      text-align: center;
      outline: none;
      margin-right: 24px;
      padding: 2px 12px;
      border: 1px solid #01c587;
      background: #01c587;

      font-weight: normal;
      font-size: 10px;
      line-height: 10px;
      color: #ffffff;
    }
    .btn-workspace-blue {
      width: 148px;
      height: 26px;
      outline: none;
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
    .btn-workspace-blue:hover {
      outline: none;
      width: 148px;
      height: 26px;

      display: flex;
      align-items: center;
      text-align: center;

      padding: 2px 12px;
      border: 1px solid #00b0ff;
      background: #00b0ff;

      font-weight: 500;
      font-size: 10px;
      line-height: 10px;
      color: #ffff;
    }
    .btn-workspace-dowland {
      margin-left: 25px;
      width: 100px;
      height: 26px;
      outline: none;
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
    .btn-workspace-dowland:hover {
      display: flex;
      align-items: center;
      text-align: center;

      padding: 2px 12px;
      border: 1px solid #00b0ff;
      background: #00b0ff;

      font-weight: 500;
      font-size: 10px;
      line-height: 10px;
      color: #ffff;
    }
  }

  .select-showing {
    margin-left: 24px;
    margin-right: 12px;
  }

  .select-period {
    display: flex;
    margin-right: 155px;

    .btn-period {
      cursor: pointer;
      border: none;

      outline: none;

      width: 80px;
      height: 24px;
      margin: 0 3px;

      background: #eaeef7;
      border-radius: 4px;

      font-weight: 600;
      font-size: 14px;
      line-height: 17px;
      display: flex;
      justify-content: center;
      align-items: center;
      text-align: center;

      color: #7b879d;
    }

    .btn-period:hover {
      border: 1px solid #ff7167;
      color: #ff7167;
    }

    .active {
      background-color: inherit;
      border: 1px solid #ff7167;
      color: #ff7167;
    }
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
}

.sub-panel {
  background-repeat: no-repeat;
  border-bottom: 1px solid hsl(220, 33%, 88%);
  /* background: #f9fafc; */

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

    position: relative;

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
  }
}

.moreCharts {
  width: 35px;
}
// .moreCharts:hover {

//   background-image: url("~assets/svg/hovPuzzle.svg");
// }
// .rollCharts:hover{
//   background-image: url("~assets/svg/hovRoll.svg");
// }
// .hideCharts:hover{
//   background-image: url("~assets/svg/hovHead.svg");
// }
</style>
