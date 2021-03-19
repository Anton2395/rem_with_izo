import de from "element-ui/src/locale/lang/de";

function preventSelection(element) { //ЗАПРЕТ НА ВЫДЕЛЕНИЕ ТЕКСТА КРОМЕ БЛОКОВ INPUT И TEXT-AREA
    var preventSelection = false;

    function addHandler(element, event, handler) {
        if (element.attachEvent)
            element.attachEvent('on' + event, handler);
        else
        if (element.addEventListener)
            element.addEventListener(event, handler, false);
    }

    function removeSelection() {
        if (window.getSelection) {
            window.getSelection().removeAllRanges();
        } else if (document.selection && document.selection.clear)
            document.selection.clear();
    }

    function killCtrlA(event) {
        var event = event || window.event;
        var sender = event.target || event.srcElement;

        if (sender.tagName.match(/INPUT|TEXTAREA/i))
            return;

        var key = event.keyCode || event.which;
        if (event.ctrlKey && key == 'A'.charCodeAt(0)) // 'A'.charCodeAt(0) можно заменить на 65
        {
            removeSelection();

            if (event.preventDefault)
                event.preventDefault();
            else
                event.returnValue = false;
        }
    }

    // не даем выделять текст мышкой
    addHandler(element, 'mousemove', function () {
        if (preventSelection)
            removeSelection();
    });
    addHandler(element, 'mousedown', function (event) {
        var event = event || window.event;
        var sender = event.target || event.srcElement;
        preventSelection = !sender.tagName.match(/INPUT|TEXTAREA/i);
    });

    // борем dblclick
    // если вешать функцию не на событие dblclick, можно избежать
    // временное выделение текста в некоторых браузерах
    addHandler(element, 'mouseup', function () {
        if (preventSelection)
            removeSelection();
        preventSelection = false;
    });

    // борем ctrl+A
    // скорей всего это и не надо, к тому же есть подозрение
    // что в случае все же такой необходимости функцию нужно 
    // вешать один раз и на document, а не на элемент
    addHandler(element, 'keydown', killCtrlA);
    addHandler(element, 'keyup', killCtrlA);
}
preventSelection(document);

export default {
    namespaced: true,

    state: () => ({
        clientsObject: null,

        typeStructured: [{
                id: 1,
                value: "Резерв1"
            },
            {
                id: 2,
                value: "Резерв2"
            },
            {
                id: 3,
                value: "Организация"
            },
            {
                id: 4,
                value: "Предприятие"
            },
            {
                id: 5,
                value: "Завод"
            },
            {
                id: 6,
                value: "Цех"
            },
            {
                id: 7,
                value: "Узел"
            },
            {
                id: 8,
                value: "Датчик"
            },
        ],
        typeStructuredTable: [{
                id: 1,
                key: 'reserves1',
                table: {
                    name: 'Название резерв1',
                },
            },
            {
                id: 2,
                key: 'reserves2',
                table: {
                    name: 'Название резерв2',
                    reserve1: 'Название резерв1',
                },
            },
            {
                id: 3,
                key: 'organisations',
                table: {
                    name: 'Название организации',
                    reserve1: 'Название резерв1',
                    reserve2: 'Название резерв2',
                },
            },
            {
                id: 4,
                key: 'companies',
                table: {
                    name: 'Название предприятие',
                    reserve1: 'Название резерв1',
                    reserve2: 'Название резерв2',
                    organisation: 'Название организации',
                },
            },
            {
                id: 5,
                key: 'factories',
                table: {
                    name: 'Название завод',
                    map: 'Местоположение',
                    reserve1: 'Название резерв1',
                    reserve2: 'Название резерв2',
                    organisation: 'Название организации',
                    company: 'Название предприятия',
                },
            },
            {
                id: 6,
                key: 'workshops',
                table: {
                    name: 'Название цех',
                    reserve1: 'Название резерв1',
                    reserve2: 'Название резерв2',
                    organisation: 'Название организации',
                    company: 'Название предприятия',
                    factory: 'Название завода',
                    smena: 'Смены',
                    break: 'Перерывы',
                },
            },
            {
                id: 7,
                key: 'knots',
                table: {
                    name: 'Название узел',
                    reserve1: 'Название резерв1',
                    reserve2: 'Название резерв2',
                    organisation: 'Название организации',
                    company: 'Название предприятия',
                    factory: 'Название завода',
                    workshop: 'Название цеха',
                },
            },
            {
                id: 8,
                key: 'sensors',
                table: {
                    name: 'Название датчик',
                    shema: 'Обозначение на схеме',
                    reserve1: 'Название резерв1',
                    reserve2: 'Название резерв2',
                    organisation: 'Название организации',
                    company: 'Название предприятия',
                    factory: 'Название завода',
                    workshop: 'Название цеха',
                    knot: 'Название узла',
                },
            },
            {
                id: 9,
                key: 'variables',
                table: {
                    name: 'Имя переменной',
                    connectOut: 'Соединение',
                    limits: 'Пределы',
                    sensor: 'Название датчика',
                    knot: 'Название узла',
                    workshop: 'Название цеха',
                    factory: 'Название завода',
                },
            },
        ],
        typeStructureTableKey: ['reserv1_id', 'reserv2_id', 'organisation_id', 'company_id', 'factory_id', 'workshop_id', 'knot_id','sensor_id','variable_id'],
        reserves1: [],
        reserves2: [],
        organisations: [],
        companies: [],
        factories: [],
        workshops: [],
        knots: [],
        sensors: [],
        variables: [],
        connection: [],
    }),
    getters: {
        typeStructuredTable(state) {
            return state.typeStructuredTable;
        },
        typeStructureTableKey(state) {
            return state.typeStructureTableKey;
        },

        clientsObject(state) {
            let clientsObject = state.clientsObject;
            //     if (!clientsObject) {
            //         // clientsObject = JSON.parse(localStorage.getItem('clientsObject'));
            //         // console.log(clientsObject);
            //         return state.clientsObject;                 
            // }

            // if (clientsObject) {
            //     return state.clientsObject;
            // };


            //
            if (!(clientsObject && state.typeStructured.length)) {
                // console.log(state.clientsObject);
                return state.clientsObject;
            }


            let newObj = JSON.parse(JSON.stringify(clientsObject));
            let newArr = [];
            clientsObject.currentStructureObject.forEach((id) => {
                try {
                    let fil = state.typeStructured.filter((item) => item.id === id)[0]
                    //console.log(fil);
                    newArr.push(fil);
                } catch (e) {
                    debugger
                }
            });

            newArr.push({
                id: 9,
                value: 'Переменные'
            });
            //console.log(newObj); 
            newObj.currentStructureObject = newArr;
            // console.log(newObj);
            return newObj;
        },

        typeStructured(state) {
            let array = [];
            array.push({
                id: 0,
                text: "Выбор типа узла",
                value: "",
                disabled: true,
            });

            state.typeStructured.forEach((item) => {
                array.push({
                    id: item.id,
                    text: item.value,
                    value: item.value,
                    disabled: false,
                });
            });

            return array;
        },
        reserves1(state) {
            let reserves1 = state.reserves1;
            // if (localStorage.getItem('reserves1'))
            //     reserves1 = JSON.parse(localStorage.getItem('reserves1'));

            return reserves1;
        },
        reserves2(state, getters) {
            let reserves2 = JSON.parse(JSON.stringify(state.reserves2));
            // if (localStorage.getItem('reserves2'))
            //     reserves2 = JSON.parse(localStorage.getItem('reserves2'));

            return reserves2.map(item => {
                let reserve1 = getters.reserves1.filter(i => i.id === item.reserv1_id);
                item.reserve1 = reserve1.length ? reserve1[0].name : "";

                return item;
            })
        },
        organisations(state, getters) {
            let organisations = JSON.parse(JSON.stringify(state.organisations));
            // if (localStorage.getItem('organisations'))
            //     organisations = JSON.parse(localStorage.getItem('organisations'));

            return organisations.map(item => {
                let reserve1 = getters.reserves1.filter(i => i.id === item.reserv1_id);
                item.reserve1 = reserve1.length ? reserve1[0].name : "";

                let reserve2 = getters.reserves2.filter(i => i.id === item.reserv2_id);
                item.reserve2 = reserve2.length ? reserve2[0].name : "";

                return item;
            })
        },
        companies(state, getters) {
            let companies = JSON.parse(JSON.stringify(state.companies));
            // if (localStorage.getItem('companies'))
            //     companies = JSON.parse(localStorage.getItem('companies'));

            return companies.map(item => {
                let reserve1 = getters.reserves1.filter(i => i.id === item.reserv1_id);
                item.reserve1 = reserve1.length ? reserve1[0].name : "";

                let reserve2 = getters.reserves2.filter(i => i.id === item.reserv2_id);
                item.reserve2 = reserve2.length ? reserve2[0].name : "";

                let organisation = getters.organisations.filter(i => i.id === item.organisation_id);
                item.organisation = organisation.length ? organisation[0].name : "";

                return item;
            })
        },
        factories(state, getters) {
            let factories = JSON.parse(JSON.stringify(state.factories));
            // if (localStorage.getItem('factories'))
            //     factories = JSON.parse(localStorage.getItem('factories'));

            return factories.map(item => {
                let reserve1 = getters.reserves1.filter(i => i.id === item.reserv1_id);
                item.reserve1 = reserve1.length ? reserve1[0].name : "";

                let reserve2 = getters.reserves2.filter(i => i.id === item.reserv2_id);
                item.reserve2 = reserve2.length ? reserve2[0].name : "";

                let organisation = getters.organisations.filter(i => i.id === item.organisation_id);
                item.organisation = organisation.length ? organisation[0].name : "";

                let company = getters.companies.filter(i => i.id === item.company_id);
                item.company = company.length ? company[0].name : "";

                return item;
            })
        },
        workshops(state, getters) {
            let workshops = state.workshops;
            // if (localStorage.getItem('workshops'))
            //     workshops = JSON.parse(localStorage.getItem('workshops'));

            let newObj = JSON.parse(JSON.stringify(workshops));
            // let factories = JSON.parse(JSON.stringify(getters.factories));

            newObj.map((item) => {
                let breaks = [];
                let smenas = [];

                if (Array.isArray(item.ranges)) {
                    item.ranges.filter(item => item.is_active).forEach(el => {
                        smenas.push((el.start + '-' + el.end).replace(':', '.'));
                        el.breaks.filter(e => e.is_active).forEach(b => breaks.push((b.start + '-' + b.end).replace(':', '.')));
                    });
                };

                let reserve1 = getters.reserves1.filter(i => i.id === item.reserv1_id);
                item.reserve1 = reserve1.length ? reserve1[0].name : "";

                let reserve2 = getters.reserves2.filter(i => i.id === item.reserv2_id);
                item.reserve2 = reserve2.length ? reserve2[0].name : "";

                let organisation = getters.organisations.filter(i => i.id === item.organisation_id);
                item.organisation = organisation.length ? organisation[0].name : "";

                let company = getters.companies.filter(i => i.id === item.company_id);
                item.company = company.length ? company[0].name : "";

                let factory = getters.factories.filter(i => i.id === item.factory_id);
                item.factory = factory.length ? factory[0].name : "";

                item.smena = smenas.join(';');
                item.break = breaks.join(';');

                return item;
            });

            return newObj;
        },
        knots(state, getters) {
            let knots = JSON.parse(JSON.stringify(state.knots));
            // if (localStorage.getItem('knots'))
            //     knots = JSON.parse(localStorage.getItem('knots'));

            return knots.map(item => {
                let factories = getters.factories.filter(i => i.id === item.factory_id);
                let workshops = getters.workshops.filter(i => i.id === item.workshop_id);

                let reserve1 = getters.reserves1.filter(i => i.id === item.reserv1_id);
                item.reserve1 = reserve1.length ? reserve1[0].name : "";

                let reserve2 = getters.reserves2.filter(i => i.id === item.reserv2_id);
                item.reserve2 = reserve2.length ? reserve2[0].name : "";

                let organisation = getters.organisations.filter(i => i.id === item.organisation_id);
                item.organisation = organisation.length ? organisation[0].name : "";

                let company = getters.companies.filter(i => i.id === item.company_id);
                item.company = company.length ? company[0].name : "";

                item.factory = factories.length ? factories[0].name : "";
                item.workshop = workshops.length ? workshops[0].name : "";

                return item;
            })
        },
        sensors(state, getters) {
            let sensors = JSON.parse(JSON.stringify(state.sensors));
            // if (localStorage.getItem('sensors'))
            //     sensors = JSON.parse(localStorage.getItem('sensors'));

            return sensors.map(item => {
                let factories = getters.factories.filter(i => i.id === item.factory_id);
                let knots = getters.knots.filter(i => i.id === item.knot_id);
                let workshops = getters.workshops.filter(i => i.id === item.workshop_id);

                let reserve1 = getters.reserves1.filter(i => i.id === item.reserv1_id);
                item.reserve1 = reserve1.length ? reserve1[0].name : "";

                let reserve2 = getters.reserves2.filter(i => i.id === item.reserv2_id);
                item.reserve2 = reserve2.length ? reserve2[0].name : "";

                let organisation = getters.organisations.filter(i => i.id === item.organisation_id);
                item.organisation = organisation.length ? organisation[0].name : "";

                let company = getters.companies.filter(i => i.id === item.company_id);
                item.company = company.length ? company[0].name : "";

                item.factory = factories.length ? factories[0].name : "";
                item.workshop = workshops.length ? workshops[0].name : "";
                item.knot = knots.length ? knots[0].name : "";

                return item;
            })
        },
        variables(state, getters) {
            let variables = JSON.parse(JSON.stringify(state.variables));
            // if (localStorage.getItem('variables'))
            //     variables = JSON.parse(localStorage.getItem('variables'));

            return variables.map(item => {
                let sensors = getters.sensors.filter(i => i.id === item.sensor_id);
                let knots = getters.knots.filter(i => i.id === item.knot_id);
                let workshops = getters.workshops.filter(i => i.id === item.workshop_id);
                let factories = getters.factories.filter(i => i.id === item.factory_id);
                // console.log(item.connect);
                item.connectOut = `${item.connect}\n${item.variablee}`; //.split(",").join("\n");
                item.limits = `Верхн.измерения = ${item.limitMaxWarn}${item.unit}\nНижн.измерения = ${item.limitMinWarn}${item.unit}\nВерхн.аварийный = ${item.limitMaxСrash}${item.unit}\nНижн.аварийный = ${item.limitMinСrash}${item.unit}\nСкорость изм. = ${item.limitSpead}`;

                item.sensor = sensors.length ? sensors[0].name : "Название датчика";
                item.knot = knots.length ? knots[0].name : "Название узла";
                item.workshop = workshops.length ? workshops[0].name : "Название цеха";
                item.factory = factories.length ? factories[0].name : "Название завода";


                return item;
            })
        },
        connection(state, getters) {
            let connection = JSON.parse(JSON.stringify(state.connection));
            // if (localStorage.getItem('variables'))
            //     variables = JSON.parse(localStorage.getItem('variables'));
            return connection;
        },

    },
    mutations: {
        setClientsObject(state, data) { //выполнение обновление DOM Объект
            let temp_data;
            if (data.result != "empty") {
                temp_data = data;
                temp_data.currentStructureObject = [];
                temp_data.date_add = new Date(temp_data.date_add).toLocaleString();
                temp_data.date_update = new Date(temp_data.date_update).toLocaleString();
                let k = 0;
                for (let a in data.structure) {
                    temp_data.currentStructureObject[k] = data.structure[a] + 1;
                    k++;
                }
                delete temp_data.structure;
                state.clientsObject = temp_data;
            }
        },
        deleteClientObject(state, data) { //мутация на удаление всего объекта
            if (typeof data.result == "string") {
                // console.log(data.result);
                state.clientsObject = null;
            }
        },

        openReserve1(state, option) { //мутация на заполнение таблицы Резерв 1 при открытии окна настроек
            state.reserves1 = option;
        },
        openReserve2(state, option) { //мутация на заполнение таблицы Резерв 2 при открытии окна настроек
            state.reserves2 = option;
        },
        openOrganization(state, option) { //мутация на заполнение таблицы Организация при открытии окна настроек
            state.organisations = option;
        },
        openСompany(state, option) { //мутация на заполнение таблицы Предприятие при открытии окна настроек
            state.companies = option;
        },
        openFactory(state, option) { //мутация на заполнение таблицы Завод при открытии окна настроек
            state.factories = option;
        },
        openWorkshop(state, option) { //мутация на заполнение таблицы Цех при открытии окна настроек
            state.workshops = option;
        },
        openKnot(state, option) { //мутация на заполнение таблицы Цех при открытии окна настроек
            state.knots = option;
        },
        openSensor(state, option) { //мутация на заполнение таблицы Цех при открытии окна настроек
            state.sensors = option;
        },
        openVariable(state, option) { //мутация на заполнение таблицы Цех при открытии окна настроек
            state.variables = option;
        },


        setReserve1(state, option) { //мутация на добавление и обновление данных в таблице Резерв1 в окне настроек

            let reserves1 = [];

            if (state.reserves1.length != 0) {
                let fIndex = state.reserves1.findIndex((item) => {
                    return (item.id == option.id)
                });
                reserves1 = state.reserves1;
                if (fIndex != -1) {
                    reserves1[fIndex].name = option.name;
                } else {
                    reserves1.push(option);
                }

            } else {
                if (Array.isArray(option)) {
                    reserves1 = option;
                } else {
                    reserves1.push(option);
                }
            }
            // console.log(JSON.parse(JSON.stringify(option)));
            //JSON.parse(localStorage.getItem('reserves1'));
            // if (option.id && reserves1.filter(item => item.id === option.id).length)
            //     for (let key in reserves1.filter(item => item.id === option.id)[0])
            //         reserves1.filter(item => item.id === option.id)[0][key] = option[key];
            // else
            // console.log(reserves1);
            state.reserves1 = reserves1;
        },
        setReserve2(state, option) { //мутация на добавление и обновление данных в таблице Резерв2 в окне настроек
            // let reserves2 = JSON.parse(localStorage.getItem('reserves2'));
            // if (option.id && reserves2.filter(item => item.id === option.id).length)
            //     for (let key in reserves2.filter(item => item.id === option.id)[0])
            //         reserves2.filter(item => item.id === option.id)[0][key] = option[key];
            // else
            //     reserves2.push(option);

            // state.reserves2 = reserves2;
            // debugger;
            let reserves2 = [];

            option.reserv1_id = option.parents.id;

            delete option.parent;
            delete option.parents;

            if (state.reserves2.length != 0) {
                let fIndex = state.reserves2.findIndex((item) => {
                    return (item.id == option.id)
                });
                reserves2 = state.reserves2;
                if (fIndex != -1) {
                    reserves2[fIndex].name = option.name;
                    reserves2[fIndex].reserv1_id = option.reserv1_id;
                } else {
                    reserves2.push(option);
                }

            } else {
                if (Array.isArray(option)) {
                    reserves2 = option;
                } else {
                    reserves2.push(option);
                }
            }

            state.reserves2 = reserves2;
        },
        setOrganization(state, option) { //мутация на добавление и обновление данных в таблице Организация в окне настроек
            // let reserves2 = JSON.parse(localStorage.getItem('reserves2'));
            // if (option.id && reserves2.filter(item => item.id === option.id).length)
            //     for (let key in reserves2.filter(item => item.id === option.id)[0])
            //         reserves2.filter(item => item.id === option.id)[0][key] = option[key];
            // else
            //     reserves2.push(option);

            // state.reserves2 = reserves2;
            // debugger;
            let organisations = [];

            option.reserv2_id = option.parents.id;
            option.reserv1_id = option.parents.parents.id;

            delete option.parent;
            delete option.parents;

            if (state.organisations.length != 0) {
                let fIndex = state.organisations.findIndex((item) => {
                    return (item.id == option.id)
                });
                organisations = state.organisations;
                if (fIndex != -1) {
                    organisations[fIndex].name = option.name;
                    organisations[fIndex].reserv1_id = option.reserv1_id;
                    organisations[fIndex].reserv2_id = option.reserv2_id;
                } else {
                    organisations.push(option);
                }

            } else {
                if (Array.isArray(option)) {
                    organisations = option;
                } else {
                    organisations.push(option);
                }
            }

            state.organisations = organisations;
        },
        setCompanies(state, option) { //мутация на добавление и обновление данных в таблице Предприятие в окне настроек
            let companies = [];
            // let companies = JSON.parse(localStorage.getItem('companies'));
            // if (option.id && companies.filter(item => item.id === option.id).length)
            //     for (let key in companies.filter(item => item.id === option.id)[0])
            //         companies.filter(item => item.id === option.id)[0][key] = option[key];
            // else
            //     companies.push(option);
            option.organisation_id = option.parents.id;
            option.reserv2_id = option.parents.parents.id;
            option.reserv1_id = option.parents.parents.parents.id;

            delete option.parent;
            delete option.parents;

            if (state.companies.length != 0) {
                let fIndex = state.companies.findIndex((item) => {
                    return (item.id == option.id)
                });
                companies = state.companies;
                if (fIndex != -1) {
                    companies[fIndex].name = option.name;
                    companies[fIndex].reserv1_id = option.reserv1_id;
                    companies[fIndex].reserv2_id = option.reserv2_id;
                    companies[fIndex].organisation_id = option.organisation_id;
                } else {
                    companies.push(option);
                }

            } else {
                if (Array.isArray(option)) {
                    companies = option;
                } else {
                    companies.push(option);
                }
            }
            state.companies = companies;
        },
        setFactories(state, option) { //мутация на добавление и обновление данных в таблице Завод в окне настроек

            // let factories = JSON.parse(localStorage.getItem('factories'));
            // if (option.id && factories.filter(item => item.id === option.id).length)
            //     for (let key in factories.filter(item => item.id === option.id)[0])
            //         factories.filter(item => item.id === option.id)[0][key] = option[key];
            // else
            //     factories.push(option);
            // debugger;
            let factories = [];
            option.company_id = option.parents.id;
            option.organisation_id = option.parents.parents.id;
            option.reserv2_id = option.parents.parents.parents.id;
            option.reserv1_id = option.parents.parents.parents.parents.id;
            option.map = option.address;

            delete option.address;
            delete option.parent;
            delete option.parents;

            if (state.factories.length != 0) {
                let fIndex = state.factories.findIndex((item) => {
                    return (item.id == option.id)
                });
                factories = state.factories;
                if (fIndex != -1) {
                    factories[fIndex].name = option.name;
                    factories[fIndex].reserv1_id = option.reserv1_id;
                    factories[fIndex].reserv2_id = option.reserv2_id;
                    factories[fIndex].organisation_id = option.organisation_id;
                    factories[fIndex].company_id = option.company_id;
                    factories[fIndex].map = option.map;
                } else {
                    factories.push(option);
                }

            } else {
                if (Array.isArray(option)) {
                    factories = option;
                } else {
                    factories.push(option);
                }
            }
            state.factories = factories;
        },
        setWorkshop(state, option) { //мутация на добавление и обновление данных в таблице Цех в окне настроек

            // let workshops = JSON.parse(localStorage.getItem('workshops'));
            // if (option.id && workshops.filter(item => item.id === option.id).length)
            //     for (let key in workshops.filter(item => item.id === option.id)[0])
            //         workshops.filter(item => item.id === option.id)[0][key] = option[key];
            // else
            //     workshops.push(option);
            let workshops = [];
            // option.company_id = option.parents.id;
            // option.organisation_id = option.parents.parents.id;
            // option.reserv2_id = option.parents.parents.parents.id;
            // option.reserv1_id = option.parents.parents.parents.parents.id;
            // option.map = option.address;

            // delete option.address;
            // delete option.parent;
            // delete option.parents;

            { //подготавливаем массив для отображения
                let emptyRanges = {
                    start: null,
                    end: null,
                    is_active: null,
                    showBreaks: false,
                    breaks: [{
                            start: null,
                            end: null,
                            is_active: false,
                        },
                        {
                            start: null,
                            end: null,
                            is_active: false,
                        },
                        {
                            start: null,
                            end: null,
                            is_active: false,
                        },
                        {
                            start: null,
                            end: null,
                            is_active: false,
                        },
                    ],
                };
                let emptyBreaks = {
                    start: null,
                    end: null,
                    is_active: false,
                };

                let ranges = [];
                option.factory_id = option.parents.id;
                option.company_id = option.parents.parents.id;
                option.organisation_id = option.parents.parents.parents.id;
                option.reserv2_id = option.parents.parents.parents.parents.id;
                option.reserv1_id = option.parents.parents.parents.parents.parents.id;


                // console.log(item.shifts);

                // item.ranges = item.shifts;

                if (Array.isArray(option.shifts)) {
                    option.shifts.forEach((item2, i) => {
                        let breaks = [];
                        let lenghtLunchs = option.shifts[i].lunchs.length;

                        option.shifts[i].lunchs.forEach((item3) => {
                            breaks.push({
                                start: item3.start.slice(0, 5),
                                end: item3.end.slice(0, 5),
                                is_active: true,
                                id: item3.id,
                            })
                        });

                        for (let ii = 0; ii <= (3 - lenghtLunchs); ii++) {
                            breaks.push(emptyBreaks);
                        }


                        ranges.push({
                            start: item2.start.slice(0, 5),
                            end: item2.end.slice(0, 5),
                            showBreaks: false,
                            is_active: true,
                            breaks: breaks,
                            id: item2.id,
                        });


                    });
                } else {
                    for (let j = 0; j <= 3; j++) {
                        ranges.push(emptyRanges);
                    }
                }

                let lenghtRanges = option.shifts.length;
                for (let kk = 0; kk <= (3 - lenghtRanges); kk++) {
                    ranges.push(emptyRanges);
                }

                option.ranges = ranges;

                delete option.shifts;
                delete option.parent;
                delete option.parents;

            }



            if (state.workshops.length != 0) {
                let fIndex = state.workshops.findIndex((item) => {
                    return (item.id == option.id)
                });
                workshops = state.workshops;
                if (fIndex != -1) {
                    workshops[fIndex].name = option.name;
                    workshops[fIndex].reserv1_id = option.reserv1_id;
                    workshops[fIndex].reserv2_id = option.reserv2_id;
                    workshops[fIndex].organisation_id = option.organisation_id;
                    workshops[fIndex].company_id = option.company_id;
                    workshops[fIndex].factory_id = option.factory_id;
                    workshops[fIndex].ranges = option.ranges;

                } else {
                    workshops.push(option);
                }

            } else {
                if (Array.isArray(option)) {
                    workshops = option;
                } else {
                    workshops.push(option);
                }
            }

            state.workshops = workshops;
        },
        setKnots(state, option) { //мутация на добавление и обновление данных в таблице Узел в окне настроек

            // let knots = JSON.parse(localStorage.getItem('knots'));
            // if (option.id && knots.filter(item => item.id === option.id).length)
            //     for (let key in knots.filter(item => item.id === option.id)[0])
            //         knots.filter(item => item.id === option.id)[0][key] = option[key];
            // else
            //     knots.push(option);
            let knots = [];
            option.workshop_id = option.parents.id;
            option.factory_id = option.parents.parents.id;
            option.company_id = option.parents.parents.parents.id;
            option.organisation_id = option.parents.parents.parents.parents.id;
            option.reserv2_id = option.parents.parents.parents.parents.parents.id;
            option.reserv1_id = option.parents.parents.parents.parents.parents.parents.id;

            delete option.parent;
            delete option.parents;

            if (state.knots.length != 0) {
                let fIndex = state.knots.findIndex((item) => {
                    return (item.id == option.id)
                });
                knots = state.knots;
                if (fIndex != -1) {
                    knots[fIndex].name = option.name;
                    knots[fIndex].reserv1_id = option.reserv1_id;
                    knots[fIndex].reserv2_id = option.reserv2_id;
                    knots[fIndex].organisation_id = option.organisation_id;
                    knots[fIndex].company_id = option.company_id;
                    knots[fIndex].factory_id = option.factory_id;
                    knots[fIndex].workshop_id = option.workshop_id;
                } else {
                    knots.push(option);
                }

            } else {
                if (Array.isArray(option)) {
                    knots = option;
                } else {
                    knots.push(option);
                }
            }
            state.knots = knots;
        },
        setSensors(state, option) { //мутация на добавление и обновление данных в таблице Датчик в окне настроек
            // let sensors = JSON.parse(localStorage.getItem('sensors'));
            // if (option.id && sensors.filter(item => item.id === option.id).length)
            //     for (let key in sensors.filter(item => item.id === option.id)[0])
            //         sensors.filter(item => item.id === option.id)[0][key] = option[key];
            // else
            //     sensors.push(option);
            let sensors = [];

            option.knot_id = option.parents.id;
            option.workshop_id = option.parents.parents.id;
            option.factory_id = option.parents.parents.parents.id;
            option.company_id = option.parents.parents.parents.parents.id;
            option.organisation_id = option.parents.parents.parents.parents.parents.id;
            option.reserv2_id = option.parents.parents.parents.parents.parents.parents.id;
            option.reserv1_id = option.parents.parents.parents.parents.parents.parents.parents.id;
            option.shema = option.designation;

            delete option.designation;
            delete option.parent;
            delete option.parents;

            if (state.sensors.length != 0) {
                let fIndex = state.sensors.findIndex((item) => {
                    return (item.id == option.id)
                });
                sensors = state.sensors;
                if (fIndex != -1) {
                    sensors[fIndex].name = option.name;
                    sensors[fIndex].reserv1_id = option.reserv1_id;
                    sensors[fIndex].reserv2_id = option.reserv2_id;
                    sensors[fIndex].organisation_id = option.organisation_id;
                    sensors[fIndex].company_id = option.company_id;
                    sensors[fIndex].factory_id = option.factory_id;
                    sensors[fIndex].workshop_id = option.workshop_id;
                    sensors[fIndex].knot_id = option.knot_id;

                    sensors[fIndex].shema = option.shema;
                } else {
                    sensors.push(option);
                }

            } else {
                if (Array.isArray(option)) {
                    sensors = option;
                } else {
                    sensors.push(option);
                }
            }
            state.sensors = sensors;
        },
        setVariables(state, option) { //мутация на добавление и обновление данных в таблице Переменная в окне настроек
            // let variables = JSON.parse(localStorage.getItem('variables'));
            // if (option.id && variables.filter(item => item.id === option.id).length)
            //     for (let key in variables.filter(item => item.id === option.id)[0])
            //         variables.filter(item => item.id === option.id)[0][key] = option[key];
            // else
            //     variables.push(option);

            // state.variables = variables;
            let variables = [];

            option.sensor_id = option.parents.id;
            option.knot_id = option.parents.parents.id;
            option.workshop_id = option.parents.parents.parents.id;
            option.factory_id = option.parents.parents.parents.parents.id;
            option.company_id = option.parents.parents.parents.parents.parents.id;
            option.organisation_id = option.parents.parents.parents.parents.parents.parents.id;
            option.reserv2_id = option.parents.parents.parents.parents.parents.parents.parents.id;
            option.reserv1_id = option.parents.parents.parents.parents.parents.parents.parents.parents.id;


            option.connect = option.name_connection;

            option.limitMaxWarn = option.up_level;
            option.limitMinWarn = option.down_level;
            option.limitMaxСrash = option.up_level_alarm;
            option.limitMinСrash = option.down_level_alarm;
            option.limitSpead = option.rate_change;
            option.variablee = "Var: " + option.table_name.slice(option.table_name.indexOf(option.name_connection) + option.name_connection.length + 1, option.table_name.length);

            delete option.name_connection;
            delete option.up_level;
            delete option.down_level;
            delete option.up_level_alarm;
            delete option.down_level_alarm;
            delete option.rate_change;
            // delete option.table_name;
            delete option.department_name;
            delete option.factory_name;
            delete option.sensor_name;
            delete option.uzel_name;
            delete option.sensor;
            delete option.parent;
            delete option.parents;

            console.log(option);
            if (state.variables.length != 0) {
                let fIndex = state.variables.findIndex((item) => {
                    return (item.id == option.id)
                });
                variables = state.variables;
                if (fIndex != -1) {

                    variables[fIndex].name = option.name;
                    variables[fIndex].reserv1_id = option.reserv1_id;
                    variables[fIndex].reserv2_id = option.reserv2_id;
                    variables[fIndex].organisation_id = option.organisation_id;
                    variables[fIndex].company_id = option.company_id;
                    variables[fIndex].factory_id = option.factory_id;
                    variables[fIndex].workshop_id = option.workshop_id;
                    variables[fIndex].knot_id = option.knot_id;
                    variables[fIndex].sensor_id = option.sensor_id;
                    variables[fIndex].unit = option.unit;
                    variables[fIndex].connect = option.connect;
                    variables[fIndex].limitMaxWarn = option.limitMaxWarn;
                    variables[fIndex].limitMinWarn = option.limitMinWarn;
                    variables[fIndex].limitMaxСrash = option.limitMaxСrash;
                    variables[fIndex].limitMinСrash = option.limitMinСrash;
                    variables[fIndex].limitSpead = option.limitSpead;
                    variables[fIndex].variablee = option.variablee;
                    variables[fIndex].table_name = option.table_name;

                } else {
                    variables.push(option);
                }

            } else {
                if (Array.isArray(option)) {
                    variables = option;
                } else {
                    variables.push(option);
                }
            }
            state.variables = variables;
        },
        setDataConnection(state, option) { //заполнение списка Соединений
            state.connection = option;
        },
        setDataConnectionTags(state, option) { //заполнение списка Переменных
            // data:arrCoonnect[0].tags,id:option.id
            state.connection[option.id].tags = option.data;
            // console.log(state.connection);
        },



        setTypeStructured(state, data) {
            state.typeStructured = data;
        },
        deleteTypeStructuredTable(state, option) { //мутация на удаление строк из таблиц в окне настроек
            // debugger;

            try {
                let ind = state[option.tabName].findIndex((item) => {
                    return (item.id == option.id);
                })
                // let newArr = state[option.tabName];
                // newArr.splice(ind,1);   
                //     state[option.tabName] = newArr;
                state[option.tabName].splice(ind, 1);
            } catch (e) {
                console.log(e);
            }
        },
        setTypeStructuredTable(state, option) {
            state.typeStructuredTable.filter((item => item.id === option.id))[0].data.rows.push(option.data);
        },


    },
    actions: {
        async updateClientsObject(store, option) {
            let data = {
                name: option.currentProject.projectName,
                customer: option.currentProject.clientName,
                contract: option.currentProject.clientContract,
                structure: {},
            };

            option.currentStructureObject.forEach((el, i, arr) => {
                data.structure["levlel_" + i] = el - 1;
            })


            await this.$axios.$post(`/settings/wizard/step1/`, data)
                .then(function () {
                    store.dispatch("getDataTableCustom");
                })
                .catch(function (e) {
                    console.error(e);
                });
            // localStorage.setItem('clientsObject', JSON.stringify(data));


        },

        async delClientsObject(store) { //Удаление целого объекта из базы
            await this.$axios.$delete(`/settings/delete_structure/`)
                .then(function (data) {
                    store.commit('deleteClientObject', data);
                })
                .catch(function (e) {
                    console.log(e);
                });


            // localStorage.setItem('clientsObject', null);
            // store.commit('setClientsObject', null);

            // localStorage.setItem('reserves1', JSON.stringify([]));
            // store.commit('deleteReserves1', null);

            // localStorage.setItem('reserves2', JSON.stringify([]));
            // store.commit('deleteReserves2', null);

            // localStorage.setItem('organisations', JSON.stringify([]));
            // store.commit('deleteOrganisations', null);

            // localStorage.setItem('companies', JSON.stringify([]));
            // store.commit('deleteCompanies', null);

            // localStorage.setItem('factories', JSON.stringify([]));
            // store.commit('deleteFactories', null);

            // localStorage.setItem('workshops', JSON.stringify([]));
            // store.commit('deleteWorkshops', null);

            // localStorage.setItem('knots', JSON.stringify([]));
            // store.commit('deleteKnots', null);

            // localStorage.setItem('sensors', JSON.stringify([]));
            // store.commit('deleteSensors', null);

            // localStorage.setItem('variables', JSON.stringify([]));
            // store.commit('deleteVariables', null);
        },
        getTypeStructured(store) {
            let data = [{
                    id: 1,
                    value: "Резерв1"
                },
                {
                    id: 2,
                    value: "Резерв2"
                },
                {
                    id: 3,
                    value: "Организация"
                },
                {
                    id: 4,
                    value: "Предприятие"
                },
                {
                    id: 5,
                    value: "Завод"
                },
                {
                    id: 6,
                    value: "Цех"
                },
                {
                    id: 7,
                    value: "Узел"
                },
                {
                    id: 8,
                    value: "Датчик"
                },
            ];
            store.commit('setTypeStructured', data);
        },
        updateTypeStructuredTable(store, option) {
            store.commit('setTypeStructuredTable', option);
        },
        async deleteTypeStructuredTable(store, option) { //Удаление строк из таблиц
            if (!option.id || !option.tab)
                return;

            let data = [{
                    id: 1,
                    valueUrl: "/structure/Reserv_1/",
                    value: "reserves1"
                },
                {
                    id: 2,
                    valueUrl: "/structure/Reserv_2/",
                    value: "reserves2"
                },
                {
                    id: 3,
                    valueUrl: "/structure/Corparation/",
                    value: "organisations"
                },
                {
                    id: 4,
                    valueUrl: "/structure/Company/",
                    value: "companies"
                },
                {
                    id: 5,
                    valueUrl: "/structure/Factory/",
                    value: "factories"
                },
                {
                    id: 6,
                    valueUrl: "/structure/Department/",
                    value: "workshops"
                },
                {
                    id: 7,
                    valueUrl: "/structure/Agreagat/",
                    value: "knots"
                },
                {
                    id: 8,
                    valueUrl: "/structure/Sensors/",
                    value: "sensors"
                },
                {
                    id: 9,
                    valueUrl: "/recorder/structure/ValueSensor/",
                    value: "variables"
                },
            ];

            let tabName = "";
            try {
                tabName = data.filter(item => item.id === option.tab);
                if (tabName) {
                    // tabName = tabName[0].value;
                    await this.$axios.$delete(`${tabName[0].valueUrl}${option.id}`)
                        .then((data) => {
                            // console.log(data);
                            option.tabName = tabName[0].value;
                            // option.array = newArrayLocal;
                            store.commit('deleteTypeStructuredTable', option);
                        })
                        .catch((e) => {
                            console.log(e);
                        });
                } else
                    return;
            } catch (e) {
                return;
            }

            // let newArrayLocal = [];

            // if (localStorage.getItem(tabName)) {
            //     JSON.parse(localStorage.getItem(tabName)).forEach(function (item, index, array) {
            //         if (item.id !== option.id)
            //             newArrayLocal.push(item)
            //     });
            //     localStorage.setItem(tabName, JSON.stringify(newArrayLocal));
            // }



        },

        //Решение добавлять ли Parent


        // ОБНОВЛЕНИЕ ДАННЫХ В ТАБЛИЦАХ
        async updateReserve1(store, option) { //Обновление, добавление Резерва1 в базу
            let name = {
                name: option.name
            };
            if (!option.id) {

                await this.$axios.$post(`/structure/Reserv_1/`, name)
                    .then(function (data) {
                        store.commit('setReserve1', data);
                        // console.log(e);
                        // store.commit('setReserve1', option);
                    })
                    .catch(function (error) {
                        console.error(error);
                    });
            } else {
                await this.$axios.$put(`/structure/Reserv_1/${option.id}/`, name)
                    .then(function (data) {
                        store.commit('setReserve1', data);
                        // console.log(e);
                        // store.commit('setReserve1', option);
                    })
                    .catch(function (error) {
                        console.error(error);
                    });
            }

        },
        async updateReserve2(store, option) { //Обновление, добавление Резерва2 в базу

            let name = {
                name: option.name,
            };

            {//? изолировал чтобы можно было свернуть
                let type = store.state.typeStructured[1].id; //этличается от того что показывает vue плагин в chrome
                let indexNum = store.state.clientsObject.currentStructureObject.findIndex((el, i) => {
                    return el == type;
                });

                if (indexNum != -1 && indexNum != 0) { //&& !option.id) { //подкидываем parent от предыдущего элемента структуры
                    name.parent = option[store.state.typeStructureTableKey[store.state.clientsObject.currentStructureObject[indexNum - 1] - 1]];
                }
            }


            if (!option.id) {
                await this.$axios.$post(`/structure/Reserv_2/`, name)
                    .then(function (data) {
                        store.commit('setReserve2', data);
                        // console.log(e);
                        // store.commit('setReserve1', option);
                    })
                    .catch(function (error) {
                        console.error(error);
                    });
            } else {

                await this.$axios.$put(`/structure/Reserv_2/${option.id}/`, name)
                    .then(function (data) {
                        store.commit('setReserve2', data);
                        // console.log(e);
                        // store.commit('setReserve1', option);
                    })
                    .catch(function (error) {
                        console.error(error);
                    });
            }

        },
        async updateOrganisation(store, option) { //Обновление, добавление Организации в базу
            
            let name = {
                name: option.name,
                //parent: option.reserv1_id,
            };


            {//? изолировал чтобы можно было свернуть
                let type = store.state.typeStructured[2].id; //этличается от того что показывает vue плагин в chrome
                let indexNum = store.state.clientsObject.currentStructureObject.findIndex((el, i) => {
                    return el == type;
                });

                if (indexNum != -1 && indexNum != 0) { //&& !option.id) { //подкидываем parent от предыдущего элемента структуры
                    name.parent = option[store.state.typeStructureTableKey[store.state.clientsObject.currentStructureObject[indexNum - 1] - 1]];
                }
            }

            if (!option.id) {
                await this.$axios.$post(`/structure/Corparation/`, name)
                    .then(function (data) {
                        store.commit('setOrganization', data);
                        // console.log(e);
                        // store.commit('setReserve1', option);
                    })
                    .catch(function (error) {
                        console.error(error);
                    });
            } else {
                await this.$axios.$put(`/structure/Corparation/${option.id}/`, name)
                    .then(function (data) {
                        store.commit('setOrganization', data);
                        // console.log(e);
                        // store.commit('setReserve1', option);
                    })
                    .catch(function (error) {
                        console.error(error);
                    });
            }
        },
        async updateCompanies(store, option) {
            
            let name = {
                name: option.name,
                // parent: option.organisation_id,
            };

            {//? изолировал чтобы можно было свернуть
                let type = store.state.typeStructured[3].id; //этличается от того что показывает vue плагин в chrome
                let indexNum = store.state.clientsObject.currentStructureObject.findIndex((el, i) => {
                    return el == type;
                });

                if (indexNum != -1 && indexNum != 0) { //&& !option.id) { //подкидываем parent от предыдущего элемента структуры
                    name.parent = option[store.state.typeStructureTableKey[store.state.clientsObject.currentStructureObject[indexNum - 1] - 1]];
                }
            }

            if (!option.id) {
                await this.$axios.$post(`/structure/Company/`, name)
                    .then(function (data) {
                        store.commit('setCompanies', data);
                        // console.log(e);
                        // store.commit('setReserve1', option);
                    })
                    .catch(function (error) {
                        console.error(error);
                    });
            } else {
                await this.$axios.$put(`/structure/Company/${option.id}/`, name)
                    .then(function (data) {
                        store.commit('setCompanies', data);
                        // console.log(e);
                        // store.commit('setReserve1', option);
                    })
                    .catch(function (error) {
                        console.error(error);
                    });
            }
        },
        async updateFactories(store, option) {
            
            let name = {
                name: option.name,
                // parent: option.company_id,
                address: option.map,
            };

            {//? изолировал чтобы можно было свернуть
                let type = store.state.typeStructured[4].id; //этличается от того что показывает vue плагин в chrome
                let indexNum = store.state.clientsObject.currentStructureObject.findIndex((el, i) => {
                    return el == type;
                });

                if (indexNum != -1 && indexNum != 0) { //&& !option.id) { //подкидываем parent от предыдущего элемента структуры
                    name.parent = option[store.state.typeStructureTableKey[store.state.clientsObject.currentStructureObject[indexNum - 1] - 1]];
                }
            }


            if (!option.id) {
                await this.$axios.$post(`/structure/Factory/`, name)
                    .then(function (data) {
                        store.commit('setFactories', data);
                        // console.log(e);
                        // store.commit('setReserve1', option);
                    })
                    .catch(function (error) {
                        console.error(error);
                    });
            } else {
                await this.$axios.$put(`/structure/Factory/${option.id}/`, name)
                    .then(function (data) {
                        store.commit('setFactories', data);
                        // console.log(e);
                        // store.commit('setReserve1', option);
                    })
                    .catch(function (error) {
                        console.error(error);
                    });
            }
        },
        async updateWorkshop(store, option) {
            let shifts = [];

            let name = {
                name: option.name,
                // parent: option.factory_id,
            };

            {//? изолировал чтобы можно было свернуть
                let type = store.state.typeStructured[5].id; //этличается от того что показывает vue плагин в chrome
                let indexNum = store.state.clientsObject.currentStructureObject.findIndex((el, i) => {
                    return el == type;
                });

                if (indexNum != -1 && indexNum != 0) { //&& !option.id) { //подкидываем parent от предыдущего элемента структуры
                    name.parent = option[store.state.typeStructureTableKey[store.state.clientsObject.currentStructureObject[indexNum - 1] - 1]];
                }
            }


            let k = 0; //счетчик числа перерывов
            option.ranges.forEach((item) => { //пробегаем по сменам
                if (item.is_active) {
                    let preObj = {
                        start: item.start + ":00",
                        end: item.end + ":00",
                        lanch: [],
                    };
                    if (item.id) {
                        preObj.id = item.id;
                    }

                    shifts.push(preObj);

                    item.breaks.forEach((item2) => { //пробегаем по перерывам в сменах
                        if (item2.is_active) {
                            let preObj2 = {
                                start: item2.start + ":00",
                                end: item2.end + ":00"
                            };
                            if (item2.id) {
                                preObj2.id = item2.id;
                            }
                            shifts[k].lanch.push(preObj2)
                        };
                    });
                    k++;
                }
            })
            name.shifts = shifts;

            // console.log(name);

            if (!option.id) {
                await this.$axios.$post(`/settings/create/department/`, name)
                    .then(function (data) {
                        console.log(data);
                        store.commit('setWorkshop', data);

                        // store.commit('setReserve1', option);
                    })
                    .catch(function (error) {
                        console.error(error);
                    });
            } else {
                await this.$axios.$put(`/settings/update/department/${option.id}/`, name)
                    .then(function (data) {
                        store.commit('setWorkshop', data);
                        // console.log(e);
                        // store.commit('setReserve1', option);
                    })
                    .catch(function (error) {
                        console.error(error);
                    });
            }






        },
        async updateKnots(store, option) {
            
            let name = {
                name: option.name,
                // parent: option.workshop_id,

            };

            {//? изолировал чтобы можно было свернуть
                let type = store.state.typeStructured[6].id; //этличается от того что показывает vue плагин в chrome
                let indexNum = store.state.clientsObject.currentStructureObject.findIndex((el, i) => {
                    return el == type;
                });

                if (indexNum != -1 && indexNum != 0) { //&& !option.id) { //подкидываем parent от предыдущего элемента структуры
                    name.parent = option[store.state.typeStructureTableKey[store.state.clientsObject.currentStructureObject[indexNum - 1] - 1]];
                }
            }

            // debugger;
            if (!option.id) {
                await this.$axios.$post(`/structure/Agreagat/`, name)
                    .then(function (data) {
                        store.commit('setKnots', data);
                        // console.log(e);
                        // store.commit('setReserve1', option);
                    })
                    .catch(function (error) {
                        console.error(error);
                    });
            } else {
                await this.$axios.$put(`/structure/Agreagat/${option.id}/`, name)
                    .then(function (data) {
                        store.commit('setKnots', data);
                        // console.log(e);
                        // store.commit('setReserve1', option);
                    })
                    .catch(function (error) {
                        console.error(error);
                    });
            };


        },
        async updateSensors(store, option) {
            
            let name = {
                name: option.name,
                // parent: option.knot_id,
                designation: option.shema,
            };

            {//? изолировал чтобы можно было свернуть
                let type = store.state.typeStructured[7].id; //этличается от того что показывает vue плагин в chrome
                let indexNum = store.state.clientsObject.currentStructureObject.findIndex((el, i) => {
                    return el == type;
                });

                if (indexNum != -1 && indexNum != 0) { //&& !option.id) { //подкидываем parent от предыдущего элемента структуры
                    name.parent = option[store.state.typeStructureTableKey[store.state.clientsObject.currentStructureObject[indexNum - 1] - 1]];
                }
            }

            if (!option.id) {
                await this.$axios.$post(`/structure/Sensors/`, name)
                    .then(function (data) {
                        // console.log(data);
                        store.commit('setSensors', data);
                        // console.log(e);
                        // store.commit('setReserve1', option);
                    })
                    .catch(function (error) {
                        console.error(error);
                    });
            } else {
                await this.$axios.$put(`/structure/Sensors/${option.id}/`, name)
                    .then(function (data) {

                        store.commit('setSensors', data);
                        // console.log(e);
                        // store.commit('setReserve1', option);
                    })
                    .catch(function (error) {
                        console.error(error);
                    });
            };
        },
        async updateVariables(store, option) {
            
            let name = {
                name: option.name,
                // sensor: option.sensor_id,
                name_connection: option.connect,
                table_name: option.table_name,
                up_level_alarm: option.limitMaxСrash,
                down_level_alarm: option.limitMinСrash,
                up_level: option.limitMaxWarn,
                down_level: option.limitMinWarn,
                rate_change: option.limitSpead,
                unit: option.unit,
            };

            {//? изолировал чтобы можно было свернуть - тк переменная всегда есть 
                // console.log(store.state.typeStructured);
                // let type = 9; //этличается от того что показывает vue плагин в chrome
                // console.log(store.state.clientsObject.currentStructureObject);
                debugger;
                // if (indexNum != -1 && indexNum != 0) { //&& !option.id) { //подкидываем parent от предыдущего элемента структуры
                    name.sensor = option[store.state.typeStructureTableKey[store.state.clientsObject.currentStructureObject[store.state.clientsObject.currentStructureObject.length - 1] - 1]];
                // }
            }

            if (!option.id) {
                await this.$axios.$post(`/recorder/structure/ValueSensor/`, name)
                    .then(function (data) {
                        console.log(data);
                        store.commit('setVariables', data);

                    })
                    .catch(function (error) {
                        console.error(error);
                    });
            } else {
                await this.$axios.$put(`/recorder/structure/ValueSensor/${option.id}/`, name)
                    .then(function (data) {

                        store.commit('setVariables', data);

                    })
                    .catch(function (error) {
                        console.error(error);
                    });
            };


        },
        // updateVariablesConnect(store, option) {
        //     let variables = [];
        //     if (localStorage.getItem('variables'))
        //         variables = JSON.parse(localStorage.getItem('variables'));
        //     else if (this.state.settingsGlobal.variables)
        //         variables = JSON.parse(JSON.stringify(this.state.settingsGlobal.variables));

        //     option.id = new Date().getTime();
        //     variables.push(option);

        //     localStorage.setItem('variables', JSON.stringify(variables));
        //     store.commit('setVariables', option);
        // },

        // ПОЛУЧЕНИЕ ДАННЫХ ПРИ ОТКРЫТИИ СТРАНИЦЫ
        async getDataTableCustom(store) { //получение всех данных о таблице Объект
            if (store.state.clientsObject === null) {
                await this.$axios.$get(`/settings/get_structure/`)
                    .then((data) => {
                        store.commit('setClientsObject', data); //передаем полученные данные в мутацию
                    })
                    .catch((e) => {
                        console.log(e);
                    })
            };
        },
        async getDataTableReserv1(store) { //получение данных о таблице Резерв1

            if (store.state.reserves1.length == 0) {
                await this.$axios.$get(`/structure/Reserv_1/`)
                    .then((data) => {
                        store.commit('openReserve1', data); //передаем полученные данные в мутацию
                    })
                    .catch((e) => {
                        console.log(e);
                    })
            };
        },
        async getDataTableReserv2(store) { //получение всех данных о таблице Резерв2
            if (store.state.reserves2.length == 0) {
                await this.$axios.$get(`/structure/Reserv_2/`)
                    .then((data) => {
                        // console.log(data);
                        data.forEach((item) => {
                            item.reserv1_id = item.parents.id;
                            delete item.parents;
                            delete item.parent;
                        })
                        // console.log(data);
                        store.commit('openReserve2', data); //передаем полученные данные в мутацию
                    })
                    .catch((e) => {
                        console.log(e);
                    })
            };
        },
        async getDataTableOrganization(store) { //получение всех данных о таблице Организация
            if (store.state.organisations.length == 0) {
                await this.$axios.$get(`/structure/Corparation/`)
                    .then((data) => {
                        data.forEach((item) => {
                            item.reserv2_id = item.parents.id;
                            item.reserv1_id = item.parents.parents.id;
                            // console.log(item.reserv1_id);
                            delete item.parent;
                            delete item.parents;
                        })
                        // console.log(data);
                        store.commit('openOrganization', data); //передаем полученные данные в мутацию
                    })
                    .catch((e) => {
                        console.log(e);
                    })
            };
        },
        async getDataTableCompany(store) { //получение всех данных о таблице Предприятие
            if (store.state.companies.length == 0) {
                await this.$axios.$get(`/structure/Company/`)
                    .then((data) => {
                        data.forEach((item) => {
                            item.organisation_id = item.parents.id;
                            item.reserv2_id = item.parents.parents.id;
                            item.reserv1_id = item.parents.parents.parents.id;
                            // console.log(item.reserv1_id);
                            delete item.parent;
                            delete item.parents;
                        })
                        // console.log(data);
                        store.commit('openСompany', data); //передаем полученные данные в мутацию
                    })
                    .catch((e) => {
                        console.log(e);
                    })
            };
        },
        async getDataTableFactory(store) { //получение всех данных о таблице Завод
            if (store.state.factories.length == 0) {
                await this.$axios.$get(`/structure/Factory/`)
                    .then((data) => {
                        // debugger;
                        data.forEach((item) => {
                            item.company_id = item.parents.id;
                            item.organisation_id = item.parents.parents.id;
                            item.reserv2_id = item.parents.parents.parents.id;
                            item.reserv1_id = item.parents.parents.parents.parents.id;
                            item.map = item.address;
                            // console.log(item.reserv1_id);
                            delete item.address;
                            delete item.parent;
                            delete item.parents;
                        })
                        // console.log(data);
                        store.commit('openFactory', data); //передаем полученные данные в мутацию
                    })
                    .catch((e) => {
                        console.log(e);
                    })
            };
        },
        async getDataTableWorkshop(store) { //получение всех данных о таблице Цех
            if (store.state.workshops.length == 0) {
                await this.$axios.$get(`/structure/Department/`)
                    .then((data) => {
                        // debugger;
                        // console.log(data);
                        { //подготавливаем массив для отображения
                            let emptyRanges = {
                                start: null,
                                end: null,
                                is_active: null,
                                showBreaks: false,
                                breaks: [{
                                        start: null,
                                        end: null,
                                        is_active: false,
                                    },
                                    {
                                        start: null,
                                        end: null,
                                        is_active: false,
                                    },
                                    {
                                        start: null,
                                        end: null,
                                        is_active: false,
                                    },
                                    {
                                        start: null,
                                        end: null,
                                        is_active: false,
                                    },
                                ],
                            };
                            let emptyBreaks = {
                                start: null,
                                end: null,
                                is_active: false,
                            };
                            data.forEach((item) => {

                                let ranges = [];
                                item.factory_id = item.parents.id;
                                item.company_id = item.parents.parents.id;
                                item.organisation_id = item.parents.parents.parents.id;
                                item.reserv2_id = item.parents.parents.parents.parents.id;
                                item.reserv1_id = item.parents.parents.parents.parents.parents.id;

                                // console.log(item.shifts);

                                // item.ranges = item.shifts;

                                if (Array.isArray(item.shifts)) {
                                    item.shifts.forEach((item2, i) => {
                                        let breaks = [];
                                        let lenghtLunchs = item.shifts[i].lunchs.length;

                                        item.shifts[i].lunchs.forEach((item3, k) => {
                                            breaks.push({
                                                start: item3.start.slice(0, 5),
                                                end: item3.end.slice(0, 5),
                                                is_active: true,
                                                id: item3.id,
                                            })
                                        });

                                        for (let ii = 0; ii <= (3 - lenghtLunchs); ii++) {
                                            breaks.push(emptyBreaks);
                                        }


                                        ranges.push({
                                            start: item2.start.slice(0, 5),
                                            end: item2.end.slice(0, 5),
                                            showBreaks: false,
                                            is_active: true,
                                            breaks: breaks,
                                            id: item2.id,
                                        });


                                    });
                                } else {
                                    for (let j = 0; j <= 3; j++) {
                                        ranges.push(emptyRanges);
                                    }
                                }

                                let lenghtRanges = item.shifts.length;
                                for (let kk = 0; kk <= (3 - lenghtRanges); kk++) {
                                    ranges.push(emptyRanges);
                                }

                                item.ranges = ranges;

                                delete item.shifts;
                                delete item.parent;
                                delete item.parents;
                            })
                        }
                        // console.log(data);
                        // console.log(data);
                        store.commit('openWorkshop', data); //передаем полученные данные в мутацию
                    })
                    .catch((e) => {
                        console.log(e);
                    })
            };
        },
        async getDataTableKnot(store) { //получение всех данных о таблице Узел
            if (store.state.knots.length == 0) {
                await this.$axios.$get(`/structure/Agreagat/`)
                    .then((data) => {
                        // debugger;
                        data.forEach((item) => {
                            item.workshop_id = item.parents.id;
                            item.factory_id = item.parents.parents.id;
                            item.company_id = item.parents.parents.parents.id;
                            item.organisation_id = item.parents.parents.parents.parents.id;
                            item.reserv2_id = item.parents.parents.parents.parents.parents.id;
                            item.reserv1_id = item.parents.parents.parents.parents.parents.parents.id;

                            // console.log(item.reserv1_id);
                            delete item.parent;
                            delete item.parents;
                        })
                        // console.log(data);
                        store.commit('openKnot', data); //передаем полученные данные в мутацию
                    })
                    .catch((e) => {
                        console.log(e);
                    })
            };
        },
        async getDataTableSensor(store) { //получение всех данных о таблице Узел
            if (store.state.sensors.length == 0) {
                await this.$axios.$get(`/structure/Sensors/`)
                    .then((data) => {
                        // debugger;
                        data.forEach((item) => {

                            item.knot_id = item.parents.id;
                            item.workshop_id = item.parents.parents.id;
                            item.factory_id = item.parents.parents.parents.id;
                            item.company_id = item.parents.parents.parents.parents.id;
                            item.organisation_id = item.parents.parents.parents.parents.parents.id;
                            item.reserv2_id = item.parents.parents.parents.parents.parents.parents.id;
                            item.reserv1_id = item.parents.parents.parents.parents.parents.parents.parents.id;

                            item.shema = item.designation;
                            // console.log(item.reserv1_id);
                            delete item.designation;
                            delete item.parent;
                            delete item.parents;
                        })
                        // console.log(data);
                        store.commit('openSensor', data); //передаем полученные данные в мутацию
                    })
                    .catch((e) => {
                        console.log(e);
                    })
            };
        },
        async getDataTableVariable(store) { //получение всех данных о таблице Узел
            if (store.state.variables.length == 0) {
                await this.$axios.$get(`/recorder/structure/ValueSensor/`)
                    .then((data) => {
                        // debugger;
                        // console.log(data);
                        let newData = [];
                        data.forEach((item) => {
                            let tempData = {
                                name: item.name,
                                id: item.id
                            };
                            tempData.sensor_id = item.parents.id;
                            tempData.knot_id = item.parents.parents.id;
                            tempData.workshop_id = item.parents.parents.parents.id;
                            tempData.factory_id = item.parents.parents.parents.parents.id;
                            tempData.company_id = item.parents.parents.parents.parents.parents.id;
                            tempData.organisation_id = item.parents.parents.parents.parents.parents.parents.id;
                            tempData.reserv2_id = item.parents.parents.parents.parents.parents.parents.parents.id;
                            tempData.reserv1_id = item.parents.parents.parents.parents.parents.parents.parents.parents.id;
                            tempData.table_name = item.table_name;
                            tempData.connect = item.name_connection;
                            tempData.limitMaxWarn = item.up_level;
                            tempData.limitMinWarn = item.down_level;
                            tempData.limitMaxСrash = item.up_level_alarm;
                            tempData.limitMinСrash = item.down_level_alarm;
                            tempData.limitSpead = item.rate_change;
                            tempData.variablee = "Var: " + item.table_name.slice(item.table_name.indexOf(item.name_connection) + item.name_connection.length + 1, item.table_name.length);

                            tempData.unit = item.unit;
                            newData.push(tempData);

                            // console.log(item.reserv1_id);

                        })
                        // console.log(newData);
                        store.commit('openVariable', newData); //передаем полученные данные в мутацию
                    })
                    .catch((e) => {
                        console.log(e);
                    })
            };
        },
        async getDataConnection(store) { //получение всех данных о таблице Узел
            if (store.state.connection.length == 0) {
                await this.$axios.$get(`/dashboard/teldafax/connections/`)
                    .then((data) => {
                        // debugger;
                        // console.log(data);
                        let newData = [];
                        data.forEach((item) => {
                            let tempData = {
                                name: item.connection_name,
                                id: item.key,
                                ip: item.ip,
                                tags: [],
                            };
                            newData.push(tempData);

                            // console.log(item.reserv1_id);

                        })
                        // console.log(newData);
                        store.commit('setDataConnection', newData); //передаем полученные данные в мутацию
                    })
                    .catch((e) => {
                        console.log(e);
                    })
            };
        },
        async getDataConnectionTags(store, option) {
            // debugger;
            let isName = false;
            let saveI;
            let arrCoonnect = store.state.connection.filter(item => item.name == option.name);
            //получение всех данных о таблице Узел
            if (arrCoonnect[0].tags.length == 0) {
                // function sleep(ms) {
                //     ms += new Date().getTime();
                //     while (new Date() < ms){}
                //     } 
                // sleep(5000);
                await this.$axios.$get(`dashboard/teldafax/connections/variables/${option.id}/`)
                    .then((data) => {
                        // debugger;
                        // console.log(data);
                        // console.log(newData);
                        store.commit('setDataConnectionTags', {
                            data: data,
                            id: option.id
                        }); //передаем полученные данные в мутацию
                    })
                    .catch((e) => {
                        console.log(e);
                    })
            } else {
                store.commit('setDataConnectionTags', {
                    data: arrCoonnect[0].tags,
                    id: option.id
                });
            }
        },


    },
    strict: process.env.NODE_ENV !== 'production'
};