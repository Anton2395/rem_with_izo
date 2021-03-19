
<template>
  <div :id="'element' + id" :ref="'element' + id">
    <div class="accordion" id="accordion">
      <div class="accordion-item">
        <h3
          class="accordion-item-head"
          @click="openedAccordion = !openedAccordion"
        >
          {{ dataWorkArea.name }}
          <IconifyIcon
            class="arrow left-arrow arrow-down"
            :class="{ 'arrow-up': openedAccordion }"
            icon="baselineKeyboardArrowDown"
            :style="{ fontSize: '24px' }"
          />
        </h3>
        <div class="accordion-item-body" v-show="openedAccordion">
          <div class="recorder-menu">
            <div class="menu">
              <div
                class="menu-svg addrem"
                @click="openVBoxAddChart = true"
              ></div>
              <div
                class="menu-svg type"
                @click="visibleTypeLine = !visibleTypeLine"
              ></div>
              <div class="typeLine" v-show="visibleTypeLine">
                <ul>
                  <li @click="changeTypeChart('line')">
                    <img src="@/assets/img/typeLine1.svg" />Line
                  </li>
                  <li @click="changeTypeChart('spline')">
                    <img src="@/assets/img/typeLine2.svg" />Spline
                  </li>
                  <li @click="changeTypeChart('step')">
                    <img src="@/assets/img/typeLine3.svg" />Step
                  </li>
                  <li @click="changeTypeChart('area')">
                    <img src="@/assets/img/typeLine4.svg" />Area
                  </li>
                  <li @click="changeTypeChart('point')">
                    <img src="@/assets/img/typeLine5.svg" />Point
                  </li>
                  <li @click="changeTypeChart('boxplot')">
                    <img src="@/assets/img/typeLine6.svg" />Box plot
                  </li>
                </ul>
              </div>
              <div class="menu-svg online"></div>
              <div class="menu-svg gannt"></div>
              <div class="menu-svg formule"></div>
              <div class="menu-svg resize" @click="changeHeightChart()"></div>
              <div class="menu-svg bulity"></div>
            </div>
          </div>
          <div class="rangeButton">
            Период
            <button class="button-range" @click="setRange({ period: 'hour' })">
              Час
            </button>
            <button class="button-range" @click="setRange({ period: 'shift' })">
              Смена
            </button>
            <button class="button-range" @click="setRange({ period: 'day' })">
              День
            </button>
            <button class="button-range" @click="setRange({ period: 'week' })">
              Неделя
            </button>
            <button class="button-range" @click="setRange({ period: 'month' })">
              Месяц
            </button>
          </div>
          <div>
            <highcharts
              style="margin-right: 20px"
              :constructorType="'stockChart'"
              class="hc"
              :options="chartOptions"
              ref="chart"
            ></highcharts>
          </div>
        </div>
      </div>
    </div>
    <VBoxAddChart
      v-if="openVBoxAddChart"
      @closeForm="openVBoxAddChart = false"
      :Vdata="dataWorkArea"
    />
    <!-- <button @click="onLog">qwerqe</button> -->
  </div>
</template>

<script>
let returnDateFormat = (date) => {
  date = new Date(date);
  return `${date.getFullYear()}-${
    (date.getMonth() + 1).toString().length != 2
      ? "0" + (date.getMonth() + 1)
      : date.getMonth() + 1
  }-${
    date.getDate().toString().length != 2
      ? "0" + date.getDate()
      : date.getDate()
  } ${
    date.getHours().toString().length != 2
      ? "0" + date.getHours()
      : date.getHours()
  }:${
    date.getMinutes().toString().length != 2
      ? "0" + date.getMinutes()
      : date.getMinutes()
  }:${
    date.getSeconds().toString().length != 2
      ? "0" + date.getSeconds()
      : date.getSeconds()
  }`;
};
// import { error } from "highcharts";
import {
  VsaList,
  VsaItem,
  VsaHeading,
  VsaContent,
  VsaIcon,
} from "vue-simple-accordion";
import Table from "@/components/Table";
import VBoxAddChart from "@/components/VBoxAddChart";
import "vue-simple-accordion/dist/vue-simple-accordion.css";
import moment from 'moment';

export default {
  props: ["baseUrl", "dataWorkArea", "id"],
  components: {
    VsaList,
    VsaItem,
    VsaHeading,
    VsaContent,
    VsaIcon,
    pointTable: Table,
    VBoxAddChart: VBoxAddChart,
  },
  data() {
    return {
      visibleTypeLine: false,
      visibleStatus: false,
      dateSt: "",
      dateEnd: "",
      enableFetch: true,
      dataNavigator: [],
      lastUrl: "",
      openedAccordion: false,
      openVBoxAddChart: false,
      chartOptions: {
        chart: {
          height: 400,
          type: "line",
          zoomType: "x",
          events: {
            load: (function (self) {
              return function () {
                self.chart = this; // saving chart reference in the component
              };
            })(this),
          },
        },
        tooltip: {
          shared: true,
          // xDateFormat: '%Y-%m-%d',
          formatter(){
            // points[0].series.userOptions.yAxis - единицы измерения
            // points[0].y величина
            // x - дата
            // points[0].series.userOptions.name - имя 
            // points[0].color
            // console.log(this);
            moment.locale('ru');
            return ["<span>"+ moment(this.x).format('LLL') + "</span>"].concat(
                this.points ?
                    this.points.map(function (point) {
                        return ["<span>" + point.series.name + ': ' + point.y + point.series.userOptions.yAxis + "</span>"];
                    }) : []
            );
          }
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
        credits: {
          enabled: false,
        },
        exporting: {
          enabled: false,
        },
        navigator: {
          adaptToUpdatedData: false,
          series: {
            data: this.dataNavigator,
          },
          xAxis: {
            tickAmount: 200,
          },
        },
        rangeSelector: {
          enabled: false,
          inputEnabled: false,
          // selected: 2,

          buttonSpacing: 10,
          buttonTheme: {
            // styles for the buttons
            width: 45,
            style: {
              color: "#000000",
            },
            states: {
              hover: {
                fill: "#42A5F5",
                style: {
                  color: "white",
                },
              },
              select: {
                fill: "#29B6F6",
                style: {
                  color: "white",
                },
              },
            },
          },
        },
        legend: {
          enabled: true,
          labelFormatter: function () {
            return (
              '<span style="color: ' + this.color + '">' + this.name + "</span>"
            );
          },
          // squareSymbol: true,
          layout: "horizontal",
          align: "center",
          verticalAlign: "top",
          // symbolHeight: 11,
          // symbolWidth: 11,
          // symbolRadius: 0,
          // symbolWidth: 12,
          // symbolRadius: 6,
          itemStyle: {
            fontFamily: "Montserrat",
            fontSize: "14px",
          },
        },
        yAxis: [],
        xAxis: {
          events: {
            setExtremes: this.getNewDate,
          },
        },
        time: {
          useUTC: false,
        },

        series: [],
      },
    };
  },
  async mounted() {
    this.getData();
    await this.$nextTick();
  },
  methods: {
    onLog() {
      console.log(this.chart);
    },
    changeHeightChart() {
      if (this.chartOptions.chart.height == 400) {
        this.chartOptions.chart.height = 710;
      } else {
        this.chartOptions.chart.height = 400;
      }

      let el = document.getElementById("element" + this.id);
      setTimeout(function () {
        el.scrollIntoView({
          block: "center",
          behavior: "smooth",
          inline: "nearest",
        });
      }, 500);
    },
    changeTypeChart(type) {
      switch (type) {
        case "line":
        case "spline":
        case "area":
          this.chartOptions.chart.type = type;
          this.chartOptions.series.forEach((item) => {
            item.step = false;
            item.lineWidth = 2;
            item.marker = {
              enabled: false,
              radius: 2,
            };
          });

          break;
        case "step":
          this.chartOptions.chart.type = "line";
          this.chartOptions.series.forEach((item) => {
            item.step = true;
            item.lineWidth = 2;
            item.marker = {
              enabled: false,
              radius: 2,
            };
          });

          break;

        case "point":
          this.chartOptions.chart.type = "line";
          this.chartOptions.series.forEach((item) => {
            item.step = false;
            item.lineWidth = 0;
            item.marker = {
              enabled: true,
              radius: 3,
              lineWidth: 1,
            };
          });
          break;
      }
      this.visibleTypeLine = false;
    },
    accordion: function (event) {
      event.target.classList.toggle("active");
    },
    setNewExtremes: function (min, max) {
      this.chart.xAxis[0].setExtremes(
        Math.round(min / 1000) * 1000,
        Math.round(max / 1000) * 1000
      );
    },

    /**
     * получение даных для графика с сервера
     *
     * @param {string} key ключ для запроса данных с сервера. Доступны [hour,shift,day,week,month]
     * @param  {boolean}  updNavigator  флаг для обновления навигатора
     */
    async getData(key = "month", updNavigator = true) {
      this.chart.showLoading();
      await this.$axios
        .$get(`${this.baseUrl}&key=${key}`)
        .then((data) => {
          if (data.child[0].values.length != 0) {
            let emptyYAxis = {
              reversed: false,
              opposite: false,
              title: {
                style: {
                  fontSize: 14,
                  fontFamily: "montserrat",
                },
                enabled: true,
                text: "",
              },
            };
            let AllYAxis = [];
            let valueYAxis=[];
            data.child.forEach((item)=>{
              valueYAxis.push(item.sensor_data.unit);
            });
            valueYAxis = Array.from(new Set(valueYAxis));

            valueYAxis.forEach((el,i)=>{
              let yAx=JSON.parse(JSON.stringify(emptyYAxis));
              yAx.title.text = el;
              yAx.id = el;
              if (i!=0){
              yAx.opposite=!AllYAxis[i-1].opposite; 
              }
              AllYAxis.push(yAx);
            });  


            
            this.chartOptions.yAxis=AllYAxis;
            this.chartOptions.series = this.setArray(data);

            

            if (updNavigator) {
              this.chartOptions.navigator.series = JSON.parse(JSON.stringify(this.chartOptions.series)).map((el)=>{
                delete el.yAxis;
                return el;
              });
              
            }
          }
          this.chart.hideLoading();
        })
        .catch((e) => {
          console.log(e);
          this.chart.hideLoading();
        });
    },
    setArray(data,yAxis_value) {
      let newArraySeries = [];
      data.child.forEach((el, i) => {
        let newObj = { name: el.sensor_data.name, color: el.color,yAxis:el.sensor_data.unit};
        newObj.data = [];
        if (el.values.length != 0) {
          el.values.forEach((item) => {
            if (item.value != null) {
              if (item.start_time) {
                newObj.data.push({
                  x: Date.parse(item.start_time),
                  y: item.value,
                });
              } else if (item.now_time) {
                newObj.data.push({
                  x: Date.parse(item.now_time),
                  y: item.value,
                });
              }
            }
          });
          newObj.data.sort((a, b) => a.x - b.x);
          newArraySeries.push(newObj);
        }
      });
      return newArraySeries;
    },
    async getNewDate(e) {
      let min = Math.round(e.min); //+(new Date().getTimezoneOffset()*60*1000);
      let max = Math.round(e.max); //+(new Date().getTimezoneOffset()*60*1000);
      if (
        ((e.triggerOp && e.DOMEvent.type == "mouseup") ||
          (e.triggerOp && e.DOMEvent.type == "click") ||
          e.triggerOp == undefined) &&
        e.trigger != undefined
      ) {
        let { chart } = e.target;
        if (min.toString() != "NaN" && max.toString() != "NaN") {
          chart.showLoading("Загрузка данных с сервера...");
          let minTime = returnDateFormat(min); //<str:YYYY-MM-DD HH:mm:SS>
          let maxTime = returnDateFormat(max);
          if (
            this.lastUrl != `${this.baseUrl}&start=${minTime}&end=${maxTime}`
          ) {
            this.lastUrl = `${this.baseUrl}&start=${minTime}&end=${maxTime}`;
            await this.$axios
              .$get(`${this.baseUrl}&start=${minTime}&end=${maxTime}`)
              .then((data) => {
                let tempArr = this.setArray(data);

                let tempArr2 = [];

                tempArr.forEach((el, i) => {
                  if (el.data.length > 1) {
                    tempArr2.push(el);
                  } else {
                    tempArr2.push(this.chartOptions.series[i]);
                  }
                });

                this.chartOptions.series = tempArr2;

                console.log(this.chartOptions.series[0].data[0].x);
                console.log(
                  this.chartOptions.series[0].data[
                    this.chartOptions.series[0].data.length - 1
                  ].x
                );

                this.setNewExtremes(
                  this.chartOptions.series[0].data[0].x,
                  this.chartOptions.series[0].data[
                    this.chartOptions.series[0].data.length - 1
                  ].x
                );
                chart.hideLoading();
              })
              .catch((error) => {
                chart.hideLoading();
                console.error(error.message);
              });
          }
        }
      }
    },

    async getExtNewDate(e) {
      this.chart.showLoading("Загрузка данных с сервера...");
      let minTime = e.min; //<str:YYYY-MM-DD HH:mm:SS>
      let maxTime = e.max;
      this.chart.showLoading();
      if (this.lastUrl != `${this.baseUrl}&start=${minTime}&end=${maxTime}`) {
        this.lastUrl = `${this.baseUrl}&start=${minTime}&end=${maxTime}`;
        await this.$axios
          .$get(`${this.baseUrl}&start=${minTime}&end=${maxTime}`)
          .then((data) => {
            let tempArr = this.setArray(data);

            let tempArr2 = [];

            tempArr.forEach((el, i) => {
              if (el.data.length > 1) {
                tempArr2.push(el);
              } else {
                tempArr2.push(this.chartOptions.series[i]);
              }
            });

            this.chartOptions.series = tempArr2;

            console.log(this.chartOptions.series[0].data[0].x);
            console.log(
              this.chartOptions.series[0].data[
                this.chartOptions.series[0].data.length - 1
              ].x
            );

            this.setNewExtremes(
              this.chartOptions.series[0].data[0].x,
              this.chartOptions.series[0].data[
                this.chartOptions.series[0].data.length - 1
              ].x
            );
            this.chart.hideLoading();
          })
          .catch((error) => {
            this.chart.hideLoading();
            console.error(error.message);
          });
      }
    },

    setRange(sel) {
      this.getData(sel.period, false);
      // debugger;
      try {
        this.setNewExtremes(
          this.chartOptions.series[0].data[0].x,
          this.chartOptions.series[0].data[
            this.chartOptions.series[0].data.length - 1
          ].x
        );
      } catch {
        console.error("Чтото пошло не так!");
      }
    },
  },
  // watch:{
  //   dataWorkArea: {
  //     handler(role) {
  //       if (role) {
  //         this.nameWorkArea = role.name;
  //       }
  //     },
  //     immediate: true,
  //   },
  // }
};
</script>

<style>
/* .accordion{
  padding-bottom: 12px;
} */
.accordion-item-body {
  margin-right: 40px;
}
.recorder-menu {
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.menu {
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 20;
  margin-left: auto;
  margin-right: 1.4em;
  margin-top: -50px;
}
.menu-svg {
  cursor: pointer;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  margin-left: 12px;
}
.addrem {
  background-image: url("~assets/svg/recorder/addRemoveGraph.svg");
  background-position: center;
  background-repeat: no-repeat;
  background-size: contain;
}
.addrem:hover {
  background-image: url("~assets/svg/recorder/AddRemoveGraphAct.svg");
}

.type {
  background-image: url("~assets/svg/recorder/typeGraph.svg");
  background-position: center;
  background-repeat: no-repeat;
  background-size: contain;
}
.type:hover {
  background-image: url("~assets/svg/recorder/hovTypeGraph.svg");
}

.online {
  background-image: url("~assets/svg/recorder/onlinePlay.svg");
  background-position: center;
  background-repeat: no-repeat;
  background-size: contain;
}

.online:hover {
  background-image: url("~assets/svg/recorder/hovOnlinePlay.svg");
}

.gannt {
  background-image: url("~assets/svg/recorder/DiagrGannt.svg");
  background-position: center;
  background-repeat: no-repeat;
  background-size: contain;
}

.gannt:hover {
  background-image: url("~assets/svg/recorder/hovDiagrammGrannt.svg");
}

.formule {
  background-image: url("~assets/svg/recorder/formule.svg");
  background-position: center;
  background-repeat: no-repeat;
  background-size: contain;
}
.formule:hover {
  background-image: url("~assets/svg/recorder/hovFormule.svg");
}

.resize {
  background-image: url("~assets/svg/recorder/resizeGraph.svg");
  background-position: center;
  background-repeat: no-repeat;
  background-size: contain;
}
.resize:hover {
  background-image: url("~assets/svg/recorder/hovResizeGraph.svg");
}
.bulity {
  background-image: url("~assets/svg/recorder/menu.svg");
  background-position: center;
  background-repeat: no-repeat;
  background-size: contain;
}
.bulity:hover {
  background-image: url("~assets/svg/recorder/hovAddicationMenu.svg");
}
.accordion-item {
  position: relative;
}
.rangeSelector {
  font-size: 12px;
  margin-left: 35px;
}
.rangeSelector button {
  border: 1px solid black;
  border-radius: 2px;
  margin: 0 5px;
}
.rangeSelector button:hover {
  border: 1px solid #00b0ff;
}
.accordion-item-head {
  color: #46627d;
  font-weight: 500;
  font-size: 14px;
  line-height: 17px;
  letter-spacing: 0.05em;
  margin-left: 24px;
  margin-top: 0px;
  cursor: pointer;
  padding: 10px;
  display: flex;
  align-items: center;
}

/* .accordion-item-head:after {
  content: " > ";

  display: block;
  height: 25px;
  position: inherit;
  transform: rotate(90deg) scaleY(2);
  top: 6px;
  margin-right: auto;

} */

/* .accordion-item-head.active:after {
  content: " < ";
} */

/* .accordion-item-body {
  display: none;
} */
.accordion-item-head.active + .accordion-item-body {
  display: block !important;
}
.typeLine {
  width: 115px;
  height: 166px;
  background-color: white;
  position: absolute;
  left: 1565px;
  top: 31px;
  border: 1px solid #90a1b1;
}

.typeLine li {
  display: flex;
  margin: 3px -36px;
  cursor: pointer;
}
.button-range {
  font-size: 12px;
  font: "Montserrat";
  color: #00b0ff;
  border: 1px solid #00b0ff;
  border-radius: 5px;
  margin-left: 5px;
}

.rangeButton {
  font-size: 12px;
  margin-left: 40px;
  color: #46627d;
}

.arrow-up {
  transform: matrix(1, 0, 0, -1, 0, 0);
}
</style>

