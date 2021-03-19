<template>
  <div>
    <div class="top-panel">
      <div class="project-box">Объекты</div>
<!--      <div class="search-wrapper">-->
<!--        <input type="text" v-model="search" placeholder="Search title.." />-->
<!--        <IconifyIcon icon="bxSearchAlt2" :style="{fontSize: '24px'}" class="input-icon" />-->
<!--      </div>-->
      <div class="btn-box">
        <button class="btn-project btn-del">
          <span class="btn-title">Удалить</span>
          <span class="btn-svg"></span>
        </button>
        <!-- <button class="btn-project btn-del" v-on:click="GET_DEMOOBJECT">GET проект</button>
        <button class="btn-project btn-del" v-on:click="updatetempobj">UPDATE проект</button>
        <button class="btn-project btn-del" v-on:click="addtempobj">ADD проект</button>
        <button class="btn-project btn-del" v-on:click="deltempobj">DELETE проект</button> -->
        <button class="btn-project btn-edit" v-on:click="changeshowCreated">
          <span class="btn-title">Изменить</span>
          <span class="btn-svg"></span>
        </button>
        <button class="btn-project btn-add" v-on:click="changeshowCreated">
          <span class="btn-title">Добавить</span>
          <span class="btn-svg"></span>
        </button>
      </div>
    </div>
    <div class="table-objects">
      <table>
        <thead>
          <tr class="table-head">
            <th>Название объекта</th>
            <th>Заказчик</th>
            <th>Договор</th>
            <th>Дата создания</th>
            <th>Дата изменения</th>
          </tr>
        </thead>
<!--        <tbody>-->
<!--          <tr v-for="(client, idx) in filteredList" :key="idx" class="table-body">-->
<!--            <td>-->
<!--              <input readonly class="input-td" type="text" v-bind:value="client.name" />-->
<!--            </td>-->
<!--            <td>-->
<!--              <input readonly class="input-td" type="text" v-bind:value="client.client" />-->
<!--            </td>-->
<!--            <td>-->
<!--              <input readonly class="input-td" type="text" v-bind:value="client.contract.name" />-->
<!--            </td>-->
<!--            <td>-->
<!--              <input readonly class="input-td" type="text" v-bind:value="client.contract.firstDate" />-->
<!--            </td>-->
<!--            <td>-->
<!--              <input readonly class="input-td" type="text" v-bind:value="client.contract.lastDate" />-->
<!--            </td>-->
<!--          </tr>-->
<!--        </tbody>-->
      </table>
    </div>
    <VobjectCreated v-show="showCreated" v-on:changeShow="changeshowCreated">></VobjectCreated>
  </div>
</template>

<script>
import VobjectCreated from "@/components/VobjectCreated";

import { mapGetters } from "vuex";
import { mapActions } from "vuex";

export default {
  layout: "header_footer",


  created() {
    this.setActiveTabHeader("OEE");
    this.setActiveTabSidebar("Setting");
  },

  components: {
    VobjectCreated,
  },

  data() {
    return {
      search: "",
      showCreated: false,
    };
  },

  computed: {
    ...mapGetters("Clients", {
      clientsObject: "clientsObject",
      demoObjectidx: "demoObjectidx",
    }),
    filteredList() {
      return this.clientsObject.filter((object) => {
        return object.name.toLowerCase().includes(this.search.toLowerCase());
      });
    },
  },
  methods: {
    ...mapActions("users", {
      setActiveTabHeader: "setActiveTabHeader",
      setActiveTabSidebar: "setActiveTabSidebar",
    }),
    ...mapActions("Clients", {
      GET_DEMOOBJECT: "GET_DEMOOBJECT",
      UPDATE_DEMOOBJECT: "UPDATE_DEMOOBJECT",
      ADD_DEMOOBJECT:"ADD_DEMOOBJECT",
      DELETE_DEMOOBJECT:"DELETE_DEMOOBJECT",
    }),
    changeshowCreated() {
      this.showCreated = !this.showCreated;
    },
    addtempobj(){
      // console.log(this.demoObjectLength);
      let newname = prompt('новое значение', "test-test");

      this.ADD_DEMOOBJECT({name:newname});
    },
    deltempobj(){
      // console.log(this.demoObjectLength);
      let idx = prompt('какой id?', 2);

      this.DELETE_DEMOOBJECT(idx);
    },
    updatetempobj(){
      // console.log(this.demoObjectLength);
      let idx = prompt('какой id?', 2);
      let newname = prompt('новое значение', "test-test");

      this.UPDATE_DEMOOBJECT({id:+idx, name:newname});
    },
  },
};
</script>

<style lang="scss" scoped>
/* top-panel */

.top-panel {
  position: absolute;
  width: 100%;
  height: 48px;
  left: 0;
  top: 48px;

  border-bottom: 1px solid #dde4ee;

  display: flex;
  flex-direction: row;
  justify-content: space-between;

  background-color: #f9fafc;
}



.search-wrapper{
  position: relative;

  margin-left: 12px;
  margin-right: auto;


  font-weight: 500;
  font-size: 14px;
  line-height: 17px;

  width: 210px;
  height: 24px;
  display: flex;
  /* justify-content: center; */
  /* align-items: center; */

  color: #4a627a;

}

.input-icon {
  position: absolute;
  top: 12px;
  /* left: 24px; */
}

.search-wrapper input{
  outline: none;
  position: absolute;
  top: 12px;
  padding-left: 24px;
  padding-top: 5px;
  border: none;
}

.project-box {
  margin-left: 144px;
  /* margin-right: auto; */

  font-weight: 500;
  font-size: 14px;
  line-height: 17px;

  width: 84px;
  display: flex;
  justify-content: space-between;
  align-items: center;

  color: #4a627a;
}
.btn-box {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-right: 30px;
}
.btn-project {
  width: 108px;
  height: 24px;

  font-weight: 500;
  font-size: 10px;
  line-height: 12px;

  display: flex;
  align-items: center;
  text-align: center;
  justify-content: space-between;
  padding-left: 24px;
  padding-right: 6px;
  color: #ffffff;

  outline: none;
  border: none;
}

.btn-del {
  color: #FF6F64;
  background-color: #ffffff;
  border: 1px solid #FF6F64;
  transition: 0.2s;

  .btn-svg {
    width: 12px;
    height: 12px;
    background-image: url("~assets/svg/setting/del_red.svg");
    background-size: contain;
    background-position: center;
    background-repeat: no-repeat;
  }

  &:hover {
    color: #ffffff;
    background-color: hsl(4, 100%, 67%);

    .btn-svg {
      background-image: url("~assets/svg/setting/del_white.svg");
      background-size: contain;
      background-position: center;
      background-repeat: no-repeat;
    }
  }
}

.btn-edit {
  color: #00B0FF;
  margin-left: 12px;
  background-color: #ffffff;
  transition: 0.2s;
  border: 1px solid #00B0FF;

  .btn-svg {
    width: 12px;
    height: 12px;
    background-image: url("~assets/svg/setting/edit_blue.svg");
    background-size: contain;
    background-position: center;
    background-repeat: no-repeat;
  }

  &:hover {
    background-color: hsl(196, 96%, 55%);
    color: #ffffff;

    .btn-svg {
      background-image: url("~assets/svg/setting/edit_white.svg");
      background-size: contain;
      background-position: center;
      background-repeat: no-repeat;
    }
  }
}

.btn-add {
  color: #01C587;
  margin-left: 24px;
  background-color: #ffffff;
  transition: 0.2s;
  border: 1px solid #01C587;

  .btn-svg {
    width: 12px;
    height: 12px;
    background-image: url("~assets/svg/setting/plus_green.svg");
    background-size: contain;
    background-position: center;
    background-repeat: no-repeat;
  }

  &:hover {
    background-color: hsl(161, 99%, 36%);
    color: #ffffff;

    .btn-svg {
      background-image: url("~assets/svg/setting/plus_white.svg");
      background-size: contain;
      background-position: center;
      background-repeat: no-repeat;
    }
  }
}
/* top-panel */

.table-objects {
  padding-top: 73px;
  padding-left: 24px;
  padding-right: 24px;
  color: #4a627a;
}

tr {
  height: 36px;
  font-weight: normal;
  font-size: 12px;
  line-height: 15px;
}

th {
  height: 36px;
  font-weight: 500;
  font-size: 10px;
  line-height: 12px;
  text-align: center;
  color: #4A627A;

  border: 1px solid #4a627a;
}

td {
  border: 1px solid #4a627a;
  padding: 0;
}

.input-td {
  width: 100%;
  height: 36px;
  border: none;
  padding-left: 12px;
  outline: none;
}

tbody {
  display: table;
  border-collapse: collapse;
  margin-top: 5px;
}
thead {
  display: table;
  border-collapse: collapse;
}

td:nth-child(1) {
  width: 472px;
}

td:nth-child(2) {
  width: 470px;
}
td:nth-child(3) {
  width: 470px;
}

td:nth-child(4) {
  width: 170px;
}

td:nth-child(5) {
  width: 170px;
}
th:nth-child(1) {
  width: 472px;
}

th:nth-child(2) {
  width: 470px;
}
th:nth-child(3) {
  width: 470px;
}

th:nth-child(4) {
  width: 170px;
}

th:nth-child(5) {
  width: 170px;
}
</style>
