<template>
  <div class="overlay" @click="$parent.$emit('closeAddForm', 'addSensor')">
    <div class="modal-created" v-on:click.stop="">
      <div class="sensor">
        <div class="sensor-header">
          <div class="title-header">Добавление датчика</div>
        </div>
        <div class="sensor-body">
          <div class="sensor-body-box">
            <div class="first-step-object">
              <input
                v-model.lazy="form.name"
                placeholder="Название датчика"
                autocomplete="off"
                id="name"
                type="text"
              />
              <label for="name">Название датчика</label>
            </div>
            <select
              type="text"
              v-model="form.reserves1"
              v-if="
                this.clientsObject.currentStructureObject.filter(
                  (item) => item.id === 1
                ).length
              "
              @change="changeNext(1)"
            >
              <option value="0" disabled>Название резерва1</option>
              <option
                :value="item.id"
                :key="item.id"
                v-for="item in lists.reserves1"
              >
                {{ item.name }}
              </option>
            </select>
            <select
              type="text"
              v-model="form.reserves2"
              v-if="
                this.clientsObject.currentStructureObject.filter(
                  (item) => item.id === 2
                ).length
              "
              @change="changeNext(2)"
            >
              <option value="0" disabled>Название резерва2</option>
              <option
                :value="item.id"
                :key="item.id"
                v-for="item in lists.reserves2"
              >
                {{ item.name }}
              </option>
            </select>
            <select
              type="text"
              v-model="form.organisations"
              v-if="
                this.clientsObject.currentStructureObject.filter(
                  (item) => item.id === 3
                ).length
              "
              @change="changeNext(3)"
            >
              <option value="0" disabled>Название организации</option>
              <option
                :value="item.id"
                :key="item.id"
                v-for="item in lists.organisations"
              >
                {{ item.name }}
              </option>
            </select>
            <select
              type="text"
              v-model="form.companies"
              v-if="
                this.clientsObject.currentStructureObject.filter(
                  (item) => item.id === 4
                ).length
              "
              @change="changeNext(4)"
            >
              <option value="0" disabled>Название предприятия</option>
              <option
                :value="item.id"
                :key="item.id"
                v-for="item in lists.companies"
              >
                {{ item.name }}
              </option>
            </select>
            <select
              type="text"
              v-model="form.factories"
              v-if="
                this.clientsObject.currentStructureObject.filter(
                  (item) => item.id === 5
                ).length
              "
              @change="changeNext(5)"
            >
              <option value="0" disabled>Название завода</option>
              <option
                :value="item.id"
                :key="item.id"
                v-for="item in lists.factories"
              >
                {{ item.name }}
              </option>
            </select>
            <select
              type="text"
              v-model="form.workshops"
              v-if="
                this.clientsObject.currentStructureObject.filter(
                  (item) => item.id === 6
                ).length
              "
              @change="changeNext(6)"
            >
              <option value="0" disabled>Название цеха</option>
              <option
                :value="item.id"
                :key="item.id"
                v-for="item in lists.workshops"
              >
                {{ item.name }}
              </option>
            </select>
            <select
              type="text"
              v-model="form.knots"
              v-if="
                this.clientsObject.currentStructureObject.filter(
                  (item) => item.id === 7
                ).length
              "
            >
              <option value="0" disabled>Название узла</option>
              <option :value="item.id" :key="item.id" v-for="item in lists.knots">
                {{ item.name }}
              </option>
            </select>
          </div>
          <div class="first-step-object last">
            <input
              v-model.lazy="form.shema"
              placeholder="Обозначение на схемах"
              autocomplete="off"
              type="text"
            />
            <label>Обозначение на схемах</label>
          </div>
        </div>
        <div class="sensor-footer">
          <button class="btn-center" @click="save">Применить</button>
        </div>
      </div>
      <button class="btn_icon2">
        <div
          class="btn-bg"
          @click="$parent.$emit('closeAddForm', 'addSensor')"
        ></div>
      </button>
    </div>
  </div>
</template>

<script>
import { mapActions, mapGetters } from "vuex";

export default {
  name: "AddSensor",
  props: ["id"],
  data() {
    return {
      form: {
        name: "",
        reserves1: 0,
        reserves2: 0,
        organisations: 0,
        companies: 0,
        factories: 0,
        workshops: 0,
        knots: 0,
        shema: "",
      },
      lists:{
        reserves1:[],
        reserves2:[],
        organisations:[],
        companies:[],
        factories:[],
        workshops:[],
        knots:[],
      },
    };
  },
  mounted() {
    document.addEventListener("keyup", this.escapeKeyListener);
  },
  destroyed() {
    document.removeEventListener("keyup", this.escapeKeyListener);
  },
  created() {
    this.recForms();
  },
  watch: {
    reserves1: {
      handler(role) {
        this.recForms();
        if (role) {
          let numType = 1; //*номер типа в полной структуре
          this.filterDataSelect(numType, role);
        }
      },
      immediate: true,
    },
    reserves2: {
      handler(role) {
        if (role) {
          let numType = 2; //*номер типа в полной структуре
          this.filterDataSelect(numType, role);
        }
      },
      immediate: true,
    },
    organisations: {
      handler(role) {
        if (role) {
          let numType = 3; //*номер типа в полной структуре
          this.filterDataSelect(numType, role);
        }
      },
      immediate: true,
    },
    companies: {
      handler(role) {
        if (role) {
          let numType = 4; //*номер типа в полной структуре
          this.filterDataSelect(numType, role);
        }
      },
      immediate: true,
    },
    factories: {
      handler(role) {
        if (role) {
          let numType = 5; //*номер типа в полной структуре
          this.filterDataSelect(numType, role);
        }
      },
      immediate: true,
    },
    workshops: {
      handler(role) {
        if (role) {
          let numType = 6; //*номер типа в полной структуре
          this.filterDataSelect(numType, role);
        }
      },
      immediate: true,
    },
    knots: {
      handler(role) {
        if (role) {
          let numType = 7; //*номер типа в полной структуре
          this.filterDataSelect(numType, role);
        }
      },
      immediate: true,
    },
  },
  
  methods: {
    filterDataSelect(numType, role) {
      let typeArray = this.typeStructuredTable[numType - 1].key;
      let currentStructureObject = this.clientsObject.currentStructureObject;
      //*текущая структура
      // debugger;
      if (
        currentStructureObject.filter((item) => {
          return item.id == numType;
        }).length
      ) {
        //*проверка есть ли исследуемый массив в общей структуре
        if (this.clientsObject.currentStructureObject[0].id != numType) {
          //* элемент не самый первый в структуре
          if (this.id != null) {
            //* нажата кнопка изменить

            {
              let currentNameType = typeArray, // * определяем как зовется текущий массив переменных
                prevNameType; // *определяем как зовется предыдущий изменяемый массив переменных

              let type_id = numType; //* id = 5

              let typeStructureTableKey = this.typeStructureTableKey; //*массив с ключами для post,get,put запросов
              let typeStructuredTable = this.typeStructuredTable; //*полная структура с названиями getters

              // currentNameType = typeStructuredTable[type_id - 1].key;
              let indexCurrentNameTypeInCurrentStructure = currentStructureObject.findIndex(
                (item) => {
                  return item.id == type_id;
                }
              );
              // console.log(indexCurrentNameTypeInCurrentStructure);
              // debugger;
              let prevIndexCurrentNameTypeInCurrentStructure =
                currentStructureObject[
                  indexCurrentNameTypeInCurrentStructure - 1
                ].id;
              // console.log(prevIndexCurrentNameTypeInCurrentStructure);
              prevNameType =
                typeStructuredTable[
                  prevIndexCurrentNameTypeInCurrentStructure - 1
                ].key;
              // console.log(prevNameType);
              let valueId =
                typeStructureTableKey[
                  prevIndexCurrentNameTypeInCurrentStructure - 1
                ];

              // if (update) {
              //   this.form[nextNameType] = 0;
              // }
              // console.log(this[typeArray]);
              try {
                this.lists[typeArray] = this[typeArray].filter((item) => {
                  // console.log(valueId+"  "+prevNameType);
                  debugger;
                  return item[valueId] == this.form[prevNameType];
                });
              } catch {
                // console.log("[]");
                this.lists[typeArray] = [];
              }
            }
          } else {
            //* нажата кнопка добавить
            // console.log("[]");
            this.lists[typeArray] = [];
          }
        } else {
          //* элемент самый первый в структуре
          this.lists[typeArray] = role;
        }
      } else {
        // console.log("[]");
        this.lists[typeArray] = [];
      }
    },
    recForms() {
      if (this.id) {
      let sensors = this.sensors.filter((item) => item.id === this.id);
      this.id = sensors[0].id;
      this.form.name = sensors[0].name;
      this.form.reserves1 = sensors[0].reserv1_id;
      this.form.reserves2 = sensors[0].reserv2_id;
      this.form.organisations = sensors[0].organisation_id;
      this.form.companies = sensors[0].company_id;
      this.form.factories = sensors[0].factory_id;
      this.form.workshops = sensors[0].workshop_id;
      this.form.knots = sensors[0].knot_id;
      this.form.shema = sensors[0].shema;
    }
    },
    escapeKeyListener: function (evt) {
      if (evt.keyCode === 27) {
        this.$parent.$emit("closeAddForm", "addSensor");
      }
      if (evt.keyCode === 13) {
        this.save();
      }
    },
    ...mapActions("settingsGlobal", {
      updateSensors: "updateSensors",
    }),
    save() {
      let data = {
        id: this.id,
        name: this.form.name,
        reserv1_id: this.form.reserves1,
        reserv2_id: this.form.reserves2,
        organisation_id: this.form.organisations,
        company_id: this.form.companies,
        factory_id: this.form.factories,
        workshop_id: this.form.workshops,
        knot_id: this.form.knots,
        shema: this.form.shema,
      };

      for (let key in data)
        if (!data[key] && key !== "id") {
          if (
            !this.clientsObject.currentStructureObject.filter(
              (item) => item.id === 1
            ).length &&
            key === "reserv1_id"
          )
            continue;

          if (
            !this.clientsObject.currentStructureObject.filter(
              (item) => item.id === 2
            ).length &&
            key === "reserv2_id"
          )
            continue;

          if (
            !this.clientsObject.currentStructureObject.filter(
              (item) => item.id === 3
            ).length &&
            key === "organisation_id"
          )
            continue;

          if (
            !this.clientsObject.currentStructureObject.filter(
              (item) => item.id === 4
            ).length &&
            key === "company_id"
          )
            continue;

          if (
            !this.clientsObject.currentStructureObject.filter(
              (item) => item.id === 5
            ).length &&
            key === "factory_id"
          )
            continue;

          if (
            !this.clientsObject.currentStructureObject.filter(
              (item) => item.id === 6
            ).length &&
            key === "workshop_id"
          )
            continue;

          if (
            !this.clientsObject.currentStructureObject.filter(
              (item) => item.id === 7
            ).length &&
            key === "knot_id"
          )
            continue;

          if (
            !this.clientsObject.currentStructureObject.filter(
              (item) => item.id === 8
            ).length &&
            key === "sensor_id"
          )
            continue;

          // this.$parent.$emit("showAttentionInput");
          this.$parent.show_warning_NecessaryFullField();
          return;
        }

      this.updateSensors(data);
      this.$parent.show_info_RowUpdate();
      this.$parent.$emit("closeAddForm", "addSensor");
    },
    changeNext(type_id, update = true) {
      //функция по заполнению
      /*
       * Изменение массива данных после выбора в селекторе
       * value_id - текущий выбранный id из списка
       * type_id - к какому типа из структуры относится id
       */

      // debugger;
      let currentNameType, // * определяем как зовется текущий массив переменных
        nextNameType, // *определяем как зовется следующий изменяемый массив переменных
        nextNameFormType; // * определяем как зовется переменная в форме которую надо сбросить в 0

      let currentStructureObject = this.clientsObject.currentStructureObject; //*текущая структура
      let typeStructureTableKey = this.typeStructureTableKey; //*массив с ключами для вывода в таблице
      let typeStructuredTable = this.typeStructuredTable; //*полная структура с названиями getters

      currentNameType = typeStructuredTable[type_id - 1].key;
      let indexCurrentNameTypeInCurrentStructure = currentStructureObject.findIndex(
        (item) => {
          return item.id == type_id;
        }
      );
      // debugger;
      let nextIndexCurrentNameTypeInCurrentStructure =
        currentStructureObject[indexCurrentNameTypeInCurrentStructure + 1].id;
      nextNameType =
        typeStructuredTable[nextIndexCurrentNameTypeInCurrentStructure - 1].key;

      let valueId = typeStructureTableKey[type_id - 1];

      if (update) {
        this.form[nextNameType] = 0;
      }

      try {
        this.lists[nextNameType] = this[nextNameType].filter((item) => {
          return item[valueId] == this.form[currentNameType];
        });
      } catch {
        this.lists[nextNameType] = [];
      }
    },
  },
  computed: {
    ...mapGetters("settingsGlobal", {
      clientsObject: "clientsObject",
      typeStructuredTable: "typeStructuredTable",
      typeStructureTableKey: "typeStructureTableKey",
      reserves1: "reserves1",
      reserves2: "reserves2",
      organisations: "organisations",
      companies: "companies",
      factories: "factories",
      workshops: "workshops",
      knots: "knots",
      sensors: "sensors",
      
    }),
  },
};
</script>

<style lang="scss" scoped>
.modal-created input {
  color: #49617b !important;
}
.overlay {
  width: 100vw;
  height: 100vh;
  position: absolute;
  z-index: 19;
  top: 0;
  left: 0;
  background-color: rgba(0, 0, 0, 0.062);
}

.modal-created {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);

  max-width: 400px;
  width: 100%;
  height: auto;

  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;

  background: #f7f8fa;
  box-shadow: 0px 2px 6px rgba(0, 0, 0, 0.25);

  .sensor {
    width: 100%;
    .sensor-header {
      width: 100%;
      height: 24px;
      padding-top: 3px;
      margin-bottom: 24px;
      display: flex;
      align-items: center;
      justify-content: center;
      text-align: center;
      .title-header {
        font-weight: 500;
        font-size: 16px;
        line-height: 20px;
        display: flex;
        align-items: center;
        text-align: center;
        color: #4b6075;
      }
    }

    .sensor-body {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      margin-bottom: 24px;

      font-size: 12px;
      line-height: 15px;

      .sensor-body-box {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        margin-bottom: 12px;

        font-size: 12px;
        line-height: 15px;

        select,
        option {
          width: 376px;
          height: 24px;

          margin-bottom: 12px;
          padding: 3px 6px;

          display: flex;
          align-items: center;

          border: 1px solid #9098af;
          box-sizing: border-box;
          border-radius: 4px;

          font-weight: normal;
          font-size: 12px;

          color: #9098af;

          outline: none;
        }

        input {
          width: 376px;
          height: 24px;

          margin-bottom: 12px;
          padding: 3px 9px;

          display: flex;
          align-items: center;

          border: 1px solid #9098af;
          box-sizing: border-box;
          border-radius: 4px;

          font-weight: normal;
          font-size: 12px;

          color: #9098af;

          outline: none;
        }

        ::placeholder {
          font-weight: normal;
          font-size: 12px;

          color: #9098af;
        }
      }

      input {
        width: 376px;
        height: 24px;

        padding: 3px 6px;

        display: flex;
        align-items: center;

        border: 1px solid #9098af;
        box-sizing: border-box;
        border-radius: 4px;

        outline: none;
      }

      ::placeholder {
        font-weight: normal;
        font-size: 12px;

        color: #9098af;
      }
    }

    .sensor-footer {
      width: 100%;
      height: 36px;
      display: flex;

      .btn-center {
        width: 100%;
        height: 36px;
        border: none;

        display: flex;
        align-items: center;
        justify-content: center;
        padding: 6px 12px;

        font-weight: 500;
        font-size: 12px;
        line-height: 15px;
        text-align: center;

        color: #0b2e13;
        background: #d4edda;

        outline: none;
        cursor: pointer;

        &:hover {
          box-shadow: 0px 0px 6px rgba(0, 0, 0, 0.25);
        }
      }
    }
  }
}

.btn_icon2 {
  position: absolute;
  top: 0;
  left: -34px;
  cursor: pointer;
  background: none;
  border: none;
  display: flex;
  justify-content: baseline;
  outline: none;

  .btn-bg {
    width: 24px;
    height: 24px;
    background-image: url("~assets/svg/clear_24px.svg");
    background-position: center;
    background-repeat: no-repeat;
    background-size: contain;

    &:hover {
      background-image: url("~assets/svg/setting/hovClose.svg");
      background-position: center;
      background-repeat: no-repeat;
      background-size: contain;
    }
  }
}

.first-step-object {
  margin-top: 0;
  border: none;
  width: 376px;
  margin-bottom: 12px;
}

.first-step-object.last {
  margin-bottom: 0;
}
</style>
