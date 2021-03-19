<template>
  <div class="wrapper">
    <div class="titletext">
      Специально для вас!
      <!--<img src="@/assets/svg/TitleHello.svg" alt="symbol">-->
    </div>

    <div class="titlelogo">
      <img src="../assets/svg/logoHW.svg" alt="symbol"/>
    </div>

    <form @submit.prevent="userLogin">
      <div class="input">
        <input type="text" v-model="login.username" class="input-round" placeholder="Логин" id="login"
               autocomplete="off"/>
        <IconifyIcon icon="bxUser" :style="{fontSize: '24px'}" class="input-icon"/>
      </div>
      <div class="input">
        <input type="password" v-model="login.password" class="input-round" placeholder="Пароль" id="password"
               autocomplete="off"/>
        <IconifyIcon icon="lockPasswordLine" :style="{fontSize: '24px'}" class="input-icon"/>
      </div>

      <div class="input btn">
        <button class="btn-round">Вход</button>

      </div>
    </form>
    <div class="button-footer">
      <button class="imgemail btn-circle"></button>
      <button class="imgesite btn-circle"></button>
    </div>
  </div>
</template>

<script>
export default {
  layout: "empty",
  data() {
    return {
      login: {
        username: '',
        password: ''
      }
    }
  },
  methods: {
    async userLogin() {
      try {
        await this.$auth.loginWith('local', {data: this.login});
         this.$router.push({ path: '/' })
      } catch (err) {
        this.open4();
      }
    },
     open4() {
        this.$notify.error({
          title: 'Ошбика',
          message: 'Учетные данные не верны'
        });
      }
  }
}
</script>

<style scoped>
img {
  max-width: 100%;
}
.wrapper {
  background: initial;
  height: inherit;
  display: flex;
  align-items: center;
  flex-direction: column;
}
.titletext {
  height: 36px;
  width: 578px;
  margin-top: 120px;
  font-weight: 600;
  font-size: 36px;
  line-height: 44px;
  color: #2b3d4e;
  text-align: center;
}
.titlelogo {
  height: 109px;
  width: 330px;
  margin-top: 48px;
  text-align: center;
}
form {
  text-align: center;
  width: 340px; /* margin-top: 72px; */
}
.input {
  margin-top: 48px;
  position: relative;
}
.input-icon {
  position: absolute;
  top: 12px;
  left: 24px;
}
.btn {
  margin-top: 48px;
  border: none;
}
.btn-round {
  width: 330px;
  height: 48px;
  outline: none;
  background: #e1fae1;
  border-radius: 28px;
  box-shadow: 3px 4px 10px rgba(0, 0, 0, 0.25);
  font-weight: 600;
  font-size: 16px;
  line-height: 20px;
  display: flex;
  align-items: center;
  text-align: center;
  justify-content: center;
  color: #3d8a3d;
  /* transition-duration: 0.2s; */
}
.btn-round:hover {
  cursor: pointer;
  background: hsl(120, 71%, 90%);
  border: 2px solid #6E7A6E;
}
.button-footer {
  margin-top: auto;
  margin-bottom: 62px;
  width: 150px;
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  border: none;
}
.btn-circle {
  background: none;
  border: none;
  display: block;
  outline: none;
  width: 60px;
  height: 60px;
  border-radius: 30px;
}
.imgemail {
  background-image: url("../assets/svg/telega.svg");
  background-repeat: no-repeat;
  background-position: center;
  background-size: auto auto;
}
.imgesite {
  background-image: url("../assets/svg/site.svg");
  background-repeat: no-repeat;
  background-position: center;
  background-size: auto auto;
}
</style>
