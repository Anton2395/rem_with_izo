import de from "element-ui/src/locale/lang/de";


export default {
    namespaced: true,

    state: () => ({
        tabs: [],
        arrPoint: [],
        clickHour: false,
     


    }),
    getters: {
        getTabs(state) {
            return state.tabs;
        },
        arrPoint(state) {
            return state.arrPoint;
        },

        currentArrPoint(state) {
            let arr = state.arrPoint.filter(item => item.machineid == state.selectChart);
            return arr;
        },



        lengthArrPoint(state, idx) {
            let arr = state.arrPoint.filter(item => item.machineid == state.selectChart);
            return arr.length;
        },

    },
    mutations: {
        mutTabs(state, data) {
            state.tabs.push(data);
        },
        setclickHour(state) {
            state.clickHour = true;
           
        },
        removePoint(state, point) {
            let indexPoint = state.arrPoint.findIndex(state => state.id == point.id);
            if (indexPoint !== -1) {
                state.arrPoint.splice(indexPoint, 1);
            }
        },
        addPoint(state, point) {

            let indexPoint = state.arrPoint.findIndex(state => state.id == point.id);
            if (indexPoint == -1) {
                state.arrPoint.push(point);
            }
        },

    },
    actions: {
        addPoint(store, point) {
            store.commit('addPoint', point);
        },
        removePoint(store, point) {
            store.commit('removePoint', point);
        },
        addTabs(store) {
            let data = { name: "Рабочее пространство" + store.state.tabs.length };
            store.commit("mutTabs", data);
        }


    },
    strict: process.env.NODE_ENV !== 'production'
};