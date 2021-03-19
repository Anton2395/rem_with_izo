<template>
  <el-table :data="tableData" style="width: 100%">
    <el-table-column prop="line" label="Линия" width="222"/>
    <el-table-column prop="timeData1" label="09.10.2019 12:30:32" width="154"/>
    <el-table-column prop="timeData2" label="09.10.2019 13:30:32" width="154"/>
    <el-table-column prop="timeData2" label="09.10.2019 14:30:32" width="154"/>
  </el-table>
</template>

<script>
export default {
  name: 'tableInRecorder',
  data() {
    return {
      tableData: [{
        line: 'Давление в трубе 1',
        timeData1: '0',
        timeData2: '2',
        timeData3: '5',
        
      }, {
        line: 'Давление в трубе 2',
         timeData1: '5',
        timeData2: '5',
        timeData3: '7',
       
      }, {
        line: 'Давление в трубе 3',
         timeData1: '0',
        timeData2: '2',
        timeData3: '8',
       
      },{
        line: 'Давление в трубе 4',
         timeData1: '8',
        timeData2: '9',
        timeData3: '11',
       
      },
      ]
    }
  }
}
</script>

<style src="./tableInRecorder.css"></style>