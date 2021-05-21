<template>
  <div>
    <background
      style="margin-top: 0px; margin-left: 0px; height: 350px; width: 285px"
      title="Продолжительность работы, ч"
    >
      <div class="chart-content">
        <div class="line" v-for="(item, id) in lineDataFirst.interval" :key="item.id">
          <div class="box-line">
            <div class="bg" :style="'width: ' + item.progress + '%'">
              <div class="start" v-if="item.progress >= 50">
                {{ item.start }}
              </div>
              <div class="end" v-if="item.progress >= 50">{{ item.end }}</div>
            </div>
          </div>
          <div class="data-line">{{ item.duration }}</div>
          <div
            class="title-line"
            :class="{ down: id === 0 }"
            v-if="item.progress < 50"
          >
            <div class="start">Начало - {{ item.start }}</div>
            <div class="end">Конец - {{ item.end }}</div>
          </div>
        </div>
      </div>
      <div class="chart-footer">
        <div class="title-footer">Общее рабочее время за день</div>
        <div class="view">{{ lineDataFirst.sum }}</div>
      </div>
    </background>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
import { mapActions } from "vuex";
import calendar from "@/components/home/calendar";
import background from "@/components/background/back.vue";

export default {
  components: {
    background,
  },
  name: "DurationWork",
  props: ["card", "calendar"],
  data() {
    return {
      periodActive: [true, false, false, false],
      lineDataFirst: {
        interval: [
          {
            id:1,
            start: 15,
            end: 30,
            duration: 15,
            progress: 50,
          },
          {
            id:2,
            start: 15,
            end: 30,
            duration: 15,
            progress: 50,
          },
        ],
      },
    };
  },
  created() {
    this.update();
  },
  watch: {
    calendar: function () {
      this.update();
    },
  },
  computed: {
    ...mapGetters("home", {
      lineDataFirst: "lineDataFirst",
    }),
    option() {
      let smena = 0;
      if (this.periodActive[1] || this.periodActive[2]) smena = 1;
      else if (this.periodActive[2]) smena = 2;
      else if (this.periodActive[3]) smena = 3;

      let now = new Date();
      if (this.calendar) now.setTime(this.calendar.time);

      return {
        date:
          now.getFullYear() + "-" + (now.getMonth() + 1) + "-" + now.getDate(),
        smena: smena,
      };
    },
  },
  methods: {
    ...mapActions("home", {
      getLineDataFirst: "getLineDataFirst",
    }),
    setPeriod(id) {
      let arr = [false, false, false, false];
      arr[id] = true;
      this.periodActive = arr;
      this.update();
    },
    update() {
      this.getLineDataFirst(this.option);
    },
  },
};
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
}

.chart-footer {
  width: 100%;
  height: 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 281px;
  padding: 4px 24px 4px 6px;

  .title-footer {
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
</style>
