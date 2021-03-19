<template>
  <div @click="hideModals">
    <div class="btn-group">
      <main>
        <button class="btn-rnd"
                :class="{'btn-close' : ShowModalPlus.modalBul}"
                @click="ShowModalPlus.modalBul=!ShowModalPlus.modalBul;"
                @click.stop="noChange"
        >+
        </button>
        <div class="plus-form" v-if="ShowModalPlus.modalBul">
          <div
              class="plus-form-item"
              @click="showCartItem('DurationWork');"
          >Продолжительность работы
          </div>
          <div
              class="plus-form-item"
              @click="showCartItem('StockBalances');"
          >Остатки на складах
          </div>
          <div
              class="plus-form-item"
              @click="showCartItem('PanelRelease');"
          >Выпуск панелей
          </div>
          <div
              class="plus-form-item"
              @click="showCartItem('TotalConsumption')"
          >Суммарный расход
          </div>
          <div
              class="plus-form-item"
              @click="showCartItem('EnergyConsumption')"
          >Расход электроэнергии
          </div>
          <div
              class="plus-form-item"
              @click="showCartItem('SpecificConsumption')"
          >Удельный расход на км
          </div>
          <div
              class="plus-form-item"
              @click="showCartItem('ComparisonModule')"
          >Модуль сравнения
          </div>
        </div>
      </main>
    </div>
    <calendar></calendar>
    <section class="charts">
      <div class="block-1">
        <durationWork v-if="DurationWork.cardShow" :card="DurationWork" :calendar="calendar"></durationWork>
        <stockBalances v-if="StockBalances.cardShow" :card="StockBalances" :calendar="calendar.date"></stockBalances>
      </div>
      <div class="block-2">
        <div
            class="chart-data panel-release"
            v-if="PanelRelease.cardShow"
        >
          <div class="chart-header">
            <div class="title">Выпуск панелей</div>
            <period title="PanelRelease"></period>
            <div
                class="bul"
                @click="PanelRelease.modalBul=!PanelRelease.modalBul"
                @click.stop="noChange"
            >
              <span></span>
            </div>
          </div>
          <div class="chart-content">
            <div
                class="menu-bul"
                v-if="PanelRelease.modalBul"
            >
              <div
                  class="btn-bul"
                  @click="PanelRelease.cardShow=!PanelRelease.cardShow; PanelRelease.modalBul=false"
              ><span class="show"></span>
                <span>Скрыть</span>
              </div>
              <div class="btn-bul">
                <span class="new"></span>
                <span @click="updatePanelRelease">Обновить</span>
              </div>
            </div>
            <div class="diagram">
              <highcharts
                  :options="chartOptionsPio"
                  :constructor-type="'stockChart'"
              ></highcharts>
            </div>
            <div class="content-box">
              <div class="indicators">
                <div class="module">
                  <div class="index">{{ panelRelease.sum }}</div>
                  <indicator :change="panelRelease.change_sum"></indicator>
                </div>
                <div class="data-list">
                  <div class="list">
                    <div class="item">
                      <div class="circle" style="background: #4BBEAA"></div>
                      <div class="title">годно</div>
                    </div>
                    <div class="data">
                      <div class="index">{{ panelRelease.suitable }}</div>
                      <indicator :change="panelRelease.change_suitable"></indicator>
                    </div>
                  </div>
                  <div class="list">
                    <div class="item">
                      <div class="circle" style="background: #2D9AD8"></div>
                      <div class="title">некондиция</div>
                    </div>
                    <div class="data">
                      <div class="index">{{ panelRelease.substandard }}</div>
                      <indicator :change="panelRelease.change_substandard"></indicator>
                    </div>
                  </div>
                  <div class="list">
                    <div class="item">
                      <div class="circle" style="background: #FC7A7A"></div>
                      <div class="title">брак</div>
                    </div>
                    <div class="data">
                      <div class="index">{{ panelRelease.defect }}</div>
                      <indicator :change="panelRelease.change_defect"></indicator>
                    </div>
                  </div>
                </div>
                <div class="indicators-footer">
                  <div class="title">Залито метров</div>
                  <div class="data">
                    <div class="index">{{ panelRelease.flooded }}</div>
                    <indicator :change="panelRelease.change_flooded"></indicator>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div
            class="chart-data consumption"
            v-if="SpecificConsumption.cardShow"
        >
          <div class="chart-header">
            <div class="title">Удельный расход на км</div>
            <period title="SpecificConsumption"></period>
            <div
                class="bul"
                @click="SpecificConsumption.modalBul = !SpecificConsumption.modalBul"
                @click.stop="noChange"
            >
              <span></span>
            </div>
          </div>
          <div class="chart-content">
            <div
                class="menu-bul"
                v-if="SpecificConsumption.modalBul"
            >
              <div
                  class="btn-bul"
                  @click="SpecificConsumption.cardShow=!SpecificConsumption.cardShow; SpecificConsumption.modalBul=false"
              ><span class="show"></span>
                <span>Скрыть</span>
              </div>
              <div class="btn-bul">
                <span class="new"></span>
                <span @click="updateSpecificConsumption">Обновить</span>
              </div>
            </div>
            <div class="iteam-group">
              <div class="item">
                <div class="data">
                  <div class="quantity">{{ specificConsumption.iso }}</div>
                  <div class="subtitle">Изоцианат, л</div>
                </div>
                <div class="icon">
                  <div class="circle" style="background: #2D9AD8">
                    <div class="title">ISO</div>
                    <div class="subtitle">km</div>
                  </div>
                </div>
              </div>
              <div class="item">
                <div class="data">
                  <div class="quantity">{{ specificConsumption.pol }}</div>
                  <div class="subtitle">Полиол, л</div>
                </div>
                <div class="icon">
                  <div class="circle" style="background: #FC7A7A">
                    <div class="title">POL</div>
                    <div class="subtitle">km</div>
                  </div>
                </div>
              </div>
              <div class="item">
                <div class="data">
                  <div class="quantity">{{ specificConsumption.pen }}</div>
                  <div class="subtitle">Пентан, л</div>
                </div>
                <div class="icon">
                  <div class="circle" style="background: #4BBEAA">
                    <div class="title">PEN</div>
                    <div class="subtitle">km</div>
                  </div>
                </div>
              </div>
              <div class="item">
                <div class="data">
                  <div class="quantity">{{ specificConsumption.kat1 }}</div>
                  <div class="subtitle">Катализатор1, л</div>
                </div>
                <div class="icon">
                  <div class="circle" style="background: #2D9AD8">
                    <div class="title">K1</div>
                    <div class="subtitle">km</div>
                  </div>
                </div>
              </div>
              <div class="item">
                <div class="data">
                  <div class="quantity">{{ specificConsumption.kat2 }}</div>
                  <div class="subtitle">Катализатор2, л</div>
                </div>
                <div class="icon">
                  <div class="circle" style="background: #FC7A7A">
                    <div class="title">K2</div>
                    <div class="subtitle">km</div>
                  </div>
                </div>
              </div>
              <div class="item">
                <div class="data">
                  <div class="quantity">{{ specificConsumption.kat3 }}</div>
                  <div class="subtitle">Катализатор3, л</div>
                </div>
                <div class="icon">
                  <div class="circle" style="background: #4BBEAA">
                    <div class="title">K3</div>
                    <div class="subtitle">km</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div
            class="chart-data consumption"
            v-if="TotalConsumption.cardShow"
        >
          <div class="chart-header">
            <div class="title">Суммарный расход</div>
            <period title="TotalConsumption"></period>
            <div
                class="bul"
                @click="TotalConsumption.modalBul=!TotalConsumption.modalBul;"
                @click.stop="noChange"
            >
              <span></span>
            </div>
          </div>
          <div class="chart-content">
            <div
                class="menu-bul"
                v-if="TotalConsumption.modalBul"
            >
              <div
                  class="btn-bul"
                  @click="TotalConsumption.cardShow=!TotalConsumption.cardShow; TotalConsumption.modalBul=false"
              ><span class="show"></span>
                <span>Скрыть</span>
              </div>
              <div class="btn-bul">
                <span class="new"></span>
                <span @click="updateTotalConsumption">Обновить</span>
              </div>
            </div>
            <div class="iteam-group">
              <div class="item">
                <div class="data">
                  <div class="quantity">{{ totalConsumption.iso }}</div>
                  <div class="subtitle">Изоцианат, л</div>
                </div>
                <div class="icon">
                  <div class="circle" style="background: #2D9AD8">ISO</div>
                </div>
              </div>
              <div class="item">
                <div class="data">
                  <div class="quantity">{{ totalConsumption.pol }}</div>
                  <div class="subtitle">Полиол, л</div>
                </div>
                <div class="icon">
                  <div class="circle" style="background: #FC7A7A">POL</div>
                </div>
              </div>
              <div class="item">
                <div class="data">
                  <div class="quantity">{{ totalConsumption.pen }}</div>
                  <div class="subtitle">Пентан, л</div>
                </div>
                <div class="icon">
                  <div class="circle" style="background: #4BBEAA">PEN</div>
                </div>
              </div>
              <div class="item">
                <div class="data">
                  <div class="quantity">{{ totalConsumption.kat1 }}</div>
                  <div class="subtitle">Катализатор1, л</div>
                </div>
                <div class="icon">
                  <div class="circle" style="background: #2D9AD8">K1</div>
                </div>
              </div>
              <div class="item">
                <div class="data">
                  <div class="quantity">{{ totalConsumption.kat2 }}</div>
                  <div class="subtitle">Катализатор2, л</div>
                </div>
                <div class="icon">
                  <div class="circle" style="background: #FC7A7A">K2</div>
                </div>
              </div>
              <div class="item">
                <div class="data">
                  <div class="quantity">{{ totalConsumption.kat3 }}</div>
                  <div class="subtitle">Катализатор3, л</div>
                </div>
                <div class="icon">
                  <div class="circle" style="background: #4BBEAA">K3</div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div
            class="chart-data comparison-module"
            v-if="ComparisonModule.cardShow"
        >
          <div class="chart-header">
            <div class="title">Модуль сравнения</div>
            <div
                class="bul"
                @click="ComparisonModule.modalBul=!ComparisonModule.modalBul;"
                @click.stop="noChange"
            >
              <span></span>
            </div>
          </div>
          <div class="chart-content">
            <div
                class="menu-bul"
                v-if="ComparisonModule.modalBul"
            >
              <div
                  class="btn-bul"
                  @click="ComparisonModule.cardShow=!ComparisonModule.cardShow; ComparisonModule.modalBul=false"
              ><span class="show"></span>
                <span>Скрыть</span>
              </div>
              <div class="btn-bul">
                <span class="new"></span>
                <span @click="updateComparisonModule">Обновить</span>
              </div>
            </div>
            <div class="content-box">
              <div class="calendar-period">
                <div class="select-date">
                  <input type="date" v-model="ComparisonModuleDate1"/>
                </div>
              </div>
              <period title="ComparisonModule" :isType2="ComparisonModule.option.isType2"></period>
              <div class="indicators" v-if="comparisonModuleData && comparisonModuleData.isQuery">
                <div class="module">
                  <div class="index">{{ comparisonModuleData.sum1 }}</div>
                  <indicator :change="comparisonModuleData.change_sum1"></indicator>
                </div>
                <div class="data-list">
                  <div class="list">
                    <div class="item">
                      <div class="circle" style="background: #4BBEAA"></div>
                      <div class="title">годно</div>
                    </div>
                    <div class="data">
                      <div class="index">{{ comparisonModuleData.suitable1 }}</div>
                      <indicator :change="comparisonModuleData.change_suitable1"></indicator>
                    </div>
                  </div>
                  <div class="list">
                    <div class="item">
                      <div class="circle" style="background: #2D9AD8"></div>
                      <div class="title">некондиция</div>
                    </div>
                    <div class="data">
                      <div class="index">{{ comparisonModuleData.substandard1 }}</div>
                      <indicator :change="comparisonModuleData.change_substandard1"></indicator>
                    </div>
                  </div>
                  <div class="list">
                    <div class="item">
                      <div class="circle" style="background: #FC7A7A"></div>
                      <div class="title">брак</div>
                    </div>
                    <div class="data">
                      <div class="index">{{ comparisonModuleData.defect1 }}</div>
                      <indicator :change="comparisonModuleData.change_defect1"></indicator>
                    </div>
                  </div>
                </div>
                <div class="indicators-footer">
                  <div class="title">Залито метров</div>
                  <div class="data">
                    <div class="index">{{ comparisonModuleData.flooded1 }}</div>
                    <indicator :change="comparisonModuleData.change_flooded1"></indicator>
                  </div>
                </div>
              </div>
            </div>
            <div class="content-box">
              <div class="calendar-period">
                <div class="select-date">
                  <input type="date" v-model="ComparisonModuleDate2"/>
                </div>
              </div>
              <period title="ComparisonModule" :isType1="ComparisonModule.option.isType1" end="1"></period>
              <div class="indicators" v-if="comparisonModuleData && comparisonModuleData.isQuery">
                <div class="module">
                  <div class="index">{{ comparisonModuleData.sum2 }}</div>
                </div>
                <div class="data-list">
                  <div class="list">
                    <div class="item">
                      <div class="circle" style="background: #4BBEAA"></div>
                      <div class="title">годно</div>
                    </div>
                    <div class="data">
                      <div class="index">{{ comparisonModuleData.suitable2 }}</div>
                    </div>
                  </div>
                  <div class="list">
                    <div class="item">
                      <div class="circle" style="background: #2D9AD8"></div>
                      <div class="title">некондиция</div>
                    </div>
                    <div class="data">
                      <div class="index">{{ comparisonModuleData.substandard2 }}</div>
                    </div>
                  </div>
                  <div class="list">
                    <div class="item">
                      <div class="circle" style="background: #FC7A7A"></div>
                      <div class="title">брак</div>
                    </div>
                    <div class="data">
                      <div class="index">{{ comparisonModuleData.defect2 }}</div>
                    </div>
                  </div>
                </div>
                <div class="indicators-footer">
                  <div class="title">Залито метров</div>
                  <div class="data">
                    <div class="index">{{ comparisonModuleData.flooded2 }}</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div
            class="chart-data-min energy-consumption"
            v-if="EnergyConsumption.cardShow"
        >
          <div class="chart-header">
            <div class="title">Расход энергоресурсов</div>
            <period title="EnergyConsumption"></period>
            <div
                class="bul"
                @click="EnergyConsumption.modalBul=!EnergyConsumption.modalBul;"
                @click.stop="noChange"
            >
              <span></span>
            </div>
          </div>
          <div class="chart-content">
            <div
                class="menu-bul"
                v-if="EnergyConsumption.modalBul"
            >
              <div
                  class="btn-bul"
                  @click="EnergyConsumption.cardShow=!EnergyConsumption.cardShow; EnergyConsumption.modalBul=false"
              ><span class="show"></span>
                <span>Скрыть</span>
              </div>
              <div class="btn-bul">
                <span class="new"></span>
                <span @click="updateEnergyConsumption">Обновить</span>
              </div>
            </div>
            <div class="iteam-group">
              <div class="item">
                <div class="data">
                  <div class="quantity">{{ energyConsumption.input1 }}</div>
                  <div class="subtitle">Ввод1, кВт</div>
                </div>
                <div class="icon">
                  <div class="circle"></div>
                </div>
              </div>
              <div class="item">
                <div class="data">
                  <div class="quantity">{{ energyConsumption.input2 }}</div>
                  <div class="subtitle">Ввод2, кВт</div>
                </div>
                <div class="icon">
                  <div class="circle"></div>
                </div>
              </div>
              <div class="item">
                <div class="data">
                  <div class="quantity">{{ energyConsumption.gas }}</div>
                  <div class="subtitle">Газ, м3</div>
                </div>
                <div class="iconLast">
                  <div class="circle"></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

  </div>
</template>

<script>

import {mapActions} from "vuex";
import {mapGetters} from "vuex";
import Period from "@/components/home/period";
import Calendar from "@/components/home/calendar";
import DurationWork from "@/components/home/DurationWork";
import StockBalances from "@/components/home/StockBalances";
import DataIndicator from '~/components/home/DataIndicator'

export default {
  layout: "header_footer",

  created() {
    this.setActiveTabHeader("HOME");
    this.setActiveTabSidebar("Dashboard");
    this.$on('hideCartItem', (name) => {
      this[name].cardShow = false;
    });
    this.$on('showModalBul', (name) => {
      this[name].modalBul = !this[name].modalBul;
    });
    this.$on('noChange', (name) => {
    });

    this.$on('changeCalendar', (calendar) => {
      this.calendar = calendar;
    });

    this.$on('setPeriod', (option) => {
      if (option.end) {
        this[option.title].option.id2 = option.id2;
        this[option.title].option.isType2 = option.isType2;
        this.updateComparisonModule();
      } else {
        this[option.title].option.id1 = option.id1;
        this[option.title].option.isType1 = option.isType1;
        this['update' + option.title]();
      }
    });

    this.updatePanelRelease();
    this.updateEnergyConsumption();
    this.updateTotalConsumption();
    this.updateSpecificConsumption();
  },

  data() {
    return {
      ShowModalPlus: {
        modalBul: false,
      },
      PanelRelease: {
        modalBul: false,
        cardShow: true,
        option: {
          id1: 0,
          isType1: 0,
        },
      },
      TotalConsumption: {
        modalBul: false,
        cardShow: true,
        option: {
          id1: 0,
          isType1: 0,
        },
      },
      EnergyConsumption: {
        modalBul: false,
        cardShow: true,
        option: {
          id1: 0,
          isType1: 0,
        },
      },
      SpecificConsumption: {
        modalBul: false,
        cardShow: true,
        option: {
          id1: 0,
          isType1: null,
        },
      },
      ComparisonModuleDate1: null,
      ComparisonModuleDate2: null,
      ComparisonModule: {
        modalBul: false,
        cardShow: true,
        option: {
          id1: 0,
          id2: 0,
          isType1: 0,
          isType2: 0,
          date1: null,
          date2: null,
        },
      },
      DurationWork: {
        modalBul: false,
        cardShow: true,
      },
      StockBalances: {
        modalBul: false,
        cardShow: true,
      },
      calendar: {
        time: new Date().getTime(),
        date: formatDate(new Date().getTime()),
      },
    }
  },

  components: {
    period: Period,
    calendar: Calendar,
    durationWork: DurationWork,
    stockBalances: StockBalances,
    indicator: DataIndicator,

  },

  watch: {
    calendar: function() {
      this.updateAll();
    },
    ComparisonModuleDate1: function (newValue) {
      this.ComparisonModule.option.date1 = newValue;
      this.updateComparisonModule();
    },
    ComparisonModuleDate2: function (newValue) {
      this.ComparisonModule.option.date2 = newValue;
      this.updateComparisonModule();
    }
  },

  computed: {
    ...mapGetters('home', {
      comparisonModuleData: 'comparisonModule',
      energyConsumption: 'energyConsumption',
      totalConsumption: "totalConsumption",
      specificConsumption: "specificConsumption",
      panelRelease: "panelRelease",
    }),
    chartOptionsPio() {
      return {
        chart: {
          height: 210,
          margin: 0,
          type: 'pie'
        },
        credits: {
          enabled: false,
          style: {
            text: null,
          },
        },
        title: {
          text: '500',
          style: {
            'font-family': '"Montserrat", sans-serif',
            'color': '#000000',
            'font-size': '24px',
            'font-weight': '500'
          },
          align: 'center',
          verticalAlign: 'middle',
          y: 30,
        },
        tooltip: {
          // pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
          split: false,
          shared: false,
        },
        accessibility: {
          point: {
            valueSuffix: '%'
          }
        },
        plotOptions: {
          pie: {
            slicedOffset: 0,
            size: 170,
            center: [140, 110],
            dataLabels: {
              enabled: false,
            },
          }
        },
        navigator: {
          enabled: false,
        },
        exporting: {
          enabled: false,
        },
        rangeSelector: {
          enabled: false
        },
        legend: false,
        xAxis: {
          visible: false,
        },
        yAxis: {
          visible: false,
        },
        series: [{
          name: 'Количество',
          innerSize: '70%',
          data: [
            {name: 'Годно', y: this.panelRelease ? this.panelRelease.suitable : 0, color: '#4BBEA9'},
            {name: 'Брак', y: this.panelRelease ? this.panelRelease.substandard : 0, color: ' #FC7A7A'},
            {name: 'Некондиция', y: this.panelRelease ? this.panelRelease.defect : 0, color: '#2D9AD8'}
          ]
        }]
      }
    },
  },

  methods: {
    //check
    ...mapActions("users", {
      setActiveTabHeader: "setActiveTabHeader",
      setActiveTabSidebar: "setActiveTabSidebar",
    }),

    ...mapActions("home", {
      getComparisonModule: "getComparisonModule",
      getEnergyConsumption: "getEnergyConsumption",
      getTotalConsumption: "getTotalConsumption",
      getSpecificConsumption: "getSpecificConsumption",
      getPanelRelease: "getPanelRelease",
    }),
    showCartItem(name) {
      this.ShowModalPlus.modalBul = false;
      this[name].cardShow = true;
    },
    hideModals() {
      if (this.ShowModalPlus.modalBul ||
          this.PanelRelease.modalBul ||
          this.TotalConsumption.modalBul ||
          this.EnergyConsumption.modalBul ||
          this.SpecificConsumption.modalBul ||
          this.ComparisonModule.modalBul ||
          this.DurationWork.modalBul ||
          this.StockBalances.modalBul
      ) {
        this.DurationWork.modalBul = false;
        this.StockBalances.modalBul = false;
        this.ShowModalPlus.modalBul = false;
        this.PanelRelease.modalBul = false;
        this.TotalConsumption.modalBul = false;
        this.EnergyConsumption.modalBul = false;
        this.SpecificConsumption.modalBul = false;
        this.ComparisonModule.modalBul = false;

      }
    },
    noChange() {
      console.log('change');
    },
    updateComparisonModule() {
      if (!(this.ComparisonModule.option.date1 && this.ComparisonModule.option.date2))
        return;

      this.getComparisonModule(this.ComparisonModule.option);
    },
    updateEnergyConsumption() {
      this.EnergyConsumption.option.date = this.calendar.date;
      this.getEnergyConsumption(this.EnergyConsumption.option);
    },
    updateTotalConsumption() {
      this.TotalConsumption.option.date = this.calendar.date;
      this.getTotalConsumption(this.TotalConsumption.option);
    },
    updateSpecificConsumption() {
      this.SpecificConsumption.option.date = this.calendar.date;
      this.getSpecificConsumption(this.SpecificConsumption.option);
    },
    updatePanelRelease() {
      this.PanelRelease.option.date = this.calendar.date;
      this.getPanelRelease(this.PanelRelease.option);
    },
    updateAll() {
      this.updatePanelRelease();
      this.updateSpecificConsumption();
      this.updateTotalConsumption();
      this.updateEnergyConsumption();
    }
  },
}

function formatDate(date) {
  let d = new Date(date);

  return d.getFullYear() + "-" + d.getMonth() + 1 + "-" + d.getDate();
}
</script>

<style>
.highcharts-scrollbar {
  display: none !important;
}
</style>

<style lang="scss" scoped>

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #E9E9E9;
  padding: 2px 8px 2px 12px;

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

.indicators {
  padding-right: 44px;

  .module {
    position: relative;
    display: flex;
    align-items: baseline;
    padding-left: 68px;
    padding-top: 12px;
    margin-bottom: 12px;

    .index {
      font-size: 24px;
      font-weight: 500;
      margin-right: 9px;
    }
  }

  .data-list {
    display: flex;
    flex-direction: column;
    align-items: flex-end;

    .list {
      max-width: 207px;
      width: 100%;
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 12px;
      font-size: 14px;

      .item {
        display: flex;
        align-items: center;
        font-weight: 500;

        .circle {
          width: 12px;
          height: 12px;
          border-radius: 50%;
          margin-right: 6px;
        }
      }
    }
  }

  .indicators-footer {
    display: flex;
    align-items: center;
    justify-content: space-between;

    .title {
      margin-left: 9px;
      font-style: normal;
      font-weight: normal;
      font-size: 14px;
    }

    .data {
      display: flex;
      align-items: baseline;

      .index {
        font-style: normal;
        font-weight: 500;
        font-size: 14px;
      }
    }
  }
}

.charts {
  height: 100%;
  display: flex;
  flex-direction: row;
  padding: 0 36px;

  .block-1 {
    width: 280px;
    margin-right: 36px;
  }

  .block-2 {
    display: flex;
    flex-wrap: wrap;

    .panel-release {
      .chart-content {
        display: flex;

        .diagram {
          width: 45%;
          overflow: hidden;
        }

        .content-box {
          width: 55%;
          padding-top: 25px;

          .indicators {
            .module {
              padding-left: 17px;
            }

            .data-list {
              align-items: end;
              margin-bottom: 8px;
            }

            .indicators-footer {
              .title {
                font-style: normal;
                font-weight: normal;
                font-size: 18px;
                margin-left: 0;
              }
            }
          }
        }
      }
    }

    .consumption {
      .chart-content {
        .iteam-group {
          padding-bottom: 12px;
          display: flex;
          flex-wrap: wrap;

          .item {
            width: 192px;
            height: 90px;
            display: flex;
            flex-direction: row;
            justify-content: center;
            align-items: center;
            padding-bottom: 6px;
            padding-right: 6px;
            padding-left: 12px;
            border: 2px solid #ECEDF4;
            box-sizing: border-box;
            border-radius: 12px;
            margin-right: 12px;
            margin-top: 11px;

            .data {
              width: 116px;
              display: flex;
              justify-content: center;
              align-items: center;
              flex-direction: column;
              margin-right: 6px;
              margin-top: 6px;

              .quantity {
                font-family: "Montserrat", -apple-system, BlinkMacSystemFont, "Segoe UI",
                Roboto, "Helvetica Neue", Arial, sans-serif;
                font-weight: 500;
                font-size: 48px;
                color: #000000;
              }

              .subtitle {
                width: 100%;
                font-family: "Montserrat", -apple-system, BlinkMacSystemFont, "Segoe UI",
                Roboto, "Helvetica Neue", Arial, sans-serif;
                font-weight: 500;
                font-size: 12px;
                color: #B1B1BC;
              }
            }

            .icon {
              font-family: "Montserrat", -apple-system, BlinkMacSystemFont, "Segoe UI",
              Roboto, "Helvetica Neue", Arial, sans-serif;
              font-weight: 500;
              font-size: 16px;
              color: #FFFFFF;

              .circle {
                width: 50px;
                height: 50px;
                border-radius: 50%;
                display: flex;
                justify-content: center;
                align-items: center;
              }
            }

            &:nth-child(3n) {
              margin-right: 0;
            }
          }
        }
      }
    }

    .chart-data-min {
      width: 628px;
      height: 144px;
      border: 2px solid #E9E9E9;
      border-radius: 9px;
      //margin-bottom: 36px;
      margin-right: 36px;

      .chart-content {
        padding: 0 12px;
        display: flex;
        flex-wrap: wrap;

        .iteam-group {
          display: flex;
          flex-wrap: wrap;

          .item {
            width: 192px;
            height: 90px;
            display: flex;
            flex-direction: row;
            justify-content: center;
            align-items: center;
            padding-bottom: 6px;
            padding-right: 6px;
            padding-left: 12px;
            border: 2px solid #ECEDF4;
            box-sizing: border-box;
            border-radius: 12px;
            margin-right: 12px;
            margin-top: 11px;

            .data {
              width: 116px;
              display: flex;
              justify-content: center;
              align-items: center;
              flex-direction: column;
              margin-right: 6px;
              margin-top: 6px;

              .quantity {
                height: 60px;
                text-align: center;
                display: flex;
                align-items: center;
                font-family: "Montserrat", -apple-system, BlinkMacSystemFont, "Segoe UI",
                Roboto, "Helvetica Neue", Arial, sans-serif;
                font-weight: 500;
                font-size: 24px;
                color: #000000;
              }

              .subtitle {
                width: 100%;
                font-family: "Montserrat", -apple-system, BlinkMacSystemFont, "Segoe UI",
                Roboto, "Helvetica Neue", Arial, sans-serif;
                font-weight: 500;
                font-size: 12px;
                color: #B1B1BC;
              }
            }

            .icon {
              width: 50px;
              height: 50px;
              border-radius: 50%;
              background-image: url("~assets/img/lightning.png");
              background-repeat: no-repeat;
              background-position: center;
              background-size: contain;

              .circle {
                display: flex;
                justify-content: center;
                align-items: center;
              }
            }

            .iconLast {
              width: 50px;
              height: 50px;
              border-radius: 50%;
              background-image: url("~assets/img/fire.png");
              background-repeat: no-repeat;
              background-position: center;
              background-size: contain;

              .circle {
                display: flex;
                justify-content: center;
                align-items: center;
              }
            }

            &:nth-child(3n) {
              margin-right: 0;
            }
          }
        }
      }
    }

    .consumption {
      .chart-content {
        padding: 0 12px;
        display: flex;
        flex-wrap: wrap;

        .item {
          width: 192px;
          height: 90px;
          display: flex;
          flex-direction: row;
          justify-content: center;
          align-items: center;
          padding-bottom: 6px;
          padding-right: 6px;
          padding-left: 12px;
          border: 2px solid #ECEDF4;
          box-sizing: border-box;
          border-radius: 12px;
          margin-right: 12px;
          margin-top: 11px;

          .data {
            width: 116px;
            display: flex;
            justify-content: center;
            align-items: center;
            flex-direction: column;
            margin-right: 6px;
            margin-top: 6px;

            .quantity {
              font-family: "Montserrat", -apple-system, BlinkMacSystemFont, "Segoe UI",
              Roboto, "Helvetica Neue", Arial, sans-serif;
              font-weight: 500;
              font-size: 48px;
              color: #000000;
            }

            .subtitle {
              width: 100%;
              font-family: "Montserrat", -apple-system, BlinkMacSystemFont, "Segoe UI",
              Roboto, "Helvetica Neue", Arial, sans-serif;
              font-weight: 500;
              font-size: 12px;
              color: #B1B1BC;
            }
          }

          .icon {
            .circle {
              width: 50px;
              height: 50px;
              border-radius: 50%;
              display: flex;
              justify-content: center;
              align-items: center;
              flex-direction: column;

              .title {
                font-family: "Montserrat", -apple-system, BlinkMacSystemFont, "Segoe UI",
                Roboto, "Helvetica Neue", Arial, sans-serif;
                font-weight: 500;
                font-size: 16px;
                color: #FFFFFF;
                text-align: center;
              }

              .subtitle {
                font-family: "Montserrat", -apple-system, BlinkMacSystemFont, "Segoe UI",
                Roboto, "Helvetica Neue", Arial, sans-serif;
                font-weight: 500;
                font-size: 12px;
                color: #FFFFFF;
                text-align: center;
              }
            }
          }

          &:nth-child(3n) {
            margin-right: 0;
          }
        }
      }
    }

    .comparison-module {
      font-size: 14px;

      .chart-content {
        display: flex;
        width: 100%;
        height: calc(100% - 21px);
        padding: 6px 3px;

        .content-box {
          width: 50%;
          height: 100%;
          margin-right: 3px;
          border-right: 1px solid #E9E9E9;

          .calendar-period {
            padding: 6px 0;

            .select-date {
              height: 20px;
              margin-left: 12px;
              font-weight: 600;
              font-size: 12px;
              line-height: 15px;
              text-align: left;
              color: #9098AF;
            }

            .select-date input {
              height: 20px;
              padding-left: 3px;
              outline: none;
              font-weight: normal;
              font-size: 12px;
              line-height: 15px;
              color: #9098AF;
              border: 1px solid #9098AF;
              border-radius: 4px;
            }
          }

          .period {
            btn.text {
              margin-right: 6px;
            }
            button:last-child {
              margin-right: 3px;
            }
          }
        }
      }

      .content-box:last-child {
        border-right: none;
        margin-right: 0;
      }
    }
  }
}

.data {
  display: flex;

  .index {
    margin-right: 4px;
  }
}

.chart-data {
  width: 628px;
  height: 246px;
  border: 2px solid #E9E9E9;
  border-radius: 9px;
  //margin-bottom: 37px;
  //margin-right: 48px;
  margin-right: 36px;
}

.resul {
  .result-ok {
    font-family: "Montserrat", -apple-system, BlinkMacSystemFont, "Segoe UI",
    Roboto, "Helvetica Neue", Arial, sans-serif;
    font-style: normal;
    font-weight: 500;
    font-size: 14px;
    line-height: 14px;
    color: #7CD420;
  }

  .result-minus {
    font-family: "Montserrat", -apple-system, BlinkMacSystemFont, "Segoe UI",
    Roboto, "Helvetica Neue", Arial, sans-serif;
    font-style: normal;
    font-weight: 500;
    font-size: 14px;
    line-height: 14px;
    color: #F3345D;
  }

  .result-null {
    font-family: "Montserrat", -apple-system, BlinkMacSystemFont, "Segoe UI",
    Roboto, "Helvetica Neue", Arial, sans-serif;
    font-style: normal;
    font-weight: 500;
    font-size: 14px;
    line-height: 14px;
    color: #96A2B0;
  }
}

.btn-group {

  main {
    width: 100%;
    height: 100%;
  }

  .btn-rnd {
    outline: none;
    width: 60px;
    height: 60px;
    border-radius: 50%;
    border: 2px #FF7167 solid;
    cursor: pointer;
    background: #FFFFFF;
    color: #FF7167;
    font-weight: 500;
    font-size: 48.4615px;
    line-height: 81px;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    text-transform: uppercase;

    position: absolute;
    bottom: 48px;
    right: 48px;
    z-index: 2;

    &.btn-close {
      transform: rotate(45deg);
      background: #FF7167;
      color: #FFFFFF;
    }
  }

  .btn-rnd:hover {
    background: #FF7167;
    color: #FFFFFF;
    transition: 0.2s linear;
  }

  .plus-form {
    width: 244px;
    height: auto;
    background: #FFFFFF;
    border: 2px solid #F3F3F3;
    border-radius: 5px;

    position: absolute;
    bottom: 112px;
    right: 48px;

    z-index: 2;

    .plus-form-item {
      cursor: pointer;
      height: 36px;
      padding-left: 24px;
      padding-right: 24px;
      font-weight: 500;
      font-size: 12px;
      line-height: 15px;
      display: flex;
      align-items: center;
      justify-content: flex-end;
      color: #BABABA;
      border-bottom: 2px solid #F3F3F3;

      &:hover {
        color: #727272;
        transition: 0.2s linear;
      }
    }

    .plus-form-item:last-child {
      border-bottom: none;
    }
  }
}

.chart-content {
  position: relative;
}

.menu-bul {
  -moz-user-select: none;
  -khtml-user-select: none;
  user-select: none;
  position: absolute;
  top: 0;
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
