<template>
  <div class="resul">
    <div
        :class="{'result-ok' : change > 0, 'result-minus' : change < 0, 'result-null' : change === 0}"
    >
      <div class="arrow"></div>
      <div class="index-res">{{ change }}%</div>
    </div>
  </div>
</template>

<script>
export default {
  name: "DataIndicator",
  props: ['change'],
  methods: {},
}
</script>

<style lang="scss">
.resul {
  .result-ok {
    display: flex;
    color: #7CD420;

    .arrow {
      width: 7px;
      height: 12px;
      background-image: url("~assets/img/arrow_green.png");
      background-repeat: no-repeat;
      background-position: bottom;
      background-size: 100%;
    }

    .index_res {
      margin-left: 2px;
      font-weight: 500;
      font-size: 14px;
      line-height: 14px;
    }
  }
}

.resul {
  .result-ok {
    font-family: "Montserrat", -apple-system, BlinkMacSystemFont, "Segoe UI",
    Roboto, "Helvetica Neue", Arial, sans-serif;
    font-style: normal;
    font-weight: 500;
    font-size: 14px;
    line-height: 14px;
    color: #7CD420;
  }

  .result-minus {
    font-family: "Montserrat", -apple-system, BlinkMacSystemFont, "Segoe UI",
    Roboto, "Helvetica Neue", Arial, sans-serif;
    font-style: normal;
    font-weight: 500;
    font-size: 14px;
    line-height: 14px;
    color: #F3345D;
  }

  .result-null {
    font-family: "Montserrat", -apple-system, BlinkMacSystemFont, "Segoe UI",
    Roboto, "Helvetica Neue", Arial, sans-serif;
    font-style: normal;
    font-weight: 500;
    font-size: 14px;
    line-height: 14px;
    color: #96A2B0;
  }
}
</style>
