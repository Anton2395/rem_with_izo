<template>
  <div class="overlay">
    <div class="modal-created">
      <div class="del-body">
        <div class="del-name">Удаление объекта</div>
        <div class="name-object">{{clientObject.name_object}}</div>
      </div>
      <div class="del-btn">
        <div
            class="btn left"
            @click="$parent.$emit('changeshowDelObject')"
         >Отмена
        </div>
        <div class="btn right" @click="callDelClientsObject">Удалить</div>
      </div>
      <button class="btn_icon2">
        <div
            class="btn-bg"
            @click="$parent.$emit('changeshowDelObject')"
         >
        </div>
      </button>
    </div>
  </div>
</template>

<script>

  import { mapActions } from "vuex";

export default {
  name: "DelObject",
  props: ['clientObject'],

  methods: {
    ...mapActions("settingsGlobal", {
      delClientsObject: "delClientsObject"
    }),

    callDelClientsObject() {
      this.delClientsObject();
      this.$parent.show_info_DeleteCustomObject();
      this.$parent.$emit('changeshowDelObject');
    },
  },
}
</script>

<style lang="scss" scoped>
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

  width: 400px;
  height: auto;

  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;

  background: #F7F8FA;
  box-shadow: 0px 2px 6px rgba(0, 0, 0, 0.25);

  .del-body {
    padding-top: 24px;
    margin-bottom: 24px;
    .del-name,
    .name-object {
      font-weight: 500;
      font-size: 16px;
      line-height: 20px;

      color: #4B6075;
    }
  }

  .del-btn {
    width: 100%;
    height: 36px;
    display: flex;


    .btn {
      width: 234px;
      height: 36px;

      padding-top: 12px;
      padding-bottom: 12px;

      text-align: center;
      font-weight: 500;
      font-size: 12px;
      line-height: 15px;

      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;

      &.left {
        display: flex;
        align-items: center;
        text-align: center;

        color: #004085;
        background: #CCE5FF;

        &:hover {
          box-shadow: 0px 0px 6px rgba(0, 0, 0, 0.25);
        }
      }

      &.right {
        display: flex;
        align-items: center;
        text-align: center;

        color: #721C24;
        background: #F7DCDF;

        &:hover {
          box-shadow: 0px 0px 6px rgba(0, 0, 0, 0.25);
        }
      }
    }
  }

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
}

</style>
