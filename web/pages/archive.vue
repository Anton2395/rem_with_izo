<template>
<div style="margin:1%;margin-button:5%;">
    
    <el-table
    height="90vh"
    confirm-filter="Ok"
    :data="tableData"
    style="width: 100%"
    empty-text="No events"
     v-loading="loading"
    v-el-table-infinite-scroll="load"
    :row-class-name="tableRowClassName">
    <el-table-column
      prop="key"
      sortable
      label="Id"
      width="90">
       <template slot-scope="scope">
      <i class="el-icon-warning"></i> {{scope.row.key}}
       </template>
    </el-table-column>
    <el-table-column
      prop="now_time"
      sortable
      label="Date"
     >
     <template slot-scope="scope">
        <i class="el-icon-time"></i>
        <span style="margin-left: 10px">{{ new Date(scope.row.now_time).toLocaleString() }} </span>
      </template>
    </el-table-column>
    <el-table-column
      prop="text_alarm"
      label="text"
      >
    </el-table-column>
    <el-table-column
      prop="status"
       width="90"
       align="center"
       :filters="[{ text: 'Not active', value: 0 }, { text: 'Active', value: 1 }]"
       :filter-method="filterTag"
       confirm-filter="Ok"
      label="status">
      <template slot-scope="scope">
          <el-popover trigger="hover" placement="top">
          <p >STATUS: {{scope.row.status===0?"Not active":"active"}}</p>
          <div slot="reference" class="name-wrapper">
        <el-tag
            size="medium"
          :type="scope.row.status === 0 ? 'primary' : 'danger'"
          disable-transitions>
           <i v-if='scope.row.status===0' class='el-icon-circle-check'></i>
           <i v-if='scope.row.status===1' class='el-icon-circle-close'></i>
           </el-tag>
          </div>
          </el-popover>
      </template>
    </el-table-column>
    <el-table-column
      prop="type_alarm"
       width="140"
       :filters="[{ text: 'warnings', value: 'warning' }, { text: 'alarms', value: 'alarm' }]"
       :filter-method="filterType"
       confirmFilter="Ok"
       :filter-multiple="false"
      label="type">
    </el-table-column>
    <el-table-column
      prop="object_alarm"
       width="320"
      label="from">
    </el-table-column>
  </el-table>
    
</div>

</template>
<script>

import elTableInfiniteScroll from 'el-table-infinite-scroll';
import {mapActions} from "vuex";
export default {
    directives: {
    'el-table-infinite-scroll': elTableInfiniteScroll
  },
    layout: "header_footer",
    data(){
        return{
            tableData:  [],
            numLoad:0,
            loading:false,
        }
    },
    computed:{

    },
    watch:{

    },
  created() {
       this.setActiveTabHeader("HOME");
    this.setActiveTabSidebar("Archive Event");
  },
  async mounted(){
      this.getData();
  },
  methods:{
      load () {
          this.getData();
      },
     async getData(){
             this.loading=true;
            let offset = 50*this.numLoad;
            this.numLoad+=1;
            let tableData = await this.$axios.get(`/dashboard/teldafax/messages/alarms/archive/?limit=50&offset=${offset}`);
            console.log(tableData);
            this.loading = true;
         this.tableData = this.tableData.concat(tableData.data.alarms);
         this.loading=false;
      },
       ...mapActions("users", {
      setActiveTabHeader: "setActiveTabHeader",
      setActiveTabSidebar: "setActiveTabSidebar",
    }),
    tableRowClassName({row, rowIndex}) {
        if (row.type_alarm === 'warning') {
          return 'warning-row';
        } else if (row.type_alarm === 'alarm') {
          return 'danger-row';
        }
        return '';
      },
       filterTag(value, row) {
        return row.status === value;
      },
      filterType(value, row) {
        return row.type_alarm === value;
      },
  }
}
</script>

<style>
  .el-table .warning-row {
    background: oldlace;
  }

  .el-table .success-row {
    background: #f0f9eb;
  }
  .el-table .danger-row {
    background: #FBE6E6;
  }
</style>