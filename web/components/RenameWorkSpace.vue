<template>
  <div class="overlay" >
    <div class="popup_rename" v-on:click.stop="">
      <button class="btn_close" @click="$emit('closeForm')"></button>
      <div class="rename_footer">
        <div class="r_footer">
          <button class="btn_left_blue" @click="$emit('closeForm')">
            Отмена
          </button>
          <button class="btn_right_green" @click="SetNewName">Применить</button>
        </div>
        <div class="rename_header">
          <span class="name">Переименование рабочего пространства</span>
          <input type="text" class="inputRename" v-model="newname" />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: ["name"],
  name: "RenameWorkSpace",
  data() {
    return {
      newname: this.name.name,
      form: {
        name: this.newname,
      },

      isRename: false,
    };
  },
  methods: {
    async SetNewName() {
      await this.$axios
        .$put(
          `/recorder/structure/Workspace/${this.name.id}/`,
          { name: this.newname }
        )
        .then((data) => {
          // let indexFind = this.$parent.workspaces.findIndex((el) => {
          //   return el.id == data.id;
          // });
          //this.$parent.workspaces[indexFind].name = data.name;
          this.$emit("closeForm");
           this.$emit("changeNameInParent",this.newname);
        })
        .catch((e) => {
          console.log(e);
        });
    },
  },
  // console.log(this);
};
</script>

<style scoped>
.popup_rename {
  width: 495px;
  height: 132px;
  display: flex;
  justify-content: space-between;
  flex-wrap: wrap;
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.btn_left_blue {
  width: 234px;
  height: 36px;

  color: #004085;
  outline: none;
  cursor: pointer;

  background: #cce5ff;
  border: none;

  font-family: "Montserrat";
  font-style: normal;
  font-weight: 500;
  font-size: 12px;
  line-height: 15px;
}

.btn_left_blue:hover {
  color: #858585;
  background: #cce5ff;
  border: none;
  border-radius: 0;
  transition: 0.2s;
  box-shadow: 0px 9px 109px rgba(0, 0, 0, 0.0372022),
    0px 3.28515px 39.7868px rgba(0, 0, 0, 0.0532451),
    0px 1.59488px 19.3158px rgba(0, 0, 0, 0.0667549),
    0px 0.781839px 9.46894px rgba(0, 0, 0, 0.0827978),
    0px 0.30914px 3.74403px rgba(0, 0, 0, 0.12);
}

.btn_right_green {
  width: 234px;
  height: 36px;

  color: #0b2e13;
  outline: none;
  cursor: pointer;

  font-family: "Montserrat";
  font-style: normal;
  font-weight: 500;
  font-size: 12px;
  line-height: 15px;

  background: #d4edda;
  border: none;
}

.btn_right_green:hover {
  color: #858585;
  background: #d4edda;
  border: none;
  border-radius: 0;
  transition: 0.2s;

  box-shadow: 0px 9px 109px rgba(0, 0, 0, 0.0372022),
    0px 3.28515px 39.7868px rgba(0, 0, 0, 0.0532451),
    0px 1.59488px 19.3158px rgba(0, 0, 0, 0.0667549),
    0px 0.781839px 9.46894px rgba(0, 0, 0, 0.0827978),
    0px 0.30914px 3.74403px rgba(0, 0, 0, 0.12);
}

.btn_close {
  background: center no-repeat url("~assets/svg/iconControlModal_1.svg");
  display: block;
  width: 24px;
  height: 24px;
  border: none;
  outline: none;
}

.btn_close:hover {
  background: center no-repeat url("~assets/svg/iconControlModal.svg");
  display: block;
  width: 24px;
  height: 24px;
  border: none;
  outline: none;
}

.rename_footer {
  width: 468px;
  height: 132px;
  display: flex;
  flex-direction: column-reverse;
  box-shadow: 0px 2px 6px rgba(0, 0, 0, 0.25);
  background-color: #f7f8fa;
}

.r_footer {
  height: auto;
  width: auto;
  display: flex;
  justify-content: space-between;
}

.rename_header {
  display: flex;
  flex-direction: column;
  align-items: center;
  background-color: #f7f8fa;
}

.name {
  font-family: "Montserrat";
  font-style: normal;
  font-weight: 500;
  font-size: 16px;
  line-height: 20px;
  color: #4b6075;
  margin-bottom: 24px;
}

.inputRename {
  outline: none;
  width: 456px;
  height: 24px;
  border: 1px solid #9098af;
  border-radius: 4px;
  margin-bottom: 24px;
  font-family: "Montserrat";
  font-style: normal;
  font-weight: normal;
  font-size: 12px;
  line-height: 15px;
}
.overlay {
  width: 100vw;
  height: 100vh;
  position: absolute;
  z-index: 200;
  top: 0;
  left: 0;
  background-color: rgba(0, 0, 0, 0.062);
}
</style>