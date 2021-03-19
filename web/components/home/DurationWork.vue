<template>
  <div class="chart first">
      <div class="chart-header">
        <div class="box-header">
          <div class="title">Продолжительность работы,ч</div>
          <div
              class="bul"
              @click="$parent.$emit('showModalBul', 'DurationWork')"
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
                @click="$parent.$emit('hideCartItem','DurationWork')"
              ><span class="show"></span>
              <span>Скрыть</span>
            </div>
            <div class="btn-bul" @click="update">
              <span class="new"></span>
              <span>Обновить</span>
            </div>
          </div>
        </div>
        <div class="period">
          <button
              v-on:click="setPeriod(0)"
              class="btn text"
              :class="{active: periodActive[0]}"
          >сутки
          </button>
          <button
              v-on:click="setPeriod(1)"
              class="btn text"
              :class="{active: periodActive[1] || periodActive[2] || periodActive[3]}"
          >смена
          </button>
          <button
              v-on:click="setPeriod(1)"
              class="btn num"
              :class="{active: periodActive[1]}"
          >1
          </button>
          <button
              v-on:click="setPeriod(2)"
              class="btn num"
              :class="{active: periodActive[2]}"
          >2
          </button>
          <button
              v-on:click="setPeriod(3)"
              class="btn num"
              :class="{active: periodActive[3]}"
          >3
          </button>
        </div>
      </div>
      <div class="chart-content">
        <div class="line" v-for="(item, id) in lineDataFirst.interval">
          <div class="box-line">
            <div class="bg" :style="'width: ' + item.progress + '%'">
              <div class="start" v-if="item.progress >= 50">{{ item.start }}</div>
              <div class="end" v-if="item.progress >= 50">{{ item.end }}</div>
            </div>
          </div>
          <div class="data-line">{{ item.duration }}</div>
          <div class="title-line" :class="{down: id===0}"  v-if="item.progress < 50">
            <div class="start">Начало - {{item.start}}</div>
            <div class="end">Конец - {{item.end}}</div>
          </div>
        </div>
      </div>
      <div class="chart-footer">
        <div class="title">Общее рабочее время за день</div>
        <div class="view">{{ lineDataFirst.sum }}</div>
      </div>

    </div>
</template>

<script>

import {mapGetters} from "vuex";
import {mapActions} from "vuex";
import calendar from "@/components/home/calendar";

export default {
  name: "DurationWork",
  props: [
      'card',
      'calendar'
  ],
  data() {
    return {
      periodActive: [true, false, false, false],
    }
  },
  created() {
    this.update();
  },
  watch: {
    calendar: function() {
      this.update();
    }
  },
  computed: {
    ...mapGetters("home", {
      lineDataFirst: "lineDataFirst",
    }),
    option() {
      let smena = 0;
      if(this.periodActive[1] || this.periodActive[2])
        smena = 1;
      else if(this.periodActive[2])
        smena = 2;
      else if(this.periodActive[3])
        smena = 3;

      let now = new Date();
      if(this.calendar)
        now.setTime(this.calendar.time);

      return {
        date: now.getFullYear() + '-' + (now.getMonth() + 1) + '-' + now.getDate(),
        smena: smena,
      }
    }
  },
  methods: {
    ...mapActions("home", {
      getLineDataFirst: "getLineDataFirst",
    }),
    setPeriod (id) {
      let arr = [false, false, false, false];
      arr[id] = true;
      this.periodActive = arr;
      this.update();
    },
    update() {
      this.getLineDataFirst(this.option);
    }
  },
}
</script>

<style lang="scss" scoped>

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

    border: 1px solid #ECEDF4;
    border-radius: 3px;
    background: #FFFFFF;

    font-weight: 500;
    font-size: 12px;
    color: #42435F;

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
    background: #FFFFFF;
    margin-right: 6px;
  }

  .active {
    background: #272848;
    color: #BFC0C9;
    text-align: center;
  }

  button:last-child {
    margin-right: 0;
  }
}
.chart {
  width: 284px;
  border: 2px solid #E9E9E9;
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
          background: #ECEDF4;

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
        background: #FFFFFF;

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
  border-bottom: 1px solid #E9E9E9;
  padding: 2px 0;

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
    width: 17px;
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
  justify-content: space-between;
  align-items: center;
  border-top: 1px solid #E9E9E9;
  padding: 4px 24px 4px 6px;

  .title {
    font-weight: normal;
    font-size: 12px;
    line-height: 15px;
    display: flex;
    align-items: center;
    color: #3F51B5;
  }

  .view {
    font-weight: bold;
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
