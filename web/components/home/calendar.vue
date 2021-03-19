<template>
  <section class="calendar">
    <button
        class="prev"
        @click="prevCalendar()"
    >
    </button>
    <div class="calendar-box">
      <div
          v-on:click="setCalendar(calendar)"
          class="day"
          v-for="calendar in calendars"
          :key="JSON.stringify(calendar.day)"
          :class="{active: calendar.isActive}"
      >
        <div class="title">{{ calendar.title }}</div>
        <div class="number">{{ calendar.day }}</div>
      </div>
      <div
          class="day new"
           v-on:click="setCalendarNow()"
      >
        now</div>
    </div>
    <button
        :disabled="!this.isNext"
        class="next"
        @click="nextCalendar()"
    >
    </button>
  </section>
</template>

<script>
export default {
  name: "calendar",
  data () {
    return {
      currentCalendar: null,
      nowDateTime: this.createDate(),
      isNext: false,
    }
  },
  created() {
    this.$parent.$emit('changeCalendar', this.nowDateTime);
  },
  computed: {
    calendars() {
      let calendars = [];
      for (let i = 22; i >= 1; i--) {
        let time = this.nowDateTime.time - i * 1000 * 3600 * 24;
        let day = new Date(time);
        calendars.push(this.createDate(day))
      }
      return calendars;
    },
  },
  methods: {
    setCalendar (calendar) {
      calendar.isActive = true;
      this.currentCalendar = calendar;
      this.$parent.$emit('changeCalendar', calendar);
    },
    setCalendarNow () {
      this.nowDateTime = this.createDate();
      this.currentCalendar = null;
      this.isNext = false;
      this.$parent.$emit('changeCalendar', this.nowDateTime);
    },
    nextCalendar () {
      if(new Date(new Date().getTime() - 1000 * 24 *3600).getDate() === new Date(this.nowDateTime.time).getDate() && new Date(new Date().getTime() - 1000 * 24 *3600).getMonth() === new Date(this.nowDateTime.time).getMonth())
        this.isNext = false;
      else
        this.nowDateTime = this.createDate(new Date(this.nowDateTime.time + 1000 * 3600 * 24));
    },
    prevCalendar (){
      this.nowDateTime = this.createDate(new Date(this.nowDateTime.time - 1000 * 3600 * 24));
      this.isNext = true;
    },
    createDate(day = new Date()) {
      let days = ["Вс", "Пн", "Вт", "Ср", "Чт", "Пт", "Сб"];
      return {
            day: day.getDate(),
            title: days[day.getDay()],
            date: day.getFullYear() + '-' + (day.getMonth() + 1) + '-' + day.getDate(),
            month: day.getMonth(),
            year: day.getFullYear(),
            time: day.getTime(),
            isActive: (this.currentCalendar && this.currentCalendar.day === day.getDate()) ? this.currentCalendar.isActive : false,
      }
    }
  },
}
</script>

<style lang="scss" scoped>

.calendar {
  width: 100%;
  display: flex;
  justify-content: center;
  position: relative;
  padding: 24px 0 12px 0;

  .prev {
    border: none;
    outline: none;
    cursor: pointer;
    position: absolute;
    top: 44px;
    left: 57px;
    width: 40px;
    height: 40px;
    background-color: transparent;
    background-image: url("~assets/img/arrow_prew.svg");
    background-position: center;
    background-repeat: no-repeat;
    background-size: cover;
  }

  .next {
    border: none;
    outline: none;
    cursor: pointer;
    position: absolute;
    top: 44px;
    right: 57px;
    width: 40px;
    height: 40px;
    background-image: url("~assets/img/arrow_next.png");
    background-position: center;
    background-repeat: no-repeat;
    background-size: cover;
  }

  .calendar-box {
    width: calc(100% - 242px);
    display: flex;
    align-items: center;
    overflow: auto;

    .day {
      height: 80px;
      width: 56px;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      padding: 9px 12px;
      background: #FFFFFF;
      border: 2px solid #ECEDF4;
      border-radius: 11px;
      margin-right: 12px;
      margin-bottom: 6px;
      cursor: pointer;

      .title {
        font-family: "Montserrat", -apple-system, BlinkMacSystemFont, "Segoe UI",
        Roboto, "Helvetica Neue", Arial, sans-serif;
        font-size: 16px;
        font-weight: 400;
        text-align: center;
        color: #B1B1BC;
        margin-bottom: 7px;
      }

      .number {
        font-family: "Montserrat", -apple-system, BlinkMacSystemFont, "Segoe UI",
        Roboto, "Helvetica Neue", Arial, sans-serif;
        font-size: 24px;
        font-weight: 500;
        text-align: center;
        color: #42435F;
      }

      &.new {
         border: 2px solid #3F51B5;
         margin-right: 0;
      }

      &:hover,
      &.active {
        background: #272848;
        transition: 0.2s;

        .number,
        .title {
          color: #BFC0C9;
        }
      }
    }

    .new {
      font-family: "Montserrat", -apple-system, BlinkMacSystemFont, "Segoe UI",
      Roboto, "Helvetica Neue", Arial, sans-serif;
      font-size: 14px;
      font-weight: 500;
      text-align: center;
      color: #42435F;
      text-transform: uppercase;

      &:hover {
        background: #272848;
        transition: 0.2s;
        color: #BFC0C9;
      }
    }
  }
}
</style>
