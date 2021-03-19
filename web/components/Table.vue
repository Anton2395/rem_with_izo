<template >
	<div>
		<table v-if = lengthArrPoint>
			<thead>
				<tr>
					<td>X</td>
					<th v-for='(point, index) in currentArrPoint' v-on:dblclick="removePoint(point)" :key="index">
						{{point.X}}
					</th>
				</tr>
			</thead>
			<tbody>
				<tr>
					<td>A</td>
					<td v-for='(point, index) in currentArrPoint' :key="index">
					{{point.A}}
					</td>
				</tr>
				<tr>
					<td>P</td>
					<td v-for='(point, index) in currentArrPoint' :key="index">
						{{point.P}}
					</td>
				</tr>
				<tr>
					<td>Q</td>
					<td v-for='(point, index) in currentArrPoint' :key="index">
						{{point.Q}}
					</td>
				</tr>
				<tr>
					<td>OEE</td>
					<td v-for='(point, index) in currentArrPoint' :key="index">
						{{point.OEE}}
					</td>
				</tr>
			</tbody>
		</table>
		

	</div>

</template>

<script>

    import {mapGetters} from 'vuex';
	import {mapActions} from 'vuex';


    export default {

		props:{
			idx: Number
		},
 
        computed: {
            ...mapGetters('oeecharts',{			
				arrPoint: 'arrPoint',
				currentArrPoint: "currentArrPoint",
				lengthArrPoint: 'lengthArrPoint'
			})
		},

        methods: {
            ...mapActions('oeecharts',{
				addPoint: 'addPoint',
				removePoint: 'removePoint'
			}),


        
        	delX(iter){
				this.removePoint(iter);
        	
        	}
        }
}

</script>

<style scoped>


table {
	font-family: "Lucida Sans Unicode", "Lucida Grande", Sans-Serif;
font-size: 14px;
border-collapse: collapse;
text-align: center;
}
th{
	cursor: pointer;
}

th, td:first-child {
background: #AFCDE7;

padding: 10px 20px;
}
th, td {
border-style: solid;
border-width: 0 1px 1px 0;
border-color: white;
}
td {
background: #D8E6F3;
}
th:first-child, td:first-child {
text-align: left;
}

</style>