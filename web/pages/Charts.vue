  <template>
  <div class="section">
    <!-- верхняя панель -->
    <div class="title-panel">
      <div class="headMenu">
        <select v-model="selectedfactory" class="headMenu_item btn_icon">
          <option
            v-for="factory in factories"
            :key="factory.factoryid"
            :value="factory"
          >
            {{ factory.name }}
          </option>
        </select>
      </div>

      <div class="select-period">
        <button
          v-on:click="setRange({ period: 1, id: 0 })"
          class="btn-period"
          :class="{ active: periodActive[0] }"
        >
          час
        </button>
        <button
          v-on:click="setRange({ period: 8, id: 1 })"
          class="btn-period"
          :class="{ active: periodActive[1] }"
        >
          смена
        </button>
        <button
          v-on:click="setRange({ period: 24, id: 2 })"
          class="btn-period"
          :class="{ active: periodActive[2] }"
        >
          день
        </button>
        <button
          v-on:click="setRange({ period: 168, id: 3 })"
          class="btn-period"
          :class="{ active: periodActive[3] }"
        >
          неделя
        </button>
        <button
          v-on:click="setRange({ period: 5040, id: 4 })"
          class="btn-period"
          :class="{ active: periodActive[4] }"
        >
          месяц
        </button>
      </div>

      <div>
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
      </div>
    </div>

    <!-- верхняя панель -->

    <!-- sub панель -->
    <div class="sub-panel">
      <div class="subMenu" v-for="shop in selectedshops" :key="shop.shopid">
        <button
          href="#"
          class="subMenu_item btn_icon"
          :class="{ actived: shop.shopid == activeshop.shopid }"
          @click="setActiveshop(shop)"
        >
          {{ shop.name }}
        </button>
      </div>
    </div>

    <!-- sub панель -->

    <!-- Список графиков -->
    <div class="charts-items">
      <ul>
        <li v-for="chartOption in chartOptions" :key="chartOption.id">
          <div class="charttitle" @click="toggle(chartOption.id)">
            Станок {{ chartOption.name }}
            <IconifyIcon
              class="arrow left-arrow arrow-down"
              :class="{ 'arrow-up': showCharts[chartOption.id] }"
              icon="baselineKeyboardArrowDown"
              :style="{ fontSize: '24px' }"
            />
          </div>
          <transition name="slide">
            <div class="highchart-box" v-show="showCharts[chartOption.id]">
              <highcharts
                class="highchart-item highchart"
                :options="chartOption.option"
                :constructor-type="'stockChart'"
                :lang="basicOptions.lang"
              ></highcharts>

              <div
                class="highchart-item details"
                @click="setChart(chartOption.id)"
              >
                <nuxt-link
                  custom
                  v-slot="{ navigate }"
                  to="/Chart"
                  class="details-btn"
                >
                  <button @click="navigate">Подробнее</button>
                </nuxt-link>
                <div class="details-oee dng">OEE - {{ chartOption.OEE }}</div>
              </div>
            </div>
          </transition>
        </li>
      </ul>
    </div>
    <!-- Список графиков -->

    <VchartBox
      v-show="isVchartBoxVisible"
      @changeShow="closeVchartBoxVisible"
      :content="content"
    ></VchartBox>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
import { mapActions } from "vuex";

import Table from "@/components/Table";

import VchartBox from "@/components/VchartBox";

var nowDate = new Date();

export default {
  layout: "header_footer",

  created() {
    this.loadData(this.opt);
    this.loadBasicOptions();

    this.setActiveTabHeader("OEE");
    this.setActiveTabSidebar("Online");
    this.setSelectedfactory(this.factories[0]);
  },

  components: {
    pointTable: Table,
    VchartBox: VchartBox,
  },

  data() {
    return {
      isVchartBoxVisible: false,

      range: 28800000,

      periodActive: [false, true, false, false, false],

      // factorys: [
      //   { value: "Завод нефтепродуктов г. Гомель" },
      //   { value: "Завод нефтепродуктов г. Мозырь" },
      //   { value: "Завод нефтепродуктов г. Полоцк" },
      // ],
      // selectedfactory: "Завод нефтепродуктов г. Гомель",
      currentsubMenu: "2",

      // selectedshop:  {name: "Цех ковки тяжелых конструкций и древесины г. Гомель", shopid: "2", factoryid: "10"},
      // arrShow: [],

      showSettings: false,
      fistDate: new Date().toISOString().substr(0, 10),
      lastDate: new Date().toISOString().substr(0, 10),
      cntPoint: 5,
      selected: "spline",
      typeChart: [{ value: "area" }, { value: "column" }, { value: "line" }],
    };
  },

  computed: {
    ...mapGetters("oeecharts", {
      selectedshops: "selectedshops",
      showCharts: "showCharts",
      // selectedfactory:"selectedfactory",
      arrPoint: "arrPoint",
      basicData: "basicData",
      basicOptions: "basicOptions",
      factories: "factories",
      shops: "shops",
      activeshop: "activeshop",
    }),

    selectedfactory: {
      get() {
        let item = this.$store.getters["oeecharts/selectedfactory"];
        return item;
      },
      set(value) {
        console.log(value);
        this.$store.dispatch("oeecharts/setSelectedfactory", value);
      },
    },

    opt: function () {
      return {
        fist: this.fistDate,
        last: this.lastDate,
        numPoint: this.cntPoint,
      };
    },

    content: function () {
      return {
        fist: this.fistDate,
        last: this.lastDate,
        title: "Настройка отображения графиков",
        btnLeft: "Экспорт",
        btnRight: "Обновить",
        selectLeft: "Графики - все подряд",
        selectRight: "Графики - группировать по группам",
      };
    },

    chartOptions: function () {
      let arrOptions = [];
      let tempArrayShow = this.showCharts.length ? this.showCharts : [];

      let chartOption;

      for (let idx = 0; idx < this.basicData.length; idx++) {
        chartOption = {
          // title: this.basicOptions.title,
          chart: this.basicOptions.chart,

          navigator: this.basicOptions.navigator,
          scrollbar: this.basicOptions.scrollbar,

          exporting: {
            enabled: false,
          },

          credits: {
            enabled: false,
          },

          //legend: this.basicOptions.legend,
          yAxis: this.basicOptions.yAxisOne,
          xAxis: {
            //type: 'datetime',
            //minRange: 30000,

            range: this.range,
            plotLines: this.arrPoint,
          },

          tooltip: this.basicOptions.tooltip,

          // rangeSelector: this.basicOptions.rangeSelector,
          rangeSelector: {
            enabled: false,
          },

          plotOptions: {
            xrange: {
              zones: [
                {
                  value: 0.99,
                  color: "#f7a35c",
                },
                {
                  value: 1,
                  color: "#7cb5ec",
                },
                {
                  value: 1.01,
                  color: "#90ed7d",
                },
              ],
              borderRadius: 0,
              borderWidth: 0,
              pointWidth: 40,
              grouping: false,
              point: {
                events: {
                  click: (e) => {
                    return;
                  },
                },
              },

              colorByPoint: false,
            },

            series: {
              cursor: "pointer",
              point: {
                events: {
                  click: (e) => {
                    // this.sendPoint(e);
                    return;
                  },
                },
              },
            },
          },

          series: [
            {
              name: "OEE",
              type: this.selected,
              yAxis: 0,
              keys: ["x", "y", "id"],
              data: this.basicData[idx][4],
            },
            {
              tooltips: { enabled: false },
              name: "ON",
              type: "xrange",
              yAxis: 1,
              keys: ["x", "x2", "y", "id", "color"],
              data: this.basicData[idx][3],
            },
          ],
        };

        arrOptions.push({
          id: idx,
          name: idx + 1,
          option: chartOption,
          OEE: this.basicData[idx][4][this.basicData[idx][4].length - 1][1],
        });
        if (this.showCharts.length == 0) {
          tempArrayShow.push(true);
          // открыт только первый график
          // tempArrayShow.push(idx == 0);
        }
      }
      this.setshowCharts(tempArrayShow);

      return arrOptions;
    },
  },

  methods: {
    ...mapActions("oeecharts", {
      setSelectedfactory: "setSelectedfactory",
      setActiveshop: "setActiveshop",
      setChart: "setChart",
      setshowCharts: "setshowCharts",
      addPoint: "addPoint",
      removePoint: "removePoint",
      loadData: "loadData",
      loadBasicOptions: "loadBasicOptions",
    }),
    ...mapActions("users", {
      setActiveTabHeader: "setActiveTabHeader",
      setActiveTabSidebar: "setActiveTabSidebar",
    }),

    setRange(sel) {
      this.range = 0;
      this.range = sel.period * 1000 * 3600;
      this.periodActive = this.periodActive.map((item) => false);
      this.periodActive.splice(sel.id, 1, true);

      // active
    },

    toggle(idToToggle) {
      // console.log(idToToggle, " - c ", this.showCharts[idToToggle], " на "б !this.showCharts[idToToggle]);
      console.log(idToToggle);
      console.log("showCharts ", this.showCharts);
      let tglShow = !this.showCharts[idToToggle];

      let arrShow = this.showCharts.slice();
      console.log("arrShow ", arrShow);
      arrShow.splice(idToToggle, 1, tglShow);
      console.log("arrShow ", arrShow);

      // console.log(this.showCharts);
      this.setshowCharts(arrShow);
      // console.log(this.showCharts);
    },

    showVchartBoxVisible() {
      this.isVchartBoxVisible = true;
    },
    closeVchartBoxVisible() {
      this.isVchartBoxVisible = false;
    },

    hideCharts() {
      let arrShow = this.showCharts.map((item) => false);
      this.setshowCharts(arrShow);
    },

    showedCharts() {
      let arrShow = this.showCharts.map((item) => true);
      this.setshowCharts(arrShow);
    },

    changeShowSettings() {
      this.showSettings = !this.showSettings;
    },

    changeFistData(val) {
      console.log(val);
      //this.fistDate =formatDate(val);
    },
    changeLastData(val) {
      //this.lastDate =formatDate(val);
    },

    sendPoint(e) {
      let dateX = new Date(e.point.x);
      dateX.getTimezoneOffset();
      let xPoint = {
        X: formatDate(dateX),
        A: this.basicData[0][e.point.index][1],
        P: this.basicData[1][e.point.index][1],
        Q: this.basicData[2][e.point.index][1],
        color: "#FF0000",
        width: 1,
        id: e.point.index,
        value: e.point.x,
      };
      this.addPoint(xPoint);
    },
  },
};

function formatDate(date = nowDate) {
  let dayOfMonth = date.getDate();
  let month = date.getMonth() + 1;
  let year = date.getFullYear();
  let hour = date.getHours();
  let minutes = date.getMinutes();
  let diffMs = new Date() - date;
  let diffSec = Math.round(diffMs / 1000);
  let diffMin = diffSec / 60;
  let diffHour = diffMin / 60;

  // форматирование
  //year = year.toString().slice(-2);
  month = month < 10 ? "0" + month : month;
  dayOfMonth = dayOfMonth < 10 ? "0" + dayOfMonth : dayOfMonth;
  hour = hour < 10 ? "0" + hour : hour;
  minutes = minutes < 10 ? "0" + minutes : minutes;

  return `${dayOfMonth}.${month}.${year} ${hour}:${minutes}`;
}
</script>

<style scoped>
/* анимация */
.slide-enter-active,
.slide-leave-active {
  transition: all 0.2s;
}
.slide-enter-active {
  max-height: 242px;
}
.slide-enter,
.slide-leave-active {
  max-height: 0;
}
.slide-leave {
  max-height: 242px;
}
/* анимация */

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

.section {
  width: 100%;
  height: 100%;
  align-self: center;
  text-align: center;
  padding-top: 108px;
}

.charts-items {
  max-height: 750px;
  width: 100%;

  overflow-y: auto;
}
.charts-items:hover {
  overflow-x: hidden;
}
.charts-items::-webkit-scrollbar {
  -webkit-appearance: none;

  width: 2px;
}
.charts-items::-webkit-scrollbar-thumb {
  border-radius: 2px;
  background-color: #3f51b5;
}

.charts-items > ul {
  padding-left: 12px;
  padding-right: 18px;
  width: 100%;
  list-style: none;
}

.title-panel {
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

  justify-content: space-between;
  width: 100%;
  /* width: 1780px; */
  /* left: 120px; */
  left: 0;
  height: 48px;

  position: absolute;
  top: 48px;
}
.headMenu {
  margin-left: 150px;
  margin-right: auto;
}
.select-period {
  display: flex;
  margin-right: 120px;
}
.select-showing {
  margin-left: 24px;
  margin-right: 12px;
}

.btn-period {
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

.charttitle {
  background-color: none;
  width: 120px;
  height: 24px;
  font-weight: 600;
  font-size: 14px;
  line-height: 17px;
  display: flex;
  align-items: center;
  letter-spacing: 0.05em;

  margin-top: 12px;

  color: #46627d;
}
.highchart-box {
  margin: 12px 0;
  display: flex;
  overflow-y: hidden;
}
.highchart-item {
  height: 242px;
}
.highchart {
  width: 100%;
}

.details {
  padding: 10px 2px 10px 10px;
  width: 142px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.details-oee {
  height: 36px;
  font-weight: 500;
  font-size: 14px;
  line-height: 17px;
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;

  margin-bottom: 4px;

  color: #721c24;
}

.btn-period:hover {
  /* background-color: inherit; */
  border: 1px solid #ff7167;
  color: #ff7167;
}

.active {
  background-color: inherit;
  border: 1px solid #ff7167;
  color: #ff7167;
}

.details-btn {
  background-color: inherit;
  height: 36px;
  font-weight: 600;
  font-size: 12px;
  line-height: 15px;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  letter-spacing: 0.05em;
  border-radius: 5px;

  border: 2px solid #3f51b5;

  color: #4b57a3;

  outline: none;
}

.highcharts {
  transition: 0.2s;
}

.arrow {
  width: 12px;
  height: 12px;
  filter: invert(1);
  transition: 0.2s;
}

.left-arrow {
  margin-left: 10px;
}

.arrow-up {
  transform: matrix(1, 0, 0, -1, 0, 0);
}
</style>
