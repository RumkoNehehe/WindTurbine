<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount } from 'vue';
import { getSocket } from './services/socket';
import MotorSection from './components/motorSection/MotorSection.vue';
import ControlPanel from './components/controlPanel/ControlPanel.vue';
import ChartPanel from './components/chartPanel/ChartPanel.vue';
import type { Motor } from './types/motor'
import type { DataSource } from './types/dataSource';
import type { LiveDashboardPayloadDto } from './types/liveDashboardPayloadDto';
import type { LiveDashboardPayloadState } from './types/liveDashBoardState';
const motors = ref<Motor[]>([
	{ name: 'Motor1', pwm: 0, rpm: 0, mode: 'Brake' },
	{ name: 'Motor2', pwm: 0, rpm: 0, mode: 'Brake' }
])

const socket = getSocket()

const isConnected = ref(false)
const isRecording = ref(false)
const isChartDataFlowPaused = ref(false)
const lastUpdate = ref('')

const logs = ref<string[]>([])

const dataSource = ref<DataSource>('liveData')
const selectedRecording = ref('')

const recordings = ref([
	'Recording 01',
	'Recording 02',
	'Recording 03'
])

const chartPoints = ref([
	{ label: '', motor1: 0, motor2: 0 },
])

const dashboardHistory = ref<LiveDashboardPayloadState[]>([])

function handleConnect() {
	isConnected.value = true
}

function handleDisconnect() {
	isConnected.value = false
}

function handleDashboardUpdate(payload: LiveDashboardPayloadDto) {
	const mapped = mapDashboardState(payload)
	dashboardHistory.value.push(mapped)
	isConnected.value = mapped.isConnected
	lastUpdate.value = mapped.lastUpdate.toLocaleString("en-GB", {
		hour: "2-digit",
		minute: "2-digit",
	})
	motors.value = mapped.motors

	mapped.motors.forEach(motor => {
		const log = `[${mapped.lastUpdate.toLocaleString("en-GB", {
			hour: "2-digit",
			minute: "2-digit",
		})}] ${motor.name} → pwm: ${motor.pwm}, rpm: ${motor.rpm}`
		logs.value.unshift(log)
	})

	chartPoints.value.push({
		label: mapped.lastUpdate.toLocaleString("en-GB", {
			hour: "2-digit",
			minute: "2-digit",
			second: "2-digit"
		}),
		motor1: payload.motors[0]?.rpm ?? 0,
		motor2: payload.motors[1]?.rpm ?? 0,
	})
}

function mapDashboardState(payload: LiveDashboardPayloadDto): LiveDashboardPayloadState {
	return {
		isConnected: payload.isConnected,
		lastUpdate: new Date(payload.lastUpdate),
		motors: payload.motors
	}
}

onMounted(() => {
	socket.connect()

	socket.on('connect', handleConnect)
	socket.on('disconnect', handleDisconnect)
	socket.on('dashboard_update', handleDashboardUpdate)
})

onBeforeUnmount(() => {
	socket.off('connect', handleConnect)
	socket.off('disconnect', handleDisconnect)
	socket.off('dashboard_update', handleDashboardUpdate)
})

</script>

<template>
	<div class="h-screen overflow-hidden bg-gray-800 p-6">
		<div class="max-w-400 mx-auto bg-gray-700 rounded-2xl flex flex-col h-full p-6">

			<h1 class="text-3xl font-bold text-center mb-6">
				Ovládanie elektrárne
			</h1>

			<div class="grid grid-cols-[1fr_0.6fr_1.6fr] gap-6 flex-1 min-h-0">
				<MotorSection class="h-full min-h-0" :motors="motors" :logs="logs"></MotorSection>
				<ControlPanel class="h-full min-h-0" :isConnected="isConnected" :is-recording="isRecording"
					:last-update="lastUpdate" />
				<ChartPanel class="h-full min-h-0" :data-source="dataSource" :recordings="recordings"
					:selected-recording="selectedRecording" :points="chartPoints" :is-paused="isChartDataFlowPaused"
					@update:data-source="dataSource = $event" @update:selected-recording="selectedRecording = $event">
				</ChartPanel>
			</div>

		</div>
	</div>
</template>

<style scoped></style>
