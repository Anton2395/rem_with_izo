<template>
  <div class="overlay"
  @click="$parent.$emit('closeAddForm', 'addFactory')">
    <div class="modal-created"
    v-on:click.stop="">
      <div class="attention-close">
        <div class="attention-header">
          <div class="title-header">Добавление завода</div>
        </div>
        <div class="attention-body">
          <div class="box select">
            <div class="first-step-object">
              <input
                v-model.lazy="form.name"
                placeholder="Название завода"
                autocomplete="off"
                type="text"
              />
              <label>Название предприятия</label>
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
          </div>

          <div class="first-step-object">
            <input
              v-model.lazy="form.map"
              placeholder="Местоположение"
              autocomplete="off"
              id="name"
              type="text"
            />
            <label for="name">Местоположение</label>
          </div>
        </div>
        <div class="attention-footer">
          <button class="btn-center" @click="save">Применить</button>
        </div>
      </div>
      <button class="btn_icon2">
        <div
          class="btn-bg"
          @click="$parent.$emit('closeAddForm', 'addFactory')"
        ></div>
      </button>
    </div>
  </div>
</template>

<script>
import {mapActions, mapGetters} from "vuex";

export default {
  name: "AddFactory",
  props: [
    'id'
  ],
  data() {
    return {
      form: {
        name: '',
        reserves1: 0,
        reserves2: 0,
        organisations: 0,
        companies: 0,
        map: "",
      },
      lists:{
        reserves1:[],
        reserves2:[],
        organisations:[],
        companies:[],
      }
    }
  },
  mounted(){
    document.addEventListener('keyup', this.escapeKeyListener);
  },
  destroyed() {
    document.removeEventListener('keyup', this.escapeKeyListener);
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
      if(this.id) {
      let factories = this.factories.filter(item => item.id === this.id);
      this.id = factories[0].id;
      this.form.name = factories[0].name;
      this.form.reserves1 = factories[0].reserv1_id;
      this.form.reserves2 = factories[0].reserv2_id;
      this.form.organisations = factories[0].organisation_id;
      this.form.companies = factories[0].company_id;
      this.form.map = factories[0].map;
    }
    },
    escapeKeyListener: function(evt) {
      if (evt.keyCode === 27 ) {
        this.$parent.$emit('closeAddForm', 'addFactory');
      };
      if (evt.keyCode === 13){
        this.save();
      }
    },
    ...mapActions('settingsGlobal', {
      updateFactories: 'updateFactories',
    }),
    save() {
      let data = {
        id: this.id,
        name: this.form.name,
        reserv1_id: this.form.reserves1,
        reserv2_id: this.form.reserves2,
        organisation_id: this.form.organisations,
        company_id: this.form.companies,
        map: this.form.map,
      }

      for(let key in data)
        if(!data[key] && key !== 'id') {
          if(!this.clientsObject.currentStructureObject.filter(item => item.id === 1).length && key === 'reserv1_id')
            continue;

          if(!this.clientsObject.currentStructureObject.filter(item => item.id === 2).length && key === 'reserv2_id')
            continue;

          if(!this.clientsObject.currentStructureObject.filter(item => item.id === 3).length && key === 'organisation_id')
            continue;

          if(!this.clientsObject.currentStructureObject.filter(item => item.id === 4).length && key === 'company_id')
            continue;

          if(!this.clientsObject.currentStructureObject.filter(item => item.id === 5).length && key === 'factory_id')
            continue;

          if(!this.clientsObject.currentStructureObject.filter(item => item.id === 6).length && key === 'workshop_id')
            continue;

          if(!this.clientsObject.currentStructureObject.filter(item => item.id === 7).length && key === 'knot_id')
            continue;

          if(!this.clientsObject.currentStructureObject.filter(item => item.id === 8).length && key === 'sensor_id')
            continue;

          // this.$parent.$emit('showAttentionInput');
          this.$parent.show_warning_NecessaryFullField();
          return;
        }

      this.updateFactories(data);
      this.$parent.show_info_RowUpdate();
      this.$parent.$emit('closeAddForm', 'addFactory')
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
    ...mapGetters('settingsGlobal', {
      clientsObject: "clientsObject",
      typeStructuredTable: "typeStructuredTable",
      typeStructureTableKey: "typeStructureTableKey",
      reserves1: 'reserves1',
      reserves2: 'reserves2',
      organisations: 'organisations',
      companies: 'companies',
      factories: 'factories',
    }),
  }
}
</script>

<style lang="scss" scoped>
.modal-created input {
  color: #49617b;
}
.modal-created {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);

  width: 400px;
  height: auto;

  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;

  background: #f7f8fa;
  box-shadow: 0px 2px 6px rgba(0, 0, 0, 0.25);

  .attention-close {
    width: 100%;

    .attention-header {
      width: 100%;
      height: 24px;
      padding-top: 3px;
      margin-bottom: 26px;
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

    .attention-body {
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

      .box {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        margin-bottom: 12px;

        font-size: 12px;
        line-height: 15px;

        .select {
          position: relative;

          option[disabled="disabled"] {
            background: #e1dbdb;
          }

          &::before {
            content: "";
            display: block;
            background-image: url("~assets/svg/setting/select_arrow.svg");
            background-repeat: no-repeat;
            background-size: 100%;
            width: 10px;
            height: 6px;
            position: absolute;
            top: 50%;
            right: 20px;
            transform: translateY(-50%);
            z-index: 1;
          }
        }
      }
    }

    .attention-footer {
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

  .box-modal {
    position: relative;

    width: 468px;
    height: 392px;

    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;

    .attention {
      width: 300px;
      height: 300px;
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
    }
  }
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
