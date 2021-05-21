<template>
  <div>  
     <modal v-show="showModal" @close="closeModal"></modal>
    <div style="
    align-items: flex-start;
    display: flex;
">
      <background title="Показания перехода" style="margin-right: 10px">
        <card
          :number="data_sensor.methane"
          description="Метан, %"
          path="445.png"
          class="card"
        >
        </card>
        <card
          :number="data_sensor.carbondioxide"
          description="Углекислый газ, %"
          path="2.svg"
          class="card"
        >
        </card>
        <card
          :number="data_sensor.oxygen"
          description="Кислород, %"
          path="3.svg"
          class="card"
        >
        </card>
      
        <card
          :number="data_sensor.pressure"
          description="Давление, мБар"
          path="5.png"
          class="card"
        >
        </card>
          <card
          :number="data_sensor.pressure_out"
          description="Давление, мБар"
          path="4.png"
          class="card"
        >
        </card>
        <card
          :number="data_sensor.consumption"
          description="Расход, м3/ч"
          path="6.png"
          class="card"
        >
        </card>
        <card
          :number="data_sensor.temperature"
          description="Температура, °C"
          path="7.png"
          class="card"
        >
        </card>
      </background>
      <background title="Режим работы">
        <card :description2="work_status.name" 
        class="card" 
        :color="work_status.color"> </card>
      </background>
    </div>

    <div style="
    align-items: flex-start;
    display: flex;
">
      <background title="Выработка электроэнергии">
        <div>
          <card
            :number="data_sensor.power1"
            description="Мощность машина 1, кВт"
            path="8.png"
            class="card"
          >
          </card>
          <card
            :number="data_sensor.power2"
            description="Мощность машина 2, кВт"
            path="9.png"
            class="card"
          >
          </card>
          <card
            :number="data_sensor.power3"
            description="Мощность машина 3, кВт"
            path="10.png"
            class="card"
          >
          </card>
          <card
            :number="data_sensor.power4"
            description="Мощность машина 4, кВт"
            path="11.png"
            class="card"
          >
          </card>
          <div>

            <card
              :number="sumPowerX"
              description="Суммарная мощность всех генераторов, кВт"
              path="12.png"
              size="4.4"
              class="card"
            >
            </card>


          </div>
        </div>
      </background>
      <background title="Компрессоры">
      <card
        :description2="compres_V501_status.name=='Работа' ? `${compres_V501_status.name} \n ${data_sensor.frequency1}Гц` : compres_V501_status.name"
        description="Компрессор V501"
        path="16.png"
        class="card"
        :color="compres_V501_status.color"
      >
      </card>
      <card
        :description2="compres_V502_status.name=='Работа' ? `${compres_V502_status.name} \n ${data_sensor.frequency2}Гц` : compres_V502_status.name"
        description="Компрессор V502"
        path="17.png"
        class="card"
        :color="compres_V502_status.color"

      >
      </card>
      <card
        :description2="compres_V503_status.name=='Работа' ? `${compres_V503_status.name} \n ${data_sensor.frequency3}Гц` : compres_V503_status.name"
        description="Компрессор V503"
        path="18.png"
        class="card"
        :color="compres_V503_status.color"
      >
      </card>
    </background>
    </div>



<div>
<background title="Машины">



        <div style="display: flex">
          <card
            :description2="`${generator_D601_status2.name} \n ${generator_D601_status1.name} `"
            description="Генератор D0601"
            path="19.png"
            class="card"
            :color="generator_D601_status1.name!='Авария' ? generator_D601_status2.color : generator_D601_status1.color"

          >
          </card>
          <card
            :description2="`${generator_D602_status2.name} \n ${generator_D602_status1.name} `"
            description="Генератор D0602"
            path="20.png"
            class="card"


            :color="generator_D602_status1.name!='Авария' ? generator_D602_status2.color : generator_D602_status1.color"

          >
          </card>
          <card
            :description2="`${generator_D603_status2.name} \n ${generator_D603_status1.name} `"
            description="Генератор D0603"
            path="21.png"
            class="card"
            :color="generator_D603_status1.name!='Авария' ? generator_D603_status2.color : generator_D603_status1.color"

          >
          </card>
          <card
            :description2="`${generator_D604_status2.name} \n ${generator_D604_status1.name} `"
            description="Генератор D0604"
            path="22.png"
            class="card"

            :color="generator_D604_status1.name!='Авария' ? generator_D604_status2.color : generator_D604_status1.color"

          >
          </card>
          <card
            :description2="fakel_A604.name"
            description="Факел А0604"
            path="23.png"
            class="card"
            :color="fakel_A604.color"
          >
          </card>
        </div>
      </background>


      <background title="Насосы">

      <card
        :description2="pump_p301_status.name"
        description="Насос Р301"
        path="13.png"
        class="card"
        :color="pump_p301_status.color"
      >
      </card>
    </background>

    <background title="Задвижки">
      <card
        :description2="valve_B1101_status.name"
        description="Задвижка B1101"
        path="14.png"
        class="card"
        :color="valve_B1101_status.color"
      >
      </card>
      <card
        :description2="valve_B1601_status.name"
        description="Задвижка B1601"
        path="15.png"
        class="card"
        :color="valve_B1601_status.color"
      >
      </card>
    </background>
      </div>
    



    <div>

      
    </div>

    


  </div>
</template>





<script>
import {mapActions} from "vuex";
import {mapGetters} from "vuex";

import card from "@/components/card/card.vue";
import background from "@/components/background/back.vue";
import data from "@iconify/icons-bx/bx-user";
// import ModalWindow from "@/components/modal-window.vue";
import modal from "@/components/modalv2.vue";

export default {
  layout: "header_footer",
  components: {
    card,
    background,
    modal,
  },
  data() {
    return {
      timerId:null,
      data_sensor: {},
      data_status_device: {},
      work_status: {},
      pump_p301_status: {},
      valve_B1101_status: {},
      valve_B1601_status: {},
      compres_V501_status: {},
      compres_V502_status: {},
      compres_V503_status: {},
      generator_D601_status1: {},
      generator_D601_status2: {},
      generator_D602_status1: {},
      generator_D602_status2: {},
      generator_D603_status1: {},
      generator_D603_status2: {},
      generator_D604_status1: {},
      generator_D604_status2: {},
      fakel_A604: {},
      showModal:false,
      sumPowerX: "",
    };
  },
  created(){
    this.setActiveTabHeader("HOME");
    this.setActiveTabSidebar("Dashboard");
  },
  mounted() {
    
this.get_data_dash(),

this.timerId=setInterval(this.get_data_dash, 5000)

    
  },
  methods: {
    ...mapActions("users", {
      setActiveTabHeader: "setActiveTabHeader",
      setActiveTabSidebar: "setActiveTabSidebar",
    }),
    show_alert() {
        this.$notify.error({

          title: 'Ошибка',

          message: 'Нет связи с микросервисом'
        });
      },
    closeModal(){
      this.showModal=false;
    },
     async get_data_dash() {
      let isSlash=(url)=>{
        let arr=[];
        // console.log(url);
        for(let i=0;i<url.length;i++){
          if (url[i]=="/"){
            arr.push(i);
          }
          }
          // console.log(arr);
          if (arr.length>0){
            let ind = ((arr[arr.length-1])+1);
            if (typeof url[ind]== "undefined" || url[ind] == ""){
              return true;
            } else{
              return false;
            }
          }
          else{
            return false;
          }
        };
      
        let urlBool = isSlash(document.URL);
        // console.log(urlBool);
        if (!urlBool){
              clearInterval(this.timerId);
              return;   
          };
      

      let list_workMode = ["Не выбран", "Автоматический режим", "Ручной режим"];
      let list_statusPump = ["Выключен", "Работа", "Авария"];
      let list_statusValve = ["Закрыта", "Открыта", "Авария", "Авария"];

      let list_statusCompressor = ["Остановлен", "Работа", "Авария"];
      let list_statusGenerator1 = [ "МУправление", "ДУправление", "Готов к ДУ", "ДУправление", "Авария","","Авария","Авария" ];
      let list_statusGenerator2 = ["Отключен"];
      list_statusGenerator2[8] = ["Генерация"];
      list_statusGenerator2[24] = ["Генерация"];
      list_statusGenerator2[16] = ["Переведен в ДУ"];
      let list_statusFakel = ["Остановлен", "Работа", "Авария", "Авария"];


    try{ 
      // this.showModal=false;
    
      this.data_sensor = await this.$axios.$get(`/dashboard/teldafax/value/`);
      this.data_status_device = await this.$axios.$get(`/dashboard/teldafax/status/`);
        }
      catch(e){
       if(e.response.status==401){
         this.$router.go("/");
       }
       this.show_alert();
        //this.showModal=true;
        // this.$refs.modal.show = true;
        return;
      }
      if (typeof this.data_sensor.sum_power != "undefined") {
         this.sumPowerX = (this.data_sensor.sum_power).toFixed(1); 
         } 

      this.showModal = false;
      this.work_status["name"] = list_workMode[+this.data_status_device.work_status];
      this.pump_p301_status["name"] = list_statusPump[+this.data_status_device.pump_p301_status];
      this.valve_B1101_status["name"] = list_statusValve[+this.data_status_device.valve_B1101_status];
      this.valve_B1601_status["name"] = list_statusValve[+this.data_status_device.valve_B1601_status];
      this.compres_V501_status["name"] = list_statusCompressor[+this.data_status_device.compres_V501_status];
      this.compres_V502_status["name"] = list_statusCompressor[+this.data_status_device.compres_V502_status];
      this.compres_V503_status["name"] = list_statusCompressor[+this.data_status_device.compres_V503_status];
      this.generator_D601_status1["name"] = list_statusGenerator1[+this.data_status_device.generator_D601_status1];         
      this.generator_D601_status2["name"] = list_statusGenerator2[+this.data_status_device.generator_D601_status2];
      this.generator_D602_status1["name"] = list_statusGenerator1[+this.data_status_device.generator_D602_status1];
      this.generator_D602_status2["name"] = list_statusGenerator2[+this.data_status_device.generator_D602_status2];
      this.generator_D603_status1["name"]= list_statusGenerator1[+this.data_status_device.generator_D603_status1];
      this.generator_D603_status2["name"]=list_statusGenerator2[+this.data_status_device.generator_D603_status2];
      this.generator_D604_status1["name"]= list_statusGenerator1[+this.data_status_device.generator_D604_status1];
      this.generator_D604_status2["name"]= list_statusGenerator2[ +this.data_status_device.generator_D604_status2];
      this.fakel_A604["name"]=list_statusFakel[+this.data_status_device.fakel_A604];


      for (let a in this.$data){
        if ((this[a].name=="Остановлен")||(this[a].name=="Готов")||(this[a].name=="Выключен")||(this[a].name=="Не выбран")||(this[a].name=="Закрыта")||(this[a].name=="Не генерирует")){
            this[a]["color"]="#000";
        };
        if (this[a].name=="Авария"){
            this[a]["color"]="#721C24";
        };
        if ((this[a].name=="Работа")||(this[a].name=="Генерация")||(this[a].name=="Открыта")||(this[a].name=="Автоматический режим")){
            this[a]["color"]="#588C64";
        };
        if ((this[a].name=="Ручной режим")||(this[a].name=="Автомат")){
            this[a]["color"]="#856404";
        };
      };


      
      

    },
  },
};
</script>

<style>
.card {
  margin-top: 12px;
  margin-left: 5px;
  margin-right: 5px;
  margin-bottom: 5px;
}
.background {
  margin-left: 20px;
  margin-top: 20px;
}

.title {
  font-weight: bold;
  font-size: 14px;
}

.backside {
  position: absolute;
  padding-top: 96px;
  left: 0;
  top: 0;
  z-index: 5;
  box-shadow: 0px 2px 6px rgba(0, 0, 0, 0.25);
  background-color: #edf2f8;
  display: flex;
  flex-direction: column;
  width: 120px;
  height: 100vh;
}

</style>
