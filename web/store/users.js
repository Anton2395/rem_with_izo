export default {
  namespaced: true,

  state: () => ({
    curentUser: {
      name: "No name",
      special: "test",
      access: true,
      accessLevel: "завод",
      company: "ООО ТелДаФакс"
    },
    currentTabHeader: "",
    currentTabSidebar:"",

  }),
  getters: {
    curentUser(state) {
      return state.curentUser;
    },
    currentTabHeader(state) {
      return state.currentTabHeader;
    },
    currentTabSidebar(state) {
      return state.currentTabSidebar;
    },

  },
  mutations: {
    setUserAuthData(state, rootState){
      state.curentUser.name = rootState.auth.user.username || "no name";
      state.curentUser.accessLevel = (rootState.auth.user.is_superuser)? "ADMIN" : "no superuser";
    },
    setActiveTabHeader(state, point) {
      state.currentTabHeader = point;
    },
    setActiveTabSidebar(state, point) {
      state.currentTabSidebar = point;
    },

  },
  actions: {
    setUserData(store){
      // console.log(store);
      store.commit('setUserAuthData',store.rootState);
    },
    setActiveTabHeader(store, point) {
      store.commit('setActiveTabHeader', point);
    },
    setActiveTabSidebar(store, point) {
      store.commit('setActiveTabSidebar', point);
    },

  },
  strict: process.env.NODE_ENV !== 'production'
};
