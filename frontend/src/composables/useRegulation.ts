import { ref, computed } from "vue";
import type { Socket } from "socket.io-client";
import type { MotorTarget } from "@/types/motorTarget";
import type { Mode } from "@/types/mode";

export function useRegulation(socket: Socket) {
    const isRegulation = ref(false);

    const motorTarget = ref<MotorTarget>("motor1");
    const targetRpm = ref(500);
    const kp = ref(0.6);
    const ki = ref(0.5);
    const kd = ref(0.12);
    const mode = ref<Mode>("FORWARD");
    const isRegulating = ref(false);

    const regulationControl = computed(() => ({
        motorTarget: motorTarget.value,
        targetRpm: targetRpm.value,
        kp: kp.value,
        ki: ki.value,
        kd: kd.value,
        mode: mode.value,
        isRegulating: isRegulating.value,
    }));

    function startRegulation() {
        socket.emit("start_regulation", {
            target: motorTarget.value,
            target_rpm: targetRpm.value,
            kp: kp.value,
            ki: ki.value,
            kd: kd.value,
            mode: mode.value,
        });

        isRegulating.value = true;
    }

    function stopRegulation() {
        socket.emit("stop_regulation");
        isRegulating.value = false;
    }

    function toggleRegulationView() {
        isRegulation.value = !isRegulation.value;
    }

    return {
        isRegulation,
        motorTarget,
        targetRpm,
        kp,
        ki,
        kd,
        mode,
        isRegulating,
        regulationControl,
        startRegulation,
        stopRegulation,
        toggleRegulationView,
    };
}