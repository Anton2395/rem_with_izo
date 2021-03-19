<template>
  <div class="overlay">
    <div class="modal-created">
      <div class="variables">
        <div class="variables-header">
          <div class="title-header">Добавление переменных</div>
        </div>
        <div class="variables-body">
          <div class="variables-body-box">
            <select type="text" v-model="form.connect">
              <option value="" disabled>Название соединения</option>
              <option :value="item.connect" v-for="item in connections">{{ item.connect }}</option>
            </select>
          </div>
          <div class="variables-body-box-row"></div>
        </div>
        <div class="variables-footer">
          <button class="btn-center" @click="save">Применить</button>
        </div>
      </div>
      <button class="btn_icon2">
        <div class="btn-bg" @click="$parent.$emit('showAddVariablesConnect', false)"></div>
      </button>
    </div>
  </div>
</template>

<script>
import {mapActions, mapGetters} from "vuex";

export default {
  name: "AddVariablesConnect",
  data() {
    return {
      form: {
        connect: "",
      },
    }
  },
  methods: {
    ...mapActions('settingsGlobal', {
      updateVariablesConnect: 'updateVariablesConnect',
    }),
    save() {
      let data = {
        connect: this.form.connect,
        name: "Давление в трубе, МПа",
        limitMinWarn: 0,
        limitMaxWarn: 2000,
        limitMinСrash: 0,
        limitMaxСrash: 1600,
        limitSpead: 400,
      }

      if (!this.form.connect) {
        this.$parent.$emit('showAttentionInput');
        return;
      }

      this.updateVariablesConnect(data);
      this.$parent.$emit('showAddVariablesConnect', false)
    }
  },
  computed: {
    ...mapGetters('Messages', {
      connections: 'currentDevMessages',
    }),
  }
}
</script>

<style lang="scss" scoped>
.modal-created input {
  color: #49617B !important;
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

  background: #F7F8FA;
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
        color: #4B6075;
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
        margin-bottom: 24px;

        font-size: 12px;
        line-height: 15px;

        select, option {
          width: 376px;
          height: 24px;

          margin-bottom: 12px;
          padding: 3px 6px;

          display: flex;
          align-items: center;

          border: 1px solid #9098AF;
          box-sizing: border-box;
          border-radius: 4px;

          font-weight: normal;
          font-size: 12px;

          color: #9098AF;
          background: #F7F8FA;

          outline: none;
        }

        input {
          width: 376px;
          height: 24px;

          margin-bottom: 12px;
          padding: 3px 9px;

          display: flex;
          align-items: center;

          border: 1px solid #9098AF;
          box-sizing: border-box;
          border-radius: 4px;
          background: #F7F8FA;

          font-weight: normal;
          font-size: 12px;

          color: #9098AF;

          outline: none;
        }

        ::placeholder {
          font-weight: normal;
          font-size: 12px;

          color: #9098AF;
        }
      }

      input {
        width: 376px;
        height: 24px;

        padding: 3px 6px;

        display: flex;
        align-items: center;

        border: 1px solid #9098AF;
        box-sizing: border-box;
        border-radius: 4px;
        background: #F7F8FA;

        outline: none;
      }

      ::placeholder {
        font-weight: normal;
        font-size: 12px;

        color: #9098AF;
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

        color: #0B2E13;
        background: #D4EDDA;;

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
