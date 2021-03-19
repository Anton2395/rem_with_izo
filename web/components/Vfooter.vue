<template>
    <div class="wraper_footer">

      <div
        class="headTable"
        v-on:click="changeShow"
        v-bind:class="dataHead.status"
      >
        <IconifyIcon
          :class="[{'arrow-up': !showTable},{'arrow': true}, {'left-arrow': true}, {'arrow-down':true}]"
          icon="baselineKeyboardArrowDown"
          :style="{fontSize: '24px'}" />


        {{ dataHead.title }}
        <IconifyIcon
          :class="[{'arrow-up': !showTable},{'arrow': true}, {'right-arrow': true}, {'arrow-down':true}]"
          icon="baselineKeyboardArrowDown"
          :style="{fontSize: '24px'}" />


      </div>

    <transition name="slide">

      <div class="bodyTable" v-show="showTable">
        <table>
          <tbody>
            <tr
              v-for="(msg, index) in DevMsgs"
              :key="index"
              v-bind:class="msg[0]"
            >
              <td>
                {{ index }}
              </td>
              <td>
                {{ msg[2] }}
              </td>
              <td>
                {{ msg[0] }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>

    </transition>

    </div>
</template>
<script>
import { mapGetters } from "vuex";

export default {
  data() {
    return {
      showTable: false,
    };
  },
  computed: {
    ...mapGetters("Messages", {
      DevMsgs: "currentDevMessages",
    }),

    dataHead() {
      let statusDev = "ok";
      let allDev = [];
      let dngDev = [];
      let okDev = null;

      for (const key in this.DevMsgs) {
        if (this.DevMsgs[key][0] == 0) {
          dngDev.push(this.DevMsgs[key][0]);
          this.DevMsgs[key][0] = "dng";
        } else {
          okDev++;
          this.DevMsgs[key][0] = "ok";
        }
        allDev++;
      }
      if (dngDev.length != 0) {
        statusDev = "dng";
      } else {
        statusDev = "ok";
      }

      return {
        title: `${okDev} из ${allDev} устройства в сети`,
        // title: `Устройства в сети`,
        status: statusDev,
      };
    },
  },

  mounted() {
    this.$store.dispatch("Messages/getCurrentDevMessages");
  },

  methods: {
    changeShow: function () {
      this.showTable = !this.showTable;
    },
  },
};
</script>

<style scoped>
/* анимация */
.slide-enter-active,
.slide-leave-active {
  transition: all 1s;
}
.slide-enter-active {
  max-height: 40vh;
}
.slide-enter,
.slide-leave-active {
  max-height: 0;
}
.slide-leave {
  max-height: 40vh;
}
/* анимация */
.wraper_footer {
  z-index: 10;
  width: 100%;
  position: absolute;
  bottom: 0;
  left: 0;
}

.headTable {
  background: #000;

  font-size: 12px;
  font-weight: 500;
  width: 100%;
  height: 24px;
  text-align: center;

  display: flex;
  align-items: center;
  text-align: center;

  transition-property: all;
  transition-duration: 0.3s;
}

.arrow {
  transition: 0.3s;
}

.left-arrow {
  margin-right: auto;
  margin-left: 20px;
}

.right-arrow {
  margin-left: auto;
  margin-right: 20px;
}

.arrow-up {
  transform: matrix(1, 0, 0, -1, 0, 0);
}

.bodyTable {
  width: 100%;
  max-height: 40vh;
  overflow: auto;
  transition: 0.2s;
}

table {
  width: 100%;
  border-collapse: collapse;
}

td {
  background: none;
  padding-left: 20px;
  font-size: 12px;
  font-weight: 600;
  line-height: 15px;
  width: auto;
  height: 48px;

  color: #155724;
}

.dng {
  background: #f7dcdf;
  color: #721c24;
}
.alert {
  background: #fff3cd;
  color: #856404;
}
.ok {
  background: #d4edda;
  color: #155724;
}
</style>
