import { ref, onMounted, onBeforeUnmount } from "vue";
import { getSocket } from "@/services/socket";
import type { Motor } from "@/types/motor";
import type { LiveDashboardPayloadDto } from "@/types/liveDashboardPayloadDto";
import type { LiveDashboardPayloadState } from "@/types/states/liveDashBoardState";

export function useSocketDashboard() {
    const socket = getSocket();

    const motors = ref<Motor[]>([
        { name: "Motor1", pwm: 0, rpm: 0, mode: "Brake" },
        { name: "Motor2", pwm: 0, rpm: 0, mode: "Brake" },
    ]);

    const isConnected = ref(false);
    const lastUpdate = ref("");
    const logs = ref<string[]>([]);
    const dashboardHistory = ref<LiveDashboardPayloadState[]>([]);

    function handleConnect() {
        isConnected.value = true;
    }

    function handleDisconnect() {
        isConnected.value = false;
    }

    function mapDashboardState(
        payload: LiveDashboardPayloadDto,
    ): LiveDashboardPayloadState {
        return {
            lastUpdate: new Date(payload.lastUpdate),
            motors: payload.motors,
        };
    }

    function handleDashboardUpdate(payload: LiveDashboardPayloadDto) {
        const mapped = mapDashboardState(payload);

        dashboardHistory.value.push(mapped);
        isConnected.value = payload.isConnected;
        lastUpdate.value = mapped.lastUpdate.toLocaleString("en-GB", {
            hour: "2-digit",
            minute: "2-digit",
        });
        motors.value = mapped.motors;

        mapped.motors.forEach((motor) => {
            const log = `[${mapped.lastUpdate.toLocaleString("en-GB", {
                hour: "2-digit",
                minute: "2-digit",
            })}] ${motor.name} → pwm: ${motor.pwm}, rpm: ${motor.rpm}, mode: ${motor.mode}`;

            logs.value.unshift(log);
        });
    }

    function connect() {
        socket.connect();

        socket.on("connect", handleConnect);
        socket.on("disconnect", handleDisconnect);
        socket.on("dashboard_update", handleDashboardUpdate);
    }

    function disconnect() {
        socket.off("connect", handleConnect);
        socket.off("disconnect", handleDisconnect);
        socket.off("dashboard_update", handleDashboardUpdate);

        socket.disconnect();
    }

    onMounted(() => {
        connect();
    });

    onBeforeUnmount(() => {
        disconnect();
    });

    return {
        socket,
        motors,
        isConnected,
        lastUpdate,
        logs,
        dashboardHistory,
        connect,
        disconnect,
    };
}