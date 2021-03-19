<template>
  <div class="lds-dual-ring"></div>
</template>

<style>
.lds-dual-ring {
  display: inline-block;
  width: 100%;
  height: calc(100% - 48px);
  position: fixed;
  top: 48px;
  left: 0;
  z-index: 100;
}
.lds-dual-ring:after {
  content: " ";
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%,-50%);
  z-index: 2;
  display: block;
  width: 64px;
  height: 64px;
  margin: 8px;
  border-radius: 50%;
  border: 6px solid #cef;
  border-color: #cef transparent #cef transparent;
  animation: lds-dual-ring 1.2s linear infinite;
}

.lds-dual-ring:before {
  content: " ";
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 1;
  background: rgba(0,0,0,0.25);
}
@keyframes lds-dual-ring {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

</style>
