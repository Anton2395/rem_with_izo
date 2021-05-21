<template>
  <div class="chartElem">
    <div class="row">
      <highcharts class="chart" :options="chartOptions" :updateArgs="updateArgs"></highcharts>
    </div>
  </div>
</template>

<script>
export default {
  props: ["points", "limits"],
  data() {
    return {
      updateArgs: [true],
      chartOptions: {
        chart: {
         height: 200,
          // width: 275,
          type: "solidgauge",
          // backgroundColor: null
        },
        credits:false,
        exporting: {
          enabled: false,
        },
        title: null,
        tooltip: {
          enabled: false,
        },
        pane: {
          center: ["50%", "85%"],
          size: "140%",
          startAngle: -90,
          endAngle: 90,
          background: {
            backgroundColor: "#EEE",
            innerRadius: "60%",
            outerRadius: "100%",
            shape: "arc",
          },
        },

        yAxis: {
          min: 0,
          max: 10,
          stops: [[0,"#4BBEA9"]],
          lineWidth: 0,
          tickWidth: 0,
          minorTickInterval: null,
          tickAmount: 2,
          title: {
            y: -70,
          },
          labels: {
            y: 16,
          },
        },
        plotOptions: {
          solidgauge: {
            dataLabels: {
              y: 5,
              borderWidth: 0,
              useHTML: true,
            },
          },
        },
        series: [
          {
            name: "Давление",
            data: [0],
            dataLabels: {
              format:
                '<div style="text-align:center">' +
                '<span style="font-size:25px">{y}</span><br/>' +
                '<span style="font-size:12px;opacity:0.4">Атм</span>' +
                "</div>",
            },
            // tooltip: {
            //   valueSuffix: " Бар",
            // },
          },
        ],
      },
    };
  },
  watch: {
    
    points(newValue, oldValue) {
      // console.log("watch firing", newValue, oldValue);
      this.chartOptions.series[0].data = [newValue];
    },

    limits(newValue){
      // let newStops=[];
      // debugger;
      let newLimit = [];
      if (newValue.length>0) {
        // newValue.forEach((item)=>{
        //   newStops.push([item.to,item.color]);
        // })
          newValue.forEach((item)=>{
            newLimit.push([item[0]/this.chartOptions.yAxis.max,item[1]]);
          })

        this.chartOptions.yAxis.stops = newLimit;
      };

      
    }

  },
 
};
</script>

<style scoped>
</style>
