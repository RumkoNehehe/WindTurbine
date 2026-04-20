import { ref, watch, type Ref } from "vue";
import type { LiveDashboardPayloadState } from "@/types/states/liveDashBoardState";

type ChartPoint = {
    label: string;
    motor1: number;
    motor2: number;
};

export function useChartData(
    dashboardHistory: Ref<LiveDashboardPayloadState[]>,
) {
    const isChartDataFlowPaused = ref(true);
    const chartPoints = ref<ChartPoint[]>([]);

    function clearChartData() {
        chartPoints.value = [];
    }

    function pauseChartDataFlow() {
        isChartDataFlowPaused.value = true;
    }

    function resumeChartDataFlow() {
        isChartDataFlowPaused.value = false;
    }

    watch(
        () => dashboardHistory.value.length,
        () => {
            const latest = dashboardHistory.value.at(-1);
            if (!latest) return;
            if (isChartDataFlowPaused.value) return;

            chartPoints.value.push({
                label: latest.lastUpdate.toLocaleString("en-GB", {
                    hour: "2-digit",
                    minute: "2-digit",
                    second: "2-digit",
                }),
                motor1: latest.motors[0]?.rpm ?? 0,
                motor2: latest.motors[1]?.rpm ?? 0,
            });

            chartPoints.value = chartPoints.value.slice(-200);
        }
    );

    return {
        isChartDataFlowPaused,
        chartPoints,
        clearChartData,
        pauseChartDataFlow,
        resumeChartDataFlow,
    };
}