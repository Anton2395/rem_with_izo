export default {
  namespaced: true,

  state: () => ({
    // currentDevMessages: [
    //   {
    //     id: 1,
    //     device: "Устройство 1",
    //     driver: "S7 TCP 192.168.34.23:102",
    //     connect: "conn = Stetum_324,var = FD1_real_324",
    //     msg: "S7 TCP 192.168.34.23:102",
    //     status: "ok",
    //   },
    //   {
    //     id: 2,
    //     device: "Устройство 2",
    //     driver: "S7 TCP 192.168.34.23:101",
    //     connect: "conn = Stetum_325, var = FD1_real_325",
    //     msg: "S7 TCP 192.168.34.21:102",
    //     status: "dng",
    //   }, 
    //   {
    //     id: 3,
    //     device: "Устройство 3",
    //     driver: "S7 TCP 192.168.34.23:101",
    //     connect: "conn = Stetum_325, var = FD1_real_325",
    //     msg: "S7 TCP 192.168.34.21:102",
    //     status: "",
    //   }
    // ],
    currentDevMessages: {
      "conn1":[1, 2, 3], 
      "conn2":[1, 2, 3]
    },
    currentMessages: [],
    archiveMessages: [],
    currentAlert: null,

  }),
  getters: {
    currentDevMessages(state) {
      return state.currentDevMessages;
    },
    currentMessages(state) {
      return state.currentMessages;
    },
    currentAlert(state) {
      return state.currentAlert;
    },

  },
  mutations: {
    updateCurrentDevMessages(state, payload) {
      state.currentDevMessages = payload;
      console.log("currentDevMessages", state.currentDevMessages);
    },
    
    updateCurrentMessages(state, payload) {
      state.currentMessages = payload;
    },
  },
  actions: {
    getCurrentDevMessages(store, payload) {

      let data = this.$axios.$get('/dashboard/teldafax/status/connections/');
      // store.commit('updateCurrentDevMessages', data.currentDevMessages);
      data.
      then(data => store.commit('updateCurrentDevMessages', data)
      );

      // data.then((data) => console.log("+++++++++", data));
    },
    async getCurrentMessages(store, payload) {
       let data = await this.$axios.$get('/dashboard/teldafax/messages/alarms/');
       if(data['error']){
         console.error(data['error']);
       }else{
         let result = data.alarms.concat(data.warnings);
         console.log(result);
         for(let i of result){
          i[1] = new Date(i[1]);
          i[1] = i[1].getFullYear() +"-"+ i[1].getMonth()+"-"+i[1].getDate()+" "+i[1].getHours()+":"+i[1].getMinutes()+":"+i[1].getSeconds();
      }
        store.commit('updateCurrentMessages', result);
       }
       
    },
    async getArchiveMessages(store, payload) {
      let data = await this.$axios.$get('/dashboard/teldafax/messages/alarms/');
      if(data['error']){
        console.error(data['error']);
      }else{
        let result = data.alarms.concat(data.warnings);
        console.log(result);
        for(let i of result){
         i[1] = new Date(i[1]);
         i[1] = i[1].getFullYear() +"-"+ i[1].getMonth()+"-"+i[1].getDate()+" "+i[1].getHours()+":"+i[1].getMinutes()+":"+i[1].getSeconds();
     }
       store.commit('updateCurrentMessages', result);
      }
      
   },
  },

  strict: process.env.NODE_ENV !== 'production'
};

