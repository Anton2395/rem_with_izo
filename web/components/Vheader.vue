<template>
  <div class="wraper_header">
    <div class="wraper">
      <div>
        <nuxt-link to="/" custom v-slot="{ navigate }" class="logo">
          <button @click="navigate">
            <img src="~/assets/svg/logo3.svg" alt />
          </button>
        </nuxt-link>
      </div>

      <div class="headMenu">
        <div v-for="tab in headerTabs" :key="tab.name">
          <nuxt-link
            :to="`/${tab.link}`"
            custom
            v-slot="{ navigate }"
            class="headMenu_item btn_icon"
            :class="{ active: currentTabHeader === tab.name }"
          >
            <button @click="navigate" role="button">
              {{ tab.name }}
            </button>
          </nuxt-link>
        </div>
      </div>

      <div>
        <nuxt-link
          to="/settingsGlobal"
          custom
          v-slot="{ navigate }"
          class="btn_icon btn-header"
        >
          <!-- <img src="~/assets/svg/settings_24px.svg" alt /> -->
          <button @click="navigate">
            <IconifyIcon icon="roundSettings" :style="{ fontSize: '29px' }" />
          </button>
        </nuxt-link>
      </div>
      <div>
        <button v-on:click="changeShowMsg" class="btn_icon btn-header">
          <!-- <img v-bind:class="dataHead.fill" src="~/assets/svg/error_24px.svg" alt /> -->
          <IconifyIcon
            icon="errorWarningFill"
            :style="{ fontSize: '29px' }"
            v-bind:class="dataHead.fill"
          />
        </button>
      </div>
      <div>
        <button
          v-on:click="changeShowUser"
          class="btn_icon btn_user btn-header"
        >
          <IconifyIcon
            icon="baselineAccountCircle"
            :style="{ fontSize: '24px' }"
          />
          <div class="userid">{{ user.name }}</div>
          <IconifyIcon
            icon="baselineKeyboardArrowDown"
            :style="{ fontSize: '24px' }"
          />
        </button>
      </div>
    </div>
    <transition name="fade">
      <VuserBox v-show="showUser" v-on:changeShow="changeShowUser"></VuserBox>
    </transition>
    <transition name="fade">
      <VmsgBox v-show="showMsg" v-on:changeShow="changeShowMsg"></VmsgBox>
    </transition>

    <Alert v-show="showAlert" v-on:changeShow="changeShowAlert"></Alert>

    <div class="headMsg" v-bind:class="dataHead.status"></div>
  </div>
</template>
<script>
import VuserBox from "@/components/VuserBox";
import VmsgBox from "@/components/VmsgBox";
import Alert from "@/components/Alert";

import { mapGetters } from "vuex";

export default {
  components: {
    VuserBox,
    VmsgBox,
    Alert,
  },

  data() {
    return {
      headerTabs: [
        // { name: "HOME", link: "" },
        // { name: "OEE", link: "Charts" },
        // { name: "VIBRO", link: "vibro" },
        // { name: "PROFILER", link: "profiler" },
        // { name: "REPAIRS", link: "repairs" },
        // { name: "RECORDER", link: "recorder" }
        { name: "HOME", link: "" },
        { name: "OEE", link: "" },
        { name: "VIBRO", link: "" },
        { name: "PROFILER", link: "" },
        { name: "REPAIRS", link: "" },
        { name: "RECORDER", link: "recorder" },
      ],

      showUser: false,
      showMsg: false,
      showAlert: false,
    };
  },
  mounted() {
    this.$store.dispatch("users/setUserData");
  },
  computed: {
    ...mapGetters("users", {
      user: "curentUser",
      currentTabHeader: "currentTabHeader",
    }),
    ...mapGetters("Messages", {
      DevMsgs: "currentMessages",
    }),
    dataHead() {
      let statusDev = "ok";
      let alertDev = this.DevMsgs.filter((item) => item.status == "alert");
      let dngDev = this.DevMsgs.find((item) => item.status == "dng");

      if (dngDev !== undefined) {
        statusDev = "dng";
      } else if (alertDev !== undefined) {
        statusDev = "alert";
      }

      return { fill: statusDev + `fill`, status: statusDev };
    },
  },

  methods: {
    changeShowUser() {
      this.showUser = !this.showUser;
    },
    changeShowMsg() {
      this.showMsg = !this.showMsg;
    },
    changeShowAlert() {
      this.showAlert = !this.showAlert;
      //  if (this.showAlert) {
      //  setTimeout(() => {
      //         this.showAlert = !this.showAlert
      //     }, 5000);
      //  }
    },
  },
};
</script>

<style scoped>
/* анимация */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s;
}
.fade-enter, .fade-leave-to /* .fade-leave-active до версии 2.1.8 */ {
  opacity: 0;
}
/* анимация */

.headMsg {
  background: rgb(188, 226, 241);

  width: 6px;
  height: 93vh;
  z-index: 5;
  position: absolute;
  top: 50;
  right: 0;
}
.wraper_header {
  z-index: 10;
  height: 48px;
}

.wraper {
  background-repeat: no-repeat;
  box-shadow: 0px 2px 6px rgba(0, 0, 0, 0.25);
  background-color: #3f51b5;
  /* background-image: url("../assets/svg/logo3.svg"); */
  align-items: center;

  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  height: 48px;

  justify-content: flex-end;
  z-index: 10;
}

.headMenu {
  display: flex;
  flex-direction: row;
  margin-left: 50px;
  margin-right: auto;
}
.headMenu_item {
  color: #b0bec5;
  font-weight: 500;
  font-size: 16px;
  line-height: 20px;

  margin-right: 24px;
}

.headMenu_item:hover {
  cursor: pointer;
  color: #fff;
}
.headMenu_item.active {
  color: #fff;
}
.btn-header {
  color: #fff;
  cursor: pointer;
}
.btn_icon {
  background: none;
  border: none;

  display: flex;
  justify-content: baseline;
  outline: none;
}

.btn_user {
  /*margin-left: 24px;*/
}

.logo {
  /* background: #3F51B5; */
  border: none;
  fill: #3f51b5;
  display: flex;
  justify-content: baseline;
  padding: 0;
  outline: none;
  margin-left: 12px;
}

img {
  align-self: center;
}

.userid {
  font-size: 14px;
  line-height: 17px;
  display: flex;
  align-items: center;
  text-align: center;

  padding: 0 10px;
  color: #fff;
  align-self: center;
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

/* заливка иконок */
.dngfill {
  color: #f7dcdf;
}

.alertfill {
  color: #fff3cd; /* filter: url(#filter_alert); */
}

.okfill {
  color: #d4edda;
}
</style>
