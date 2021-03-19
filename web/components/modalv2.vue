<template>
  <transition name="modal">
    <div class="modal-mask">
      <div class="modal-wrapper">
        <div class="modal-container">
          <div class="modal-header">
            <slot name="header"> Внимание! </slot>
          </div>

          <div class="modal-body">
            <slot name="body"> Потеряна связь с сервером </slot>
          </div>

          <div class="modal-footer">
            <slot name="footer">
              <button class="modal-default-button" @click="close">OK</button>
            </slot>
          </div>
        </div>
      </div>
    </div>
  </transition>
</template>
    
    
<script>
export default {
  name: "modal",

  methods: {
    close() {
      this.$emit("close");
    },
  },
};
</script>
<style>
.modal-mask {
  position: fixed;
  z-index: 9998;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
}

.modal-wrapper {
  display: flex;
  vertical-align: middle;
}

.modal-container {
  background: #fff;
  border-radius: 8px;
  padding: 15px;
  min-width: 420px;
  max-width: 480px;
  position: absolute;
  top: 45%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 1002;
  margin: 0px auto;
  padding: 20px 30px;
  border-radius: 2px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.33);
 
}

.modal-header {
  color: #edbe45;
  z-index: 1002;
  text-align: center;
  border-bottom: #edbe45 solid 2px;
  padding: 5px;
}
.modal-body {
  margin: 30px 0;
  z-index: 1002;
  text-align: center;
}

.modal-default-button {
  background-color: #edbe45;
  color: #fff;
  padding: 8px;
  font-size: 17px;
  font-weight: 500;
  border-radius: 8px;
  min-width: 150px;
  z-index: 1002;
  margin-left: 28%;
}
  

/*
 * The following styles are auto-applied to elements with
 * transition="modal" when their visibility is toggled
 * by Vue.js.
 *
 * You can easily play with the modal transition by editing
 * these styles.
 */

.modal-enter {
  opacity: 0;
}

.modal-leave-active {
  opacity: 0;
}

.modal-enter .modal-container,
.modal-leave-active .modal-container {
  -webkit-transform: scale(1.1);
  transform: scale(1.1);
}
</style>