<template>
  <div class="overlay" v-on:click="$emit('changeShow')">
    <div class="aboutuser" v-on:click.stop="noChange">
      <button class="btn_close">
        <img 
          v-on:click="$emit('changeShow')"
          src="../assets/svg/clear_24px.svg"
          alt
        />
      </button>
      <div>
        <h2>{{ user.company }}</h2>
      </div>
      <div>
        <p>
          <span>Приветствую,</span>
          {{ user.name }}
        </p>
      </div>
      <div>
        <p>
          <span>Доступ уровень -</span>
          {{ user.accessLevel }}
        </p>
      </div>
      <div>
        <p>
          <span>Текущее время -</span>
          {{ currenttime }}
        </p>
      </div>
      <hr />

      <nuxt-link to="/Login" class="logout" custom v-slot="{ navigate }">
        <button @click="navigate">
          <IconifyIcon
            icon="baselineEdit"
            :style="{ color: '#4B6075', fontSize: '24px' }"
          />
          <div class="userid">Редактировать профиль</div>
        </button>
      </nuxt-link>
      <div class="logout" @click="logout">
        <IconifyIcon
          icon="outlineOpenInBrowser"
          :style="{ color: '#4B6075', fontSize: '24px' }"
          :rotate="1"
        />
        <div class="userid">Выйти из профиля</div>
      </div>
    </div>
  </div>
</template>
<script>
import { mapGetters } from "vuex";
import { time } from "highcharts";

export default {
  computed: {
    ...mapGetters("users", {
      user: "curentUser",
    }),
    currenttime() {
      let ctime = new Date();

      let hours = ctime.getHours();
      let minutes = ctime.getMinutes();
      return hours + ":" + minutes;
    },
  },
  methods: {
    noChange() {
      1 + 1;
    },
    async logout() {
      try {
        await this.$auth.logout();
      } catch (e) {
      
      }
    },
  },
};
</script>

<style scoped>
.overlay {
  width: 100vw;
  height: 100vh;
  background-color: rgba(0, 0, 0, 0.062);
  z-index: 100;
  position: absolute;
  top: 0;
  right: 0;
}
.aboutuser {
  width: 350px;
  height: 212px;
  padding: 0 12px;
  background-color: #f7f8fa;

  z-index: 25;

  position: absolute;
  top: 50px;
  right: 0;
  box-shadow: 0px 2px 6px rgba(0, 0, 0, 0.25);
}

.btn_close {
  cursor: pointer;
  position: absolute;
  top: -7px;
  right: 353px;
}
.img:hover {
  background: center no-repeat url("~assets/svg/iconControlModal.svg");
}
div {
  padding: 6px 0;
}

button {
  margin: 7px 0;
  padding: 0;
}
p {
  font-size: 14px;
  cursor: default;

  /* padding: 1px 0; */
}

h2 {
  font-size: 18px;
  cursor: default;

  /* padding: 1px 0; */
}

hr {
  margin: 12px;
}
p,
h2 {
  color: #4b6075;
}
p span {
  color: #000;
}

.logout {
  border: none;
  background: none;
  outline: none;
  text-align: left;
  /* vertical-align: middle;  */
  /* padding: 5px; */
  width: 100%;
  display: flex;
  flex-direction: row;
  align-items: center;
}

button {
  cursor: pointer;
  background: none;
  border: none;
  /* border-radius: 50%; */
  display: flex;
  /* justify-content: baseline; */
  outline: none;
}

img {
  align-self: center;
}

.userid {
  font: 12px sans-serif;
  padding: 6px 10px;

  align-self: center;
}

/* .aboutuser > p,h2{
     padding: 2px;
} */
</style>
