<template>
  <div class="overlay" @click="$emit('changeShow')">
    <div
      class="settings-charts"
      v-on:click.stop="noChange"
      :style="{ top: topPosition + 'px' }"
    >
      <button class="btn_close" @click="$emit('changeShow')"></button>
      <div class="tabhead">
        <button style="margin: auto" class="btn_icon">
          <div class="tabhead_title">{{ content.title }}</div>
        </button>
      </div>
<!-- 
      <div class="switchBox">
        <div class="switchOn" v-on:click="toggleSwitchOn">
          {{ content.selectLeft }}
        </div>
        <div class="switchcheck" v-on:click="toggleSwitch">
          <IconifyIcon
            icon="baselineToggleOff"
            :style="{ color: '#3F51B5', fontSize: '24px' }"
            v-if="isChartOne"
          />
          <IconifyIcon
            icon="baselineToggleOff"
            :style="{ color: '#3F51B5', fontSize: '24px' }"
            :horizontal-flip="true"
            v-else
          />
        </div>
        <div class="switchOff" v-on:click="toggleSwitchOff">
          {{ content.selectRight }}
        </div>
      </div> -->
      <!-- <div style="display: inline">
        <div style="margin-right:20px" class="time-update-title">Время обновления, мс
          <input class="checkbox" type="checkbox" id="scales" name="scales" />
        <label class="checkBoxTitle" for="scales">По умолчанию</label>

        </div>
         
      </div> -->
        <!-- <input class="timeUpdateInput" placeholder="10" type="text" size="30" /> -->
       
      <div class="select-date-title">Задать период времени</div>
      <div class="select-date">
        <input type="datetime-local" v-model="start" />

        <label>-</label>
      

        <input type="datetime-local" v-model="end" />
      </div>
      <div class="tabfoot">
        <!-- <button class="tabfoot-left btn_icon">
          <div class="tabfoot_title">{{ content.btnLeft }}</div>
        </button> -->
        <button class="tabfoot-right btn_icon" @click="loadData()">
          <div class="tabfoot_title">{{ content.btnRight }}</div>
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { mapActions, mapGetters } from "vuex";

const nowDate = new Date();
const nowDateTime = nowDate.toLocaleTimeString();
export default {
  name: "VFunctionGraph",
  // props: {
  //   content: Object,
  //   topPosition
  // },
  props: ["content", "topPosition"],
  data() {
    return {
      ShowSwitchOn: true,
      start: nowDate.toISOString().substr(0, 10) + "T" + nowDateTime,
      end: nowDate.toISOString().substr(0, 10) + "T" + nowDateTime,
    };
  },
  computed: {
    ...mapGetters("oeecharts", {
      isChartOne: "isChartOne",
    }),
  },
  methods: {
    ...mapActions("oeecharts", {
      getBasicData: "getBasicData",
      getTimeStatus: "getTimeStatus",
      getReason: "getReason",
      getTableOEE: "getTableOEE",
      updateIsChartOne: "updateIsChartOne",
    }),
    toggleSwitchOn() {
      this.updateIsChartOne(true);
    },
    toggleSwitch() {
      this.updateIsChartOne(!this.isChartOne);
    },
    toggleSwitchOff() {
      this.updateIsChartOne(false);
    },
    noChange() {
   
    },
    loadData() {
      // this.content.opt.smena = 0;
      // this.content.opt.start = parseInt(new Date(this.start).getTime()/1000);
      // this.content.opt.end = parseInt(new Date(this.end).getTime()/1000);
      // this.getTimeStatus(this.content.opt);
      // this.getReason(this.content.opt);
      // this.getBasicData(this.content.opt);
      // this.getTableOEE(this.content.opt);
      let min = this.start.replace("T", " "),
        max = this.end.replace("T", " ");
     
      if (min.length <= 16) {
        min = min + ":00";
      }
      if (max.length <= 16) {
        max = max + ":00";
      }
      let sel = { min, max };

      let el = this.$parent;
        el.getExtNewDate(sel);
      
      this.$emit("changeShow");
    },
  },
};
</script>

<style scoped>
.overlay {
  width: 100vw;
  height: 100vh;
  background-color: rgba(0, 0, 0, 0.062);
  z-index: 100;
  position: absolute;
  top: 0;
  right: 0;
}

.settings-charts {
  background-color: #f7f8fa;
  color: #4b6075;
  box-shadow: 0px 2px 6px rgba(0, 0, 0, 0.25);

  width: 466px;
  height: 180px;
  z-index: 110;

  position: absolute;
  /* top: 96px; */
  right: 16px;
  /* добавила рита */
  padding: 0 0 12px 0;
}

.btn_icon {
  background: none;
  border: none;

  display: flex;
  justify-content: baseline;
  outline: none;
}

.tabhead_title {
  font-weight: 500;
  font-size: 18px;
  line-height: 22px;
  padding-top: 3px;
  padding-left: 40px;

  color: #4b6075;
}

.tabhead {
  height: 24px;
  display: flex;
  justify-content: flex-start;
  width: 100%;
  margin-left: -35px;
}

.select-date {
  height: 24px;
  margin-top: 6px;
  margin-left: 12px;
  font-weight: 600;
  font-size: 12px;
  line-height: 15px;
  text-align: left;
  color: #9098af;
}

.select-date input {
  height: 24px;
  padding-left: 3px;
  outline: none;
  font-weight: normal;
  font-size: 12px;
  line-height: 15px;
  color: #9098af;
  border: 1px solid #9098af;
  border-radius: 4px;
}
.timeUpdateInput {
  height: 24px;
  margin-top: 6px;
  margin-left: 12px;
  font-weight: 600;
  font-size: 12px;
  line-height: 15px;
  text-align: left;
  color: #9098af;
  color: #9098af;
  border: 1px solid #9098af;
  border-radius: 4px;
  outline: none;
  font-weight: normal;
  text-align: center;
}

.select-date-title {
  height: 21px;
  margin-top: 24px;
  margin-left: 12px;
  font-weight: 600;
  font-size: 12px;
  line-height: 15px;
  text-align: left;
}
.time-update-title {
  height: 21px;
  margin-top: 24px;
  margin-left: 12px;
  font-weight: 600;
  font-size: 12px;
  line-height: 15px;
  text-align: left;
  display: flex;
  align-items: center;
}

.switchBox {
  cursor: pointer;
  margin-top: 22px;
  font-weight: 600;
  font-size: 12px;
  line-height: 15px;
  display: flex;
  flex-direction: row;
  justify-content: flex-start;
  align-items: center;
}

.switchcheck {
  cursor: pointer;
  padding: 0 6px;
  width: 24px;
  height: 24px;
}

.switchOn {
  padding-left: 12px;
}

.switchOff {
  padding-left: 12px;
}

.switch {
  position: relative;
  display: inline-block;
  width: 20px;
  height: 10px;
}

.tabfoot {
  margin-top: 46px;
  /* width: 466px; */
  display: flex;
  flex-direction: row;
}

.tabfoot button {
  padding: 0;
  width: 466px;
  height: 36px;
}

.tabfoot button:hover {
  box-shadow: 0px 0px 6px rgba(0, 0, 0, 0.25);
}

.tabfoot-left {
  background-color: hsl(211, 100%, 90%);
}

.tabfoot-left:hover {
  background-color: hsl(211, 100%, 87%);
}

.tabfoot-right {
  background-color: hsl(134, 41%, 88%);
}

.tabfoot-right:hover {
  background-color: hsl(134, 41%, 85%);
}

.tabfoot_title {
  width: 100%;
  font-weight: 500;
  font-size: 14px;
  line-height: 17px;
  padding-top: 9px;
  text-align: center;
}
.btn_close {
  cursor: pointer;
  position: absolute;
  /* добавила рита */
  right: 469px;
  width: 24px;
  height: 24px;
  background-image: url("~assets/svg/clear_24px.svg");
  background-position: center;
  background-repeat: no-repeat;
  background-size: contain;
}

.checkBoxTitle{
  
 
  margin-left: 5px;
  font-weight: normal;
  font-size: 12px;
  line-height: 15px;
  text-align: left;
}
.checkbox{
  margin-left: 30px;
  transform: scale(0.9);
}
</style>
