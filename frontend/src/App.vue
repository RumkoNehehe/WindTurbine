<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount } from "vue";
import { getSocket } from "./services/socket";
import MotorSection from "./components/motorSection/MotorSection.vue";
import ControlPanel from "./components/controlPanel/ControlPanel.vue";
import ChartPanel from "./components/chartPanel/ChartPanel.vue";
import type { Motor } from "./types/motor";
import type { ToggleData } from "./types/dataSource";
import type { LiveDashboardPayloadDto } from "./types/liveDashboardPayloadDto";
import type { LiveDashboardPayloadState } from "./types/liveDashBoardState";
import type { Mode } from "./types/mode";
import { isFunctionExpression } from "typescript";
const motors = ref<Motor[]>([
    { name: "Motor1", pwm: 0, rpm: 0, mode: "Brake" },
    { name: "Motor2", pwm: 0, rpm: 0, mode: "Brake" },
]);

const socket = getSocket();

const isConnected = ref(false);
const isRecording = ref(false);
const isChartDataFlowPaused = ref(true);
const isAdmin = ref(true);
const lastUpdate = ref("");

const username = "Admin";

const logs = ref<string[]>([]);

const dataTypeToggle = ref<ToggleData>("first");
const controllsToggle = ref<ToggleData>("first");
const motorToggle = ref<ToggleData>("first");
const selectedRecording = ref("");

const recordings = ref(["Recording 01", "Recording 02", "Recording 03"]);

const chartPoints = ref([{ label: "", motor1: 0, motor2: 0 }]);
const customChartPoints = ref([{ label: "", motor1: 0, motor2: 0 }]);

const dashboardHistory = ref<LiveDashboardPayloadState[]>([]);
const record = ref<LiveDashboardPayloadState[]>([]);

const controlPwm = ref(60);
const mode = ref<Mode>("FORWARD");

function applyMotorChanges() {
    if (motorToggle.value === "first") {
        socket.emit("set_motor_1", {
            pwm: controlPwm.value,
            mode: mode.value,
        });
    }
    if (motorToggle.value === "second") {
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

function handleConnect() {
    isConnected.value = true;
}

function handleDisconnect() {
    isConnected.value = false;
}

function startRecording() {
	record.value = []
    isRecording.value = true;
}

function stopRecording() {
    isRecording.value = false;
}

function downloadRecording() {
    if (isRecording.value) {
        return;
    }
    const dataStr = JSON.stringify(record.value, null, 2);
    const blob = new Blob([dataStr], { type: "application/json" });
    const url = URL.createObjectURL(blob);

    const fileName = `recording-${new Date()
        .toISOString()
        .replace(/[:.]/g, "-")}.json`;
    const a = document.createElement("a");
    a.href = url;
    a.download = fileName;
    a.click();

    URL.revokeObjectURL(url);
}

function handleFileUpload(event: Event) {
    const target = event.target as HTMLInputElement
    const file = target.files?.[0]

    if (!file) return

    const reader = new FileReader()

    reader.onload = () => {
        try {
            const text = reader.result as string
            const parsed = JSON.parse(text)

            if (!Array.isArray(parsed)) {
                throw new Error('Invalid format')
            }

            customChartPoints.value = parsed.map((item: any) => ({
                label: item.lastUpdate,
                motor1: item.motors?.[0]?.rpm ?? 0,
                motor2: item.motors?.[1]?.rpm ?? 0
            }))

        } catch (err) {
            console.error(err)
            alert('Invalid JSON file')
        }
    }

    reader.readAsText(file)
    target.value = ''
}

function handleDashboardUpdate(payload: LiveDashboardPayloadDto) {
    console.log("received socket");
    const mapped = mapDashboardState(payload);
    dashboardHistory.value.push(mapped);
    isConnected.value = payload.isConnected;
    lastUpdate.value = mapped.lastUpdate.toLocaleString("en-GB", {
        hour: "2-digit",
        minute: "2-digit",
    });
    motors.value = mapped.motors;

    if (isRecording.value) {
        record.value.push(mapped);
    }

    mapped.motors.forEach((motor) => {
        const log = `[${mapped.lastUpdate.toLocaleString("en-GB", {
            hour: "2-digit",
            minute: "2-digit",
        })}] ${motor.name} → pwm: ${motor.pwm}, rpm: ${motor.rpm}, mode: ${motor.mode}`;
        logs.value.unshift(log);
    });

    if (isChartDataFlowPaused.value) {
        return;
    }
    chartPoints.value.push({
        label: mapped.lastUpdate.toLocaleString("en-GB", {
            hour: "2-digit",
            minute: "2-digit",
            second: "2-digit",
        }),
        motor1: payload.motors[0]?.rpm ?? 0,
        motor2: payload.motors[1]?.rpm ?? 0,
    });
}

function mapDashboardState(
    payload: LiveDashboardPayloadDto,
): LiveDashboardPayloadState {
    return {
        lastUpdate: new Date(payload.lastUpdate),
        motors: payload.motors,
    };
}

function clearChartData() {
    chartPoints.value = [];
}

function clearCustomChartData() {
    customChartPoints.value = [];
}

function pauseChartDataFlow() {
    if (!isConnected.value) {
        return;
    }
    isChartDataFlowPaused.value = true;
}

function resumeChartDataFlow() {
    if (!isConnected.value) {
        return;
    }
    isChartDataFlowPaused.value = false;
}

onMounted(() => {
    socket.connect();

    socket.on("connect", handleConnect);
    socket.on("disconnect", handleDisconnect);
    socket.on("dashboard_update", handleDashboardUpdate);
});

onBeforeUnmount(() => {
    socket.off("connect", handleConnect);
    socket.off("disconnect", handleDisconnect);
    socket.off("dashboard_update", handleDashboardUpdate);

	socket.disconnect()
});
</script>

<template>
    <div class="h-screen overflow-hidden bg-gray-800 p-4">
        <div
            class="max-w-400 mx-auto bg-gray-700 rounded-2xl flex flex-col h-full p-6"
        >
            <h1 class="text-3xl font-bold text-center mb-6">
                Ovládanie elektrárne
            </h1>

            <div class="grid grid-cols-[1fr_0.6fr_1.6fr] gap-6 flex-1 min-h-0">
                <MotorSection
                    class="h-full min-h-0"
                    :motors="motors"
                    :is-admin
                    :controlsToggleData="controllsToggle"
                    :mode="mode"
                    :logs="logs"
                    :motorToggleData="motorToggle"
                    :pwm="controlPwm"
                    @update:motor-toggle-data="motorToggle = $event"
                    @update:mode="mode = $event"
                    @update:pwm="controlPwm = $event"
                    @apply="applyMotorChanges"
                    @stop-system="stopSystem"
                >
                </MotorSection>
                <ControlPanel
                    :isConnected="isConnected"
                    :is-recording="isRecording"
                    :username="username"
                    :is-admin
                    :data-source="controllsToggle"
                    :last-update="lastUpdate"
                    @update:toggle-data="controllsToggle = $event"
                    @start-recording="startRecording"
                    @stop-recording="stopRecording"
                    @download-file="downloadRecording"
                />

                <ChartPanel 
					v-if="dataTypeToggle === 'first'"
                    class="h-full min-h-0"
                    :toggleData="dataTypeToggle"
                    :recordings="recordings"
                    :selected-recording="selectedRecording"
                    :points="chartPoints"
                    :is-paused="isChartDataFlowPaused"
                    @clear-chart="clearChartData"
                    @pause-data-flow="pauseChartDataFlow"
                    @resume-data-flow="resumeChartDataFlow"
                    @upload-file="handleFileUpload"
                    @update:toggle-data="dataTypeToggle = $event"
                    @update:selected-recording="selectedRecording = $event"
                >
                </ChartPanel>

                <ChartPanel 
					v-if="dataTypeToggle === 'second'"
                    class="h-full min-h-0"
                    :toggleData="dataTypeToggle"
                    :recordings="recordings"
                    :selected-recording="selectedRecording"
                    :points="customChartPoints"
                    :is-paused="isChartDataFlowPaused"
                    @clear-chart="clearCustomChartData"
                    @pause-data-flow="pauseChartDataFlow"
                    @resume-data-flow="resumeChartDataFlow"
                    @upload-file="handleFileUpload"
                    @update:toggle-data="dataTypeToggle = $event"
                    @update:selected-recording="selectedRecording = $event"
                >
                </ChartPanel>
            </div>
        </div>
    </div>
</template>

<style scoped></style>
