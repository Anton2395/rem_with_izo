export default {
  namespaced: true,

  state: () => ({
    workarea: {},

  }),
  getters: {

  },
  mutations: {
    setWorkarea(state, workarea) {
      state.workarea = workarea;
    },
    deleteWorkArea(state, index) {
      // console.log(state.workarea);
      state.workarea.workares.splice(index, 1);
    },
    addEmptyWorkArea(state, data) {
      state.workarea.workares.push(data);
    },
    renameWorkarea(state, data) {
      // debugger;ы
      state.workarea.workares[
        state.workarea.workares.findIndex(
          (el) => {
            return data.id == el.id;
          }
        )
      ].name = data.name;


    },
    renameWorkspace(state,name){
      debugger;
      try{state.workarea.name = name}
      catch(e){};
    }
  },
  actions: {
    SetActiveWorkarea(store, workarea) {
      // console.log(store);
      store.commit('setWorkarea', workarea);
    },
    DeleteActiveWorkarea(store, Vdata) {
      let index = store.state.workarea.workares.findIndex(
        (el) => {
          return Vdata.id == el.id;
        }
      );
      store.commit('deleteWorkArea', index);
    },
    AddEmptyWorkArea(store, data) {
      // console.log(data);
      store.commit('addEmptyWorkArea', data);
    },
    RenameWorkArea(store, data) {
      // console.log(store);
      store.commit('renameWorkarea', data);
    },
    FixRenameWorkSpace(store,name){
      debugger;
      store.commit('renameWorkspace', name);
    }

  },
};
