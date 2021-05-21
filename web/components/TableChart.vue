<template >
  <div style="overflow-x:auto;">
    <table>
      <thead>
        <tr>
          <th>Переменные / Время</th>
          <th  v-for="(point, index) in arrHead" :key="index">
            {{ point }}
            <button @click="$parent.delColTable(index)">
              <img  class="closeTable" src="@/assets/svg/recorder/carbon_close.svg" /> 
            </button>
          </th>
            </tr>
      </thead>

      <tbody>
        <tr v-for="(p1, i1) in arrBody" :key="i1">
          <td :style="{color:p1.color}">{{ p1.name }}</td>
          <td v-for="(p2, i2) in p1.value" :key="i2">
            {{ p2 }}
          </td>
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
  name: "TableChart",
  props: ["tData"],
  data() {
    return {
      arrHead: [],
      arrBody: [],
    };
  },
  computed: {},

  methods: {},
  watch: {
    tData: function (val, old) {
      // debugger;

      if (val) {
        this.arrHead = [];
        this.arrBody = [];
        let xAxisLine = [];

        if (val.length != 0) {
          val.forEach((el1) => {
            this.arrHead.push(formatDate(new Date(el1.time)));
            xAxisLine.push({
              value: el1.time,
              color: "red",
              dashStyle: "dash",
            });

            el1.chart.forEach((el2) => {
              let indexName = this.arrBody.findIndex((it1) => {
                return it1.name == el2.name;
              });
              if (indexName == -1) {
                this.arrBody.push({ name: el2.name,color:el2.color, value: [el2.value] });
              } else {
                this.arrBody[indexName].value.push(el2.value);
              }
            });
          });
          // console.log(this);
          this.$parent.$children[0].$parent.chartOptions.xAxis.plotLines = xAxisLine;
        } else {
          this.$parent.$children[0].$parent.chartOptions.xAxis.plotLines = [];
        }
      }
    },
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
  
}

th,
td:first-child {
  font-family: "Montserrat";
  font-style: normal;
align-items: center;
  padding: 10px 20px;
  font-weight: 500;
  line-height: 12px;
}
th,
td {
  border-style: solid;
  border-width: 1px 1px 1px;
  border-color: #4a627a;
  font-weight: 500;
}
td {
}
th:first-child,
td:first-child {
  text-align: center;
}
.closeTable{
float:right;


}
.closeTable:hover{
 background-image: url("~assets/svg/hov_carbon_close.svg");
 outline: none;
}

</style>