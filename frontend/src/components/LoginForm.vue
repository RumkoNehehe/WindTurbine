<script setup lang="ts">
import { ref } from "vue";
import BaseButton from "@/components/base/BaseButton.vue";
import BaseCard from "./base/BaseCard.vue";

const emit = defineEmits<{
    (e: "login", username: string, password: string): void;
}>();

defineProps<{
    errorMessage?: string;
}>();

const username = ref("");
const password = ref("");

function handleSubmit() {
    emit("login", username.value, password.value);
}
</script>

<template>
        <BaseCard variant="dark" class="w-full max-w-md p-6 bg-gray-800 shadow-lg">
            <h1 class="mb-6 text-center text-3xl font-bold text-white">
                Log in
            </h1>

            <div class="flex flex-col gap-4">
                <div class="flex flex-col gap-2">
                    <label class="text-sm font-semibold text-white">
                        Username
                    </label>
                    <input
                        v-model="username"
                        type="text"
                        class="rounded-xl bg-white px-4 py-2 text-sm outline-none"
                    />
                </div>

                <div class="flex flex-col gap-2">
                    <label class="text-sm font-semibold text-white">
                        Password
                    </label>
                    <input
                        v-model="password"
                        type="password"
                        class="rounded-xl bg-white px-4 py-2 text-sm outline-none"
                        @keyup.enter="handleSubmit"
                    />
                </div>

                <p v-if="errorMessage" class="text-sm font-semibold text-red-300">
                    {{ errorMessage }}
                </p>

                <BaseButton variant="primary" @click="handleSubmit">
                    Login
                </BaseButton>
            </div>
        </BaseCard>
</template>