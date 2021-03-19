<template>
  <transition name="fade">
    <div v-show="showAlert" v-if="this.currentAlert" class="boxAlert" v-bind:class="alertMsg.status">
      <div class="alertMsg">{{ alertMsg.msg }}</div>
      <button v-on:click="changeShow">
        <!-- <button v-on:click="$emit('changeShow')"> -->

        <img src="../assets/svg/clear.svg" alt="" />
      </button>
    </div>
  </transition>
</template>
<script>
import { mapGetters } from "vuex";

export default {
  data() {
    return {
      showAlert: true
    };
  },

  computed: {
    ...mapGetters("Messages", {
      currentAlert: "currentAlert"
    }),
    alertMsg: function() {
      return this.currentAlert;
    }
  },
  methods: {
    changeShow() {
      this.showAlert = !this.showAlert;
      //  if (this.showAlert) {
      //  setTimeout(() => {
      //         this.showAlert = !this.showAlert
      //     }, 5000);
      //  }
    }
  }
};

function randomInteger(min, max) {
  let rand = min + Math.random() * (max + 1 - min);
  return Math.floor(rand);
}
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
.boxAlert {
  display: flex;
  justify-content: space-between;
  width: 1680px;

  z-index: 15;
  position: absolute;
  top: 60px;
  left: 180px;
}
.alertMsg {
  margin: auto;
}
button {
  background: none;
  border: none;

  justify-content: baseline;
  outline: none;
}

.dng {
  background: #f7dcdf;
  color: #721C24;
}

.alert {
  background: #fff3cd;
}

.ok {
  background: #d4edda;
}
</style>
