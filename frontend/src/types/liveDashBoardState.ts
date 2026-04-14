import type { Motor } from "./motor"

export type LiveDashboardPayloadState = {
    isConnected: boolean,
    lastUpdate: Date,
    motors: Motor[],
}