import type { MotorTarget } from "../motorTarget"
import type { Mode } from "../mode"

export type MotorRegulationState = {
    motorTarget: MotorTarget
    targetRpm: number
    kp: number
    ki: number
    kd: number
    mode: Mode
    isRegulating: boolean
}