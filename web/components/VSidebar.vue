<template>
  <div class="wraper_sidebar">
    <div
      class="item"
      v-for="sidetab in SidebarTabs[currentTabHeader]"
      :key="sidetab.name"
      :class="{ active: currentTabSidebar === sidetab.name }"
    >
      <nuxt-link
        :to="`/${sidetab.link}`"
        custom
        v-slot="{ navigate }"
        class="button_item"
      >
        <!-- <img class="img_item" :src="require(`../assets/svg/${sidetab.img}.svg`)" :alt="sidetab">        -->
        <!-- <IconifyIcon class="img_item" :icon="icons.monitorIcon" :style="{fontSize: '38px'}" />  -->
        <button @click="navigate">
          <IconifyIcon :icon="sidetab.icon" :style="{ fontSize: '38px' }" />
          <p>{{ sidetab.name }}</p>
        </button>
      </nuxt-link>
    </div>
    <!-- <div>
      <img class="imgreport" style="margin-left: 42px;
    margin-top: 10px;" 
    src="@/assets/svg/carbon_report.png" />
      <a style="outline: none;" href="/report.xls" download class="btn-workspace-dowland">

        <div>Скачать отчет</div>
      </a>
    </div> -->
  </div>
</template>
<script>
import { mapGetters } from "vuex";

export default {
  data() {
    return {
      SidebarTabs: {
        HOME: [
          {
            name: "Dashboard",
            link: "",
            img: "Dashboard",
            icon: "dashboard3Line",
          },
          {
            name: "Archive Event",
            link: "archive",
            img: "Archive_Event",
            icon: "calendar4Event",
          },

          // { name: "Admin", link: "", img: "Admin", icon: "guyUser" },
        ],
        // OEE: [
        //   {
        //     name: "Online",
        //     link: "Charts",
        //     img: "feather_monitor",
        //     icon: "monitorIcon",
        //   },
        //   {
        //     name: "Report",
        //     link: "",
        //     img: "carbon_report",
        //     icon: "reportIcon",
        //   },
        //   {
        //     name: "Setting",
        //     link: "Projects",
        //     img: "carbon_data-structured",
        //     icon: "dataStructured",
        //   },
        // ],
        // VIBRO: [
        //   { name: "Dashboard", link: "", img: "Dashboard", icon: "dashboard3Line" },
        //   { name: "Archive Event", link: "", img: "Archive_Event", icon: "calendar4Event" },
        //   { name: "Admin", link: "", img: "Admin", icon: "guyUser" }
        // ],
        // PROFILER: [
        //   { name: "Online", link: "Charts", img: "feather_monitor", icon: "monitorIcon" },
        //   { name: "Report", link: "", img: "carbon_report", icon: "reportIcon" },
        //   { name: "Setting", link: "Projects", img: "carbon_data-structured", icon: "dataStructured" }
        // ],
        // REPAIRS: [
        //   { name: "Dashboard", link: "", img: "Dashboard", icon: "dashboard3Line" },
        //   { name: "Archive Event", link: "", img: "Archive_Event", icon: "calendar4Event" },
        //   { name: "Admin", link: "", img: "Admin", icon: "guyUser" }
        // ],
        RECORDER: [
          {
            name: "Online",
            link: "Charts",
            img: "feather_monitor",
            icon: "monitorIcon",
          },
          // {
          //   name: "Report",
          //   link: "",
          //   img: "carbon_report",
          //   icon: "reportIcon",
          // },
          {
            name: "Setting",
            link: "settingsGlobal",
            img: "carbon_data-structured",
            icon: "dataStructured",
          },
        ],
        SETTING: [
          {
            name: "Setting",
            link: "Projects",
            img: "carbon_data-structured",
            icon: "dataStructured",
          },
        ],
      },
    };
  },
  computed: {
    ...mapGetters("users", {
      currentTabHeader: "currentTabHeader",
      currentTabSidebar: "currentTabSidebar",
    }),
  },
};
</script>

<style scoped>
.wraper_sidebar {
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

.button_item {
  cursor: pointer;
  margin: auto;
  padding-top: 12px;
  padding-bottom: 12px;
  background: none;
  border: none;
  display: flex;
  flex-direction: column;
  align-items: center;
  outline: none;

  color: inherit;
}
.button_item p {
  padding-top: 5px;
}

.item {
  /* margin: 2px 0; */
  position: relative;
  width: 100%;
  height: 79px;
  /* border-top: 1px solid #AEA8A8;
  border-bottom: 1px solid #AEA8A8;
   */
  border-left: 3px solid #edf2f8;
  color: #9aaaba;
  background-color: #edf2f8;
  /* box-shadow: 0px 2px 2px rgba(0, 0, 0, 0.25); */
  font-size: 12px;
  text-align: center;
}

.item::after {
  content: "";
  position: absolute;
  bottom: 0;
  left: 12px;

  width: 96px;
  border-bottom: 1px solid #aea8a8;
  opacity: 0.3;
}
.item::before {
  content: "";
  position: absolute;
  top: 0;
  left: 12px;

  width: 96px;
  border-top: 1px solid #aea8a8;
  opacity: 0.3;
}

.item:hover {
  color: #ff7167;
}
.btn-workspace-dowland {

  margin-left: 10px;
margin-right: 10px;
  outline: none;
  display: flex;
  align-items: center;
  text-align: center;

  padding: 2px 12px;
  border: 1px solid #9aaaba;
  background: #edf2f8;

  font-weight: 500;
  font-size: 10px;
  line-height: 10px;
  color: #9aaaba;
}
.btn-workspace-dowland:hover {
  display: flex;
  align-items: center;
  text-align: center;

  padding: 2px 12px;
  border: 1px solid #ff7167;
  background: #ff7167;

  font-weight: 500;
  font-size: 10px;
  line-height: 10px;
  color: #ffff;
}
.item.active {
  background-color: #eaeef7;
  border-left: 3px solid #ff7167;
  /* border-bottom: 1px solid rgba(174, 168, 168, 0.3);
  border-top: 1px solid rgba(174, 168, 168, 0.3); */
  color: #ff7167;
}
.item.active::after {
  content: "";
  position: absolute;
  top: 0;
  left: 0;

  width: 100%;
  border-top: 1px solid #aea8a8;
  opacity: 0.3;
}

.item.active::before {
  content: "";
  position: absolute;
  bottom: 0;
  left: 0;

  width: 100%;
  border-bottom: 1px solid #aea8a8;
  opacity: 0.3;
}

img {
  align-self: center;
}

</style>
