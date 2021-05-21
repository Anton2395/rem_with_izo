import Vue from "vue";
import Highcharts from "highcharts";
import HighchartsVue from "highcharts-vue";
import stockInit from "highcharts/modules/stock";
import xrangeInit from "highcharts/modules/xrange";
import exportingInit from "highcharts/modules/exporting";
import highchartsMoreInit from "highcharts/highcharts-more";
import solidGaugeInit from "highcharts/modules/solid-gauge";


if (typeof Highcharts === "object") {
  stockInit(Highcharts);
  exportingInit(Highcharts);
  xrangeInit(Highcharts);
  highchartsMoreInit(Highcharts);
  solidGaugeInit(Highcharts);

  Highcharts.setOptions({
    lang: {
        loading: 'Загрузка...',
        months: ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'],
        weekdays: ['Воскресенье', 'Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота'],
        shortMonths: ['Янв', 'Фев', 'Март', 'Апр', 'Май', 'Июнь', 'Июль', 'Авг', 'Сент', 'Окт', 'Нояб', 'Дек'],
        exportButtonTitle: "Экспорт",
        printButtonTitle: "Печать",
        rangeSelectorFrom: "С",
        rangeSelectorTo: "По",
        rangeSelectorZoom: "Период",
        downloadPNG: 'Скачать PNG',
        downloadJPEG: 'Скачать JPEG',
        downloadPDF: 'Скачать PDF',
        downloadSVG: 'Скачать SVG',
        printChart: 'Напечатать график'  ,
        resetZoom: "Сбросить" 
    },
    // useUTC:true,
});
}

Vue.use(HighchartsVue);


