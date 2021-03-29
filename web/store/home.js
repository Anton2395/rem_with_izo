export default {
    namespaced: true,

    state: () => ({
        lineDataFirst: {
            interval: [],
            sum: 0,
        },
        stockBalances: {
            storehouse: [
                {
                    name: '',
                    iso: [],
                    pol: [],
                    pen: [],
                },
            ],
            in_total: {
                iso: 0,
                pol: 0,
                pen: 0
            },
        },
        comparisonModule: {
            suitable1: 0,
            change_suitable1: 0,
            suitable2: 0,
            substandard1: 0,
            change_substandard1: 0,
            substandard2: 0,
            defect1: 0,
            change_defect1: 0,
            defect2: 0,
            flooded1: 0,
            change_flooded1: 0,
            flooded2: 0,
            sum1: 0,
            change_sum1: 0,
            sum2: 0,
            isQuery: false,
        },
        energyConsumption: {
            input1: 0,
            input2: 0,
            gas: 0,
        },
        totalConsumption: {
            iso: 0,
            pol: 0,
            pen: 0,
            kat1: 0,
            kat2: 0,
            kat3: 0,
        },
        specificConsumption: {
            iso: 0,
            pol: 0,
            pen: 0,
            kat1: 0,
            kat2: 0,
            kat3: 0,
        },
        panelRelease: {
            suitable: 0,
            change_suitable: 0,
            substandard: 0,
            change_substandard: 0,
            defect: 0,
            change_defect: 0,
            flooded: 0,
            change_flooded: 0,
            sum: 0,
            change_sum: 0,
        }
    }),
    getters: {
        lineDataFirst(state) {
            let lineDataFirst = JSON.parse(JSON.stringify(state.lineDataFirst));
            let intervalNew = [];
            lineDataFirst.interval.forEach((item) => {
                item.progress = Math.floor((item.duration / lineDataFirst.sum) * 100);
                item.duration = item.duration.toFixed(2);

                intervalNew.push(item);
            });

            lineDataFirst.interval = intervalNew;

            return lineDataFirst;
        },
        comparisonModule(state) {
            return state.comparisonModule;
        },
        energyConsumption(state) {
            return state.energyConsumption;
        },
        totalConsumption(state) {
            return state.totalConsumption;
        },
        specificConsumption(state) {
            return state.specificConsumption;
        },
        stockBalances(state) {
            return state.stockBalances;
        },
        panelRelease(state) {
            return state.panelRelease;
        }
    },
    mutations: {
        setLineDataFirst(state, data) {
            state.lineDataFirst = data;
        },
        setComparisonModule(state, data) {
            state.comparisonModule = data;
        },
        setEnergyConsumption(state, data) {
            state.energyConsumption = data;
        },
        setTotalConsumption(state, data) {
            state.totalConsumption = data;
        },
        setSpecificConsumption(state, data) {
            state.specificConsumption = data;
        },
        setStockBalances(state, data) {
            state.stockBalances = data;
        },
        setPanelRelease(state, data) {
            state.panelRelease = data;
        }
    },
    actions: {
        async getLineDataFirst(store, option) {
            let data = {
                interval: [],
                sum: 0,
            };

            try {
                if (option.smena)
                    data = await this.$axios.$get(`/dashboard/duration/${formatDate(option.date)}/shift/${option.smena}`);
                else
                    data = await this.$axios.$get(`/dashboard/duration/${formatDate(option.date)}/day/`);

                if (!data)
                    throw new Error('return data is null');

            } catch (e) {
                console.log(e.message);
                console.error("getLineDataFirst axios");
                //later remove
                //start block
                // data.sum = getRandomInt(90) + 10;
                // let start = "";
                // let end = "";
                // for (let i = 0; i < 10; i++) {
                //     start = new Date(2020, 1, 11, getRandomInt(12), getRandomInt(59), 0, 0);
                //     end = new Date(2020, 1, 11, getRandomInt(12) + 11, getRandomInt(59), 0, 0);
                //     data.interval.push({
                //         start: start.getHours() + ':' + start.getMinutes(),
                //         end: end.getHours() + ':' + end.getMinutes(),
                //         duration: Math.random() * 23,
                //     });
                // }
                //end block
            }

            store.commit('setLineDataFirst', data);
        },
        async getComparisonModule(store, option) {
            debugger
            let data = null;
            try {
                if (option.id1 && option.id2)
                    data = await this.$axios.$get(`/dashboard/comparison/shift/${formatDate(option.date1)}/${option.id1}/${formatDate(option.date2)}/${option.id2}`);
                else if (option.isType1 === 'day')
                    data = await this.$axios.$get(`/dashboard/comparison/day/${formatDate(option.date1)}/${formatDate(option.date2)}`);
                else if (option.isType1 === 'month')
                    data = await this.$axios.$get(`/dashboard/comparison/month/${formatDate(option.date1)}/${formatDate(option.date2)}`);

                data.isQuery = true;

                if (!data)
                    throw new Error('return data is null');
            } catch (e) {
                console.error("getComparisonModule axios");
                //latter remove
                //start block
                // data = {
                //     suitable1: getRandomInt(300) + 200,
                //     change_suitable1: 0,
                //     suitable2: getRandomInt(300) + 200,
                //
                //     substandard1: getRandomInt(100),
                //     change_substandard1: 0,
                //     substandard2: getRandomInt(100),
                //
                //     defect1: getRandomInt(70),
                //     change_defect1: 0,
                //     defect2: getRandomInt(70),
                //
                //     flooded1: getRandomInt(100000) + 10000,
                //     change_flooded1: 0,
                //     flooded2: getRandomInt(100000) + 10000,
                //
                //     sum1: getRandomInt(900) + 100,
                //     change_sum1: 0,
                //     sum2: getRandomInt(900) + 100,
                // };
                //
                // data.change_suitable1 = ((data.suitable1 / data.suitable2) * 100).toFixed();
                // data.change_substandard1 = ((data.substandard1 / data.substandard2) * 100).toFixed();
                // data.change_defect1 = ((data.defect1 / data.defect2) * 100).toFixed();
                // data.change_flooded1 = ((data.flooded1 / data.flooded2) * 100).toFixed();
                // data.change_sum1 = ((data.sum1 / data.sum2) * 100).toFixed();
                // data.isQuery = true;

                //end block
            }

            store.commit('setComparisonModule', data);
        },
        async getEnergyConsumption(store, option) {
            let data = {
                    input1: 0,
                    input2: 0,
                    gas: 0,
                };

            try {
                if (option.id1)
                    data = await this.$axios.$get(`/dashboard/energyconsumption/${formatDate(option.date)}/shift/${option.id1}/`);
                else if (option.isType1 === 'day')
                    data = await this.$axios.$get(`/dashboard/energyconsumption/${formatDate(option.date)}/day/`);
                else if (option.isType1 === 'month')
                    data = await this.$axios.$get(`/dashboard/energyconsumption/${formatDate(option.date)}/month/`);

                if (!data)
                    throw new Error('return data is null');

            } catch (e) {
                console.error("getEnergyConsumption axios");

                //latter remove
                //start block
                // data = {
                //     input1: getRandomInt(300) + 200,
                //     input2: getRandomInt(100000) + 10000,
                //     gas: getRandomInt(100000) + 100000,
                // };
                //end block
            }

            store.commit('setEnergyConsumption', data);
        },
        async getTotalConsumption(store, option) {
            let data = {
                    iso: 0,
                    pol: 0,
                    pen: 0,
                    kat1: 0,
                    kat2: 0,
                    kat3: 0,
                };
            try {
                if (option.id1)
                    data = await this.$axios.$get(`/dashboard/sumexpense/${formatDate(option.date)}/shift/${option.id1}/`);
                else if (option.isType1 === 'day')
                    data = await this.$axios.$get(`/dashboard/sumexpense/${formatDate(option.date)}/day/`);
                else if (option.isType1 === 'month')
                    data = await this.$axios.$get(`/dashboard/sumexpense/${formatDate(option.date)}/month/`);

                if (!data)
                    throw new Error('return data is null');
            } catch (e) {
                console.error("getTotalСonsumption axios");

                //latter remove
                //start block
                // data = {
                //     iso: getRandomInt(300) + 200,
                //     pol: getRandomInt(300) + 200,
                //     pen: getRandomInt(300) + 200,
                //     kat1: getRandomInt(50) + 50,
                //     kat2: getRandomInt(50) + 50,
                //     kat3: getRandomInt(50) + 50,
                // };
                //end block
            }

            store.commit('setTotalConsumption', data);
        },
        async getSpecificConsumption(store, option) {
            let data = {
                    iso: 0,
                    pol: 0,
                    pen: 0,
                    kat1: 0,
                    kat2: 0,
                    kat3: 0,
                };

            try {
                if (option.id1)
                    data = await this.$axios.$get(`/dashboard/specificconsumption/${formatDate(formatDate(option.date))}/shift/${option.id1}/`);
                else if (option.isType1 === 'day')
                    data = await this.$axios.$get(`/dashboard/specificconsumption/${formatDate(formatDate(option.date))}/day/`);
                else if (option.isType1 === 'month')
                    data = await this.$axios.$get(`/dashboard/specificconsumption/${formatDate(formatDate(option.date))}/month/`);

                if (!data)
                    throw new Error('return data is null');

            } catch (e) {
                console.error("getSpecificConsumption axios");

                //latter remove
                // start block
                // data = {
                //     iso: (Math.random() * 10).toFixed(1),
                //     pol: (Math.random() * 10).toFixed(1),
                //     pen: (Math.random() * 10).toFixed(1),
                //     kat1: (Math.random() * 10).toFixed(1),
                //     kat2: (Math.random() * 10).toFixed(1),
                //     kat3: (Math.random() * 10).toFixed(1),
                // };
                //end block
            }

            store.commit('setSpecificConsumption', data);
        },
        async getStockBalances(store, option) {
            let data = {
                    storehouse: [],
                    "in_total": {
                        "iso": 0,
                        "pol": 0,
                        "pen": 0,

                    }
                };
            try {
                data = await this.$axios.$get(`/dashboard/remainder/${formatDate(option.date)}/`);
                if (!data)
                    throw new Error('return data is null');
            } catch (e) {
                console.error("getStockBalances axios");

                //latter remove
                //start block
                // data = {
                //     storehouse: [
                //         {
                //             name: "Скалад 1",
                //             iso: [getRandomInt(100), getRandomInt(100)],
                //             pol: [getRandomInt(100), getRandomInt(100)],
                //             pen: [],
                //         },
                //         {
                //             name: "Скалад 2",
                //             iso: [getRandomInt(100), getRandomInt(100), getRandomInt(100)],
                //             pol: [],
                //             pen: [getRandomInt(100)],
                //         },
                //         {
                //             name: "Скалад 3",
                //             iso: [getRandomInt(100), getRandomInt(100), getRandomInt(100)],
                //             pol: [getRandomInt(100), getRandomInt(100)],
                //             pen: [],
                //         },
                //     ],
                //     "in_total": {
                //         "iso": getRandomInt(100),
                //         "pol": getRandomInt(100),
                //         "pen": getRandomInt(100),
                //
                //     }
                // };
                //end block
            }

            store.commit('setStockBalances', data);
        },
        async getPanelRelease(store, option) {
            let data = {
                    suitable: 0,
                    change_suitable: 0,
                    substandard: 0,
                    change_substandard: 0,
                    defect: 0,
                    change_defect: 0,
                    flooded: 0,
                    change_flooded: 0,
                    sum: 0,
                    change_sum: 0,
                };
            try {
                if (option.id1)
                    data = await this.$axios.$get(`/dashboard/edition/${formatDate(option.date)}/shift/${option.id1}/`);
                else if (option.isType1 === 'day')
                    data = await this.$axios.$get(`/dashboard/edition/${formatDate(option.date)}/day/`);
                else if (option.isType1 === 'month')
                    data = await this.$axios.$get(`/dashboard/edition/${formatDate(option.date)}/month/`);

                if (!data)
                    throw new Error('return data is null');
            } catch (e) {
                console.error("getSpecificConsumption axios");

                //latter remove
                //start block
                // data = {
                //     suitable: getRandomInt(500),
                //     change_suitable: getRandomInt(100),
                //     substandard: getRandomInt(100),
                //     change_substandard: getRandomInt(100),
                //     defect: getRandomInt(100),
                //     change_defect: getRandomInt(100),
                //     flooded: getRandomInt(1000000),
                //     change_flooded: getRandomInt(100),
                //     sum: getRandomInt(500),
                //     change_sum: getRandomInt(100),
                // }
                //end block
            }

            store.commit('setPanelRelease', data);
        }
    },
    strict: process.env.NODE_ENV !== 'production'
};

function getRandomInt(max) {
    return Math.floor(Math.random() * Math.floor(max));
}

function formatDate(date) {
    let d = new Date(date);

    return d.getFullYear() + "-" + d.getMonth() + 1 + "-" + d.getDate();
}