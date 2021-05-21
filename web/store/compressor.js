export default {
  namespaced: true,
  state: () => ({
    compressor_data: {},//данные по обновлению чисел и статусов
    duration_time: [],//данные для виджета продолжительность работы
    limits: {},//пределы с цветами
  }),
  getters: {
    compressor_data(state) {

      let tmp = JSON.parse(JSON.stringify(state.compressor_data));
      tmp.current_temp = parseFloat(tmp.current_temp).toFixed(1);
      tmp.current_pressure = tmp.current_pressure/1000;
      return tmp;
    },

    compressor_time(state) {
      let tmp = JSON.parse(JSON.stringify(state.duration_time));
      tmp.forEach((item) => {
        
        item.start_time = item.start_time.slice(11, 16);
        item.end_time = item.end_time.slice(11, 16);
        
        item.work_time = item.work_time.toFixed(2);
        item.progress = item.progress.toFixed(2);
      })
      return tmp;
    },

    compressor_limits(state) {
      let newLimits = [];
      if (state.limits.length > 0) {
        newLimits.push([0,'#4BBEA9']);
        state.limits.forEach((item) => {
          newLimits.push([item.to, item.color]);
        })

      }
      return newLimits;
    }

  },
  mutations: {
    compressor_data(state, data) {
      state.compressor_data = data;

    },

    compressor_time(state, data) {
      state.duration_time = data;
    },
    compressor_limits(state, data) {
      state.limits = data;
    },

  },
  actions: {
    async get_compressor_data({ commit }) {
      let data = await this.$axios.$get(`/dashboard/compressor/data/`); //{ current_temp: 100, current_state: 2, current_pressure: 80 };
      commit("compressor/compressor_data", data, { root: true })
    },

    async get_compressor_time({ commit }) {
      let data = await this.$axios.$get(`/dashboard/compressor/dur/`);
      commit("compressor/compressor_time", data, { root: true })
    },

    async get_compressor_limits({ commit }) {
      let data = await this.$axios.$get(`/dashboard/compressor/statecolor/`);
      commit("compressor/compressor_limits", data.state, { root: true })
    },

  }
}