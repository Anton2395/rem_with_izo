<template>
  <!--  <div class="attention-close" v-show="showTable">-->
  <div class="popup">
    <div class="attention-close">
      <div class="attention-header">
        <IconifyIcon icon="warningStandardLine" width="68" height="58" :style="{ color: 'white' }"/>
      </div>
      <div class="attention-body">
        <div class="title">Внимание!</div>
        <div class="subtitle">Для создания объекта должны быть заполнены все строки</div>
      </div>
      <div class="attention-footer">
        <button class="btn-close" @click="$parent.$emit('closeAttentionInput')">Закрыть</button>
      </div>
    </div>
    <div class="popup-overlay"></div>
  </div>
</template>

<script>
export default {
  name: "AttentionInput",
}
</script>

<style lang="scss" scoped>
.popup {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 111;
  width: 100%;
  height: 100%;
}

.popup-overlay {
  width: 100%;
  height: 100%;
  position: absolute;
  top: 0;
  left: 0;
  z-index: 1;
}

.attention-close {
  position: absolute;
  top: 50%;
  left: 50%;
  z-index: 100;
  transform: translate(-50%, -50%);
  width: 298px;
  height: 258px;
  display: flex;
  flex-direction: column;
  align-items: center;
  background: #FFFFFF;
  box-shadow: 2px 4px 4px rgba(0, 0, 0, 0.25);
  border-radius: 18px;

  .attention-header {
    width: 100%;
    height: 96px;
    display: flex;
    justify-content: center;
    align-items: center;
    border-radius: 18px 18px 0px 0px;
    background-color: #FFDC75;
  }

  .attention-body {
    padding: 0 24px;
    margin-bottom: 17px;
    text-align: center;

    .title {
      margin-top: 18px;
      margin-bottom: 17px;
      font-weight: 500;
      font-size: 24px;
      line-height: 29px;
      color: #000000;
    }

    .subtitle {
      font-weight: normal;
      font-size: 14px;
      line-height: 17px;
      color: #000000;
    }
  }

  .attention-footer {
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 0 24px 12px 24px;

    .btn-close {
      width: 202px;
      height: 36px;

      padding: 6px 16px;

      font-weight: 500;
      font-size: 18px;
      text-transform: uppercase;

      color: #FFDC75;
      outline: none;
      cursor: pointer;

      background: #FFFFFF;
      border: 1px solid #FFDC75;
      border-radius: 6px;

      &:hover {
        color: #FFFFFF;
        background: #FFDC75;
        border: 1px solid #FFDC75;
        border-radius: 6px;
        transition: 0.2s;
      }
    }
  }
}
</style>
