
<template>
  <div :id="'element' + id" :ref="'element' + id">
    <div class="accordion" id="accordion">
      <div class="accordion-item">
        <h3
          style="margin-top: 10px"
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
                  <li class="type1" @click="changeTypeChart('line')">
                    <img src="~assets/svg/sqare.svg" />
                  </li>
                  <li class="type2" @click="changeTypeChart('spline')">
                    <img src="~assets/svg/sqare.svg" />
                  </li>
                  <li class="type3" @click="changeTypeChart('step')">
                    <img src="~assets/svg/sqare.svg" />
                  </li>
                  <li class="type4" @click="changeTypeChart('area')">
                    <img src="~assets/svg/sqare.svg" />
                  </li>
                  <li class="type5" @click="changeTypeChart('point')">
                    <img src="~assets/svg/sqare.svg" />
                  </li>
                  <!-- <li class="type6" @click="changeTypeChart('boxplot')">
                    <img src="~assets/svg/sqare.svg" />
                  </li> -->
                </ul>
              </div>
              <!-- <div class="menu-svg online"></div>
              <div class="menu-svg gannt"></div> -->
              <div
                class="menu-svg formule"
                @click="openStatisticsTableFunc()"
                v-bind:class="{}"
              ></div>
              <div class="menu-svg resize" @click="changeHeightChart()"></div>
              <div
                class="menu-svg bulity"
                @click="openFunctionGraphFunc()"
              ></div>
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
            <!-- <highcharts
              style="margin-right: 20px"
              :options="chartXRange"
            ></highcharts> -->
            <!-- Таблицы -->
            <pointTable
              style="margin-left: 40px; margin-bottom: 20px"
              :tData="dataTablePoint"
              v-show="dataTablePoint.length != 0"
            ></pointTable>
            <StatisticsTable
              v-if="openStatisticsTable"
              :chart="chartOptions.series"
              @closeForm="openStatisticsTable = false"
              style="margin-top: 20px; margin-left: 40px; margin-bottom: 30px"
            />
            <!-- Таблицы -->
          </div>
        </div>
      </div>
    </div>

    <VBoxAddChart
      :workspaces.sync="workspaces"
      v-if="openVBoxAddChart"
      @closeForm="openVBoxAddChart = false"
      :Vdata="dataWorkArea"
    />
    <VFunctionGraph
      v-show="openFunctionGraph"
      @changeShow="openFunctionGraph = false"
      :content="content"
      :topPosition="topPositionOpenFunctionGraf"
    />
    <!-- <button @click="onLog">qwerqe</button> -->
  </div>
  <!-- <button @click="onLog">qwerqe</button> -->
</template>

<script>
let returnDateFormat = (date) => {
  date = new Date(date)
  return `${date.getFullYear()}-${
    (date.getMonth() + 1).toString().length != 2
      ? '0' + (date.getMonth() + 1)
      : date.getMonth() + 1
  }-${
    date.getDate().toString().length != 2
      ? '0' + date.getDate()
      : date.getDate()
  } ${
    date.getHours().toString().length != 2
      ? '0' + date.getHours()
      : date.getHours()
  }:${
    date.getMinutes().toString().length != 2
      ? '0' + date.getMinutes()
      : date.getMinutes()
  }:${
    date.getSeconds().toString().length != 2
      ? '0' + date.getSeconds()
      : date.getSeconds()
  }`
}
// import { error } from "highcharts";
import {
  VsaList,
  VsaItem,
  VsaHeading,
  VsaContent,
  VsaIcon,
} from 'vue-simple-accordion'
import TableChart from '@/components/TableChart'
import VBoxAddChart from '@/components/VBoxAddChart'
import 'vue-simple-accordion/dist/vue-simple-accordion.css'
import moment from 'moment'
import VFunctionGraph from '@/components/VFunctionGraph'
import StatisticsTable from '@/components/StatisticsTable'
export default {
  props: ['baseUrl', 'dataWorkArea', 'id', 'workspaces'],
  components: {
    VsaList,
    VsaItem,
    VsaHeading,
    VsaContent,
    VsaIcon,
    pointTable: TableChart,
    VBoxAddChart: VBoxAddChart,
    VFunctionGraph,
    StatisticsTable,
  },
  data() {
    return {
      graphObjectLastZoom: null,
      setRangeVar: null,
      chart: null,
      visibleTypeLine: false,
      visibleStatus: false,
      dateSt: '',
      dateEnd: '',
      enableFetch: true,
      dataNavigator: [],
      lastUrl: '',
      openedAccordion: false,
      openVBoxAddChart: false,
      openFunctionGraph: false,
      openStatisticsTable: false,
      topPositionOpenFunctionGraf: 0,
      dataTablePoint: [],
      chartOptions: {
        chart: {
          height: 400,
          type: 'line',
          zoomType: 'x',
          events: {
            load: (function (self) {
              return function () {
                self.chart = this
              }
            })(this),
          },
        },
        tooltip: {
          shared: true,

          formatter() {
            moment.locale('ru')
            return ['<span>' + moment(this.x).format('LLL') + '</span>'].concat(
              this.points
                ? this.points.map(function (point) {
                    return [
                      '<span>' +
                        point.series.name +
                        ': ' +
                        point.y +
                        point.series.userOptions.yAxis +
                        '</span>',
                    ]
                  })
                : []
            )
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
          series: [],
          xAxis: {
            tickAmount: 200,
          },
        },
        rangeSelector: {
          enabled: false,
          inputEnabled: false,

          buttonSpacing: 10,
          buttonTheme: {
            width: 45,
            style: {
              color: '#000000',
            },
            states: {
              hover: {
                fill: '#42A5F5',
                style: {
                  color: 'white',
                },
              },
              select: {
                fill: '#29B6F6',
                style: {
                  color: 'white',
                },
              },
            },
          },
        },
        legend: {
          enabled: true,
          labelFormatter: function () {
            if (this.visible) {
              return (
                '<span style="color: ' +
                this.color +
                '">' +
                this.name +
                '</span>'
              )
            } else {
              return '<span style="color:#CCCCCC">' + this.name + '</span>'
            }
          },
          itemHiddenStyle: {
            color: '#CCCCCC',
          },

          layout: 'horizontal',
          align: 'center',
          verticalAlign: 'top',

          itemStyle: {
            fontFamily: 'Montserrat',
            fontSize: '14px',
          },
        },
        yAxis: [],
        xAxis: {
          events: {
            setExtremes: this.getNewDate,
          },
          plotLines: [],
        },
        time: {
          useUTC: false,
        },
        plotOptions: {
          series: {
            cursor: 'pointer',
            turboThreshold: 999999999,
            point: {
              events: {
                click: (e) => {
                  console.log(e.point.x)
                  this.sendPoint(e.point.x)
                },
              },
            },
          },
        },
        series: [],
      },
    }
  },

  async mounted() {
    this.getData()
    await this.$nextTick()
  },
  methods: {
    delColTable(index) {
      this.dataTablePoint.splice(index, 1)
    },
    onLog() {
      console.log(this.chart)
    },
    changeHeightChart() {
      if (this.chartOptions.chart.height == 400) {
        this.chartOptions.chart.height = 710
      } else {
        this.chartOptions.chart.height = 400
      }

      let el = document.getElementById('element' + this.id)
      setTimeout(function () {
        el.scrollIntoView({
          block: 'center',
          behavior: 'smooth',
          inline: 'nearest',
        })
      }, 500)
    },
    changeTypeChart(type) {
      switch (type) {
        case 'line':
        case 'spline':
        case 'area':
          this.chartOptions.chart.type = type
          this.chartOptions.series.forEach((item) => {
            item.step = false
            item.lineWidth = 2
            item.marker = {
              enabled: false,
              radius: 2,
            }
          })

          break
        case 'step':
          this.chartOptions.chart.type = 'line'
          this.chartOptions.series.forEach((item) => {
            item.step = true
            item.lineWidth = 2
            item.marker = {
              enabled: false,
              radius: 2,
            }
          })

          break

        case 'point':
          this.chartOptions.chart.type = 'line'
          this.chartOptions.series.forEach((item) => {
            item.step = false
            item.lineWidth = 0
            item.marker = {
              enabled: true,
              radius: 3,
              lineWidth: 1,
            }
          })
          break
      }
      this.visibleTypeLine = false
    },
    accordion: function (event) {
      event.target.classList.toggle('active')
    },
    setNewExtremes: function (min, max) {
      // debugger;
      this.chart.xAxis[0].setExtremes(
        Math.round(min / 1000) * 1000,
        Math.round(max / 1000) * 1000
      )
      // this.chart.navigator.xAxis.setExtremes(
      //   Math.round(min / 1000) * 1000,
      //   Math.round(max / 1000) * 1000
      // );
    },
    openFunctionGraphFunc() {
      this.openFunctionGraph = true
      console.log('element' + this.id)
      function getCoords(elem) {
        // кроме IE8-
        let box = elem.getBoundingClientRect()
        return {
          top: box.top + pageYOffset,
          left: box.left + pageXOffset,
        }
      }
      let currentPosition = getCoords(
        document.getElementById('element' + this.id)
      )
      console.log(currentPosition.top)
      let heightWindow = window.innerHeight
      let heightModal = 302
      let heightMenu = 44

      if (currentPosition.top + heightModal + heightMenu > heightWindow) {
        this.topPositionOpenFunctionGraf = currentPosition.top - heightModal
      } else {
        this.topPositionOpenFunctionGraf = currentPosition.top + heightMenu
      }
      console.log('qwe ' + this.topPositionOpenFunctionGraf)
    },
    openStatisticsTableFunc() {
      if (this.openStatisticsTable) {
        this.openStatisticsTable = false
      } else {
        this.openStatisticsTable = true
      }
    },

    /**
     * получение даных для графика с сервера
     *
     * @param {string} key ключ для запроса данных с сервера. Доступны [hour,shift,day,week,month]
     * @param  {boolean}  updNavigator  флаг для обновления навигатора
     */
    async getData(key = 'day', updNavigator = true) {
      this.chart.showLoading()
      await this.$axios
        .$get(`${this.baseUrl}&key=${key}`)
        .then((data) => {
          if (data.child[0] != undefined && data.child[0].values.length != 0) {
            let emptyYAxis = {
              reversed: false,
              opposite: false,
              title: {
                style: {
                  fontSize: 14,
                  fontFamily: 'montserrat',
                },
                enabled: true,
                text: '',
              },
            }
            let AllYAxis = []
            let valueYAxis = []
            data.child.forEach((item) => {
              valueYAxis.push(item.sensor_data.unit)
            })
            valueYAxis = Array.from(new Set(valueYAxis))

            valueYAxis.forEach((el, i) => {
              let yAx = JSON.parse(JSON.stringify(emptyYAxis))
              yAx.title.text = el
              yAx.id = el
              if (i != 0) {
                yAx.opposite = !AllYAxis[i - 1].opposite
              }
              AllYAxis.push(yAx)
            })

            this.chartOptions.yAxis = AllYAxis
            this.chartOptions.series = this.setArray(data)

            if (updNavigator) {
              // debugger;
              this.chartOptions.navigator.series = JSON.parse(
                JSON.stringify(this.chartOptions.series)
              ).map((el) => {
                delete el.yAxis
                delete el.name
                return el
              })
            }
          }
          this.chart.hideLoading()
        })
        .catch((e) => {
          console.log(e)
          this.chart.hideLoading()
        })
    },
    setArray(data, yAxis_value) {
      let newArraySeries = []
      data.child.forEach((el, i) => {
        let newObj = {
          name: el.sensor_data.name,
          color: el.color,
          yAxis: el.sensor_data.unit,
        }
        newObj.data = []
        if (el.values.length != 0) {
          el.values.forEach((item) => {
            if (item.value != null) {
              if (item.start_time) {
                newObj.data.push({
                  x: Date.parse(item.start_time),
                  y: item.value,
                })
              } else if (item.now_time) {
                newObj.data.push({
                  x: Date.parse(item.now_time),
                  y: item.value,
                })
              }
            }
          })
          newObj.data.sort((a, b) => a.x - b.x)
          newArraySeries.push(newObj)
        }
      })
      return newArraySeries
    },
    async getFromChildDate() {
      // console.log(e);
      let e = this.graphObjectLastZoom
      let min = Math.round(e.min) //+(new Date().getTimezoneOffset()*60*1000);
      let max = Math.round(e.max) //+(new Date().getTimezoneOffset()*60*1000);
      this.setRangeVar = null
      // this.graphObjectLastZoom = e;
      // let { chart } = e.target;
      if (min.toString() != 'NaN' && max.toString() != 'NaN') {
        this.chart.showLoading('Загрузка данных с сервера...')
        let minTime = returnDateFormat(min) //<str:YYYY-MM-DD HH:mm:SS>
        let maxTime = returnDateFormat(max)
        // if (this.lastUrl != `${this.baseUrl}&start=${minTime}&end=${maxTime}`) {
        this.lastUrl = `${this.baseUrl}&start=${minTime}&end=${maxTime}`
        await this.$axios
          .$get(`${this.baseUrl}&start=${minTime}&end=${maxTime}`)
          .then((data) => {
            let emptyYAxis = {
              reversed: false,
              opposite: false,
              title: {
                style: {
                  fontSize: 14,
                  fontFamily: 'montserrat',
                },
                enabled: true,
                text: '',
              },
            }
            let AllYAxis = []
            let valueYAxis = []
            data.child.forEach((item) => {
              valueYAxis.push(item.sensor_data.unit)
            })
            valueYAxis = Array.from(new Set(valueYAxis))

            valueYAxis.forEach((el, i) => {
              let yAx = JSON.parse(JSON.stringify(emptyYAxis))
              yAx.title.text = el
              yAx.id = el
              if (i != 0) {
                yAx.opposite = !AllYAxis[i - 1].opposite
              }
              AllYAxis.push(yAx)
            })

            this.chartOptions.yAxis = AllYAxis

            let tempArr = this.setArray(data)

            let tempArr2 = []

            tempArr.forEach((el, i) => {
              if (el.data.length > 1) {
                tempArr2.push(el)
              } else {
                tempArr2.push(this.chartOptions.series[i])
              }
            })
            // debugger;
            this.chartOptions.series = tempArr2
            // console.log(this.chartOptions.series,"2345ewsdf");
            // console.log(this);
            this.setNewExtremes(
              tempArr2[0].data[0].x,
              tempArr2[0].data[tempArr2[0].data.length - 1].x
            )
            this.chart.hideLoading()
          })
          .catch((error) => {
            this.chart.hideLoading()
            console.error(error.message)
          })
        // }
      }
    },
    async getNewDate(e) {
      let min = Math.round(e.min) //+(new Date().getTimezoneOffset()*60*1000);
      let max = Math.round(e.max) //+(new Date().getTimezoneOffset()*60*1000);
      this.setRangeVar = null
      this.graphObjectLastZoom = e
      if (
        ((e.triggerOp && e.DOMEvent.type == 'mouseup') ||
          (e.triggerOp && e.DOMEvent.type == 'click') ||
          e.triggerOp == undefined) &&
        e.trigger != undefined
      ) {
        let { chart } = e.target
        if (min.toString() != 'NaN' && max.toString() != 'NaN') {
          chart.showLoading('Загрузка данных с сервера...')
          let minTime = returnDateFormat(min) //<str:YYYY-MM-DD HH:mm:SS>
          let maxTime = returnDateFormat(max)
          if (
            this.lastUrl != `${this.baseUrl}&start=${minTime}&end=${maxTime}`
          ) {
            this.lastUrl = `${this.baseUrl}&start=${minTime}&end=${maxTime}`
            await this.$axios
              .$get(`${this.baseUrl}&start=${minTime}&end=${maxTime}`)
              .then((data) => {
                let tempArr = this.setArray(data)

                let tempArr2 = []

                tempArr.forEach((el, i) => {
                  if (el.data.length > 1) {
                    tempArr2.push(el)
                  } else {
                    tempArr2.push(this.chartOptions.series[i])
                  }
                })

                this.chartOptions.series = tempArr2

                // console.log(this.chartOptions.series[0].data[0].x);
                // console.log(
                //   this.chartOptions.series[0].data[
                //     this.chartOptions.series[0].data.length - 1
                //   ].x
                // );

                this.setNewExtremes(
                  this.chartOptions.series[0].data[0].x,
                  this.chartOptions.series[0].data[
                    this.chartOptions.series[0].data.length - 1
                  ].x
                )
                chart.hideLoading()
              })
              .catch((error) => {
                chart.hideLoading()
                console.error(error.message)
              })
          }
        }
      }
    },

    async getExtNewDate(e) {
      this.chart.showLoading('Загрузка данных с сервера...')
      //this.setRangeVar = null;
      let minTime = e.min //<str:YYYY-MM-DD HH:mm:SS>
      let maxTime = e.max
      // this.graphObjectLastZoom = e;
      this.chart.showLoading()
      if (this.lastUrl != `${this.baseUrl}&start=${minTime}&end=${maxTime}`) {
        this.lastUrl = `${this.baseUrl}&start=${minTime}&end=${maxTime}`
        await this.$axios
          .$get(`${this.baseUrl}&start=${minTime}&end=${maxTime}`)
          .then((data) => {
            let tempArr = this.setArray(data)

            let tempArr2 = []

            tempArr.forEach((el, i) => {
              if (el.data.length > 1) {
                tempArr2.push(el)
              } else {
                tempArr2.push(this.chartOptions.series[i])
              }
            })

            this.chartOptions.series = tempArr2

            // console.log(this.chartOptions.series[0].data[0].x);
            // console.log(
            //   this.chartOptions.series[0].data[
            //     this.chartOptions.series[0].data.length - 1
            //   ].x
            // );

            this.setNewExtremes(
              this.chartOptions.series[0].data[0].x,
              this.chartOptions.series[0].data[
                this.chartOptions.series[0].data.length - 1
              ].x
            )
            this.chart.hideLoading()
          })
          .catch((error) => {
            this.chart.hideLoading()
            console.error(error.message)
          })
      }
    },

    async setRange(sel) {
      this.graphObjectLastZoom = null
      this.setRangeVar = sel.period
      await this.getData(sel.period, false)
        .then((d) => {
          this.setNewExtremes(
            this.chartOptions.series[0].data[0].x,
            this.chartOptions.series[0].data[
              this.chartOptions.series[0].data.length - 1
            ].x
          )
        })
        .catch((e) => {
          console.error('Что-то пошло не так')
        })
    },

    sendPoint(xTime) {
      function arraySum(array) {
        var sum = 0
        for (var i = 0; i < array.length; i++) {
          sum += array[i]
        }
        return sum
      }
      // debugger;
      let xPoint = {
        time: xTime,
        chart: [],
      }

      this.chartOptions.series.forEach((el) => {
        let tmpObj = {
          name: el.name,
          unit: el.yAxis,
          color: el.color,
          value: 0,
        }
        let sum = []
        el.data.forEach((item, i, arr) => {
          if (
            i != arr.length - 1 &&
            item.x != xTime &&
            item.x < xTime &&
            xTime < arr[i + 1].x
          ) {
            sum.push(item.y, arr[i + 1].y)
          }

          if (item.x == xTime) {
            sum.push(item.y.toFixed(1))
          }
        })

        if (sum.length != 0) {
          tmpObj.value = (arraySum(sum) / sum.length).toFixed(1)
        }

        xPoint.chart.push(tmpObj)
      })
      if (
        this.dataTablePoint.filter((f1) => {
          return f1.time == xPoint.time
        }).length == 0
      ) {
        this.dataTablePoint.push(xPoint)
      }
    },
  },
  computed: {
    content: function () {
      return {
        // fist: this.fistDate,
        // last: this.lastDate,
        title: 'Настройка отображения графиков области',
        btnLeft: 'Экспорт',
        btnRight: 'Обновить',
        selectLeft: 'Графики - все подряд',
        selectRight: 'Графики - группировать по группам',
      }
    },
  },
}
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
  z-index: 2;
  margin-left: auto;
  margin-right: 1.4em;
  margin-top: -24px;
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
  background-image: url('~assets/svg/recorder/addRemoveGraph.svg');
  background-position: center;
  background-repeat: no-repeat;
  background-size: contain;
}
.addrem:hover {
  background-image: url('~assets/svg/recorder/AddRemoveGraphAct.svg');
}

.type {
  background-image: url('~assets/svg/recorder/typeGraph.svg');
  background-position: center;
  background-repeat: no-repeat;
  background-size: contain;
}
.type:hover {
  background-image: url('~assets/svg/recorder/hovTypeGraph.svg');
}

.online {
  background-image: url('~assets/svg/recorder/onlinePlay.svg');
  background-position: center;
  background-repeat: no-repeat;
  background-size: contain;
}

.online:hover {
  background-image: url('~assets/svg/recorder/hovOnlinePlay.svg');
}

.gannt {
  background-image: url('~assets/svg/recorder/DiagrGannt.svg');
  background-position: center;
  background-repeat: no-repeat;
  background-size: contain;
}

.gannt:hover {
  background-image: url('~assets/svg/recorder/hovDiagrammGrannt.svg');
}

.formule {
  background-image: url('~assets/svg/recorder/formule.svg');
  background-position: center;
  background-repeat: no-repeat;
  background-size: contain;
}
.formule:hover {
  background-image: url('~assets/svg/recorder/hovFormule.svg');
}

.resize {
  background-image: url('~assets/svg/recorder/resizeGraph.svg');
  background-position: center;
  background-repeat: no-repeat;
  background-size: contain;
}
.resize:hover {
  background-image: url('~assets/svg/recorder/hovResizeGraph.svg');
}
.resize:checked {
  background-image: url('~assets/svg/recorder/resizeActive.svg');
  /* transition: background 0s; */
}
.bulity {
  background-image: url('~assets/svg/recorder/menu.svg');
  background-position: center;
  background-repeat: no-repeat;
  background-size: contain;
}
.bulity:hover {
  background-image: url('~assets/svg/recorder/hovAddicationMenu.svg');
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
  width: 98px;
  height: 146px;
  background-color: white;
  position: absolute;
  left: 1595px;
  top: 49px;
  border: 1px solid #90a1b1;
}

.typeLine li {
  border: 0;
  outline: none;
  display: flex;
  margin: 3px -41px;
  cursor: pointer;
  font-family: 'Montserrat';
  font-size: 12px;
}
.button-range {
  outline: none;
  font-size: 12px;
  font: 'Montserrat';
  color: #00b0ff;
  border: 1px solid #00b0ff;
  border-radius: 5px;
  margin-left: 5px;
}
.button-range:hover {
  outline: none;
  font-size: 12px;
  font: 'Montserrat';
  color: #ffffff;
  border: 1px solid #00b0ff;
  border-radius: 5px;
  margin-left: 5px;
  background-color: #00b0ff;
}

.rangeButton {
  font-size: 12px;
  margin-left: 40px;
  color: #46627d;
}

.arrow-up {
  transform: matrix(1, 0, 0, -1, 0, 0);
}

.type1 img {
  outline: 0;
  height: 24px;
  width: 98px;
  background-image: url('~assets/svg/recorder/Line.svg');
  background-repeat: no-repeat;
}
.type1 img:hover {
  background-image: url('~assets/svg/recorder/hovLine.svg');
  background-repeat: no-repeat;
}
.type2 img {
  height: 24px;
  width: 98px;
  background-image: url('~assets/svg/recorder/Spline.svg');
  background-repeat: no-repeat;
}
.type2 img:hover {
  background-image: url('~assets/svg/recorder/hovSpline.svg');
  background-repeat: no-repeat;
}

.type3 img {
  height: 24px;
  width: 98px;
  background-image: url('~assets/svg/recorder/Step.svg');
  background-repeat: no-repeat;
  border: 0;
  text-indent: -100vw;
}
.type3 img:hover {
  background-image: url('~assets/svg/recorder/hovStep.svg');
  background-repeat: no-repeat;
  border: none;
}

.type4 img {
  height: 24px;
  width: 98px;
  background-image: url('~assets/svg/recorder/Area.svg');
  background-repeat: no-repeat;
}
.type4 img:hover {
  background-image: url('~assets/svg/recorder/hovArea.svg');
  background-repeat: no-repeat;
}

.type5 img {
  height: 24px;
  width: 98px;
  background-image: url('~assets/svg/recorder/Point.svg');
  background-repeat: no-repeat;
}
.type5 img:hover {
  background-image: url('~assets/svg/recorder/hovPoint.svg');
  background-repeat: no-repeat;
}

.type6 img {
  height: 24px;
  width: 98px;
  background-image: url('~assets/svg/recorder/Boxplot.svg');
  background-repeat: no-repeat;
}
.type6 img:hover {
  background-image: url('~assets/svg/recorder/hovBoxplot.svg');
  background-repeat: no-repeat;
}
</style>

