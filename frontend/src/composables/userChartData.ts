import { ref, watch, type Ref } from "vue";
import type { LiveDashboardPayloadState } from "@/types/states/liveDashBoardState";
import type { ChartPoint } from "@/types/chartPoint";

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

    function toPwmPercent(number: number){
       return Math.round((number/255)*100)
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
                motor1Rpm: latest.motors[0]?.rpm ?? 0,
                motor1Pwm: toPwmPercent(latest.motors[0]?.pwm ?? 0),
                motor2Rpm: latest.motors[1]?.rpm ?? 0,
                motor2Pwm: toPwmPercent(latest.motors[1]?.pwm ?? 0),
            });

            chartPoints.value = chartPoints.value.slice(-200);
        },
    );

    return {
        isChartDataFlowPaused,
        chartPoints,
        clearChartData,
        pauseChartDataFlow,
        resumeChartDataFlow,
    };
}
