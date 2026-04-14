<script setup lang="ts">
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  LineElement,
  PointElement,
  CategoryScale,
  LinearScale,
} from 'chart.js'
import { Line } from 'vue-chartjs'
import { computed } from 'vue'

ChartJS.register(
  Title,
  Tooltip,
  Legend,
  LineElement,
  PointElement,
  CategoryScale,
  LinearScale
)

type ChartPoint = {
  label: string
  motor1: number
  motor2: number
}

const props = defineProps<{
  points: ChartPoint[]
}>()

const chartData = computed(() => ({
  labels: props.points.map(p => p.label),
  datasets: [
    {
      label: 'Motor 1 RPM',
      data: props.points.map(p => p.motor1),
      tension: 0.25
    },
    {
      label: 'Motor 2 RPM',
      data: props.points.map(p => p.motor2),
      tension: 0.25
    }
  ]
}))

const chartOptions = computed(() => ({
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      display: true,
      position: 'top' as const
    },
    title: {
      display: true,
      text: 'Motor performance'
    }
  },
  scales: {
    y: {
      beginAtZero: true
    }
  }
}))
</script>

<template>
  <div class="h-full w-full">
    <Line :data="chartData" :options="chartOptions" />
  </div>
</template>