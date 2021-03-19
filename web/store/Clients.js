
export default {
  namespaced: true,

  state: () => ({

    demoObject: [{
      "id": 2,
      "name": "test2"
    }],

    demoObjectidx: 0,

    typeStructured: [
      "Холдинг",
      "Завод",
      "Цех",
      "Узел",
      "Технологические группы",
    ],

    clientsObject: [{
        name: "Объект №1",
        client: "Tur",
        contract: {
          name: "contractTur",
          firstDate: "01/01/20",
          lastDate: "31/12/22"
        }
      },
      {
        name: "Объект №2",
        client: "Wet",
        contract: {
          name: "contractWet",
          firstDate: "01/02/20",
          lastDate: "31/12/23"
        }
      },
      {
        name: "Объект №3",
        client: "Wetles",
        contract: {
          name: "contractWetles",
          firstDate: "01/02/20",
          lastDate: "31/12/23"
        }
      },
      {
        name: "Объект №4",
        client: "sWetl",
        contract: {
          name: "contractsWetl",
          firstDate: "01/02/20",
          lastDate: "31/12/23"
        }
      },
    ],

    currentClient: {
      name: "",
      client: "",
      contract: "",
      objectUnit: {}
    },
    currentStructureObject: null,

    currentContract: {
      name: "",
      firstDate: "",
      lastDate: "",
    },
    currentObject: {
      nameObject: "",
      factorys: {},
      workshops: {},
      units: {},
      technologyGroups: {},
      machines: {},
    },
    currentFactory: {
      nameObject: "",
      nameFactory: "",
      workshops: {},
      units: {},
      technologyGroups: {},
      machines: {},
    },
    currentWorkshop: {
      nameObject: "",
      nameFactory: "",
      nameWorkshop: "",
      units: {},
      technologyGroups: {},
      machines: {},
    },
    currentUnit: {
      nameObject: "",
      nameFactory: "",
      nameWorkshop: "",
      nameUnit: "",
      technologyGroups: {},
      machines: {},
    },
    currentTechnologyGroups: {
      nameObject: "",
      nameFactory: "",
      nameWorkshop: "",
      nameUnit: "",
      nameTechnologyGroup: "",
      machines: {},
    },
    currentMachine: {
      nameObject: "",
      nameFactory: "",
      nameWorkshop: "",
      nameUnit: "",
      nameTechnologyGroup: "",
      nameMachine: "",
      aDriver: {},
      pDriver: {},
      qDriver: {},
      baseOEE: 0,
      targetOEE: 0,
    },
    driverOptions: {
      nameDriver: "",
      ipAddress: "",
      port: "",
      works: {},
      crash: {},
      switchedOff: {},
      plain: {},
      repairs: {},
    },



  }),
  getters: {

    demoObject(state) {
      return state.demoObject;
    },

    demoObjectidx(state) {
      return state.demoObjectidx;
    },

    typeStructured(state) {
      return state.typeStructured;
    },

    clientsObject(state) {
      return state.clientsObject;
    },
    currentStructureObject(state) {
      return state.currentStructureObject;
    },
    currentClient(state) {
      return state.currentClient;
    },
    currentContract(state) {
      return state.currentContract;
    },
    currentObject(state) {
      return state.currentObject;
    },
    currentFactory(state) {
      return state.currentFactory;
    },
    currentWorkshop(state) {
      return state.currentWorkshop;
    },
    currentUnit(state) {
      return state.currentUnit;
    },
    currentTechnologyGroups(state) {
      return state.currentTechnologyGroups;
    },
    currentMachine(state) {
      return state.currentMachine;
    },
    driverOptions(state) {
      return state.driverOptions;
    },
  },
  mutations: {

    GET_DEMOOBJECT(state, payload ) {
      // console.log(payload);
      state.demoObject = payload;
      // state.demoObjectidx = state.demoObject[0].id;
      // console.log(state.demoObjectidx);

    },

    ADD_DEMOOBJECT (state, payload ) {

    },

    DELETE_DEMOOBJECT (state, payload ) {

    },

    UPDATE_DEMOOBJECT(state, payload ) {

    },

    updateCurrentClient(state, currentData) {
      state.currentClient[currentData.key] = currentData[currentData.key];
    },
    updateCurrentStructureObject(state, currentData) {
      state.currentStructureObject[currentData.key] = currentData[currentData.key];
    },

  },
  actions: {
    // ------------

    async GET_DEMOOBJECT (store, payload){

      let data = await this.$axios.$get('http://192.168.0.12/api/Association/');

      console.log(data);
      store.commit('GET_DEMOOBJECT', data);
    },

    async UPDATE_DEMOOBJECT (store, obj){

      console.log(obj);

      let olddata = await this.$axios.$put(`http://192.168.0.12/api/Association/${obj.id}/`, {name:obj.name});
      // let olddata = await this.$axios.$put(`http://192.168.0.12/api/Association/${obj.id}`, {name:obj.name});
      // let olddata = await this.$axios.$put(`http://192.168.0.12/api/Association/`, obj);

      console.log(olddata);

      let data = await this.$axios.$get('http://192.168.0.12/api/Association/');

      // console.log(data);
      store.commit('GET_DEMOOBJECT', data);
    },



    async ADD_DEMOOBJECT (store, obj){
      // console.log(obj);
      let olddata = await this.$axios.$post('http://192.168.0.12/api/Association/', obj);

      let data = await this.$axios.$get('http://192.168.0.12/api/Association/');

      store.commit('GET_DEMOOBJECT', data);


    },

    async DELETE_DEMOOBJECT (store, obj){

      console.log(obj);

      let olddata = await this.$axios.$delete(`http://192.168.0.12/api/Association/${obj}/ `);

      console.log(olddata);

      let data = await this.$axios.$get('http://192.168.0.12/api/Association/');

      console.log(data);
      store.commit('GET_DEMOOBJECT', data);


    },

    // ------------


    updateCurrentClient(store, currentData) {
      store.commit('updateCurrentClient', currentData);
    },

    updateCurrentStructureObject(store, currentData) {
      store.commit('updateCurrentStructureObject', currentData);
    },

  },
  strict: process.env.NODE_ENV !== 'production'
};
