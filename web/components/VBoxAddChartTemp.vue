<template>
  <div class="overlay" @click="$emit('closeForm')">
    <div class="popup_grafik" v-on:click.stop="">
      <button class="btn_close"></button>
      <div class="rename_grafik">
        <div class="r_footer">
          <button class="btn_left_del" to="#">Удалить область</button>
          <button class="btn_right_done" to="#">Применить</button>
        </div>

        <div class="add_grafik">
          <div class="head_head">
            <table class="tab1" rules="all">
              <td style="width: 308px">Название графика</td>
              <td style="width: 154px">Единицы измерения</td>
              <td style="width: 158px">Позиционное обозначение</td>
              <td style="width: 70px">Цвет</td>
              <td class="carbon_close" style="width: 24px"></td>
            </table>
          </div>

          <div class="body_tabl">
            <table class="tab2" rules="all">
              <tr v-for="item in form.data" :key="item.value">
                <td style="width: 308px" :style="{ color: item.color }">
                  {{ item.name }}
                </td>
                <td style="width: 154px">
                  {{ item.unit }}
                </td>
                <td style="width: 158px">
                  {{ item.designation }}
                </td>
                <td style="width: 70px">
                  <div class="seriesColor">
                    <div class="row">
                      <input
                        class="colorPicker"
                        type="color"
                        v-model="item.color"
                      />
                    </div>
                  </div>

                  <!-- <div id="rectangle"></div> -->
                </td>
                <td class="carbon_close" style="width: 24px">
                  <button class="carbon_close">
                    <img src="~/assets/svg/carbon_close.svg" alt="/" />
                  </button>
                </td>
              </tr>
            </table>
          </div>
        </div>
        <div class="rentv_header">
          <div class="verx">
            <span class="rentv"
              >Работа с графиками:
              <span v-show="!isRename">{{ form.name }}</span>
              <input v-show="isRename" type="text" v-model.lazy="form.name"
            /></span>
            <button class="perecl" @click="isRename = !isRename"></button>
          </div>
          <!-- <span class="rentv">Работа с графиками: Рабочая облась 1</span> -->
          <div class="splusom">
            <select v-model="addVarible.varible" class="addtv">
              <option disabled value="0">Выберите один из вариантов</option>
              <option
                :value="item.id"
                :key="item.id"
                v-for="item in lists.varibles"
              >
                {{ item.name }}
              </option>
            </select>

            <input
              class="colorPicker"
              type="color"
              v-model="addVarible.color"
            />

            <button class="carbon_close">
              <img src="~/assets/svg/plus.svg" alt="/" />
            </button>
          </div>
          <!-- <input class="addtv" type="text" placeholder="Рабочее пространство 1" /> -->
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
import { mapActions } from "vuex";

export default {
  name: "VBoxAddChart",
  props: ["Vdata"],
  data() {
    return {
      lists: {
        varibles: [],
      },
      addVarible: {
        color: "#000",
        varible: "0",
      },
      form: {
        name: this.Vdata.name,
        parent: this.Vdata.id,
        data: [],
      },
      varibleSelect: 0,
      showTable: true,
      seriesColor: "#6fcd98",
      colorInputIsSupported: null,
      isRename: false,
    };
  },

  computed: {
    
    dataHead() {
      let statusDev = "ok";

      let allDev = this.DevMsgs.length;

      let arrOkDev = this.DevMsgs.filter((item) => item.status == "ok");

      let dngDev = this.DevMsgs.find((item) => item.status == "dng");

      let okDev = arrOkDev.length;

      if (dngDev !== undefined) {
        statusDev = "dng";
      } else if (okDev / allDev < 0.5) {
        statusDev = "alert";
      }

      return {
        title: `${okDev} из ${allDev} устройства в сети`,
        status: statusDev,
      };
    },
  },
  methods: {
    async getVaribles() {
      await this.$axios
        .$get(`/recorder/structure/ValueSensor/`)
        .then((data) => {
          console.log(data);
          this.lists.varibles = data;
        })
        .catch((e) => {
          console.log(e);
        });
    },
    async getDataWorkArea() {
      await this.$axios
        .$get(`/recorder/structure/Workarea/${this.Vdata.id}`)
        .then((data) => {
          console.log(data);
          this.form.data = data.child.map((el, i) => {
            let newObj = {
              name: el.sensors_data.name,
              value: el.value,
              color: el.color,
              unit: el.sensors_data.unit,
              designation: el.sensors_data.parents.designation,
            };
            return newObj;
          });
        })
        .catch((e) => {
          console.log(e);
        });
    },
  },
  mounted() {
    {
      let i = document.createElement("input");
      i.setAttribute("type", "color");
      i.type === "color"
        ? (this.colorInputIsSupported = true)
        : (this.colorInputIsSupported = false);
    }
    this.getVaribles();
    this.getDataWorkArea();
  },
};
</script>

<style scoped>
.overlay {
  width: 100vw;
  height: 100vh;
  position: absolute;
  z-index: 200;
  top: 0;
  left: 0;
  background-color: rgba(0, 0, 0, 0.062);
}

.popup_grafik {
  width: 751px;
  height: 328px;
  display: flex;
  justify-content: space-between;
  flex-wrap: wrap;
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.rename_grafik {
  width: 724px;
  height: 328px;
  display: flex;
  flex-direction: column-reverse;
  box-shadow: 0px 2px 6px rgba(0, 0, 0, 0.25);
  background-color: #f7f8fa;
}

.btn_left_del {
  width: 362px;
  height: 36px;

  color: #721c24;
  outline: none;
  cursor: pointer;

  background: #f7f8fa;
  border: none;

  font-family: "Montserrat";
  font-style: normal;
  font-weight: 500;
  font-size: 12px;
  line-height: 15px;
}

.btn_left_del:hover,
.btn_left_del:active,
.btn_left_del:focus {
  color: #ffffff;
  background: #ff7167;
  border: none;
  border-radius: 0;
  transition: 0.2s;
  box-shadow: 0px 9px 109px rgba(0, 0, 0, 0.0372022),
    0px 3.28515px 39.7868px rgba(0, 0, 0, 0.0532451),
    0px 1.59488px 19.3158px rgba(0, 0, 0, 0.0667549),
    0px 0.781839px 9.46894px rgba(0, 0, 0, 0.0827978),
    0px 0.30914px 3.74403px rgba(0, 0, 0, 0.12);
}

.btn_right_done {
  width: 362px;
  height: 36px;

  color: #0b2e13;
  outline: none;
  cursor: pointer;

  font-family: "Montserrat";
  font-style: normal;
  font-weight: 500;
  font-size: 12px;
  line-height: 15px;

  background: #d4edda;
  border: none;
}

.btn_right_done:hover,
.btn_right_done:active,
.btn_right_done:focus {
  color: #858585;
  background: #d4edda;
  border: none;
  border-radius: 0;
  transition: 0.2s;

  box-shadow: 0px 9px 109px rgba(0, 0, 0, 0.0372022),
    0px 3.28515px 39.7868px rgba(0, 0, 0, 0.0532451),
    0px 1.59488px 19.3158px rgba(0, 0, 0, 0.0667549),
    0px 0.781839px 9.46894px rgba(0, 0, 0, 0.0827978),
    0px 0.30914px 3.74403px rgba(0, 0, 0, 0.12);
}

.add_grafik {
  display: flex;
  flex-direction: column;
  padding-left: 6px;
  height: 208px;
}

.head_head {
  justify-content: center;
  text-align: center;
}
.body_tabl {
  padding-top: 6px;
  text-align: center;
  font-family: "Montserrat";
}

.tab1 td {
  font-family: "Montserrat";
  font-style: normal;
  font-weight: 600;
  font-size: 10px;
  line-height: 12px;
}

td {
  vertical-align: middle;
  border: 1px solid grey;
  font-family: "Montserrat";
  font-style: normal;
  font-weight: 500;
  font-size: 10px;
  line-height: 12px;
  color: #4a627a;
  border-spacing: 6px;
  height: 24px;
}

.rentv {
  font-family: "Montserrat";
  font-style: normal;
  font-weight: 500;
  font-size: 16px;
  line-height: 20px;
  color: #4b6075;
  margin-bottom: 24px;
  margin-left: 24px;
}

.rentv_header {
  display: flex;
  flex-direction: column;
}

.addtv {
  width: 628px;
  height: 24px;
  border: 1px solid #9098af;
  border-radius: 4px;
  margin-bottom: 12px;
  font-family: "Montserrat";
  font-style: normal;
  font-weight: normal;
  font-size: 12px;
  line-height: 15px;
  margin-left: 6px;
}

.carbon_close {
  border: none;
  background: none;
}

#rectangle {
  width: 14px;
  height: 14px;
  background-color: pink;
  margin-left: 28px;
}
.verx {
  display: flex;
  justify-content: space-between;
}

.perecl {
  width: 24px;
  height: 24px;
  padding: 0;
  border: none;
  background: none;
  margin: 0px 6px 0px 0px;
  background: center no-repeat url("~assets/svg/perecl.svg");
  /* background: center no-repeat url("~assets/svg/clear.svg"); */
}
.perecl:hover,
.perecl:active,
.perecl:focus {
  width: 24px;
  height: 24px;
  padding: 0;
  border: none;
  background: none;
  margin: 0px 6px 0px 0px;
  background: center no-repeat url("~assets/svg/plus_2.svg");
}

input[type="color"]::-webkit-color-swatch-wrapper {
  padding: 0;
  border: none;
}

.colorPicker {
  border: none;
  padding: 0;
  margin: 0;
  width: 14px;
  height: 14px;
}
</style>

