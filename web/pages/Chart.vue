<template>
  <div class="section">
    <!-- верхняя панель -->
    <div class="title-panel">
      <div class="headMenu">{{ activeshop.name }} / Станок {{ chartOptions.name }}</div>

      <div class="select-period">
        <button
            v-on:click="setRange({period:1, id: 0})"
            class="btn-period"
            :class="{ active: periodActive[0] }"
        >час
        </button>
        <button
            v-on:click="setRange({period:8, id: 1})"
            class="btn-period"
            :class="{ active: periodActive[1] }"
        >смена
        </button>
        <button
            v-on:click="setRange({period:24, id: 2})"
            class="btn-period"
            :class="{ active: periodActive[2] }"
        >день
        </button>
        <button
            v-on:click="setRange({period:168, id: 3})"
            class="btn-period"
            :class="{ active: periodActive[3] }"
        >неделя
        </button>
        <button
            v-on:click="setRange({period:5040, id: 4})"
            class="btn-period"
            :class="{ active: periodActive[4] }"
        >месяц
        </button>
      </div>

      <div>
        <button class="btn_icon btn-submenu" @click="prevChart">
          <IconifyIcon icon="outlineArrowBackIos" :style="{fontSize: '30px'}"/>
        </button>
      </div>
      <div>
        <button class="btn_icon btn-submenu" @click="nextChart">
          <IconifyIcon icon="outlineArrowForwardIos" :style="{fontSize: '30px'}"/>
        </button>
      </div>
      <div class="select-showing">
        <button v-on:click="showVchartBoxVisible" class="btn_icon btn-submenu">
          <IconifyIcon icon="baselineExtension" :style="{fontSize: '30px'}"/>
        </button>
      </div>
    </div>

    <!-- верхняя панель -->

    <!-- Данные OEE -->
    <div class="sub-panel">
      <div class="oee-current" v-bind:class="dataHead.statusOEE">
        <div class="oee-items left">
          OEE
          <div class="oee-item left">
            <p>AxPxQ</p>
            {{ chartOptions.A }}x{{ chartOptions.P }}x{{ chartOptions.Q }}
          </div>
        </div>

        <div class="oee-items right">
          <div class="oee-item right">
            <p>Цель: 65%</p>
            <p>Базовый:45%</p>
          </div>
          {{ chartOptions.OEE }} %
        </div>
      </div>

      <div class="apq-current">
        <div class="a-current apq-item" v-bind:class="dataHead.statusA">
          <p>Availability</p>
          {{ chartOptions.A }} %
        </div>
        <div class="p-current apq-item" v-bind:class="dataHead.statusP">
          <p>Performance</p>
          {{ chartOptions.P }} %
        </div>
        <div class="q-current apq-item" v-bind:class="dataHead.statusQ">
          <p>Quality</p>
          {{ chartOptions.Q }} %
        </div>
      </div>
      <div class="time-items">
        <div class="time-item">
          <p>Общее время</p>{{ timeStatusOut.all }}
        </div>
        <div class="time-item">
          <p>Время простоя</p>{{ timeStatusOut.idle }}
        </div>
        <div class="time-item">
          <p>Время аварий</p>{{ timeStatusOut.crash }}
        </div>
        <div class="time-item">
          <p>Время в выключении</p>{{ timeStatusOut.off }}
        </div>
        <div class="time-item">
          <p>Время работы</p>{{ timeStatusOut.working }}
        </div>
      </div>
      <div class="top5">
        <highcharts
            class="highchartBar"
            :constructor-type="'chart'"
            :options="chartOptionsTop5.option"
            :lang="basicOptions.lang"
        ></highcharts>
      </div>
    </div>
    <!-- Данные OEE -->
    <!-- График -->
    <div class="charts-items">
      <highcharts
          v-show="isChartOne"
          class="highchart"
          :options="chartOptions.option"
          :constructor-type="'stockChart'"
          :lang="basicOptions.lang"
      ></highcharts>

      <highcharts
          v-show="!isChartOne"
          class="highchart"
          :options="chartOptions.optionA"
          :constructor-type="'stockChart'"
          :lang="basicOptions.lang"
      ></highcharts>

      <highcharts
          v-show="!isChartOne"
          class="highchart"
          :options="chartOptions.optionP"
          :constructor-type="'stockChart'"
          :lang="basicOptions.lang"
      ></highcharts>

      <highcharts
          v-show="!isChartOne"
          class="highchart"
          :options="chartOptions.optionQ"
          :constructor-type="'stockChart'"
          :lang="basicOptions.lang"
      ></highcharts>

      <highcharts
          v-show="!isChartOne"
          class="highchart"
          :options="chartOptions.optionOEE"
          :constructor-type="'stockChart'"
          :lang="basicOptions.lang"
      ></highcharts>

      <!-- Таблица -->
      <pointTable :idx="idx"></pointTable>
      <!-- Таблица -->
    </div>
    <!-- График -->
    <VchartBox v-show="isVchartBoxVisible" @changeShow="closeVchartBoxVisible" :content="content"
               :key="idx"></VchartBox>

    <!--    Loader-->
    <Loader v-if="loader"/>
  </div>
</template>

<script>
import {mapGetters} from "vuex";
import {mapActions} from "vuex";

import Table from "@/components/Table";
import VchartBox from "@/components/VchartBox";
import Loader from "@/components/Loader";

import Highcharts from "highcharts";

const nowDate = new Date();
// const nowDateTime = nowDate.getTime() - nowDate.getTimezoneOffset() * 60 * 1000;
const nowDateTime = nowDate.getTime();
let legendVisible = {
  A: false,
  P: false,
  Q: false,
  OEE: true,
};

let range = (8 * 3600 * 1000);

export default {
  layout: "header_footer",

  created() {
    this.loadBasicOptions();

    this.setActiveTabHeader("OEE");
    this.setActiveTabSidebar("Online");

    this.getTimeStatus(this.opt);
    this.getReason(this.opt);
    this.getBasicData(this.opt);
    this.getTableOEE(this.opt);

    Highcharts.setOptions({
      global: {
        timezoneOffset: -3 * 60,
      }
    });
  },

  components: {
    pointTable: Table,
    VchartBox: VchartBox,
    Loader: Loader,
  },

  data() {
    return {
      isVchartBoxVisible: false,
      range: range,
      periodActive: [false, true, false, false, false],
      // cntPoint: 5,
      selected: "spline",
      typeChart: [{value: "area"}, {value: "column"}, {value: "line"}],
      opt: {
        smena: 1,
        idx: this.idx ? this.idx : 0,
        chart: 'OEE',
        start: parseInt((nowDateTime - range) / 1000),
        end: parseInt(nowDateTime / 1000),
      },
    };
  },

  computed: {
    ...mapGetters("oeecharts", {
      idx: "selectChart",
      arrPoint: "arrPoint",
      currentArrPoint: "currentArrPoint",
      basicData: "basicData",
      basicOptions: "basicOptions",
      activeshop: "activeshop",
      reason: "reason",
      timeStatus: "timeStatus",
      loader: "loader",
      tableOEE: "tableOEE",
      isChartOne: "isChartOne",
    }),

    timeStatusOut() {
      let newTimeStatus = {};
      for (let key in this.timeStatus)
        if (this.timeStatus.hasOwnProperty(key))
          newTimeStatus[key] = formatTime(this.timeStatus[key]);

      return newTimeStatus;
    },

    dataHead() {
      let statusOEE = "ok";
      let statusA = "ok";
      let statusP = "ok";
      let statusQ = "ok";

      let OEE = this.chartOptions.OEE;
      let A = this.chartOptions.A;
      let P = this.chartOptions.P;
      let Q = this.chartOptions.Q;

      if (OEE < 45) {
        statusOEE = "dng";
      } else if (OEE < 65) {
        statusOEE = "alert";
      }
      if (A < 45) {
        statusA = "dng";
      } else if (A < 65) {
        statusA = "alert";
      }
      if (P < 45) {
        statusP = "dng";
      } else if (P < 65) {
        statusP = "alert";
      }
      if (Q < 45) {
        statusQ = "dng";
      } else if (Q < 65) {
        statusQ = "alert";
      }

      return {
        statusOEE: statusOEE,
        statusA: statusA,
        statusP: statusP,
        statusQ: statusQ,
      };
    },

    content: function () {
      return {
        opt: this.opt,
        title: "Настройка отображения графиков",
        btnLeft: "Экспорт",
        btnRight: "Обновить",
        selectLeft: "Графики - все в одном",
        selectRight: "Графики - все отдельно",
      };
    },

    chartOptions() {
      let arrOptions = {};
      let chartOption;
      chartOption = {
        chart: this.basicOptions.chart,

        navigator: {
          adaptToUpdatedData: true,
          series: [
            {data: this.basicData[3]},
          ],
        },

        scrollbar: this.basicOptions.scrollbar,

        exporting: {
          enabled: false,
        },

        credits: {
          enabled: false,
        },

        legend: this.basicOptions.legendAll,
        yAxis: this.basicOptions.yAxisAll,
        xAxis: {
          range: this.range,
          // plotLines: this.arrPoint,
          plotLines: this.currentArrPoint,
        },

        tooltip: this.basicOptions.tooltip,

        rangeSelector: {
          enabled: false,
        },

        plotOptions: {
          xrange: {
            showInLegend: false,

            borderRadius: 0,
            borderWidth: 0,
            pointWidth: 100,
            grouping: false,
            colorByPoint: true,
            point: {
              events: {
                click: (e) => {
                },
              },
            },
          },

          series: {
            cursor: "pointer",
            events: {
              legendItemClick: function (e) {
                legendVisible[this.name] = !this.visible;
              },
            },

            point: {
              events: {
                click: (e) => {
                  this.sendPoint(e);
                  return;
                },
              },
            },
          },
        },

        series: [
          {
            name: "A",
            type: this.selected,
            yAxis: 0,
            keys: ["x", "y", "id"],
            data: this.basicData.length ? this.basicData[0] : [],
            visible: legendVisible.A,
            showInNavigator: true || legendVisible.A,
          },
          {
            name: "P",
            type: this.selected,
            yAxis: 1,
            keys: ["x", "y", "id"],
            data: this.basicData.length ? this.basicData[1] : [],
            visible: legendVisible.P,
            showInNavigator: true || legendVisible.P,
          },
          {
            name: "Q",
            type: this.selected,
            yAxis: 2,
            keys: ["x", "y", "id"],
            data: this.basicData.length ? this.basicData[2] : [],
            visible: legendVisible.Q,
            showInNavigator: true || legendVisible.Q,
          },
          {
            name: "OEE",
            type: this.selected,
            yAxis: 3,
            keys: ["x", "y", "id"],
            data: this.basicData.length ? this.basicData[3] : [],
            visible: legendVisible.OEE,
            showInNavigator: true || legendVisible.OEE,
          },
          {
            name: "работает",
            type: "xrange",
            yAxis: 4,
            keys: ["x", "x2", "y", "id", "color"],
            data: this.basicData.length ? this.basicData[5] : [],
          },
          {
            name: "простой",
            type: "xrange",
            yAxis: 5,
            keys: ["x", "x2", "y", "id", "color"],
            data: this.basicData.length ? this.basicData[6] : [],
          },
          {
            name: "выключен",
            type: "xrange",
            yAxis: 6,
            keys: ["x", "x2", "y", "id", "color"],
            data: this.basicData.length ? this.basicData[7] : [],
          },

          {
            name: "авария",
            type: "xrange",
            yAxis: 7,
            keys: ["x", "x2", "y", "id", "color"],
            data: this.basicData.length ? this.basicData[8] : [],
          },
        ],
      };


      let chartOptionA = {
        chart: this.basicOptions.chart,

        navigator: {
          adaptToUpdatedData: true,
          series: [
            {data: this.basicData[0]},
          ],
        },

        scrollbar: this.basicOptions.scrollbar,

        exporting: {
          enabled: false,
        },

        credits: {
          enabled: false,
        },

        legend: this.basicOptions.legendAll,
        yAxis: this.basicOptions.yAxisAll,
        xAxis: {
          range: this.range,
          // plotLines: this.arrPoint,
          plotLines: this.currentArrPoint,
        },

        tooltip: this.basicOptions.tooltip,

        rangeSelector: {
          enabled: false,
        },

        plotOptions: {
          xrange: {
            showInLegend: false,

            borderRadius: 0,
            borderWidth: 0,
            pointWidth: 100,
            grouping: false,
            colorByPoint: true,
            point: {
              events: {
                click: (e) => {
                },
              },
            },
          },

          series: {
            cursor: "pointer",
            events: {
              // legendItemClick: function (e) {
              //   legendVisible[this.name] = !this.visible;
              // },
            },

            point: {
              events: {
                click: (e) => {
                  this.sendPoint(e);
                  return;
                },
              },
            },
          },
        },

        series: [
          {
            name: "A",
            type: this.selected,
            yAxis: 0,
            keys: ["x", "y", "id"],
            data: this.basicData.length ? this.basicData[0] : [],
            color: '#ffdb66'
          },
          {
            name: "работает",
            type: "xrange",
            yAxis: 4,
            keys: ["x", "x2", "y", "id", "color"],
            data: this.basicData.length ? this.basicData[5] : [],
          },
          {
            name: "простой",
            type: "xrange",
            yAxis: 5,
            keys: ["x", "x2", "y", "id", "color"],
            data: this.basicData.length ? this.basicData[6] : [],
          },
          {
            name: "выключен",
            type: "xrange",
            yAxis: 6,
            keys: ["x", "x2", "y", "id", "color"],
            data: this.basicData.length ? this.basicData[7] : [],
          },

          {
            name: "авария",
            type: "xrange",
            yAxis: 7,
            keys: ["x", "x2", "y", "id", "color"],
            data: this.basicData.length ? this.basicData[8] : [],
          },
        ],
      };

      let chartOptionP = {
        chart: this.basicOptions.chart,

        navigator: {
          adaptToUpdatedData: true,
          series: [
            {data: this.basicData[1]},
          ],
        },

        scrollbar: this.basicOptions.scrollbar,

        exporting: {
          enabled: false,
        },

        credits: {
          enabled: false,
        },

        legend: this.basicOptions.legendAll,
        yAxis: this.basicOptions.yAxisAll,
        xAxis: {
          range: this.range,
          // plotLines: this.arrPoint,
          plotLines: this.currentArrPoint,
        },

        tooltip: this.basicOptions.tooltip,

        rangeSelector: {
          enabled: false,
        },

        plotOptions: {
          xrange: {
            showInLegend: false,

            borderRadius: 0,
            borderWidth: 0,
            pointWidth: 100,
            grouping: false,
            colorByPoint: true,
            point: {
              events: {
                click: (e) => {
                },
              },
            },
          },

          series: {
            cursor: "pointer",
            events: {
              // legendItemClick: function (e) {
              //   legendVisible[this.name] = !this.visible;
              // },
            },

            point: {
              events: {
                click: (e) => {
                  this.sendPoint(e);
                  return;
                },
              },
            },
          },
        },

        series: [
          {
            name: "P",
            type: this.selected,
            yAxis: 0,
            keys: ["x", "y", "id"],
            data: this.basicData.length ? this.basicData[1] : [],
            color: '#8ccf9c',
          },
          {
            name: "работает",
            type: "xrange",
            yAxis: 4,
            keys: ["x", "x2", "y", "id", "color"],
            data: this.basicData.length ? this.basicData[5] : [],
          },
          {
            name: "простой",
            type: "xrange",
            yAxis: 5,
            keys: ["x", "x2", "y", "id", "color"],
            data: this.basicData.length ? this.basicData[6] : [],
          },
          {
            name: "выключен",
            type: "xrange",
            yAxis: 6,
            keys: ["x", "x2", "y", "id", "color"],
            data: this.basicData.length ? this.basicData[7] : [],
          },

          {
            name: "авария",
            type: "xrange",
            yAxis: 7,
            keys: ["x", "x2", "y", "id", "color"],
            data: this.basicData.length ? this.basicData[8] : [],
          },
        ],
      };

      let chartOptionQ = {
        chart: this.basicOptions.chart,

        navigator: {
          adaptToUpdatedData: true,
          series: [
            {data: this.basicData[2]},
          ],
        },

        scrollbar: this.basicOptions.scrollbar,

        exporting: {
          enabled: false,
        },

        credits: {
          enabled: false,
        },

        legend: this.basicOptions.legendAll,
        yAxis: this.basicOptions.yAxisAll,
        xAxis: {
          range: this.range,
          // plotLines: this.arrPoint,
          plotLines: this.currentArrPoint,
        },

        tooltip: this.basicOptions.tooltip,

        rangeSelector: {
          enabled: false,
        },

        plotOptions: {
          xrange: {
            showInLegend: false,

            borderRadius: 0,
            borderWidth: 0,
            pointWidth: 100,
            grouping: false,
            colorByPoint: true,
            point: {
              events: {
                click: (e) => {
                },
              },
            },
          },

          series: {
            cursor: "pointer",
            events: {
              // legendItemClick: function (e) {
              //   legendVisible[this.name] = !this.visible;
              // },
            },

            point: {
              events: {
                click: (e) => {
                  this.sendPoint(e);
                  return;
                },
              },
            },
          },
        },

        series: [
          {
            name: "Q",
            type: this.selected,
            yAxis: 0,
            keys: ["x", "y", "id"],
            data: this.basicData.length ? this.basicData[2] : [],
            color: '#66b0ff',
          },
          {
            name: "работает",
            type: "xrange",
            yAxis: 4,
            keys: ["x", "x2", "y", "id", "color"],
            data: this.basicData.length ? this.basicData[5] : [],
          },
          {
            name: "простой",
            type: "xrange",
            yAxis: 5,
            keys: ["x", "x2", "y", "id", "color"],
            data: this.basicData.length ? this.basicData[6] : [],
          },
          {
            name: "выключен",
            type: "xrange",
            yAxis: 6,
            keys: ["x", "x2", "y", "id", "color"],
            data: this.basicData.length ? this.basicData[7] : [],
          },

          {
            name: "авария",
            type: "xrange",
            yAxis: 7,
            keys: ["x", "x2", "y", "id", "color"],
            data: this.basicData.length ? this.basicData[8] : [],
          },
        ],
      };

      let chartOptionOEE = {
        chart: this.basicOptions.chart,

        navigator: {
          adaptToUpdatedData: true,
          series: [
            {data: this.basicData[3]},
          ],
        },

        scrollbar: this.basicOptions.scrollbar,

        exporting: {
          enabled: false,
        },

        credits: {
          enabled: false,
        },

        legend: this.basicOptions.legendAll,
        yAxis: this.basicOptions.yAxisAll,
        xAxis: {
          range: this.range,
          // plotLines: this.arrPoint,
          plotLines: this.currentArrPoint,
        },

        tooltip: this.basicOptions.tooltip,

        rangeSelector: {
          enabled: false,
        },

        plotOptions: {
          xrange: {
            showInLegend: false,

            borderRadius: 0,
            borderWidth: 0,
            pointWidth: 100,
            grouping: false,
            colorByPoint: true,
            point: {
              events: {
                click: (e) => {
                },
              },
            },
          },

          series: {
            cursor: "pointer",
            events: {
              // legendItemClick: function (e) {
              //   legendVisible[this.name] = !this.visible;
              // },
            },

            point: {
              events: {
                click: (e) => {
                  this.sendPoint(e);
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
            data: this.basicData.length ? this.basicData[3] : [],
            color: '#000000',
          },
          {
            name: "работает",
            type: "xrange",
            yAxis: 4,
            keys: ["x", "x2", "y", "id", "color"],
            data: this.basicData.length ? this.basicData[5] : [],
          },
          {
            name: "простой",
            type: "xrange",
            yAxis: 5,
            keys: ["x", "x2", "y", "id", "color"],
            data: this.basicData.length ? this.basicData[6] : [],
          },
          {
            name: "выключен",
            type: "xrange",
            yAxis: 6,
            keys: ["x", "x2", "y", "id", "color"],
            data: this.basicData.length ? this.basicData[7] : [],
          },

          {
            name: "авария",
            type: "xrange",
            yAxis: 7,
            keys: ["x", "x2", "y", "id", "color"],
            data: this.basicData.length ? this.basicData[8] : [],
          },
        ],
      };

      arrOptions = {
        id: this.idx,
        name: this.idx + 1,
        option: chartOption,
        optionA: chartOptionA,
        optionP: chartOptionP,
        optionQ: chartOptionQ,
        optionOEE: chartOptionOEE,
        A: (this.tableOEE.A * 100).toFixed(),
        P: (this.tableOEE.P * 100).toFixed(),
        Q: (this.tableOEE.Q * 100).toFixed(),
        OEE: (this.tableOEE.OEE * 100).toFixed(),
      };


      if (this.opt.idx !== this.idx) {
        this.opt.idx = this.idx;
        this.getTimeStatus(this.opt);
        this.getReason(this.opt);
        this.getBasicData(this.opt);
        this.getTableOEE(this.opt);
      }
      return arrOptions;
    },

    chartOptionsTop5() {
      return {
        option: {
          chart: {
            type: 'column',
            inverted: true
          },
          title: {
            text: 'TOP 5 причин простоя',
            style: {
              fontSize: 14
            },
            margin: 5
          },

          exporting: {
            enabled: false,
          },

          credits: {
            enabled: false,
          },

          accessibility: {
            announceNewData: {
              enabled: true
            }
          },
          xAxis: {
            type: 'category'
          },
          yAxis: {
            title: {
              enabled: false
            },

          },

          legend: {
            enabled: false
          },
          plotOptions: {
            series: {
              borderWidth: 0,
              dataLabels: {
                enabled: true,
                formatter: function () {
                  return formatTime(this.y);
                }
              }
            }
          },

          series: [
            {
              colorByPoint: true,
              data: this.reason
            }
          ],
          tooltip: {
            formatter: function () {
              return this.y + 'сек';
            }
          },
        }
      }
    },
  },

  methods: {
    ...mapActions("oeecharts", {
      nextChart: "nextChart",
      prevChart: "prevChart",
      addPoint: "addPoint",
      removePoint: "removePoint",
      getBasicData: "getBasicData",
      getTimeStatus: "getTimeStatus",
      getReason: "getReason",
      loadBasicOptions: "loadBasicOptions",
      getTableOEE: "getTableOEE",
    }),
    ...mapActions("users", {
      setActiveTabHeader: "setActiveTabHeader",
      setActiveTabSidebar: "setActiveTabSidebar",
    }),

    setRange(sel) {
      this.range = sel.period * 1000 * 3600;
      this.periodActive = this.periodActive.map((item) => false);
      this.periodActive.splice(sel.id, 1, true);

      this.opt.start = this.opt.end - sel.period * 3600;
      if (sel.period === 8)
        this.opt.smena = 1;
      else
        this.opt.smena = 0;
      this.getTimeStatus(this.opt);
      this.getReason(this.opt);
      this.getBasicData(this.opt);
      this.getTableOEE(this.opt);
    },

    showVchartBoxVisible() {
      this.isVchartBoxVisible = true;
    },
    closeVchartBoxVisible() {
      this.isVchartBoxVisible = false;
    },

    changeFistData(val) {
      console.log(val);
      //this.fistDate =formatDate(val);
    },
    changeLastData(val) {
      //this.lastDate =formatDate(val);
    },
/////////////////
    sendPoint(e) {
      let dateX = new Date(e.point.x);
      dateX.getTimezoneOffset();
      let idxPoint = this.idx;
      let xPoint = {
        machineid: idxPoint,
        X: formatDate(dateX),
        A: this.basicData[0].length ? this.basicData[0][e.point.index][1] : "",
        P: this.basicData[0].length ? this.basicData[1][e.point.index][1] : "",
        Q: this.basicData[0].length ? this.basicData[2][e.point.index][1] : "",
        OEE: this.basicData[3][e.point.index][1],
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
  -  hour < 10 ? "0" + hour : hour;
  minutes = minutes < 10 ? "0" + minutes : minutes;

  return `${dayOfMonth}.${month}.${year} ${hour}:${minutes}`;
}

function formatTime(time) {
  let hour = Math.trunc(time / 3600);
  let min = Math.trunc((time - hour * 3600) / 60);
  let sec = time - hour * 3600 - min * 60;
  return `${hour}h:${min}m:${sec}s`;
}
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

div {
  cursor: default;
}

.section {
  width: 100%;
  height: 100%;
  align-self: center;
  text-align: center;
  padding-top: 228px;
}

.charts-items {
  height: 100%;
  width: 100%;
  padding-left: 24px;
  padding-right: 18px;
  overflow-y: auto;
  padding-bottom: 50px;
}

.highchart {
  width: 100%;
  margin-top: 24px;
  height: 296px;
}

.highchartBar {
  width: 100%;
  /* margin-top: 24px; */
  padding-right: 24px;
  height: 100%;
}

.title-panel {
  background-color: #f9fafc;
  background-repeat: no-repeat;
  border-bottom: 1px solid hsl(220, 33%, 88%);

  font-weight: 500;
  font-size: 14px;
  line-height: 17px;

  align-items: center;

  display: flex;
  flex-direction: row;
  flex-wrap: wrap;

  justify-content: space-between;
  width: 100%;
  left: 0;
  height: 48px;
  padding-left: 120px;

  position: absolute;
  top: 48px;
}

.headMenu {
  margin-left: 30px;
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

.sub-panel {
  background-repeat: no-repeat;

  font-weight: 500;
  font-size: 14px;
  line-height: 17px;

  align-items: center;

  display: flex;
  flex-direction: row;
  flex-wrap: wrap;

  justify-content: flex-start;

  width: 100%;
  left: 0;
  padding-left: 156px;
  height: 156px;

  position: absolute;
  top: 120px;
}

.oee-current {
  padding: 5px;
  font-weight: 600;
  font-size: 36px;
  line-height: 44px;
  display: flex;
  justify-content: space-between;

  letter-spacing: 0.05em;

  color: #721c24;
  width: 304px;
  height: 156px;
}

.oee-items {
  display: flex;
  flex-direction: column;
}

.left {
  justify-content: flex-start;
  align-items: flex-start;
}

.right {
  justify-content: flex-end;
  align-items: flex-end;
}

.oee-item {
  font-weight: 600;
  font-size: 10px;
  line-height: 12px;
  display: flex;
  flex-direction: column;

  color: #9098af;
}

.oee-item.left {
  padding-left: 5px;
}

.apq-current {
  font-weight: 600;
  font-size: 18px;
  line-height: 22px;
  display: flex;
  align-items: center;

  color: #721c24;

  width: 100px;
  height: 156px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;

  padding-left: 6px;
}

.apq-current p {
  font-size: 10px;
  line-height: 12px;
}

.apq-item {
  width: 100px;
  height: 48px;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  justify-content: center;
  padding-left: 5px;
}

.time-items {
  margin-left: 36px;
  width: 120px;
  height: 156px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.time-item {
  font-weight: 600;
  font-size: 10px;
  line-height: 12px;

  color: #9098af;

  width: 120px;
  height: 30px;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  justify-content: center;
}

.time-item p {
  color: #4a627a;
}

.top5 {
  margin-left: auto;
  /* background-image: url("../assets/img/top5.jpg"); */
  height: 156px;
  width: 736px;
}

.btn_icon {
  cursor: pointer;
  background: none;
  border: none;

  display: flex;
  justify-content: baseline;
  outline: none;
}

.btn-submenu {
  cursor: pointer;
  color: #3f51b5;
}

.btn-submenu:hover {
  color: hsl(231, 48%, 45%);
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

.dng {
  background: #f7dcdf;
  color: #721c24;
}

.alert {
  background: #fff3cd;
  color: #856404;
}

.ok {
  background: #d4edda;
  color: #155724;
}
</style>
