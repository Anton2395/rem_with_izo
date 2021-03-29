import Vue from 'vue';

export default {
  namespaced: true,

  state: () => ({

    factories: [ 
      { name: "Завод нефтепродуктов г. Мозырь", factoryid: "20" },
      { name: "Завод нефтепродуктов г. Гомель", factoryid: "10" },
      { name: "Завод нефтепродуктов г. Полоцк", factoryid: "30"  },
    ],

    selectedfactory: {},

    shops: [
      { name: "Цех ковки тяжелых конструкций и древесины г. Гомель", shopid: "2", factoryid: "10"},
      { name: "Цех ковки тяжелых конструкций и древесины г. Мозырь", shopid: "4", factoryid: "20"},
      { name: "Цех ковки тяжелых конструкций и древесины г. Полоцк", shopid: "6", factoryid: "30"},
      { name: "Цех отлива тяжелых конструкций и древесины г. Гомель", shopid: "8", factoryid: "10"},
      { name: "Цех отлива тяжелых конструкций и древесины г. Мозырь", shopid: "3", factoryid: "20"},
      { name: "Цех отлива тяжелых конструкций и древесины г. Полоцк", shopid: "5", factoryid: "30"},
      
    ],
    selectedshops: [],

    activeshop:  {name: "Цех ковки тяжелых конструкций и древесины г. Гомель", shopid: "2", factoryid: "10"},

    showCharts:[],

    selectChart: 0,

    arrPoint: [],

    basicData: [],

    basicOptions: {},

    reason: [
      {name:"Unassigned", y:884}, 
      {name:"Unidentified", y:101.3}, 
      {name:"Test", y:72.8}, 
      {name:"Changeover", y:31.8}, 
      {name:"Manual Stop | Packaging", y:11.7}
    ],

    timeStatus:{
      all:223546798654321,
      idle:222222222222,
      crash:11111111,
      off:1111111,
      working:123546798654321,
    },

  }),

  getters: {
    
    factories(state) {
      return state.factories;
    },

    selectedfactory(state) {
      return state.selectedfactory;
    },

    shops(state) {
      return state.shops;
    },

    selectedshops(state) {
      return state.selectedshops;
    },

    

    activeshop(state) {
      return state.activeshop;
    },

    showCharts(state) {
      return state.showCharts;
    },

    selectChart(state) {
      return state.selectChart;
    },

    arrPoint(state) {
      return state.arrPoint;
    },

    currentArrPoint(state) {
      let arr = state.arrPoint.filter(item => item.machineid == state.selectChart);
      return arr;
    },

    

    lengthArrPoint(state, idx) {
      let arr = state.arrPoint.filter(item => item.machineid == state.selectChart);
      return arr.length;
    },

    basicData(state) {

      return state.basicData;
    },

    basicOptions(state) {
      return state.basicOptions;
    },

    reason(state) {
      return state.reason;
    },

    timeStatus(state) {
      return state.timeStatus;
    },

    

    
  },
  mutations: {
    setChart(state, idx) {

      state.selectChart = idx;
    },

    setshowCharts(state, arr) {

      state.showCharts = arr.slice();
    },

    setSelectedfactory(state, factory){
      

      state.selectedfactory = factory;
      // store.commit('setSelectedshops', idx);

    },

    setActiveshop(state, shop){

      state.activeshop = shop;

    },

    setSelectedshops(state, idx){   
      let filterShops = state.shops.filter(function(item) {
        return item.factoryid ==  idx;
      });
      state.selectedshops = filterShops;
      state.activeshop = filterShops[0];
    },

    nextChart(state) {

      if (state.selectChart < state.basicData.length - 1) {
        state.selectChart++
      } else {
        state.selectChart = 0
      };
    },
    prevChart(state) {

      if (state.selectChart > 0) {
        state.selectChart--
      } else {
        state.selectChart = state.basicData.length - 1
      }
    },
    removePoint(state, point) {
      let indexPoint = state.arrPoint.findIndex(state => state.id == point.id);
      if (indexPoint !== -1) {
        state.arrPoint.splice(indexPoint, 1);
      }
    },
    addPoint(state, point) {

      let indexPoint = state.arrPoint.findIndex(state => state.id == point.id);
      if (indexPoint == -1) {
        state.arrPoint.push(point);
      }
    },
    clearData(state) {
      state.basicData = [];
    },
    loadData(state, data) {
      state.basicData = data;
    },
    loadBasicOptions(state, data) {
      state.basicOptions = data;
    },

  },
  actions: {    
    setChart(store, idx) {
      store.commit('setChart', idx);
    },

    setshowCharts(store, arr) {
      store.commit('setshowCharts', arr);
    },

    setActiveshop(store, shop){
      store.commit('setActiveshop', shop);
    },

    setSelectedshops(store, idx){
      store.commit('setSelectedshops', idx);
    },

    setSelectedfactory(store, factory){
      store.commit('setSelectedfactory', factory);
      store.commit('setSelectedshops', factory.factoryid);
    },
    nextChart(store) {
      store.commit('nextChart');
    },
    prevChart(store) {
      store.commit('prevChart');
    },


    addPoint(store, point) {
      store.commit('addPoint', point);
    },
    removePoint(store, point) {
      store.commit('removePoint', point);
    },
    loadData(store, opt) {
      let data = getBasicData(opt);
      store.commit('loadData', data);
    },
    loadBasicOptions(store) {
      let data = getBasicOptions();
      store.commit('loadBasicOptions', data);
    }


  },
  strict: process.env.NODE_ENV !== 'production'
};

function getBasicData(opt = {
  fist: new Date(),
  last: new Date(),
  numPoint: 5
}) {

  let arrAllData = [];

  for (let idx = 0; idx < 3; idx++) {

    let date = (new Date(opt.fist));
    let datefirst = date.setMinutes(date.getMinutes());
    let datelast = (new Date(opt.last));
    datelast = datelast.setMinutes(datelast.getMinutes() + 60 * 24 - 1);
    let diff = datelast - datefirst;

    let iter = opt.numPoint;
    let array = new Array;

    for (let i = datefirst; i < datelast; i += iter * 60000) {
      array.push(new Date(i));
    }




    let arrayData = [];

    let arrayA = array.map((elem, index) => elem = [elem.getTime(), Number(Math.random().toFixed(2)), "A" + index]);

    let arrayP = array.map((elem, index) => elem = [elem.getTime(), Number(Math.random().toFixed(2)), "P" + index]);

    let arrayQ = array.map((elem, index) => elem = [elem.getTime(), Number(Math.random().toFixed(2)), "Q" + index]);

    let arrayOEE = array.map((elem, index) => elem = [elem.getTime(), Number(Math.random().toFixed(2)), "OEE" + index]);

    let arrayTempON = array.map((elem, index) => elem = [elem.getTime(), Number(Math.random().toFixed(2)), "ON" + index]);

    let arrayON = [];

    


    let result = arrayTempON.map(function (item) {

      if (item[1] <= 0.11) {

        return [item[0], 1, "простой", '#ffdb66'];
      } else if (item[1] <= 0.94) {

        return [item[0], 1, "работает", '#8ccf9c'];
      } else if (item[1] <= 0.98) {

        return [item[0], 1, "выключен", '#66b0ff'];
      } else if (item[1] <= 1) {

        return [item[0], 1, "авария", '#e9818a'];
      };
    });

    let tempON = result[0];
    let lastON = result[result.length - 1];


    result.forEach(function (item, i, arr) {

      if (tempON[2] !== item[2]) {
        arrayON.push([tempON[0], item[0], tempON[1], tempON[2], tempON[3]]);
        tempON = item;
      };
    });

    if (tempON !== lastON) {
      arrayON.push([tempON[0], lastON[0], tempON[1], tempON[2], tempON[3]]);
    };

    arrayData.push(arrayA);
    arrayData.push(arrayP);
    arrayData.push(arrayQ);

    arrayData.push(arrayON);
    arrayData.push(arrayOEE);

    

    arrayData.push(arrayON.filter((item) => item[3] == "работает"));
    arrayData.push(arrayON.filter((item) => item[3] == "простой"));
    arrayData.push(arrayON.filter((item) => item[3] == "выключен"));
    arrayData.push(arrayON.filter((item) => item[3] == "авария"));

    arrAllData.push(arrayData);
    
  }
  return arrAllData;

};

function getBasicOptions() {
  let basicOptions = {

    

    title: {
      text: "APQ"
    },
    titleOEE: {
      text: "OEE"
    },
    chart: {
      zoomType: 'x'
    },

    legend: {
      enabled: true,
      align: 'left',
      layout: 'proximate'
    },
    legendAll: {
      enabled: true,
      verticalAlign: 'top',
      
    },

    scrollbar: {
      enabled: false
    },
    yAxis: [
      {
      labels: {
        align: 'right',
        x: -3
      },
      title: {
        text: ''
      },

      lineWidth: 1,
      max: 1,
      top: '20%',
      height: '18%',
      offset: 0,

      resize: {
        enabled: true
      }

    }, {
      labels: {
        align: 'right',
        x: -3
      },
      title: {
        text: ''
      },

      lineWidth: 1,
      max: 1,
      top: '40%',
      height: '18%',
      offset: 0,

      resize: {
        enabled: true
      }

    }, {
      labels: {
        align: 'right',
        x: -3
      },
      title: {
        text: ''
      },

      lineWidth: 1,
      max: 1,
      top: '60%',
      height: '18%',
      offset: 0,

      resize: {
        enabled: true
      }

    }, {
      labels: {
        align: 'right',
        x: -3
      },
      title: {
        text: ''
      },

      lineWidth: 1,
      max: 2,
      top: '80%',
      height: '20%',
      offset: 0,

      resize: {
        enabled: true
      }

    }],

    yAxisOne: [{
      labels: {
        align: 'right',
        x: -3
      },
      title: {
        text: ''
      },

      lineWidth: 1,
      max: 1,

      height: '78%',
      offset: 0,

      resize: {
        enabled: true
      }

    }, {
      labels: {
        align: 'right',
        x: -3
      },
      title: {
        text: ''
      },

      lineWidth: 1,
      max: 2,
      top: '80%',
      height: '20%',
      offset: 0,

      resize: {
        enabled: true
      }

    }],

    yAxisAll: [
      {
      labels: {
        align: 'right',
        x: -3
      },
      title: {
        text: ''
      },

      lineWidth: 1,
      max: 1,

      height: '78%',
      offset: 0,

      resize: {
        enabled: true
      }

    },
      {
      labels: {
        align: 'right',
        x: -3
      },
      title: {
        text: ''
      },

      lineWidth: 1,
      max: 1,

      height: '78%',
      offset: 0,

      resize: {
        enabled: true
      }

    },
      {
      labels: {
        align: 'right',
        x: -3
      },
      title: {
        text: ''
      },

      lineWidth: 1,
      max: 1,

      height: '78%',
      offset: 0,

      resize: {
        enabled: true
      }

    },
      {
      labels: {
        align: 'right',
        x: -3
      },
      title: {
        text: ''
      },

      lineWidth: 1,
      max: 1,

      height: '78%',
      offset: 0,

      resize: {
        enabled: true
      }

    },
   {
      labels: {
        align: 'right',
        x: -3
      },
      title: {
        text: ''
      },

      

      lineWidth: 1,
      max: 2,
      top: '80%',
      height: '20%',
      offset: 0,

      resize: {
        enabled: true
      }
    },
   {
      labels: {
        align: 'right',
        x: -3
      },
      title: {
        text: ''
      },

      lineWidth: 1,
      max: 2,
      top: '80%',
      height: '20%',
      offset: 0,

      resize: {
        enabled: true
      }
    },
   {
      labels: {
        align: 'right',
        x: -3
      },
      title: {
        text: ''
      },

      lineWidth: 1,
      max: 2,
      top: '80%',
      height: '20%',
      offset: 0,

      resize: {
        enabled: true
      }
    },
   {
      labels: {
        align: 'right',
        x: -3
      },
      title: {
        text: ''
      },

      lineWidth: 1,
      max: 2,
      top: '80%',
      height: '20%',
      offset: 0,

      resize: {
        enabled: true
      }
    },
  ],

    navigator: {
      enabled: true
    },


    tooltip: {
      
      formatter: function () {
        
        return this.points.reduce(function (s, point) {
          if (point.x2===undefined) {
            return s + '<br/>' + point.series.name + ': ' +
             point.y;
          } else{
            return s + '<br/>' + point.series.name;}
        },  '<b>' + this.x + '</b>');
    },

      shared: true,

    },

    xAxis: {
      type: 'datetime',
      minRange: 30000
    }
  };
  return basicOptions;

};

function formatDate(x = nowDate) {
  let date = new Date(x);
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
  month = month < 10 ? '0' + month : month;
  dayOfMonth = dayOfMonth < 10 ? '0' + dayOfMonth : dayOfMonth;
  hour = hour < 10 ? '0' + hour : hour;
  minutes = minutes < 10 ? '0' + minutes : minutes;


  return `${dayOfMonth}.${month}.${year} ${hour}:${minutes}`

};
