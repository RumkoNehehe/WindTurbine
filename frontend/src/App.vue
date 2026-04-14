<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount } from 'vue';
import { getSocket } from './services/socket';
import MotorSection from './components/motorSection/MotorSection.vue';
import ControlPanel from './components/controlPanel/ControlPanel.vue';
import ChartPanel from './components/chartPanel/ChartPanel.vue';
import type { Motor } from './types/motor'
import type { DataSource } from './types/dataSource';
import type { LiveDashboardPayload } from './types/liveDashboardPayload';

const motors = ref<Motor[]>([
	{ name: 'Motor1', pwm: 0, rpm: 0, mode:'Brake' },
	{ name: 'Motor2', pwm: 0, rpm: 0, mode: 'Brake'}
])

const socket = getSocket()

const isConnected = ref(false)
const isRecording = ref(false)
const lastUpdate = ref('No data yet')

const logs = ref<string[]>([])

const dataSource = ref<DataSource>('liveData')
const selectedRecording = ref('')

const recordings = ref([
	'Recording 01',
	'Recording 02',
	'Recording 03'
])

function handleConnect(){
	isConnected.value = true
}

function handleDisconnect(){
	isConnected.value = false
}

function handleDashboardUpdate(payload: LiveDashboardPayload) {
	isConnected.value = payload.isConnected
	lastUpdate.value = payload.lastUpdate
	motors.value = payload.motors

	const motor = payload.motors.at(0)
	const log = `[${payload.lastUpdate}] ${motor?.name} → pwm: ${motor?.pwm}, rpm: ${motor?.rpm}`
	logs.value.unshift(log)
	// payload.motors.forEach(motor => {
	// 	const log = `[${payload.lastUpdate}] ${motor.name} → pwm: ${motor.pwm}, rpm: ${motor.rpm}`
	// 	logs.value.unshift(log)
	// })
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
				<ControlPanel class="h-full min-h-0" :isConnected="isConnected" :is-recording="isRecording" :last-update="lastUpdate"/>
				<ChartPanel class="h-full min-h-0" :data-source="dataSource" :recordings="recordings" :selected-recording="selectedRecording"
					@update:data-source="dataSource = $event" @update:selected-recording="selectedRecording = $event">
				</ChartPanel>
			</div>

		</div>
	</div>
</template>

<style scoped></style>
