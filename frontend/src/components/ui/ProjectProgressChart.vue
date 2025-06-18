<template>
  <div class="w-full bg-white dark:bg-gray-900 rounded-xl shadow-md border border-gray-200 dark:border-gray-700 p-4">
    <h3 class="text-lg font-semibold text-gray-800 dark:text-white mb-4">
      📊 {{ project ? 'Прогресс проекта' : 'Общий прогресс' }}
    </h3>

    <div class="h-64">
      <Doughnut :data="chartData" :options="chartOptions" />
    </div>
  </div>
</template>

<script>
import { Doughnut } from 'vue-chartjs'
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  ArcElement
} from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, ArcElement)

export default {
  name: 'ProjectProgressChart',
  components: { Doughnut },
  props: {
    project: Object,
    allProjects: Array
  },
  computed: {
    chartData() {
      if (this.project) {
        return {
          labels: [this.project.name],
          datasets: [{
            data: [this.project.progress, 100 - this.project.progress],
            backgroundColor: ['#3B82F6', '#E5E7EB']
          }]
        }
      } else {
        const labels = this.allProjects.map(p => p.name)
        const data = this.allProjects.map(p => p.progress)
        return {
          labels,
          datasets: [{
            label: 'Прогресс',
            data,
            backgroundColor: labels.map(() => `hsl(${Math.floor(Math.random() * 360)}, 70%, 60%)`)
          }]
        }
      }
    },
    chartOptions() {
      return {
        responsive: true,
        plugins: {
          legend: { labels: { color: '#fff' } }
        }
      }
    }
  }
}
</script>
