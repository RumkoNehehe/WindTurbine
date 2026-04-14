import type { Motor } from "./motor"

export type LiveDashboardPayload = {
    isConnected: boolean,
    lastUpdate: string,
    motors: Motor[],
    logs:string[]
}