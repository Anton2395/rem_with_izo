<template>
  <div class="period">
    <button
        v-on:click="setPeriod(0)"
        class="btn text"
        :class="{active: periodActive[0]}"
    >месяц
    </button>
    <button
        v-on:click="setPeriod(1)"
        class="btn text"
        :class="{active: periodActive[1]}"
    >сутки
    </button>
    <button
        v-on:click="setPeriod(2)"
        class="btn text"
        :class="{active: periodActive[2] || periodActive[3] || periodActive[4]}"
    >смена
    </button>
    <button
        v-on:click="setPeriod(2)"
        class="btn num"
        :class="{active: periodActive[2]}"
    >1
    </button>
    <button
        v-on:click="setPeriod(3)"
        class="btn num"
        :class="{active: periodActive[3]}"
    >2
    </button>
    <button
        v-on:click="setPeriod(4)"
        class="btn num"
        :class="{active: periodActive[4]}"
    >3
    </button>
  </div>
</template>

<script>
export default {
  name: "period",

  data() {
    return {
      periodActive: [false, true, false, false, false],
    }
  },
  props: ['title', 'end', 'isType1', 'isType2'],
  created() {
    this.setPeriod(1);
  },
  methods: {
    setPeriod(index) {
      let arr = [false, false, false, false, false];
      arr[index] = true;
      this.periodActive = arr;
      let isType = 'shift';
      let id = 0;
      if (index === 0)
        isType = 'month';
      else if (index === 1)
        isType = 'day';
      else if (index === 2 || index === 2)
        id = 1;
      else if (index === 3)
        id = 2;
      else if (index === 4)
        id = 3;

      let option;
      if (this.end)
        option = {
          id2: id,
          isType2: isType,
          title: this.title,
          end: 1,
        }
      else
        option = {
          id1: id,
          isType1: isType,
          title: this.title,
          end: 0,
        }

      this.$parent.$emit('setPeriod', option);
    }
  },
  watch: {
    isType1: function(newValue) {
      if(newValue === 'month')
        this.setPeriod(0);
      else if(newValue === 'day')
        this.setPeriod(1);
      else
        this.setPeriod(2);
    },
    isType2: function(newValue) {
      if(newValue === 'month')
        this.setPeriod(0);
      else if(newValue === 'day')
        this.setPeriod(1);
      else
        this.setPeriod(2);
    }
  }
}
</script>

<style lang="scss" scoped>

.period {
  display: flex;
  justify-content: center;
  align-items: center;

  .btn {
    cursor: pointer;
    outline: none;
    height: 23px;

    display: flex;
    justify-content: center;
    align-items: center;

    margin-right: 12px;
    padding: 0 6px;

    border: 1px solid #ECEDF4;
    border-radius: 3px;
    background: #FFFFFF;

    font-weight: 500;
    font-size: 12px;
    color: #42435F;

    &:hover {
      border: 1px solid #272848;
    }
  }

  .text {
    width: 52px;
  }

  .btn.text:nth-child(3) {
    margin-right: 6px;
  }

  .num {
    width: 42px;
    background: #FFFFFF;
    margin-right: 6px;
  }

  .active {
    background: #272848;
    color: #BFC0C9;
    text-align: center;
  }

  button:last-child {
    margin-right: 0;
  }
}

.comparison-module {
  .chart-content {
    .content-box {
      .period {
        .btn.text {
          margin-right: 6px;
        }
        button:last-child {
          margin-right: 3px;
        }
      }
    }
  }
}

</style>
