<template>
  <div class="overlay" @click="$parent.$emit('closeAddForm', 'addVariables')">
    <div class="modal-created" v-on:click.stop="">
      <div class="variables">
        <div class="variables-header">
          <div class="title-header">Добавление переменной</div>
        </div>
        <div class="variables-body">
          <div class="variables-body-box">
            <div class="first-step-object">
              <input
                v-model.lazy="form.name"
                placeholder="Имя переменной"
                autocomplete="off"
                type="text"
              />
              <label>Имя переменной</label>
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
              @change="changeNext(7)"
            >
              <option value="0" disabled>Название узла</option>
              <option
                :value="item.id"
                :key="item.id"
                v-for="item in lists.knots"
              >
                {{ item.name }}
              </option>
            </select>
            <select
              type="text"
              v-model="form.sensors"
              v-if="
                this.clientsObject.currentStructureObject.filter(
                  (item) => item.id === 8
                ).length
              "
            >
              <option value="0" disabled>Название датчика</option>
              <option
                :value="item.id"
                :key="item.id"
                v-for="item in lists.sensors"
              >
                {{ item.name }}
              </option>
            </select>
          </div>
          <div class="variables-body-box">
            <!--            <select type="text" v-model="form.connect" disabled v-if="id">-->
            <!--              <option :value="form.connect" selected>{{ form.connect }}</option>-->
            <!--            </select>-->
            <select type="text" v-model="form.connect" @change="changeTags">
              <option value="" disabled>Название соединения</option>
              <option
                :value="item.name"
                v-for="item in connections"
                :key="item.id"
              >
                {{ item.name }}
              </option>
            </select>
            <select type="text" v-model="form.variablee">
              <option value="" disabled>Название переменной</option>
              <option
                :value="item.name"
                v-for="item in variableess"
                :key="item.name"
              >
                {{ item.name }}
              </option>
            </select>
            <select type="text" v-model="form.unit">
              <option value="" disabled>Единицы измерения</option>
              <option :value="item" v-for="item in units" :key="item">
                {{ item }}
              </option>
            </select>
          </div>

          <div class="limits-body-box">
            <h3 class="title">Пределы</h3>
            <div class="form-group">
              <div class="first-step-object col-6">
                <input
                  v-model.lazy="form.limitMinWarn"
                  placeholder="Нижн. предупредительный"
                  autocomplete="off"
                  type="number"
                />
                <label>Нижн. предупредительный</label>
              </div>
              <div class="first-step-object col-6">
                <input
                  v-model.lazy="form.limitMaxWarn"
                  placeholder="Верхн. предупредительный"
                  autocomplete="off"
                  type="number"
                />
                <label>Верхн. предупредительный</label>
              </div>
              <!--              <input type="text" class="col-6" v-model="form.limitMinWarn" placeholder="Нижн. предупредительный">-->
              <!--              <input type="text" class="col-6" v-model="form.limitMaxWarn" placeholder="Верхн. предупредительный">-->
            </div>
            <div class="form-group">
              <div class="first-step-object col-6">
                <input
                  v-model.lazy="form.limitMinСrash"
                  placeholder="Нижн. аварийный"
                  autocomplete="off"
                  type="number"
                />
                <label>Нижн. аварийный</label>
              </div>
              <div class="first-step-object col-6">
                <input
                  v-model.lazy="form.limitMaxСrash"
                  placeholder="Верхн. аварийный"
                  autocomplete="off"
                  type="number"
                />
                <label>Верхн. аварийный</label>
              </div>
              <!--              <input type="text" class="col-6" v-model="form.limitMinСrash" placeholder="Нижн. аварийный">-->
              <!--              <input type="text" class="col-6" v-model="form.limitMaxСrash" placeholder="Верхн. аварийный">-->
            </div>
            <div class="form-group">
              <div class="first-step-object">
                <input
                  v-model.lazy="form.limitSpead"
                  placeholder="Аварийная скорость изменения переменной"
                  autocomplete="off"
                  type="number"
                />
                <label>Аварийная скорость изменения переменной</label>
              </div>
              <!--              <input type="text" v-model="form.limitSpead" placeholder="Аварийная скорость изменения переменной">-->
            </div>
          </div>
          <div class="variables-body-box-row"></div>
        </div>
        <div class="variables-footer">
          <button class="btn-center" @click="save">Применить</button>
        </div>
      </div>
      <button class="btn_icon2">
        <div
          class="btn-bg"
          @click="$parent.$emit('closeAddForm', 'addVariables')"
        ></div>
      </button>
    </div>
  </div>
</template>

<script>
import { mapActions, mapGetters } from "vuex";

export default {
  name: "AddVariables",
  props: ["id"],
  destroyed() {
    document.removeEventListener("keyup", this.escapeKeyListener);
  },
  created() {
    // console.log("11"+this.id);
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
    sensors: {
      handler(role) {
        if (role) {
          let numType = 8; //*номер типа в полной структуре
          this.filterDataSelect(numType, role);
        }
      },
      immediate: true,
    },
  },
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
        sensors: 0,
        connect: "",
        connectId: 0,
        variablee: "",
        unit: "",
        limitMinWarn: "",
        limitMaxWarn: "",
        limitMinСrash: "",
        limitMaxСrash: "",
        limitSpead: "",
        table_name: "",
      },
      variableess: [],
      units: [
        "бит",
        "гр",
        "кг",
        "тн",
        "мм",
        "м",
        "A",
        "Oм",
        "°C",
        "°F",
        "м³/ч",
        "мБар",
        "Бар",
        "МПа",
        "кВт",
        "%",
        "мм/с²",
        "Гц",
        "Н·м",
      ],
      lists: {
        reserves1: [],
        reserves2: [],
        organisations: [],
        companies: [],
        factories: [],
        workshops: [],
        knots: [],
        sensors: [],
      },
    };
  },
  mounted() {
    document.addEventListener("keyup", this.escapeKeyListener);
    this.getDataConnection()
      .then(() => {
        // debugger;
        if (this.form.connect && this.variableess.length == 0) {
          this.changeTags();
        }
      })
      .catch((e) => {
        console.log(e);
      });

    // if (this.id) {
    //   let variables = this.variables.filter((item) => item.id === this.id);
    //   console.log(variables);
    //   this.id = variables[0].id;
    //   this.form.name = variables[0].name;

    //   this.form.reserve1 = variables[0].reserve1_id
    //     ? variables[0].reserve1_id
    //     : 0;
    //   this.form.reserve2 = variables[0].reserve2_id
    //     ? variables[0].reserve2_id
    //     : 0;
    //   this.form.organisation = variables[0].organisation_id
    //     ? variables[0].organisation_id
    //     : 0;
    //   this.form.company = variables[0].company_id ? variables[0].company_id : 0;
    //   this.form.factory = variables[0].factory_id ? variables[0].factory_id : 0;
    //   this.form.workshop = variables[0].workshop_id
    //     ? variables[0].workshop_id
    //     : 0;
    //   this.form.knot = variables[0].knot_id ? variables[0].knot_id : 0;
    //   this.form.sensor = variables[0].sensor_id ? variables[0].sensor_id : 0;

    //   this.form.unit = variables[0].unit ? variables[0].unit : "";
    //   this.form.connect = variables[0].connect ? variables[0].connect : 0;
    //   this.form.variablee = variables[0].variablee ? variables[0].variablee : 0;

    //   this.form.limitMinWarn = variables[0].limitMinWarn;
    //   this.form.limitMaxWarn = variables[0].limitMaxWarn;
    //   this.form.limitMinСrash = variables[0].limitMinСrash;
    //   this.form.limitMaxСrash = variables[0].limitMaxСrash;
    //   this.form.limitSpead = variables[0].limitSpead;
    // }
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
        let variables = this.variables.filter((item) => item.id === this.id);
        // console.log(variables);

        this.id = variables[0].id;
        this.form.name = variables[0].name;

        this.form.reserves1 = variables[0].reserv1_id
          ? variables[0].reserv1_id
          : 0;
        this.form.reserves2 = variables[0].reserv2_id
          ? variables[0].reserv2_id
          : 0;
        this.form.organisations = variables[0].organisation_id
          ? variables[0].organisation_id
          : 0;
        this.form.companies = variables[0].company_id
          ? variables[0].company_id
          : 0;
        this.form.factories = variables[0].factory_id
          ? variables[0].factory_id
          : 0;
        this.form.workshops = variables[0].workshop_id
          ? variables[0].workshop_id
          : 0;
        this.form.knots = variables[0].knot_id ? variables[0].knot_id : 0;
        this.form.sensors = variables[0].sensor_id ? variables[0].sensor_id : 0;

        this.form.unit = variables[0].unit ? variables[0].unit : "";
        this.form.connect = variables[0].connect ? variables[0].connect : 0;
        this.form.variablee = variables[0].variablee
          ? variables[0].variablee.substring(5)
          : 0;

        this.form.limitMinWarn = variables[0].limitMinWarn;
        this.form.limitMaxWarn = variables[0].limitMaxWarn;
        this.form.limitMinСrash = variables[0].limitMinСrash;
        this.form.limitMaxСrash = variables[0].limitMaxСrash;
        this.form.limitSpead = variables[0].limitSpead;
        // debugger;
      }
    },
    escapeKeyListener: function (evt) {
      if (evt.keyCode === 27) {
        this.$parent.$emit("closeAddForm", "addVariables");
      }
      if (evt.keyCode === 13) {
        this.save();
      }
    },
    ...mapActions("settingsGlobal", {
      updateVariables: "updateVariables",
      getDataConnection: "getDataConnection",
      getDataConnectionTags: "getDataConnectionTags",
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
        sensor_id: this.form.sensors,
        connect: this.form.connect,
        variablee: this.form.variablee,
        unit: this.form.unit,
        table_name: `mvlab_${
          this.form.connect
        }_${this.form.variablee.toLowerCase()}`,

        limitMinWarn: this.form.limitMinWarn != "" ? this.form.limitMinWarn : 0,
        limitMaxWarn: this.form.limitMaxWarn != "" ? this.form.limitMaxWarn : 0,
        limitMinСrash:
          this.form.limitMinСrash != "" ? this.form.limitMinСrash : 0,
        limitMaxСrash:
          this.form.limitMaxСrash != "" ? this.form.limitMaxСrash : 0,
        limitSpead: this.form.limitSpead != "" ? this.form.limitSpead : 0,
      };
      debugger;
      for (let key in data) 
        if (!data[key] && key !== "id") {
          if (
            key === "limitMinWarn" ||
            key === "limitMaxWarn" ||
            key === "limitMinСrash" ||
            key === "limitMaxСrash" ||
            key === "limitSpead"
          )
            continue;

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
  
        this.updateVariables(data);
        this.$parent.show_info_RowUpdate();
        this.$parent.$emit("closeAddForm", "addVariables");
    },
    changeTags() {
      let nameConnect = this.form.connect;
      let findId = this.connections.filter(
        (item) => item.name == nameConnect
      )[0].id;
      this.form.connectId = findId;
      // console.log(findId);
      this.getDataConnectionTags({ name: nameConnect, id: findId })
        .then(() => {
          // debugger;
          this.variableess = this.connections[this.form.connectId].tags;
          if (
            this.form.variablee &&
            this.variableess.filter((item) => item.name == this.form.variablee)
              .length == 0
          ) {
            this.form.variablee = "";
          }
        })
        .catch((e) => {
          console.log(e);
        });
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
      variables: "variables",
      connections: "connection",
    }),
    listTags() {
      return this.connections[this.form.connectId].tags;
    },

    // ...mapGetters("Messages", {
    //   connections: "currentDevMessagesVar",
    // }),
  },
};
</script>

<style lang="scss" scoped>
h3.title {
  font-family: Montserrat;
  font-size: 12px;
  font-style: normal;
  font-weight: 600;
  line-height: 15px;
  letter-spacing: 0em;
  text-align: center;
  color: rgba(127, 145, 162, 0.6);
  margin-bottom: 12px;
}

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

  .variables {
    width: 100%;

    .variables-header {
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

    .variables-body {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      margin-bottom: 24px;

      font-size: 12px;
      line-height: 15px;

      .variables-body-box {
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
          background: #f7f8fa;

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
          background: #f7f8fa;

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
        background: #f7f8fa;

        outline: none;
      }

      ::placeholder {
        font-weight: normal;
        font-size: 12px;

        color: #9098af;
      }
    }

    .variables-footer {
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

.form-group {
  width: 100%;
  display: flex;
  justify-content: space-between;
  margin-bottom: 12px;

  .col-6 {
    width: calc(50% - 3px) !important;
  }
}

.form-group:last-child {
  margin-bottom: 0;
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

.col-6 {
  margin-bottom: 0;
}

.col-6 input {
  width: 100% !important;
}
</style>
