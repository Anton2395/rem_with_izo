<template>
  <div class="chart-data consumption">
    <div class="chart-header">
      <div class="title">Удельный расход на км</div>
      <period title="SpecificConsumption"></period>
      <!-- <div
        class="bul"
        @click="SpecificConsumption.modalBul = !SpecificConsumption.modalBul"
        @click.stop="noChange"
      >
        <span></span>
      </div> -->
    </div>
    <div class="chart-content">
      <!-- <div
                class="menu-bul"
                v-if="SpecificConsumption.modalBul"
            >
              <div
                  class="btn-bul"
                  @click="SpecificConsumption.cardShow=!SpecificConsumption.cardShow; SpecificConsumption.modalBul=false"
              ><span class="show"></span>
                <span>Скрыть</span>
              </div>
              <div class="btn-bul">
                <span class="new"></span>
                <span @click="updateSpecificConsumption">Обновить</span>
              </div>
            </div> -->
      <div class="iteam-group">
        <div class="item">
          <div class="data">
            <div class="quantity">{{ specificConsumption.iso }}</div>
            <div class="subtitle">Изоцианат, л</div>
          </div>
          <div class="icon">
            <div class="circle" style="background: #2d9ad8">
              <div class="title">ISO</div>
              <div class="subtitle">km</div>
            </div>
          </div>
        </div>
        <div class="item">
          <div class="data">
            <div class="quantity">{{ specificConsumption.pol }}</div>
            <div class="subtitle">Полиол, л</div>
          </div>
          <div class="icon">
            <div class="circle" style="background: #fc7a7a">
              <div class="title">POL</div>
              <div class="subtitle">km</div>
            </div>
          </div>
        </div>
        <div class="item">
          <div class="data">
            <div class="quantity">{{ specificConsumption.pen }}</div>
            <div class="subtitle">Пентан, л</div>
          </div>
          <div class="icon">
            <div class="circle" style="background: #4bbeaa">
              <div class="title">PEN</div>
              <div class="subtitle">km</div>
            </div>
          </div>
        </div>
        <div class="item">
          <div class="data">
            <div class="quantity">{{ specificConsumption.kat1 }}</div>
            <div class="subtitle">Катализатор1, л</div>
          </div>
          <div class="icon">
            <div class="circle" style="background: #2d9ad8">
              <div class="title">K1</div>
              <div class="subtitle">km</div>
            </div>
          </div>
        </div>
        <div class="item">
          <div class="data">
            <div class="quantity">{{ specificConsumption.kat2 }}</div>
            <div class="subtitle">Катализатор2, л</div>
          </div>
          <div class="icon">
            <div class="circle" style="background: #fc7a7a">
              <div class="title">K2</div>
              <div class="subtitle">km</div>
            </div>
          </div>
        </div>
        <div class="item">
          <div class="data">
            <div class="quantity">{{ specificConsumption.kat3 }}</div>
            <div class="subtitle">Катализатор3, л</div>
          </div>
          <div class="icon">
            <div class="circle" style="background: #4bbeaa">
              <div class="title">K3</div>
              <div class="subtitle">km</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import { mapActions } from 'vuex'
import { mapGetters } from 'vuex'
import card from '@/components/card/card.vue'
import background from '@/components/background/back.vue'
import Period from '@/components/home/period'
export default {
  components: {
    card,
    background,
    Period,
  },
  created() {
       this.$on('changeCalendar', (calendar) => {
      this.calendar = calendar
    })

    this.$on('setPeriod', (option) => {
      if (option.end) {
        this[option.title].option.id2 = option.id2
        this[option.title].option.isType2 = option.isType2
        this.updateComparisonModule()
      } else {
        this[option.title].option.id1 = option.id1
        this[option.title].option.isType1 = option.isType1
        this['update' + option.title]()
      }
    })
    this.updateSpecificConsumption()
  },
  props:['date'],
  data() {
    return {
      ShowModalPlus: {
        modalBul: false,
      },
      SpecificConsumption: {
        modalBul: false,
        cardShow: true,
        option: {
          id1: 0,
          isType1: null,
        },
      },
      calendar: {
        time: new Date().getTime(),
        date: new Date().getTime(),//formatDate(new Date().getTime()),
      },
    }
  },
  watch: {
    calendar: function () {
      this.updateAll()
    },
     date: function(newD){
    
      this.calendar.date = +formatDate(newD)*1000;
      this.updateSpecificConsumption();
    }
   
  },

  computed: {
    ...mapGetters('home', {
      specificConsumption: 'specificConsumption',
    }),
  },

  methods: {
    ...mapActions('home', {
      getSpecificConsumption: 'getSpecificConsumption',
    }),
    showCartItem(name) {
      this.ShowModalPlus.modalBul = false
      this[name].cardShow = true
    },
    hideModals() {
      if (this.SpecificConsumption.modalBul) {
        this.SpecificConsumption.modalBul = false
      }
    },
    noChange() {
      console.log('change')
    },

    updateSpecificConsumption() {
      this.SpecificConsumption.option.date = this.calendar.date
      this.getSpecificConsumption(this.SpecificConsumption.option)
    },

    updateAll() {
      this.updateSpecificConsumption()
    },
  },
  
}
function formatDate(date) {
  let d = new Date(date)
  // console.log(d.getTime(), 'ggggg')
  return (d.getTime()/1000).toFixed();
}
</script>
<style lang="scss" scoped>
.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #e9e9e9;
  padding: 2px 8px 2px 12px;

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
    width: 25px;
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

.indicators {
  padding-right: 44px;

  .module {
    position: relative;
    display: flex;
    align-items: baseline;
    padding-left: 68px;
    padding-top: 12px;
    margin-bottom: 12px;

    .index {
      font-size: 24px;
      font-weight: 500;
      margin-right: 9px;
    }
  }

  .data-list {
    display: flex;
    flex-direction: column;
    align-items: flex-end;

    .list {
      max-width: 207px;
      width: 100%;
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 12px;
      font-size: 14px;

      .item {
        display: flex;
        align-items: center;
        font-weight: 500;

        .circle {
          width: 12px;
          height: 12px;
          border-radius: 50%;
          margin-right: 6px;
        }
      }
    }
  }

  .indicators-footer {
    display: flex;
    align-items: center;
    justify-content: space-between;

    .title {
      margin-left: 9px;
      font-style: normal;
      font-weight: normal;
      font-size: 14px;
    }

    .data {
      display: flex;
      align-items: baseline;

      .index {
        font-style: normal;
        font-weight: 500;
        font-size: 14px;
      }
    }
  }
}

.charts {
  height: 100%;
  display: flex;
  flex-direction: row;
  padding: 0 36px;

  .block-1 {
    width: 280px;
    margin-right: 36px;
  }

  .block-2 {
    display: flex;
    flex-wrap: wrap;

    .panel-release {
      .chart-content {
        display: flex;

        .diagram {
          width: 45%;
          overflow: hidden;
        }

        .content-box {
          width: 55%;
          padding-top: 25px;

          .indicators {
            .module {
              padding-left: 17px;
            }

            .data-list {
              align-items: end;
              margin-bottom: 8px;
            }

            .indicators-footer {
              .title {
                font-style: normal;
                font-weight: normal;
                font-size: 18px;
                margin-left: 0;
              }
            }
          }
        }
      }
    }

    .consumption {
      .chart-content {
        .iteam-group {
          padding-bottom: 12px;
          display: flex;
          flex-wrap: wrap;

          .item {
            width: 192px;
            height: 90px;
            display: flex;
            flex-direction: row;
            justify-content: center;
            align-items: center;
            padding-bottom: 6px;
            padding-right: 6px;
            padding-left: 12px;
            border: 2px solid #ecedf4;
            box-sizing: border-box;
            border-radius: 12px;
            margin-right: 12px;
            margin-top: 11px;

            .data {
              width: 116px;
              display: flex;
              justify-content: center;
              align-items: center;
              flex-direction: column;
              margin-right: 6px;
              margin-top: 6px;

              .quantity {
                font-family: 'Montserrat', -apple-system, BlinkMacSystemFont,
                  'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
                font-weight: 500;
                font-size: 42px;
                color: #000000;
              }

              .subtitle {
                width: 100%;
                font-family: 'Montserrat', -apple-system, BlinkMacSystemFont,
                  'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
                font-weight: 500;
                font-size: 12px;
                color: #b1b1bc;
              }
            }

            .icon {
              font-family: 'Montserrat', -apple-system, BlinkMacSystemFont,
                'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
              font-weight: 500;
              font-size: 16px;
              color: #ffffff;

              .circle {
                width: 50px;
                height: 50px;
                border-radius: 50%;
                display: flex;
                justify-content: center;
                align-items: center;
              }
            }

            &:nth-child(3n) {
              margin-right: 0;
            }
          }
        }
      }
    }

    .chart-data-min {
      width: 628px;
      height: 144px;
      border: 2px solid #e9e9e9;
      border-radius: 9px;
      //margin-bottom: 36px;
      margin-right: 36px;

      .chart-content {
        padding: 0 12px;
        display: flex;
        flex-wrap: wrap;

        .iteam-group {
          display: flex;
          flex-wrap: wrap;

          .item {
            width: 192px;
            height: 90px;
            display: flex;
            flex-direction: row;
            justify-content: center;
            align-items: center;
            padding-bottom: 6px;
            padding-right: 6px;
            padding-left: 12px;
            border: 2px solid #ecedf4;
            box-sizing: border-box;
            border-radius: 12px;
            margin-right: 12px;
            margin-top: 11px;

            .data {
              width: 116px;
              display: flex;
              justify-content: center;
              align-items: center;
              flex-direction: column;
              margin-right: 6px;
              margin-top: 6px;

              .quantity {
                height: 60px;
                text-align: center;
                display: flex;
                align-items: center;
                font-family: 'Montserrat', -apple-system, BlinkMacSystemFont,
                  'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
                font-weight: 500;
                font-size: 24px;
                color: #000000;
              }

              .subtitle {
                width: 100%;
                font-family: 'Montserrat', -apple-system, BlinkMacSystemFont,
                  'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
                font-weight: 500;
                font-size: 12px;
                color: #b1b1bc;
              }
            }

            .icon {
              width: 50px;
              height: 50px;
              border-radius: 50%;
              background-image: url('~assets/img/lightning.png');
              background-repeat: no-repeat;
              background-position: center;
              background-size: contain;

              .circle {
                display: flex;
                justify-content: center;
                align-items: center;
              }
            }

            .iconLast {
              width: 50px;
              height: 50px;
              border-radius: 50%;
              background-image: url('~assets/img/fire.png');
              background-repeat: no-repeat;
              background-position: center;
              background-size: contain;

              .circle {
                display: flex;
                justify-content: center;
                align-items: center;
              }
            }

            &:nth-child(3n) {
              margin-right: 0;
            }
          }
        }
      }
    }

    .consumption {
      .chart-content {
        padding: 0 12px;
        display: flex;
        flex-wrap: wrap;

        .item {
          width: 192px;
          height: 90px;
          display: flex;
          flex-direction: row;
          justify-content: center;
          align-items: center;
          padding-bottom: 6px;
          padding-right: 6px;
          padding-left: 12px;
          border: 2px solid #ecedf4;
          box-sizing: border-box;
          border-radius: 12px;
          margin-right: 12px;
          margin-top: 11px;

          .data {
            width: 116px;
            display: flex;
            justify-content: center;
            align-items: center;
            flex-direction: column;
            margin-right: 6px;
            margin-top: 6px;

            .quantity {
              font-family: 'Montserrat', -apple-system, BlinkMacSystemFont,
                'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
              font-weight: 500;
              font-size: 48px;
              color: #000000;
            }

            .subtitle {
              width: 100%;
              font-family: 'Montserrat', -apple-system, BlinkMacSystemFont,
                'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
              font-weight: 500;
              font-size: 12px;
              color: #b1b1bc;
            }
          }

          .icon {
            .circle {
              width: 50px;
              height: 50px;
              border-radius: 50%;
              display: flex;
              justify-content: center;
              align-items: center;
              flex-direction: column;

              .title {
                font-family: 'Montserrat', -apple-system, BlinkMacSystemFont,
                  'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
                font-weight: 500;
                font-size: 16px;
                color: #ffffff;
                text-align: center;
              }

              .subtitle {
                font-family: 'Montserrat', -apple-system, BlinkMacSystemFont,
                  'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
                font-weight: 500;
                font-size: 12px;
                color: #ffffff;
                text-align: center;
              }
            }
          }

          &:nth-child(3n) {
            margin-right: 0;
          }
        }
      }
    }

    .comparison-module {
      font-size: 14px;

      .chart-content {
        display: flex;
        width: 100%;
        height: calc(100% - 21px);
        padding: 6px 3px;

        .content-box {
          width: 50%;
          height: 100%;
          margin-right: 3px;
          border-right: 1px solid #e9e9e9;

          .calendar-period {
            padding: 6px 0;

            .select-date {
              height: 20px;
              margin-left: 12px;
              font-weight: 600;
              font-size: 12px;
              line-height: 15px;
              text-align: left;
              color: #9098af;
            }

            .select-date input {
              height: 20px;
              padding-left: 3px;
              outline: none;
              font-weight: normal;
              font-size: 12px;
              line-height: 15px;
              color: #9098af;
              border: 1px solid #9098af;
              border-radius: 4px;
            }
          }

          .period {
            btn.text {
              margin-right: 6px;
            }
            button:last-child {
              margin-right: 3px;
            }
          }
        }
      }

      .content-box:last-child {
        border-right: none;
        margin-right: 0;
      }
    }
  }
}

.data {
  display: flex;

  .index {
    margin-right: 4px;
  }
}

.chart-data {
  width: 628px;
  height: 246px;
  border: 2px solid #e9e9e9;
  border-radius: 9px;
  //margin-bottom: 37px;
  //margin-right: 48px;
  margin-right: 36px;
}

.resul {
  .result-ok {
    font-family: 'Montserrat', -apple-system, BlinkMacSystemFont, 'Segoe UI',
      Roboto, 'Helvetica Neue', Arial, sans-serif;
    font-style: normal;
    font-weight: 500;
    font-size: 14px;
    line-height: 14px;
    color: #7cd420;
  }

  .result-minus {
    font-family: 'Montserrat', -apple-system, BlinkMacSystemFont, 'Segoe UI',
      Roboto, 'Helvetica Neue', Arial, sans-serif;
    font-style: normal;
    font-weight: 500;
    font-size: 14px;
    line-height: 14px;
    color: #f3345d;
  }

  .result-null {
    font-family: 'Montserrat', -apple-system, BlinkMacSystemFont, 'Segoe UI',
      Roboto, 'Helvetica Neue', Arial, sans-serif;
    font-style: normal;
    font-weight: 500;
    font-size: 14px;
    line-height: 14px;
    color: #96a2b0;
  }
}

.btn-group {
  main {
    width: 100%;
    height: 100%;
  }

  .btn-rnd {
    outline: none;
    width: 60px;
    height: 60px;
    border-radius: 50%;
    border: 2px #ff7167 solid;
    cursor: pointer;
    background: #ffffff;
    color: #ff7167;
    font-weight: 500;
    font-size: 48.4615px;
    line-height: 81px;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    text-transform: uppercase;

    position: absolute;
    bottom: 48px;
    right: 48px;
    z-index: 2;

    &.btn-close {
      transform: rotate(45deg);
      background: #ff7167;
      color: #ffffff;
    }
  }

  .btn-rnd:hover {
    background: #ff7167;
    color: #ffffff;
    transition: 0.2s linear;
  }

  .plus-form {
    width: 244px;
    height: auto;
    background: #ffffff;
    border: 2px solid #f3f3f3;
    border-radius: 5px;

    position: absolute;
    bottom: 112px;
    right: 48px;

    z-index: 2;

    .plus-form-item {
      cursor: pointer;
      height: 36px;
      padding-left: 24px;
      padding-right: 24px;
      font-weight: 500;
      font-size: 12px;
      line-height: 15px;
      display: flex;
      align-items: center;
      justify-content: flex-end;
      color: #bababa;
      border-bottom: 2px solid #f3f3f3;

      &:hover {
        color: #727272;
        transition: 0.2s linear;
      }
    }

    .plus-form-item:last-child {
      border-bottom: none;
    }
  }
}

.chart-content {
  position: relative;
}

.menu-bul {
  -moz-user-select: none;
  -khtml-user-select: none;
  user-select: none;
  position: absolute;
  top: 0;
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
