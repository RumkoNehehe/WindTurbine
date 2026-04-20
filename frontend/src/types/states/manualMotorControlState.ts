import type { MotorTarget } from "../motorTarget"
import type { Mode } from "../mode"

export type ManualMotorControlState = {
    motorTarget: MotorTarget
    pwm: number
    mode: Mode
}