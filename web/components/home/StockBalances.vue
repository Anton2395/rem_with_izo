<template>
  <div class="chart second">
    <div class="chart-header">
      <div class="title">Остатки на складах</div>
      <div
          class="bul"
          @click="$parent.$emit('showModalBul', 'StockBalances')"
          @click.stop="$parent.$emit('noChange')"
      >
        <span></span>
      </div>
      <div
          class="menu-bul"
          v-if="card.modalBul"
      >
        <div
            class="btn-bul"
            @click="$parent.$emit('hideCartItem','StockBalances')"
        ><span class="show"></span>
          <span>Скрыть</span>
        </div>
        <div class="btn-bul">
          <span class="new"></span>
          <span @click="update">Обновить</span>
        </div>
      </div>
    </div>
    <div class="chart-content">
      <div class="box" v-for="el in stockBalances.storehouse">
        <div class="name-block">{{ el.name }}</div>
        <div class="block-content" v-if="el.iso.length">
          <div class="title-position">Изоционат</div>
          <div class="group">
            <div class="number-lit" v-for="i in el.iso">{{ i }}л
              <div class="line-progress">
                <div class="data-progress" :style="'width: ' + i + '%'"></div>
              </div>
            </div>
          </div>
        </div>
        <div class="block-content" v-if="el.pol.length">
          <div class="title-position">Полиол</div>
          <div class="group">
            <div class="number-lit" v-for="i in el.pol">{{ i }}л
              <div class="line-progress">
                <div class="data-progress" :style="'width: ' + i + '%'"></div>
              </div>
            </div>
          </div>
        </div>
        <div class="block-content" v-if="el.pen.length">
          <div class="title-position">Пентан</div>
          <div class="group">
            <div class="number-lit" v-for="i in el.pen">{{ i }}л
              <div class="line-progress">
                <div class="data-progress" :style="'width: ' + i + '%'"></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="chart-footer">
      <div class="title">Итого - ISO: <b>{{ stockBalances.in_total.iso }}л</b>; POL: <b>{{ stockBalances.in_total.pol }}л</b>; PEN: <b>{{ stockBalances.in_total.pen }}л</b></div>
    </div>
  </div>
</template>

<script>

import {mapActions} from "vuex";
import {mapGetters} from "vuex";
import calendar from "@/components/home/calendar";

export default {
  name: "StockBalances",
  props: [
    'card',
    'calendar'
  ],
  created() {
    this.update();
  },
  data() {
    return {}
  },
  watch: {
    calendar: function() {
      this.update();
    }
  },
  methods: {
    ...mapActions('home', {
      getStockBalances: 'getStockBalances',
    }),
    update() {
      this.getStockBalances(this.option);
    },
    noChange() {
      console.log('change');
    },
  },
  computed: {
    ...mapGetters('home', {
      stockBalances: 'stockBalances',
    }),
    option() {
      return {
        date: this.calendar ? this.calendar : new Date().getTime(),
      }
    }
  },
}
</script>

<style lang="scss" scoped>

.chart {
  width: 284px;
  border: 2px solid #E9E9E9;
  border-radius: 9px;
}

.chart.second {
  height: 378px;
  margin-bottom: 24px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;

  .chart-content {
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    overflow: auto;

    .box {
      display: flex;
      flex-direction: column;
      padding: 6px 8px 6px 12px;
      font-weight: normal;
      font-size: 10px;
      line-height: 12px;
      color: #000000;
      border-bottom: 1px solid #E9E9E9;

      .name-block {
        margin-bottom: 6px;
      }

      .block-content {
        display: flex;
        flex-direction: column;
        padding-left: 12px;
        margin-bottom: 6px;

        .title-position {
          font-weight: normal;
          font-size: 10px;
          line-height: 12px;
          color: #000000;
        }

        .group {
          display: flex;
          flex-direction: column;

          .number-lit {
            display: flex;
            align-items: center;
            justify-content: flex-end;
            font-weight: 500;
            font-size: 12px;
            line-height: 15px;
            color: #000000;
          }

          .line-progress {
            width: 178px;
            height: 8px;
            background: #ECEDF4;
            border-radius: 2px;
            margin-left: 6px;

            .data-progress {
              height: 8px;
              background: #3F51B5;
              border-radius: 2px;
              z-index: 2;
            }
          }
        }
      }
    }
  }
}

.chart-header {
  display: flex;
  position: relative;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #E9E9E9;
  padding: 3px 6px 3px 12px;

  .title {
    font-family: "Montserrat", -apple-system, BlinkMacSystemFont, "Segoe UI",
    Roboto, "Helvetica Neue", Arial, sans-serif;
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
      background-color: #CFCDCD;
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

      background-color: #CFCDCD;
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
      background-color: #CFCDCD;
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
  justify-content: center;
  align-items: center;
  border-top: 1px solid #E9E9E9;
  padding: 6px 24px;

  .title {
    font-weight: normal;
    font-size: 12px;
    line-height: 15px;
    display: flex;
    align-items: center;
    text-align: center;
    color: #3F51B5;
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
  background: #F7F8FA;
  box-shadow: 0px 2px 6px rgba(0, 0, 0, 0.25);
  border-radius: 4px 0px 4px 4px;

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
    color: #BABABA;

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
