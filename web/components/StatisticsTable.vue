<template >
  <div style="overflow-x: auto">
    <div class="table_title">
      Статистические данные
      <img
        class="closeStatisticsTable"  @click="$emit('closeForm')"
        src="@/assets/svg/recorder/carbon_close.svg"
      />
    </div>
    <table style="margin-top: 10px">
      <thead>
        <tr>
          <th>Название графика</th>
          <!-- <th  v-for="(point, index) in arrHead" :key="index">
            {{ point }}
            <button @click="$parent.delColTable(index)">
              <img  class="closeTable" src="@/assets/svg/recorder/carbon_close.svg" /> 
            </button>
          </th> -->
          <th>Единицы измерения</th>
          <th>Количество точек</th>
          <th>MAX</th>
          <th>MIN</th>
          <th>AVERAGE</th>
          <!-- <th>MAX_common</th>
          <th>MIN_common</th>
          <th>AVERAGE_common</th> -->
        </tr>
      </thead>

      <tbody>
        <tr v-for="ch in chart" :key="ch.name">
          <!-- <td :style="{ color: p1.color }">{{ p1.name }}</td>
          <td v-for="(p2, i2) in p1.value" :key="i2">
            {{ p2 }}
          </td> -->
          <td :style="{ color: ch.color }">{{ ch.name }}</td>
          <td>{{ ch.yAxis }}</td>
          <td>{{ ch.data.length }}</td>
          <td>{{ ch.max }}</td>
          <td>{{ ch.min }}</td>
          <td>{{ ch.average.toFixed(2) }}</td>
         
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
// import {mapGetters} from 'vuex';
// import {mapActions} from 'vuex';

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
  -hour < 10 ? "0" + hour : hour;
  minutes = minutes < 10 ? "0" + minutes : minutes;

  return `${dayOfMonth}.${month}.${year} ${hour}:${minutes}`;
}

export default {
  name: "StatisticsTable",
  props: ["tData", "chart"],
  data() {
    return {
      arrHead: [],
      arrBody: [],
    };
  },
  computed: {},
  created() {
    this.updateTable();
  },
  watch: {
    chart: function (val) {
      if (val) {
        this.updateTable();
      }
    },
  },
  methods: {
    updateTable(){
      this.chart.forEach((item, i) => {
        // debugger;
          let min = item.data[0].y,
            max = item.data[0].y,
            average = 0;
          item.data.forEach((el) => {
            if (el.y > max) {
              max = el.y;
            }
            if (el.y < min) {
              min = el.y;
            }
            average = average + el.y;
          });
          average = average / item.data.length;

          this.chart[i].min = min;
          this.chart[i].max = max;
          this.chart[i].average = average;
        });
    }
  },
};
</script>

<style scoped>
table {
  font-family: "Montserrat", Sans-Serif;
  font-size: 12px;
  border-collapse: collapse;
  text-align: center;
}
th {
  cursor: pointer;
  border-collapse: collapse;
}

th,
td:first-child {
  font-family: "Montserrat";
  font-style: normal;
  align-items: center;
  padding: 10px 20px;
  /* font-weight: 500;
  line-height: 12px; */

}
th,
td {
  border-style: solid;
  border-width: 1px 1px 1px;
  border-color: #4a627a;
  font-weight: 500;
        width: 265px;
}

th:first-child,
td:first-child {
  text-align: center;
}
.closeStatisticsTable {
  margin-left: 5px;
  cursor: pointer;
}
.closeStatisticsTable:hover {
  background-image: url("~assets/svg/hov_carbon_close.svg");
  outline: none;
}
.table_title {
  font-family: "Montserrat";
  font-size: 12px;
  color: #90a1b1;
}
table th {

margin-bottom: 5px;
}
</style>