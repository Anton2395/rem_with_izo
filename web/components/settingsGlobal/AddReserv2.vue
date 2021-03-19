<template>
  <div class="overlay" @click="$parent.$emit('closeAddForm', 'addReserv2')">
    <div class="modal-created" v-on:click.stop="">
      <div class="attention-close">
        <div class="attention-header">
          <div class="title-header">Добавление резерв2</div>
        </div>
        <div class="attention-body">
          <div class="first-step-object">
            <input
              v-model.lazy="form.name"
              placeholder="Название резерва2"
              autocomplete="off"
              id="name"
              type="text"
            />
            <label for="name">Название резерва2</label>
          </div>
          <select
            type="text"
            v-model="form.reserve1"
            v-if="
              this.clientsObject.currentStructureObject.filter(
                (item) => item.id === 1
              ).length
            "
          >
            <option value="0" disabled>Название резерва1</option>
            <option :value="item.id" :key="item.id" v-for="item in reserves1">
              {{ item.name }}
            </option>
          </select>
        </div>
        <div class="attention-footer">
          <button class="btn-center" @click="save">Применить</button>
        </div>
      </div>
      <button class="btn_icon2">
        <div
          class="btn-bg"
          @click="$parent.$emit('closeAddForm', 'addReserv2')"
        ></div>
      </button>
    </div>
  </div>
</template>

<script>
import { mapActions, mapGetters } from "vuex";

export default {
  name: "AddReserv2",
  props: ["id"],
  mounted() {
    document.addEventListener("keyup", this.escapeKeyListener);
  },
  destroyed() {
    document.removeEventListener("keyup", this.escapeKeyListener);
  },
  created() {
    if (this.id) {
      let reserv2 = this.reserves2.filter((item) => item.id === this.id);
      this.id = reserv2[0].id;
      this.form.name = reserv2[0].name;
      this.form.reserve1 = reserv2[0].reserv1_id;
    }
  },
  data() {
    return {
      form: {
        name: "",
        reserve1: 0,
      },
    };
  },
  methods: {
    escapeKeyListener: function (evt) {
      if (evt.keyCode === 27) {
        this.$parent.$emit("closeAddForm", "addReserv2");
      }
      if (evt.keyCode === 13) {
        this.save();
      }
    },
    ...mapActions("settingsGlobal", {
      updateReserve2: "updateReserve2",
    }),
    save() {
      let data = {
        id: this.id,
        name: this.form.name,
        reserv1_id: this.form.reserve1,
      };

      for (let key in data)
        if ((data[key] === "" || data[key] === 0) && key !== "id") {
          // debugger;
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

          this.$parent.show_warning_NecessaryFullField();
          // this.$parent.$emit('showAttentionInput');
          return;
        }

      this.updateReserve2(data);
      this.$parent.show_info_RowUpdate();
      this.$parent.$emit("closeAddForm", "addReserv2");
    },
  },
  computed: {
    ...mapGetters("settingsGlobal", {
      reserves1: "reserves1",
      reserves2: "reserves2",
      clientsObject: "clientsObject",
    }),
  },
};
</script>
<style lang="scss" scoped>
.modal-created input {
  color: #49617b !important;
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
