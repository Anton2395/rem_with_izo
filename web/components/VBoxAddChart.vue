<template>
  <div class="overlay" @click="$emit('closeForm')">
    <div class="popup_grafik" v-on:click.stop="">
      <button class="btn_close" @click="$emit('closeForm')"></button>
      <div class="rename_grafik">
        <div class="rentv_header">
          <div class="verx">
            <span class="rentv"
              >Работа с графиками:
              <span v-show="!isRename">{{ form.name }}</span>
              <input
                class="inputRename"
                v-show="isRename"
                type="text"
                v-model.lazy="form.name"
            /></span>

            <button class="perecl" @click="isRename = !isRename"></button>
          </div>
          <div style="display: flex" class="splusom">
            <select v-model="addVarible.varible" class="addtv">
              <option disabled value="0">Выберите переменную</option>
              <option
                :value="item.id"
                :key="item.id"
                v-for="item in lists.varibles"
              >
                {{ item.name }}
              </option>
            </select>
            <input
              class="colorPicker1"
              type="color"
              v-model="addVarible.color"
            />
            <button class="addChart" @click="addLineChart"></button>
          </div>
        </div>

        <div class="add_grafik">
          <div class="body_tabl" style="overflow-y: auto">
            <table style="border-collapse: collapse" class="tab2">
              <thead>
                <tr>
                  <th style="width: 308px">Название графика</th>
                  <th style="width: 154px">Единицы измерения</th>
                  <th style="width: 158px">Позиционное обозначение</th>
                  <th style="width: 70px">Цвет</th>
                </tr>
              </thead>
              <tbody>
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
                    <div>
                      <div class="row">
                        <input
                          class="colorPicker"
                          type="color"
                          v-model="item.color"
                        />
                      </div>
                    </div>
                  </td>
                  <td
                    class="carbon_close"
                    style="width: 24px"
                    @click="deleteLineChart(item.value)"
                  >
                    <!-- <button
                  @click="deleteLineChart(item.value)"></button> -->
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
        <div class="r_footer">
          <button class="btn_left_del" @click="deleteWorkarea">
            Удалить область
          </button>
          <button class="btn_right_done" @click="SetNewWorkArea">
            Применить
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
// import { mapGetters } from "vuex";
// import { mapActions } from "vuex";

export default {
  name: "VBoxAddChart",
  props: ["Vdata", "workspaces"],
  data() {
    return {
      lists: {
        varibles: [],
      },
      addVarible: {
        color: "#000000",
        varible: "0",
      },

      form: {
        name: this.Vdata.name,
        parent: this.$parent.$parent.actualWorkspace.id,
        data: [],
      },
      varibleSelect: 0,
      showTable: true,
      seriesColor: "#6fcd98",
      colorInputIsSupported: null,
      isRename: false,
    };
  },
  computed: {},
  methods: {
    addLineChart() {
      try {
        // debugger;
        if (
          this.addVarible.varible != "0" &&
          this.form.data.filter((item) => {
            return item.value == this.addVarible.varible;
          }).length == 0
        ) {
          let tempObj = this.lists.varibles.filter((item, i) => {
            return item.id == this.addVarible.varible;
          });
          this.form.data.push({
            color:
              this.addVarible.color == "#000000"
                ? "#" + Math.floor(Math.random() * 16777215).toString(16)
                : this.addVarible.color,
            designation: tempObj[0].parents.designation,
            name: tempObj[0].name,
            unit: tempObj[0].unit,
            value: tempObj[0].id,
          });
        }
      } catch (e) {}
    },
    async deleteWorkarea() {
      // debugger;
      // let index = this.$store.state.selectedWorkarea.workarea.workares.findIndex(
      //   (el) => {
      //     return this.Vdata.id == el.id;
      //   }
      // );
      // this.$store.state.selectedWorkarea.workarea.workares.splice(index, 1);
      this.$store.dispatch("selectedWorkarea/DeleteActiveWorkarea",this.Vdata);
      await this.$axios.$delete(
        `/recorder/structure/Workarea/${this.Vdata.id}`
      );
    },
    deleteLineChart(id) {
      // debugger;
      let findIndex = this.form.data.findIndex((el) => {
        return id == el.value;
      });
      this.form.data.splice(findIndex, 1);
    },
    async getVaribles() {
      await this.$axios
        .$get(`/recorder/structure/ValueSensor/`)
        .then((data) => {
          this.lists.varibles = data;
        })
        .catch((e) => {});
    },
    async getDataWorkArea() {
      await this.$axios
        .$get(`/recorder/structure/Workarea/${this.Vdata.id}`)
        .then((data) => {
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
        .catch((e) => {});
    },

    async SetNewWorkArea() {
      // debugger;
      try {
        if (this.form.data.length>0) {
          this.form.data.map((el) => {
            delete el.designation;
            delete el.unit;
            delete el.name;
          });
        };
          // debugger;
          await this.$axios
            .$put(`/recorder/structure/Workarea/${this.Vdata.id}/`, this.form)
            .then((data) => {
              this.$emit("closeForm");
              if (this.$parent.setRangeVar != null) {
                this.$parent.getData(this.$parent.setRangeVar);
                // console.log(this.$parent.setRangeVar, 'button');
                this.$parent.graphObjectLastZoom = null;
              }

              if (this.$parent.graphObjectLastZoom != null) {
                //  console.log(this.$parent.graphObjectLastZoom, 'graph obj');
                this.$parent.getFromChildDate();
              }
              if (
                this.$parent.setRangeVar == null &&
                this.$parent.graphObjectLastZoom == null
              ) {
                this.$parent.getData();
              }
              // debugger;
                      // this.$parent.$parent.actualWorkspace.workares[
                      //   this.$parent.$parent.actualWorkspace.workares.findIndex(
                      //     (el) => {
                      //       return this.Vdata.id == el.id;
                      //     }
                      //   )
                      // ].name = data.name;
                      this.$store.dispatch("selectedWorkarea/RenameWorkArea",{
                        id:this.Vdata.id,
                        parent:this.form.parent,
                        name:this.form.name
                      })
            })
            .catch((e) => {});
        
      } catch (e) {}
    },
  },
  mounted() {
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
  flex-direction: column;
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
  margin-right: 26px;
  border: 1px solid grey;
}
.body_tabl {
  padding-top: 6px;
  text-align: center;
  font-family: "Montserrat";
}

.tab1 td,
th {
  font-family: "Montserrat";
  font-style: normal;
  font-weight: 600;
  font-size: 10px;
  line-height: 12px;
}

td,
th {
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

th {
  margin-bottom: 10px;
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
  /* margin-top: 10px; */
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
  background: center no-repeat url("~assets/svg/carbon_close.svg");
}
.carbon_close:hover {
  background: center no-repeat url("~assets/svg/recorder/hovClose.svg");
  cursor: pointer;
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
  margin-top: 10px;
}

.perecl {
  outline: none;
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
.colorPicker1 {
  border: none;
  padding: 0;
  margin-left: 13px;
  margin-right: 5px;
  margin-top: 5px;
  width: 14px;
  height: 14px;
}
.r_footer {
  display: flex;
  margin-top: auto;
}
.btn_close {
  width: 24px;
  height: 24px;
  background-image: url("~assets/svg/clear_24px.svg");
  background-position: center;
  background-repeat: no-repeat;
  background-size: contain;
}
.btn_close:hover {
  background: center no-repeat url("~assets/svg/iconControlModal.svg");
  display: block;
  width: 24px;
  height: 24px;
  border: none;
  outline: none;
}
.addChart {
  outline: none;
  width: 24px;
  height: 24px;
  background-image: url("~assets/svg/recorder/addChart.svg");
}
.addChart:hover {
  /* background-image: url("~assets/svg/recorder/hovaddChart.svg"); */
}
.inputRename {
  width: 484px;
  border: 1px solid grey;
  border-radius: 3px;
  outline: none;
  padding: 3px;
}
</style>

