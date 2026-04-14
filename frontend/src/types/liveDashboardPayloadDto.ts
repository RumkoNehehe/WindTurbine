import type { Motor } from "./motor"

export type LiveDashboardPayloadDto = {
    isConnected: boolean,
    lastUpdate: string,
    motors: Motor[],
    logs:string[]
}