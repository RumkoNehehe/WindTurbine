import { onMounted, ref } from "vue";
import type { LiveDashboardPayloadState } from "@/types/states/liveDashBoardState";
import type { ChartPoint } from "@/types/chartPoint";
import type { RecordingListItem } from "@/types/recordingListItem";
import type { RecordingSnapshot } from "@/types/recordingSnapshot";

export function useRecording() {
    const isRecording = ref(false);
    const record = ref<LiveDashboardPayloadState[]>([]);
    const customChartPoints = ref<ChartPoint[]>([]);
    const recordings = ref<RecordingListItem[]>([]);
    const selectedRecordingId = ref<number | null>(null);
    const selectedRecording = ref<any>(null);

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

    async function fetchRecordings() {
        try {
            const response = await fetch("http://localhost:8000/recording", {
                credentials: "include",
            });

            if (!response.ok) {
                throw new Error(`HTTP error: ${response.status}`);
            }

            const result = await response.json();
            recordings.value = result.data;
        } catch (error) {
            console.error("Fetch recordings failed:", error);
        }
    }

    async function fetchRecordingById(id: number) {
        const response = await fetch(`http://localhost:8000/recording/${id}`, {
            credentials: "include",
        });

        const result = await response.json();
        return mapRecordingToChartPoints(result.data);
    }

    function mapRecordingToChartPoints(
        data: RecordingSnapshot[],
    ): ChartPoint[] {
        return data.map((snapshot) => {
            const motor1 = snapshot.motors.find((m) => m.name === "Motor 1");
            const motor2 = snapshot.motors.find((m) => m.name === "Motor 2");

            return {
                label: new Date(snapshot.lastUpdate).toLocaleTimeString(
                    "en-GB",
                    {
                        hour: "2-digit",
                        minute: "2-digit",
                        second: "2-digit",
                    },
                ),
                motor1Rpm: motor1?.rpm ?? 0,
                motor1Pwm: motor1?.pwm ?? 0,
                motor2Rpm: motor2?.rpm ?? 0,
                motor2Pwm: motor2?.pwm ?? 0,
            };
        });
    }

    async function saveFileToDatabase() {
        if (isRecording.value || record.value.length === 0) {
            return;
        }

        const now = new Date();

        const name = `rec-${now
            .toISOString()
            .slice(0, 16)
            .replace("T", "_")
            .replace(":", "-")}`;
        try {
            const response = await fetch("http://localhost:8000/recording", {
                method: "POST",
                credentials: "include",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    name,
                    data: record.value,
                }),
            });

            const result = await response.json();

            if (!response.ok) {
                throw new Error(
                    result.message || `HTTP error: ${response.status}`,
                );
            }

            await fetchRecordings();
        } catch (error) {
            console.error("Save recording failed:", error);
        }
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
                    motor1Rpm: item.motors?.[0]?.rpm ?? 0,
                    motor1Pwm: item.motors?.[0]?.pmw ?? 0,
                    motor2Rpm: item.motors?.[1]?.rpm ?? 0,
                    motor2Pwm: item.motors?.[1]?.pmw ?? 0,
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

    onMounted(() => {
        fetchRecordings();
    });

    return {
        isRecording,
        customChartPoints,
        recordings,
        selectedRecordingId,
        fetchRecordingById,
        startRecording,
        stopRecording,
        appendToRecording,
        downloadRecording,
        handleFileUpload,
        saveFileToDatabase,
        clearCustomChartData,
    };
}
