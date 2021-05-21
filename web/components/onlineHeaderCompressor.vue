<template>
  <div>
    <div class="title-panel">
      <!-- <div class="headMenu">
        <select style=" outline: none;">
          <option>Компрессорная установка 1</option>
        </select>
      </div> -->
    </div>
    <!-- 
    <VchartBox
      v-show="visibleVBox"
      @changeShow="visibleVBox = false"
      :content="content"
    ></VchartBox> -->
  </div>
</template>

<script>
import { mapGetters } from "vuex";
import { mapActions } from "vuex";

import VchartBox from "@/components/VchartBox";

export default {
  name: "onlineHeader",
  data() {
    return {};
  },
  computed: {
    ...mapGetters("compressor", {
      selectedshops: "selectedshops",
      factories: "factories",
      shops: "shops",
      activeshop: "activeshop",
    }),

   
    content: function () {
      return {
        // fist: this.fistDate,
        // last: this.lastDate,
        title: "Настройка отображения графиков",
        btnLeft: "Экспорт",
        btnRight: "Обновить",
        selectLeft: "Графики - все подряд",
        selectRight: "Графики - группировать по группам",
      };
    },
  },

  getters: {
    factories(state) {
      return state.factories;
    },
  },

  components: {
    VchartBox: VchartBox,
  },
};
</script>

<style lang="scss" scoped>
.title-panel {
  background-repeat: no-repeat;
  border-bottom: 1px solid hsl(220, 33%, 88%);
  background: #f9fafc;
  z-index: 4;
  font-weight: 500;
  font-size: 14px;
  line-height: 17px;
  align-items: center;
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  justify-content: space-between;
  width: 100%;
  /* width: 1780px; */
  /* left: 120px; */
  left: 0;
  height: 48px;

  position: absolute;
  top: 49px;

  .headMenu {
    display: flex;
    margin-left: 150px;
    margin-right: auto;
    outline:none;
  }
}

.sub-panel {
  background-repeat: no-repeat;
  border-bottom: 1px solid hsl(220, 33%, 88%);
  /* background: #f9fafc; */

  font-weight: 500;
  font-size: 14px;
  line-height: 17px;

  align-items: center;

  display: flex;
  flex-direction: row;
  flex-wrap: wrap;

  justify-content: flex-start;
  /* width: 1640px; */
  /* left: 260px; */
  margin-left: 15%;

  width: 85%;
  height: 48px;

  position: absolute;
  top: 96px;
  left: 0;

  .subMenu {
    width: 140px;
    height: 48px;
    font-weight: 500;
    font-size: 10px;
    line-height: 12px;
    display: flex;
    align-items: center;
    text-align: center;
    outline: none;
    color: #49617b;

    position: relative;

    .subMenu_item {
      text-decoration: none;

      display: block;
      transition: 0.3s;
    }

    .subMenu_item:hover:before {
      content: "";
      width: 100%;
      border-bottom: 1px solid #2dc2fa;
      position: absolute;
      bottom: 0;
      left: 0;
    }
    .subMenu_item.actived:before {
      content: "";
      width: 100%;
      border-bottom: 1px solid #2dc2fa;
      position: absolute;
      bottom: 0;
      left: 0;
    }
  }
}
select {
  outline: none;
}
</style>
