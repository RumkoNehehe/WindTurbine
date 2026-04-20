import { ref } from "vue";
import type { LiveDashboardPayloadState } from "@/types/states/liveDashBoardState";

type ChartPoint = {
    label: string;
    motor1: number;
    motor2: number;
};

export function useRecording() {
    const isRecording = ref(false);
    const record = ref<LiveDashboardPayloadState[]>([]);
    const customChartPoints = ref<ChartPoint[]>([]);

    function startRecording() {
        record.value = [];
        isRecording.value = true;
    }

    function stopRecording() {
        isRecording.value = false;
    }

    function appendToRecording(entry: LiveDashboardPayloadState) {
        if (!isRecording.value) return;
        record.value.push(entry);
    }

    function downloadRecording() {
        if (isRecording.value || record.value.length === 0) {
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
        const target = event.target as HTMLInputElement;
        const file = target.files?.[0];

        if (!file) return;

        const reader = new FileReader();

        reader.onload = () => {
            try {
                const text = reader.result as string;
                const parsed = JSON.parse(text);

                if (!Array.isArray(parsed)) {
                    throw new Error("Invalid format");
                }

                customChartPoints.value = parsed.map((item: any) => ({
                    label: new Date(item.lastUpdate).toLocaleString("en-GB", {
                        hour: "2-digit",
                        minute: "2-digit",
                        second: "2-digit",
                    }),
                    motor1: item.motors?.[0]?.rpm ?? 0,
                    motor2: item.motors?.[1]?.rpm ?? 0,
                }));
            } catch (err) {
                console.error(err);
                alert("Invalid JSON file");
            }
        };

        reader.readAsText(file);
        target.value = "";
    }

    function clearCustomChartData() {
        customChartPoints.value = [];
    }

    return {
        isRecording,
        customChartPoints,
        startRecording,
        stopRecording,
        appendToRecording,
        downloadRecording,
        handleFileUpload,
        clearCustomChartData,
    };
}