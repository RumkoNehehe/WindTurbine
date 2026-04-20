import type { Motor } from "../motor"

export type LiveDashboardPayloadState = {
    lastUpdate: Date,
    motors: Motor[],
}