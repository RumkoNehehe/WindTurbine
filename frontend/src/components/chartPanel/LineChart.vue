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
} from "chart.js";
import { Line } from "vue-chartjs";
import { computed } from "vue";
import type { ChartPoint } from "@/types/chartPoint";

ChartJS.register(
    Title,
    Tooltip,
    Legend,
    LineElement,
    PointElement,
    CategoryScale,
    LinearScale,
);

const props = defineProps<{
    points: ChartPoint[];
}>();

const chartData = computed(() => ({
    labels: props.points.map((p) => p.label),
    datasets: [
        {
            label: "Motor 1 RPM",
            data: props.points.map((p) => p.motor1Rpm),
            tension: 0.25,
            borderColor: "#e53935", // strong red
            backgroundColor: "#e53935",
        },
        {
            label: "Motor 2 RPM",
            data: props.points.map((p) => p.motor2Rpm),
            tension: 0.25,
            borderColor: "#ef9a9a", // lighter red
            backgroundColor: "#ef9a9a",
        },
        {
            label: "Motor 1 PWM%",
            data: props.points.map((p) => p.motor1Pmw),
            tension: 0.25,
            borderColor: "#1e88e5", // strong blue
            backgroundColor: "#1e88e5",
        },
        {
            label: "Motor 2 PWM%",
            data: props.points.map((p) => p.motor2Pmw),
            tension: 0.25,
            borderColor: "#90caf9", // lighter blue
            backgroundColor: "#90caf9",
        },
    ],
}));

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
    x: {
      title: {
        display: true,
        text: 'Time of Measurement (HH:mm:ss)'
      }
    },
    y: {
      beginAtZero: true,
      title: {
        display: true,
        text: 'Value'
      }
    }
  }
}))
</script>

<template>
    <div class="h-full w-full">
        <Line :data="chartData" :options="chartOptions" />
    </div>
</template>
