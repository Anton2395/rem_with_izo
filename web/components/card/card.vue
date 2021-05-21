<template>
  <div
    class="container"
    :class="{ backRed: flash }"
    :style="{ width: +size * 180 + 'px' }"
   
  >
    <div class="text-block">
      <div class="middle-text">{{ number }}</div>
      <div class="bottom-text">{{ description }}</div>
      <div class="middle-text2" :style="{ color: color }">
        <span>{{ description2 }} </span>
      </div>
    </div>
    <img class="image" :src="require(`~/assets/img/${path}`)" v-if="path" />
  </div>
</template>

<script  >
export default {
  name: "card",

  props: ["number", "description", "path", "size", "description2", "color"],
  data() {
    return {
      flash: false,
      intervalT: null,
    };
  },
  mounted() {
    this.updateColor();
    setInterval(this.updateColor, 1000);
  },
  methods: {
    updateColor() {
      if (this.color == "#721C24") {
        if (this.flash) {
          this.flash = false;
        } else {
          this.flash = true;
        }
      } else {
        this.flash = false;
      }
    },
  },
};
</script>

<style>
.container {
  
  display: inline-flex;
  width: 186px;
  height: 86px;
  padding: 6px;
  border: 2px solid #ecedf4;
  border-radius: 12px;
  position: relative;
  margin:5px;
 
}

.container .text-block {
  display: inline-block;
  width: 100%;
  vertical-align: middle;
}

.container .bottom-text {
  font-size: 12px;
  margin-top: 0px;
  color: darkgrey;
  font-family: "Montserrat", sans-serif;
  position: absolute;
  bottom: 6px;
}

.container .middle-text {
  margin-top: 10px;
  font-size: 36px;
  font-family: "Montserrat", sans-serif;
  display: flex;
  align-items: center;
  justify-content: center;
}

.container .image {
  margin-top: 6px;
  width: 50px;
  height: 50px;
  border-radius: 50%;
}
.container .middle-text2 {
  margin-top: -8px;
  display: flex;
  align-items: center;
  justify-content: center;
  height: 60px;
  font-weight: bold;
  font-size: 16px;
  font-family: "Montserrat", sans-serif;
  color: #000;
  text-align: center;
  white-space: pre-line;
}

.red {
  color: #ff0101;
}
.green {
  color: #588c64;
}
.black {
  color: #000000;
}

.backRed {
  background-color: #E7717C;
}

</style>