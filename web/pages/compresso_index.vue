<template>
  <div>
    <onlinePeriod />
    <div style="margin-top: 50px">
      <div style="align-items: flex-start; display: flex">
        <div>
          <div>
            <background title="Давление" style="height: 265px; width: 283px">
              <gauge
                :points="compressor_data.current_pressure"
                :limits="compressor_limits"
              />
            </background>
          </div>
          <div>
            <!-- <durationWork style="margin-left: 20px"></durationWork> -->
            <background
              title="Продолжительность работы, ч"
              style="
                height: 310px;
                width: 283px;
                display: flex;
                flex-wrap: wrap;
                align-content: start;
                flex-direction: column;
                justify-content: flex-start;
              "
            >
              <div style="width: 100%; height: 82%; overflow-y: auto">
                <div
                  class="item"
                  v-for="item in compressor_time"
                  :key="item.start_time"
                >
                  <div
                    class="line_time"
                    :style="'width: ' + (item.progress - 10) + '%'"
                  >
                    <div class="start_time">
                      {{ item.start_time }}
                    </div>
                    <div class="end_time">
                      {{ item.end_time }}
                    </div>
                  </div>
                  <div class="work_time">{{ item.work_time }}</div>
                </div>
              </div>

              <div class="sum_work" style="width: 100%; margin: auto 0 0 0">
                <div class="sum_work_title">Общее рабочее время за день</div>
                <div class="sum_work_time">{{ compressor_sum_time }}</div>
              </div>
            </background>
          </div>
        </div>
        <div>
          <div>
            <background
              title="График изменения давления"
              style="height: 442px; width: 1100px"
            >
              <highcharts
                style="height: 400px; width: 1090px"
                class="highcharts"
                :constructor-type="'stockChart'"
                :options="chartOptions"
                :updateArgs="[true, true]"
                ref="chart"
              ></highcharts>
            </background>
          </div>
          <div style="align-items: flex-start; display: flex">
            <div>
              <background title="Текущее состояние">
                <card
                  :description2="compressor_data.current_state"
                  description="Компрессорная установка"
                  path="13.png"
                  class="card"
                  color="#588C64"
                  style="margin-top: 5px"
                >
                </card>
              </background>
            </div>
            <div>
              <background title="Температура">
                <card
                  :number="compressor_data.current_temp"
                  description="Температура, °С"
                  path="7.png"
                  class="card"
                  style="margin-top: 5px"
                >
                </card>
              </background>
            </div>
          </div>

          <!-- <div>
            <background title="Панель управления">
              <card
                description2="Пуск"
                description="Компрессорная установка"
                path="pusk.svg"
                class="card"
                color="#588C64"
                style="margin-top: 5px"
              >
              </card>
              <card
                description2="Стоп"
                description="Компрессорная установка"
                path="stop.svg"
                class="card"
                color="#80272F"
                style="margin-top: 5px"
              >
              </card>
              <card
                description2="Блокировка"
                description="Компрессорная установка"
                path="block.svg"
                class="card"
                color="#EDB320"
                style="margin-top: 5px"
              >
              </card>
            </background>
          </div> -->
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import { mapGetters } from 'vuex'
import { mapActions } from 'vuex'
import OnlineHeader from '/components/onlineHeaderCompressor'
import card from '@/components/card/card.vue'
import background from '@/components/background/back.vue'
import gauge from '@/components/gauge'

export default {
  layout: 'header_footer',
  components: {
    onlinePeriod: OnlineHeader,
    card,
    background,
    gauge,
  },
  data() {
    return {
      baseUrl: '/dashboard/compressor/davlenie_graph/',
      chart: null,
      dateSt: '',
      dateEnd: '',
      enableFetch: true,
      dataNavigator: [],
      lastUrl: '',
      timerId: null,
      polling: null,
      chartOptions: {
        chart: {
          height: 400,
          // type: 'spline',
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
        },
        credits: {
          enabled: false,
        },
        scrollbar: {
          enabled: false,
        },
        exporting: {
          enabled: false,
        },
        navigator: {
          enabled: false,
        },
        rangeSelector: {
          enabled: false,
        },
        legend: {
          enabled: false,
        },
        yAxis: [
          {
            height: '88%',
            lineWidth: 1,
            // offset:0,
            labels: {
              align: 'right',
              x: -3,
            },
            resize: {
              enabled: true,
            },
            // max:1,
          },
          {
            categories: [''],
            lineWidth: 1,
            // offset:"10%",
            top: '90%',
            height: '10%',
            labels: {
              align: 'right',
              x: -3,
            },
            resize: {
              enabled: true,
            },
            // max:2,
          },
        ],
        xAxis: {
          type: 'datetime',
          plotLines: [],
        },
        time: {
          useUTC: false,
        },
        plotOptions: {
          series: {
            cursor: 'pointer',
            turboThreshold: 999999999,
          },
          xrange: {
            borderRadius: 0,
            borderWidth: 0,
            colorByPoint: false,
            grouping: false,
            pointWidth: 40,
          },
        },
        series: [
          // {
          //   data: [],
          //   name: "",
          //   type: "spline",
          //   yAxis: 0,
          // },
          // {
          //   color: "#FF7167",
          //   data: [
          //     // {
          //     //   x: 1617473956000,
          //     //   x2: 1617735748000,
          //     //   y: 0,
          //     // },
          //   ],
          //   name: "No",
          //   type: "xrange",
          //   yAxis: 1,
          // },
          // {
          //   color: "#FFDC75",
          //   data: [
          //     {
          //       x: 1617191428000,
          //       x2: 1617473956000,
          //       y: 0,
          //     },
          //   ],
          //   name: "Yes",
          //   type: "xrange",
          //   yAxis: 1,
          // },
          // {
          //   color: "#4BBEA9",
          //   data: [
          //     {
          //       x: 1617735748000,
          //       x2: 1618046788000,
          //       y: 0,
          //     },
          //   ],
          //   name: "Ok",
          //   type: "xrange",
          //   yAxis: 1,
          // },
        ],
      },
    }
  },

  computed: {
    ...mapGetters('compressor', {
      // activeshop: "activeshop",
      compressor_data: 'compressor_data',
      compressor_time: 'compressor_time',
      compressor_limits: 'compressor_limits',
    }),

    compressor_sum_time: function () {
      let sum = 0
      if (this.compressor_time) {
        this.compressor_time.forEach((item) => {
          sum += parseFloat(item.work_time)
        })
      }
      return sum.toFixed(2)
    },

    content: function () {
      return {}
    },
  },

  methods: {
    ...mapActions('users', {
      setActiveTabHeader: 'setActiveTabHeader',
      setActiveTabSidebar: 'setActiveTabSidebar',
    }),

    pollData() {
      this.polling = setInterval(() => {
        this.$store.dispatch('compressor/get_compressor_data')
      }, 5000)
    },

    // showVchartBoxVisible() {
    //   this.isVchartBoxVisible = true;
    // },
    // closeVchartBoxVisible() {
    //   this.isVchartBoxVisible = false;
    // },

    // changeFistData(val) {
    //   console.log(val);
    //   //this.fistDate =formatDate(val);
    // },
    // changeLastData(val) {
    //   //this.lastDate =formatDate(val);
    // },

    async getData(key = 'hour', updNavigator = true) {
      this.chart.showLoading()
      await this.$axios
        .$get(`${this.baseUrl}?key=${key}`)
        .then((data) => {
          if (data.data != undefined && data.data.length != 0) {
            let newSeries = []

            newSeries.push({
              data: this.setArray(data.data),
              name: 'Компрессорная установка 1',
              color: '#4BBEA9',
              yAxis: 0,
              type: 'spline',
            }) //график непрерывный

            // data.state.forEach((item) => {
            //   //график состояний
            //   if (item.data.length > 0) {
            //     item.data.forEach((item2) => {
            //       item2.x1 = Date.parse(item2.x1);
            //       item2.x2 = Date.parse(item2.x2);

            //       // if (item2.x2<item2.x1){
            //       //   let buff = JSON.parse(JSON.stringify(item2.x1));
            //       //   item2.x1 = item2.x2;
            //       //   item2.x2 = buff;
            //       // }
            //     });
            //   }
            //   newSeries.push({
            //     color: item.color,
            //     data: item.data,
            //     name: item.name_state,
            //     type: "xrange",
            //     yAxis: 1,
            //   });
            // });

            this.chartOptions.yAxis[0].name = 'Атм'
            // this.chartOptions.series[0].name = "Компрессорная установка 1";
            // this.chartOptions.series[0].color = "#4BBEA9";
            // debugger;
            // this.$nextTick(function(){
            this.chartOptions.series = newSeries
            //   this.$set(this.chartOptions,"series",newSeries)

            // })
          }
          this.chart.hideLoading()
        })
        .catch((e) => {
          console.log(e)
          this.chart.hideLoading()
        })
    },
    setArray(data) {
      let newObj = []
      data.forEach((el, i) => {
        if (el.y != null) {
          let tmp = {
            x: Date.parse(el.x),
            y: el.y,
          }
          newObj.push(tmp)
        }
      })

      newObj.sort((a, b) => a.x - b.x)

      return newObj
    },
    // async getNewDate(e) {
    //   let min = Math.round(e.min); //+(new Date().getTimezoneOffset()*60*1000);
    //   let max = Math.round(e.max); //+(new Date().getTimezoneOffset()*60*1000);
    //   if (
    //     ((e.triggerOp && e.DOMEvent.type == "mouseup") ||
    //       (e.triggerOp && e.DOMEvent.type == "click") ||
    //       e.triggerOp == undefined) &&
    //     e.trigger != undefined
    //   ) {
    //     let { chart } = e.target;
    //     if (min.toString() != "NaN" && max.toString() != "NaN") {
    //       chart.showLoading("Загрузка данных с сервера...");
    //       let minTime = returnDateFormat(min); //<str:YYYY-MM-DD HH:mm:SS>
    //       let maxTime = returnDateFormat(max);
    //       if (
    //         this.lastUrl != `${this.baseUrl}&start=${minTime}&end=${maxTime}`
    //       ) {
    //         this.lastUrl = `${this.baseUrl}&start=${minTime}&end=${maxTime}`;
    //         await this.$axios
    //           .$get(`${this.baseUrl}&start=${minTime}&end=${maxTime}`)
    //           .then((data) => {
    //             let tempArr = this.setArray(data);

    //             let tempArr2 = [];

    //             tempArr.forEach((el, i) => {
    //               if (el.data.length > 1) {
    //                 tempArr2.push(el);
    //               } else {
    //                 tempArr2.push(this.chartOptions.series[i]);
    //               }
    //             });

    //             this.chartOptions.series = tempArr2;
    //             this.setNewExtremes(
    //               this.chartOptions.series[0].data[0].x,
    //               this.chartOptions.series[0].data[
    //                 this.chartOptions.series[0].data.length - 1
    //               ].x
    //             );
    //             chart.hideLoading();
    //           })
    //           .catch((error) => {
    //             chart.hideLoading();
    //             console.error(error.message);
    //           });
    //       }
    //     }
    //   }
    // },

    // async getExtNewDate(e) {
    //   this.chart.showLoading("Загрузка данных с сервера...");
    //   let minTime = e.min; //<str:YYYY-MM-DD HH:mm:SS>
    //   let maxTime = e.max;
    //   this.chart.showLoading();
    //   if (this.lastUrl != `${this.baseUrl}&start=${minTime}&end=${maxTime}`) {
    //     this.lastUrl = `${this.baseUrl}&start=${minTime}&end=${maxTime}`;
    //     await this.$axios
    //       .$get(`${this.baseUrl}&start=${minTime}&end=${maxTime}`)
    //       .then((data) => {
    //         let tempArr = this.setArray(data);

    //         let tempArr2 = [];

    //         tempArr.forEach((el, i) => {
    //           if (el.data.length > 1) {
    //             tempArr2.push(el);
    //           } else {
    //             tempArr2.push(this.chartOptions.series[i]);
    //           }
    //         });

    //         this.chartOptions.series = tempArr2;
    //         this.setNewExtremes(
    //           this.chartOptions.series[0].data[0].x,
    //           this.chartOptions.series[0].data[
    //             this.chartOptions.series[0].data.length - 1
    //           ].x
    //         );
    //         this.chart.hideLoading();
    //       })
    //       .catch((error) => {
    //         this.chart.hideLoading();
    //         console.error(error.message);
    //       });
    //   }
    // },

    // async setRange(sel) {
    //   await this.getData(sel.period, false)
    //     .then((d) => {
    //       this.setNewExtremes(
    //         this.chartOptions.series[0].data[0].x,
    //         this.chartOptions.series[0].data[
    //           this.chartOptions.series[0].data.length - 1
    //         ].x
    //       );
    //     })
    //     .catch((e) => {
    //       console.error("Что-то пошло не так");
    //     });
    // },
  },
  mounted() {
    this.getData()
    this.$store.dispatch('compressor/get_compressor_limits')
    this.$store.dispatch('compressor/get_compressor_time')
    this.pollData()
  },
  beforeDestroy() {
    clearInterval(this.polling)
  },
}
</script>

<style lang="scss" scoped>
.sum_work {
  display: flex;
  justify-content: space-between;
  border-top: 1px solid #e9e9e9;
  align-items: center;
  position: relative;
  //  bottom:376px;
}
.sum_work_time {
  margin-top: 5px;
  font-size: 16px;
  font-weight: bold;
  margin-right: 6px;
  color: #3f51b5;
}
.sum_work_title {
  margin-top: 5px;
  margin-left: 6px;
  font-size: 12px;
  color: #3f51b5;
}
.item {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.line_time {
  width: 200px;
  height: 20px;
  background: #ecedf4;
  margin: 6px;
  display: flex;
  justify-content: space-between;

  align-items: center;
}
.work_time {
  font-size: 16px;
  font-weight: bold;
  margin-right: 6px;
}
.start_time,
.end_time {
  font-size: 14px;
  margin-right: 5px;
  margin-left: 5px;
}
.period {
  display: flex;
  justify-content: center;
  align-items: center;

  .btn {
    cursor: pointer;
    outline: none;
    height: 23px;

    display: flex;
    justify-content: center;
    align-items: center;

    margin-right: 12px;
    padding: 0 6px;

    border: 1px solid #ecedf4;
    border-radius: 3px;
    background: #ffffff;

    font-weight: 500;
    font-size: 12px;
    color: #42435f;

    &:hover {
      border: 1px solid #272848;
    }
  }

  .text {
    width: 52px;
  }

  .btn.text:nth-child(3) {
    margin-right: 6px;
  }

  .num {
    width: 42px;
    background: #ffffff;
    margin-right: 6px;
  }

  .active {
    background: #272848;
    color: #bfc0c9;
    text-align: center;
  }

  button:last-child {
    margin-right: 0;
  }
}
.chart {
  width: 284px;
  border: 2px solid #e9e9e9;
  border-radius: 9px;
}
.chart.first {
  height: 348px;
  margin-bottom: 12px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;

  .chart-header {
    padding-bottom: 6px;
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    align-items: center;

    .box-header {
      width: 100%;
      position: relative;
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 9px;
      padding-left: 12px;
      padding-right: 6px;
    }

    .period {
      padding-left: 12px;
      padding-right: 6px;
      .btn {
        margin-right: 6px;

        &:nth-child(1) {
          margin-right: 12px;
        }
      }
    }
  }

  .chart-content {
    height: 100%;
    padding: 6px 8px 6px 6px;
    justify-content: flex-start;
    overflow: auto;

    .line {
      position: relative;
      display: flex;
      width: 100%;
      justify-content: space-between;
      margin-bottom: 12px;

      .box-line {
        max-width: 222px;
        width: 100%;
        font-weight: normal;
        font-size: 10px;
        color: #000000;

        .bg {
          cursor: pointer;
          max-width: 100%;
          padding: 0 10px;
          display: flex;
          justify-content: space-between;
          align-items: center;
          height: 16px;
          background: #ecedf4;

          .start {
            margin-right: 10px;
          }
        }

        .start,
        .end {
          display: flex;
        }
      }

      .data-line {
        font-weight: bold;
        font-size: 12px;
        line-height: 15px;
        color: #000000;
      }

      &:hover {
        .title-line {
          display: block;
        }
      }

      .title-line {
        display: none;
        position: absolute;
        top: -3px;
        left: 0;
        transform: translateY(-100%);

        width: 100px;
        height: 26px;
        padding: 1px 6px;

        font-weight: normal;
        font-size: 10px;
        color: #000000;
        background: #ffffff;

        box-shadow: 0px 1px 4px rgba(0, 0, 0, 0.15);
        border-radius: 3px;

        .start {
          margin-bottom: 1px;
        }

        &.down {
          top: -3px;
          left: 25px;
          transform: none;
        }
      }
    }
  }
}
.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #e9e9e9;
  padding: 2px 0;

  .title {
    font-family: 'Montserrat', -apple-system, BlinkMacSystemFont, 'Segoe UI',
      Roboto, 'Helvetica Neue', Arial, sans-serif;
    font-weight: 500;
    font-size: 14px;
    text-align: center;
    color: #000000;
  }

  .bul {
    cursor: pointer;
    width: 17px;
    height: 20px;
    display: flex;
    justify-content: center;
    align-items: center;

    span {
      position: relative;
      background-color: #cfcdcd;
      width: 3px;
      height: 3px;
      border-radius: 50%;
      font-size: 0;
      left: -10px;
    }

    span:before {
      position: absolute;
      left: 5px;
      top: 0;
      content: '';

      background-color: #cfcdcd;
      font-size: 0;
      width: 3px;
      height: 3px;
      border-radius: 50%;
    }

    span:after {
      position: absolute;
      left: 10px;
      top: 0;
      content: '';
      background-color: #cfcdcd;
      font-size: 0;
      width: 3px;
      height: 3px;
      border-radius: 50%;
    }
  }
}
.chart-footer {
  width: 100%;
  height: 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-top: 1px solid #e9e9e9;
  padding: 4px 24px 4px 6px;

  .title {
    font-weight: normal;
    font-size: 12px;
    line-height: 15px;
    display: flex;
    align-items: center;
    color: #3f51b5;
  }

  .view {
    font-weight: bold;
    font-size: 12px;
    line-height: 15px;
    display: flex;
    align-items: center;
    text-align: center;
    color: #3f51b5;
  }
}
.menu-bul {
  -moz-user-select: none;
  -khtml-user-select: none;
  user-select: none;
  position: absolute;
  top: 25px;
  right: 0;
  height: auto;
  width: 110px;
  display: flex;
  flex-direction: column;
  background: #f7f8fa;
  box-shadow: 0px 2px 6px rgba(0, 0, 0, 0.25);
  border-radius: 4px 0px 4px 4px;
  z-index: 50;

  .btn-bul {
    cursor: pointer;
    position: relative;
    width: 100%;
    height: 40px;
    padding-left: 32px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: flex-start;
    font-weight: 500;
    font-size: 10px;
    line-height: 12px;
    color: #bababa;

    &:hover {
      color: #727272;
      transition: 0.2s linear;

      .show {
        background-image: url('https://api.iconify.design/ant-design:eye-invisible-outlined.svg?color=%23727272');
      }

      .new {
        background-image: url('https://api.iconify.design/ic:baseline-update.svg?color=%23727272');
      }
    }
  }

  .show {
    position: absolute;
    top: 50%;
    left: 12px;
    transform: translateY(-50%);
    width: 14px;
    height: 14px;
    background-image: url('https://api.iconify.design/ant-design:eye-invisible-outlined.svg?color=%23BABABA');
    background-repeat: no-repeat;
    background-position: center;
    background-size: contain;
  }

  .new {
    content: '';
    position: absolute;
    top: 50%;
    left: 12px;
    transform: translateY(-50%);
    width: 14px;
    height: 14px;
    background-image: url('https://api.iconify.design/ic:baseline-update.svg?color=%23BABABA');
    background-repeat: no-repeat;
    background-position: center;
    background-size: contain;
  }
}
</style>
