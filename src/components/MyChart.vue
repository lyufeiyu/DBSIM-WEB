<template>
    <!-- <div>
    <Bar :data="chartData" :options="chartOptions"/>
  </div> -->
    <div>
        <line-chart :chart-data="datacollection"></line-chart>
    </div>
</template>

<script lang="ts">
import { Line } from "vue-chartjs";
// import { mapActions, mapState } from "vuex";

export default {
    name: "MyChart",
    extends: Line,
    data () {
    return {
      datacollection: {
        labels: ['January', 'February', 'March'],
        datasets: [
          {
            label: 'Data One',
            backgroundColor: '#f87979',
            data: [40, 20, 12] // Dummy data
          }
        ]
      }
    }
  },

};
// import { Bar } from 'vue-chartjs'
// // import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js'

// // ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

// export default {
//   name: 'MyChart',
//   components: { Bar },
//   data() {
//     return {
//       chartData: {
//         labels: [ 'January', 'February', 'March' ],
//         datasets: [ { data: [40, 20, 12] } ]
//       },
//       chartOptions: {
//         responsive: true
//       }
//     }
//   }
// }
</script>