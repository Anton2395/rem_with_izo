<template>
  <div class="overlay" v-on:click="$emit('changeShow')">
    <div class="addGraph" v-on:click.stop="noChange">

      <div class="formHeader">
        <button class="btn_icon">
          <img v-on:click="$emit('changeShow')" src="~assets/svg/clear_24px.svg" alt />
        </button>
        <div class="title">Работа с графиками:</div>
      </div>

      <div class="form-body">
        <div class="addform">
          <input class="addform-style" type="text" placeholder="Добавить график">
          <div>+</div>
        </div>
      </div>

    </div>
  </div>
</template>

<script>
import { mapGetters } from "vuex";

export default {
name: "RAddChard",
  data() {
    return {
      showTable: false
    };
  },

  methods: {
    noChange() {
      1 + 1;
    }
  }
}
</script>

<style lang="scss" scoped>
.overlay {
  width: 100vw;
  height: 100vh;
  background-color: rgba(0, 0, 0, 0.062);
  z-index: 19;
  position: absolute;
  top: 0;
  right: 0;

  .addGraph {
    width: 724px;
    max-height: 92vh;
    padding: 0;
    background: #f7f8fa;
    box-shadow: 0px 2px 6px rgba(0, 0, 0, 0.25);

    z-index: 20;

    position: absolute;
    top: 50%;
    right: 50%;
    transform: translate(50%, 50%);

    display: flex;
    flex-direction: column;
    justify-content: flex-start;

    .formHeader {
      display: flex;
      justify-content: flex-start;
      width: 100%;
      margin-left: -35px;
      margin-bottom: 24px;

      .btn_icon {

        cursor: pointer;
        background: none;
        border: none;

        display: flex;
        justify-content: baseline;
        outline: none;
      }

      .title {
        padding-top: 6px;
        padding-left: 24px;
        padding-right: 6px;
        font-weight: 500;
        font-size: 16px;
        line-height: 20px;
        color: #4B6075;

      }
    }

    .form-body {
      padding-left: 6px;
      .addform {
        display: flex;
        align-items: center;
        margin-bottom: 12px;

        input {
          outline: none;
        }

        input::placeholder {
          font-family: "Montserrat", -apple-system, BlinkMacSystemFont, "Segoe UI",
          Roboto, "Helvetica Neue", Arial, sans-serif;
          font-style: normal;
          font-weight: normal;
          font-size: 12px;
          line-height: 15px;
          color: #778A9C;
        }

        .addform-style {
          width: 628px;
          height: 24px;
          border: 1px solid #9098AF;
          border-radius: 4px;
          margin-right: 8px;
          padding: 3px 6px;
        }
      }
    }
  }
}
</style>
