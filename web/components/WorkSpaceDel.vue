<template>
 <div class="overlay" @click="$emit('closeForm')">
  <div class="popup" v-on:click.stop="">
    <button class="btn_close" @click="$emit('closeForm')"></button>
    <div class="footer">
      <div class="del_footer">
        <button class="btn_left" @click="$emit('closeForm')">Отмена</button>
        <button class="btn_right" @click="DeleteWorkArea">Удалить</button>
      </div>
      <div class="del_body">
        <p class="del">
          {{ del }}
        </p>
        <p class="wht_del">
          {{ deletedWorkspace.name }}
        </p>
      </div>
    </div>
  </div>
 </div>
</template>

<script>
export default {
  data() {
    return {};
  },
  props: ["del", "whtdel",'deletedWorkspace'],
  name: "WorkSpaceDel",
  methods: {
 async DeleteWorkArea() {
    
          await this.$axios
            .delete(`/recorder/structure/Workspace/${this.deletedWorkspace.id}/`)
            .then((data) => {
            
            })
            this.$emit("closeForm");
              this.$parent.getWorkspaces();
           
        }
      
     
    },
  };


</script>
<style scoped>
.popup{
  width: 498px;
  height: 108px;
  display: flex;
  justify-content: space-between;
  flex-wrap: wrap;
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.del_body{

  width: 468px;
  height: 72px;
  background: #F7F8FA;
  font-family: 'Montserrat';
  font-style: normal;
  font-weight: 500;
  font-size: 16px;
  line-height: 20px;
  color: #4B6075;

  text-align: center;
}

.btn_left {
  width: 234px;
  height: 36px;
 
  color:#004085;
  outline: none;
  cursor: pointer;
  
  background:#CCE5FF;
  border: none;

  font-family: 'Montserrat';
  font-style: normal;
  font-weight: 500;
  font-size: 12px;
  line-height: 15px;
}

.btn_left:hover {
  color: #858585;
  background: #CCE5FF;
  border: none;
  border-radius: 0;
  transition: 0.2s;
  box-shadow: 0px 9px 109px rgba(0, 0, 0, 0.0372022),
  0px 3.28515px 39.7868px rgba(0, 0, 0, 0.0532451),
  0px 1.59488px 19.3158px rgba(0, 0, 0, 0.0667549),
  0px 0.781839px 9.46894px rgba(0, 0, 0, 0.0827978),
  0px 0.30914px 3.74403px rgba(0, 0, 0, 0.12);
}    
  
.btn_right {
  width: 234px;
  height: 36px;

  color: #721C24;;
  outline: none;
  cursor: pointer;

  font-family: 'Montserrat';
  font-style: normal;
  font-weight: 500;
  font-size: 12px;
  line-height: 15px;
  
  background: #F7DCDF;
  border: none;
}

.btn_right:hover {
  color: #858585;
  background: #F7DCDF;
  border: none;
  border-radius: 0;
  transition: 0.2s;

  box-shadow: 0px 9px 109px rgba(0, 0, 0, 0.0372022),
  0px 3.28515px 39.7868px rgba(0, 0, 0, 0.0532451),
  0px 1.59488px 19.3158px rgba(0, 0, 0, 0.0667549),
  0px 0.781839px 9.46894px rgba(0, 0, 0, 0.0827978),
  0px 0.30914px 3.74403px rgba(0, 0, 0, 0.12);

}  

.btn_close{
  background: center no-repeat  url('~assets/svg/iconControlModal_1.svg');
  display: block;
  width: 24px;
  height: 24px;
  border: none;
  outline: none; 
}

.btn_close:hover{
  background: center no-repeat  url('~assets/svg/iconControlModal.svg');
  display: block;
  width: 24px;
  height: 24px;
  border: none;
  outline: none; 
  
} 

.footer{
  width: 468px;
  height: 108px;
  display: flex;
  flex-direction: column-reverse;
  box-shadow: 0px 2px 6px rgba(0, 0, 0, 0.25);
  
}

.del_footer{
  height: auto;
  width: auto;
  display: flex;
  justify-content: space-between;

}

.del{
  margin-top:16px;
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