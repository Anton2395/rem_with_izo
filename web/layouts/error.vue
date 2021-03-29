
<template>
  <div class="body">
    <main class="Site-content">
      <section>
        <h1>Ошибка 404</h1>
        <h2>Страница не найдена</h2>

        <hr />

        <nuxt-link to="/" custom v-slot="{ navigate }">
          <button @click="navigate">Главная страница</button>
        </nuxt-link>
      </section>
    </main>
  </div>
</template>




<style scoped>
html {
  font-family: "Montserrat", -apple-system, BlinkMacSystemFont, "Segoe UI",
    Roboto, "Helvetica Neue", Arial, sans-serif;
  font-size: 18px;
  word-spacing: 1px;
  -ms-text-size-adjust: 100%;
  -webkit-text-size-adjust: 100%;
  -moz-osx-font-smoothing: grayscale;
  -webkit-font-smoothing: antialiased;
  box-sizing: border-box;
}

h1,
h2 {
  color: red;
}
.body {
  display: flex;
  min-height: 100vh;
  flex-direction: column;
  background: #f7f8fa;
  align-items: center;
}

.Site-content {
  flex: 1;
  width: 100%;
  background-image: url("../assets/svg/LogoMenu.svg");
  background-repeat: no-repeat;
  background-size: 500px;
  background-position: 10% 80%;
}
section {
  position: relative;
  right: 0;
  width: 600px;
  margin-left: 50%;
  margin-top: 10%;
}

button {
  border: 1px solid #6e7a6e;

  border-radius: 20px;
  box-shadow: 0px 4px 4px #6e7a6e25;
  color: #6e7a6e;
  padding: 0 30px;
  height: 40px;
  width: 330px;
  margin: 15px 0;
  text-align: center;
  font-size: 24px;
  outline: none;
}
</style>