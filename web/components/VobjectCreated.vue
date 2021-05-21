<template>
  <div class="overlay">
    <div class="modal-created">
      <div class="box-modal">
        <div class="title">Мастер создания объектов</div>

        <div class="steps">
          <div
            class="first"
            :class="{
              active: arrActiveStep.firstStep,
              done: arrDoneStep.firstStep,
            }"
          >
            <div class="first-step step active">1</div>
            <div class="description-step first-description">
              Описание объекта
            </div>
          </div>
          <div class="ellipsis">
            <div
              class="small-point"
              :class="{
                active: arrActiveStep.secondStep,
                done: arrDoneStep.secondStep,
              }"
            ></div>
            <div
              class="small-point"
              :class="{
                active: arrActiveStep.secondStep,
                done: arrDoneStep.secondStep,
              }"
            ></div>
            <div
              class="small-point"
              :class="{
                active: arrActiveStep.secondStep,
                done: arrDoneStep.secondStep,
              }"
            ></div>
          </div>
          <div
            class="second"
            :class="{
              active: arrActiveStep.secondStep,
              done: arrDoneStep.secondStep,
            }"
          >
            <div class="second-step step">2</div>
            <div class="description-step second-description">
              Структура объекта
            </div>
          </div>
        </div>
        <!--      <div class="description-steps"></div>-->
        <hr />
        <div class="first-step-objects" v-show="arrActiveStep.firstStep">
          <div class="first-step-object">
            <input
              v-model.lazy="currentProject.projectName"
              placeholder="Название объекта"
              autocomplete="off"
              id="name"
              type="text"
            />
            <label for="name">Название объекта</label>
          </div>
          <div class="first-step-object">
            <input
              v-model.lazy="currentProject.clientName"
              placeholder="Заказчик"
              autocomplete="off"
              id="client"
              type="text"
            />
            <label for="client">Заказчик</label>
          </div>
          <div class="first-step-object">
            <input
              v-model.lazy="currentProject.clientContract"
              placeholder="Договор"
              autocomplete="off"
              id="contract"
              type="text"
            />
            <label for="contract">Договор</label>
          </div>
        </div>

        <!-- <attentionInput v-if="showAttentionInput"></attentionInput> -->

        <div class="second-step-objects" v-show="arrActiveStep.secondStep">
          <div id="levelList" class="second-step-object">
            <div
              class="structure-object"
              v-for="(structureItem, idx) in currentStructureObject"
              :key="idx"
            >
              <div class="level-name level">Уровень {{ idx }}</div>

              <select
                class="level-value level"
                v-model="currentStructureObject[idx]"
                :disabled="idx < currentStructureObject.length - 1"
              >
                <option
                  v-for="type in typeStructured"
                  :value="type.id"
                  :disabled="type.disabled"
                  :class="{ hide: type.disabled }"
                  :key="type.id"
                >
                  {{ type.text }}
                </option>
              </select>

              <button
                class="level-remove level btn_icon level-btn btn_icon-panel"
                @click="removeLevel"
                :disabled="
                  !(idx >= currentStructureObject.length - 1 && idx !== 0)
                "
                :class="{
                  hide_minus: !(
                    idx >= currentStructureObject.length - 1 && idx !== 0
                  ),
                }"
              >
                <IconifyIcon
                  icon="baselineRemove"
                  :style="{ fontSize: '24px' }"
                />
              </button>

              <button
                class="level-add level btn_icon level-btn btn_icon-panel"
                @click="addLevel"
                :disabled="
                  !(
                    currentStructureObject[idx] &&
                    idx >= currentStructureObject.length - 1 &&
                    currentStructureObject[
                      currentStructureObject.length - 1
                    ] !== 8
                  )
                "
                :class="{
                  hide_plus: !(
                    idx >= currentStructureObject.length - 1 &&
                    currentStructureObject[
                      currentStructureObject.length - 1
                    ] !== 8
                  ),
                }"
              >
                <IconifyIcon icon="addIcon" :style="{ fontSize: '24px' }" />
              </button>
            </div>
          </div>
        </div>

        <div class="tabfoot">
          <button class="tabfoot-left btn_icon">
            <div class="tabfoot_title" v-on:click="prevStep">
              {{ this.prevbtn }}
            </div>
          </button>
          <button class="tabfoot-right btn_icon">
            <div class="tabfoot_title" v-on:click="nextStep">
              {{ this.nextbtn }}
            </div>
          </button>
        </div>

        <attentionClose v-if="showAttentionClose"></attentionClose>
      </div>
      <button class="btn_icon2">
        <div class="btn-bg" @click="showAttentionClose = true"></div>
      </button>
    </div>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
import { mapActions } from "vuex";

import AttentionClose from "@/components/settingsGlobal/AttentionClose";
// import AttentionInput from "@/components/settingsGlobal/AttentionInput";

export default {
  data() {
    return {
      arrActiveStep: {
        firstStep: true,
        secondStep: false,
      },

      arrDoneStep: {
        firstStep: false,
        secondStep: false,
      },
      currentProject: {
        projectName: null,
        clientName: null,
        clientContract: null,
      },
      selected: "",
      currentStructureObject: [0],

      showAttentionClose: false,
      // showAttentionInput: false,
    };
  },

  created() {
    this.getTypeStructured();
    this.$on("closeVobjectCreated", () => {
      this.$parent.$emit("closeVobjectCreated");
    });
    this.$on("closeAttentionClose", () => {
      this.showAttentionClose = false;
    });
    this.$on("closeAttentionInput", () => {
      this.showAttentionInput = false;
    });

    if (this.clientsObject) {
      this.currentProject.projectName = this.clientsObject.name_object;
      this.currentProject.clientContract = this.clientsObject.contact;
      this.currentProject.clientName = this.clientsObject.customer;
      let clientsObject = JSON.parse(
        JSON.stringify(this.clientsObject.currentStructureObject)
      );
      clientsObject.pop();
      let newArr = [];
      clientsObject.forEach((item) => {
        newArr.push(item.id);
      });
      this.currentStructureObject = newArr;
    }
  },

  components: {
    attentionClose: AttentionClose,
    // attentionInput: AttentionInput,
  },

  watch: {
    currentStructureObject: function (newValue) {
      if (newValue.length < 2) {
        for (let i = 1; i <= this.typeStructured.length - 1; i++)
          this.typeStructured[i].disabled = false;

        return false;
      }

      let index = newValue[newValue.length - 2];
      for (let i = 1; i <= this.typeStructured.length - 1; i++) {
        if (i <= index) this.typeStructured[i].disabled = true;
        else this.typeStructured[i].disabled = false;
      }
    },
  },

  computed: {
    ...mapGetters("settingsGlobal", {
      typeStructured: "typeStructured",
      clientsObject: "clientsObject",
    }),
    nextbtn() {
      let title = this.arrActiveStep.secondStep
        ? "Создать объект"
        : "Следующий шаг";

      return title;
    },
    prevbtn() {
      let title = this.arrActiveStep.firstStep ? "Закрыть" : "Предыдущий шаг";

      return title;
    },
  },
  methods: {
    ...mapActions("settingsGlobal", {
      updateClientsObject: "updateClientsObject",
      getTypeStructured: "getTypeStructured",
    }),
    show_warning1() {
        this.$notify.warning({
          title: 'Внимание',
          message: 'Необходимо заполнить все поля'
        });
      },
    // show_warning2() {
    //     this.$notify.error({
    //       title: 'Вниманиe',
    //       message: 'Изменения не будут приняты'
    //     });
    //   },
    nextStep() {
      if (this.arrActiveStep.firstStep) {
        if (
          this.currentProject.projectName &&
          this.currentProject.clientName &&
          this.currentProject.clientContract
        ) {
          this.arrActiveStep.firstStep = false;
          this.arrActiveStep.secondStep = true;

          this.arrDoneStep.firstStep = true;
          this.arrDoneStep.secondStep = false;
        } else {
          this.show_warning1();
        }
      } else {
        if (this.currentStructureObject.indexOf(8) > -1) {
     
          this.updateClientsObject({
            currentProject: this.currentProject,
            currentStructureObject: this.currentStructureObject,
          });
          this.$parent.$emit("closeVobjectCreated");
        } 
        else {
          this.showAttentionInput = true;
        }
      }
    },
    prevStep() {
      if (this.arrActiveStep.secondStep) {
        this.arrActiveStep.firstStep = true;
        this.arrActiveStep.secondStep = false;

        this.arrDoneStep.firstStep = false;
        this.arrDoneStep.secondStep = true;
      } else if (this.arrActiveStep.secondStep) {
        this.arrActiveStep.firstStep = false;
        this.arrActiveStep.secondStep = true;

        this.arrDoneStep.firstStep = true;
        this.arrDoneStep.secondStep = false;
      } else {
        this.showAttentionClose = true;
      }
    },
    addLevel() {
      this.currentStructureObject.push(0);
    },
    removeLevel() {
      this.currentStructureObject.pop();
    },
  },
};
</script>

<style lang="scss" scoped>
.sub-panel {
  margin-left: 66px;
}

.active-item:before {
  content: "";
  width: 100%;
  border-bottom: 1px solid #2dc2fa;
  position: absolute;
  bottom: -1px;
  left: 0;
}

.level-name {
  font-weight: 600;
  font-size: 14px;
  line-height: 17px;
  display: flex;
  align-items: center;

  color: #00c484;
  width: 100px;
  height: 24px;
}

.level-value {
  outline: none;

  width: 246px;
  height: 24px;

  border: 1px solid #9098af;
  border-radius: 4px;

  font-weight: normal;
  font-size: 12px;
  line-height: 15px;
  display: flex;
  align-items: center;

  color: #778a9c;
  background-color: inherit;
}

.level-add {
  color: #01c587;
}

.level-remove {
  color: #ff6f64;
}

.tabfoot {
  margin-top: auto;

  width: 100%;
  display: flex;
  flex-direction: row;
}

button {
  padding: 0;
  font-style: 24px;
}

.btn_icon {
  background: none;
  border: none;
  display: flex;
  justify-content: baseline;
  outline: none;
}

.tabfoot button {
  padding: 0;
  width: 50%;
  height: 36px;
}

.tabfoot button:hover {
  box-shadow: 0px 0px 6px rgba(0, 0, 0, 0.25);
}

.tabfoot-left {
  color: #9aaaba;
  background: #f7f8fa;
}

.tabfoot-left:hover {
  background: #f7f8fa;
}

.tabfoot-right {
  background: #d4edda;
}

//.tabfoot-right:hover {
//  background-color: hsl(134, 41%, 85%);
//}

.tabfoot_title {
  width: 100%;
  font-weight: 500;
  font-size: 14px;
  line-height: 17px;
  padding-top: 9px;
  text-align: center;
}

.third-step-objects {
  width: 100%;
  background: inherit;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  text-align: center;
  justify-content: center;
}

.second-step-objects {
  width: 100%;
  background: inherit;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  text-align: center;
  justify-content: flex-start;
  min-height: 225px;
}

.second-step-object {
  margin-top: 24px;
  margin-left: auto;
  margin-right: auto;
  min-height: 100%;

  .structure-object {
    display: flex;
    flex-direction: row;
    margin-top: 24px;
  }

  .structure-object:last-child {
    margin-bottom: 24px;
  }
}

.first-step-objects {
  width: 100%;
  background: inherit;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  justify-content: center;
}

hr {
  border: none; /* Убираем границу для браузера Firefox */
  width: 100%;
  height: 1px;
  margin-top: 10px;
  background: #dde4ee;
  color: #778a9c;
}

.third-description {
  margin-right: auto;
}

.description-steps {
  margin-top: 10px;

  height: 17px;
  display: flex;
  align-items: center;
  text-align: center;

  font-weight: 500;
  font-size: 14px;
  line-height: 17px;

  color: #778a9c;
}

.small-point {
  width: 6px;
  height: 6px;
  border-radius: 3px;
  background-color: #c3cbd7;
}

.ellipsis {
  display: flex;
  width: 22px;
  height: 6px;
  margin-bottom: 20px;
  justify-content: space-between;
}

.step {
  width: 40px;
  height: 40px;
  border-radius: 50%;

  font-weight: 500;
  font-size: 24px;
  line-height: 29px;
  display: flex;
  align-items: center;
  text-align: center;
  justify-content: center;

  color: #c3cbd7;
  background: #f8f9fb;
  border: 2px solid #e8e8f3;
}

.steps {
  margin-top: 12px;
  width: 286px;
  height: 70px;
  display: flex;
  align-items: center;
  text-align: center;
  justify-content: space-between;

  .first {
    width: 120px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;

    .first-step {
      margin-bottom: 10px;
    }

    .first-description {
      font-style: normal;
      font-weight: 500;
      font-size: 12px;
      line-height: 15px;
      display: flex;
      align-items: center;
      text-align: center;
      color: #778a9c;
    }

    .active {
      .step {
        background: #2ec3fb;
        border-color: #2ec3fb;
        color: #ffffff;
      }

      .second-description {
        color: #778a9c !important;
      }
    }

    &.done {
      .step {
        background: #00c484;
        border-color: #00c484;
        color: #ffffff;
      }
    }
  }

  .second {
    width: 120px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;

    .second-step {
      margin-bottom: 10px;
    }

    .second-description {
      font-style: normal;
      font-weight: 500;
      font-size: 12px;
      line-height: 15px;
      display: flex;
      align-items: center;
      text-align: center;
      color: #a8b2bd;
    }
  }
}

.active {
  .step {
    background: #2ec3fb;
    border-color: #2ec3fb;
    color: #ffffff;
  }

  .second-description {
    color: #778a9c !important;
  }
}

.title {
  width: 368px;
  height: 38px;

  font-style: normal;
  font-weight: 500;
  font-size: 16px;
  line-height: 20px;
  display: flex;
  align-items: center;
  text-align: center;
  justify-content: center;

  color: #4a627a;
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

  width: 468px;
  min-height: 392px;
  height: auto;

  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;

  background: #f7f8fa;
  box-shadow: 0px 2px 6px rgba(0, 0, 0, 0.25);

  .btn_icon2 {
    position: absolute;
    top: 0;
    left: -29px;
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
    min-height: 392px;
    height: auto;

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

option.hide {
  color: rgb(170, 170, 170);
}

.hide_minus {
  opacity: 0;
}

.hide_plus {
  opacity: 0;
}
</style>

<style lang="scss">
.first-step-object {
  position: relative;
  margin-top: 24px;
  height: 24px;
  width: 444px;
  background: inherit;

  border: 1px solid #9098af;
  border-radius: 4px;

  font-size: 12px;
  line-height: 15px;

  color: #778a9c;

  outline: none;
  cursor: pointer;

  input {
    width: 100%;
    height: 100%;
    outline: none;
    border-radius: 4px;
    border: none;
    background: #f7f8fa;
    padding: 0 5px;
    //cursor: initial;
    transition: 0.1s;
  }

  input + label {
    position: absolute;
    top: -20px;
    left: 6px;
    transition: all 0.1s;
    opacity: 1;
    background: #f7f8fa;

    transform: translateY(calc(50% + 2px));
  }

  input:placeholder-shown + label {
    opacity: 0;
    transform: translateY(100%);
  }

  input:focus + label {
    opacity: 1;
    transform: translateY(calc(50% + 2px));
    color: #00c484;
  }

  input:focus:placeholder-shown {
    -webkit-text-fill-color: transparent;
  }
}
</style>

