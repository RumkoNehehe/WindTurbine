import type { RecordingMotor } from "./recordingMotor";

export type RecordingSnapshot = {
    lastUpdate: string;
    motors: RecordingMotor[];
};
