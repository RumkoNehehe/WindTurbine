<script setup lang="ts">
import { ref, watch, computed, onMounted } from "vue";
import MotorSection from "./components/motorSection/MotorSection.vue";
import ControlPanel from "./components/controlPanel/ControlPanel.vue";
import LoginForm from "./components/LoginForm.vue";
import ChartPanel from "./components/chartPanel/ChartPanel.vue";
import { useSocketDashboard } from "./composables/useSocketDashboard";
import { useRecording } from "./composables/useRecording";
import { useChartData } from "./composables/userChartData";
import { useAuth } from "./composables/useAuth";
import type { ChartDataSource } from "./types/chartDataSource";
import type { LeftPanelView } from "./types/leftPanelView";
import type { MotorTarget } from "./types/motorTarget";
import type { Mode } from "./types/mode";
import { useRegulation } from "./composables/useRegulation";


const { socket, motors, isConnected, lastUpdate, logs, dashboardHistory } =
useSocketDashboard();

const {
    isRegulation,
    motorTarget: regulationMotorTarget,
    targetRpm,
    kp,
    ki,
    kd,
    mode: regulationMode,
    isRegulating,
    regulationControl,
    startRegulation,
    stopRegulation,
    toggleRegulationView,
} = useRegulation(socket);

const {
    isRecording,
    recordings,
    selectedRecordingId,
    customChartPoints,
    fetchRecordingById,
    startRecording,
    stopRecording,
    appendToRecording,
    downloadRecording,
    handleFileUpload,
    saveFileToDatabase,
    clearCustomChartData,
} = useRecording();

const {
    isChartDataFlowPaused,
    chartPoints,
    clearChartData,
    pauseChartDataFlow,
    resumeChartDataFlow,
} = useChartData(dashboardHistory);

const { userRole, isCheckingAuth, loginError, login, logout } = useAuth();

const chartDataToggle = ref<ChartDataSource>("live");
const controllsToggle = ref<LeftPanelView>("logs");
const motorToggle = ref<MotorTarget>("motor1");

const controlPwm = ref(128);
const mode = ref<Mode>("FORWARD");


const manualControl = computed(() => ({
    motorTarget: motorToggle.value,
    pwm: controlPwm.value,
    mode: mode.value,
}));

function applyMotorChanges() {
    if (motorToggle.value === "motor1") {
        socket.emit("set_motor_1", {
            pwm: controlPwm.value,
            mode: mode.value,
        });
    }
    if (motorToggle.value === "motor2") {
        socket.emit("set_motor_2", {
            pwm: controlPwm.value,
            mode: mode.value,
        });
    }
}

function stopSystem() {
    console.log("sending event to stop system");
    socket.emit("stop_system");
}

function handleToggleRegulation() {
    isRegulation.value = !isRegulation.value;
}

async function handleLogin(username: string, password: string) {
    await login(username, password);
}

watch(
    () => dashboardHistory.value.length,
    () => {
        const latest = dashboardHistory.value.at(-1);
        if (!latest) return;

        appendToRecording(latest);
    },
);

watch(selectedRecordingId, async (newId) => {
    if (!newId) return;

    customChartPoints.value = await fetchRecordingById(newId);
});
</script>

<template>
    <div class="h-screen overflow-hidden bg-gray-800 p-4">
        <div
            class="max-w-400 mx-auto bg-gray-700 rounded-2xl flex flex-col h-full p-6"
        >
            <h1 class="text-3xl font-bold text-center mb-6 text-white">
                Wind Turbine
            </h1>
            <div
                v-if="isCheckingAuth"
                class="flex min-h-screen items-center justify-center bg-gray-800 text-white"
            >
                Loading...
            </div>
            <div
                v-else-if="userRole === 'guest'"
                class="flex justify-center items-start mt-10"
            >
                <LoginForm :error-message="loginError" @login="handleLogin" />
            </div>
            <div
                v-else
                class="grid grid-cols-[1fr_0.6fr_1.6fr] gap-6 flex-1 min-h-0"
            >
                <MotorSection
                    class="h-full min-h-0"
                    :motors="motors"
                    :logs="logs"
                    :is-regulation="isRegulation"
                    :left-panel-view="controllsToggle"
                    :regulation-control="regulationControl"
                    :manual-control="manualControl"
                    @update:kd="kd = $event"
                    @update:ki="ki = $event"
                    @update:kp="kp = $event"
                    @update:target-rpm="targetRpm = $event"
                    @update:motor-target="regulationMotorTarget = $event"
                    @update:motor-toggle-data="motorToggle = $event"
                    @update:mode="mode = $event"
                    @update:mode2="regulationMode = $event"
                    @update:pwm="controlPwm = $event"
                    @start-regulation="startRegulation"
                    @stop-regulation="stopRegulation"
                    @apply="applyMotorChanges"
                    @stop-system="stopSystem"
                    @toggle-regulation="toggleRegulationView"
                >
                </MotorSection>
                <ControlPanel
                    :isConnected="isConnected"
                    :is-recording="isRecording"
                    :username="userRole.toString()"
                    :is-admin="userRole"
                    :leftPanelToggle="controllsToggle"
                    :last-update="lastUpdate"
                    @log-off="logout"
                    @save-file="saveFileToDatabase"
                    @update:left-panel-toggle="controllsToggle = $event"
                    @start-recording="startRecording"
                    @stop-recording="stopRecording"
                    @download-file="downloadRecording"
                />

                <ChartPanel
                    v-if="chartDataToggle === 'live'"
                    class="h-full min-h-0"
                    :chartDataSource="chartDataToggle"
                    :recordings="recordings"
                    :selectedRecordingId="selectedRecordingId"
                    :points="chartPoints"
                    :is-paused="isChartDataFlowPaused"
                    @clear-chart="clearChartData"
                    @pause-data-flow="pauseChartDataFlow"
                    @resume-data-flow="resumeChartDataFlow"
                    @upload-file="handleFileUpload"
                    @update:chart-data-source="chartDataToggle = $event"
                    @update:selected-recording="selectedRecordingId = $event"
                >
                </ChartPanel>

                <ChartPanel
                    v-if="chartDataToggle === 'recorded'"
                    class="h-full min-h-0"
                    :chartDataSource="chartDataToggle"
                    :recordings="recordings"
                    :selectedRecordingId="selectedRecordingId"
                    :points="customChartPoints"
                    :is-paused="isChartDataFlowPaused"
                    @clear-chart="clearCustomChartData"
                    @pause-data-flow="pauseChartDataFlow"
                    @resume-data-flow="resumeChartDataFlow"
                    @upload-file="handleFileUpload"
                    @update:chart-data-source="chartDataToggle = $event"
                    @update:selected-recording="selectedRecordingId = $event"
                >
                </ChartPanel>
            </div>
        </div>
    </div>
</template>

<style scoped></style>
