import { ref, onMounted } from "vue";
import {config} from '@/config'

export type UserRole = "guest" | "user" | "admin";

export function useAuth() {
    const userRole = ref<UserRole>("guest");
    const isCheckingAuth = ref(true);
    const loginError = ref("");

    async function checkSession() {
        try {
            isCheckingAuth.value = true;
            loginError.value = "";

            const response = await fetch(`${config.backendBaseUrl}/me`, {
                credentials: "include",
            });

            if (!response.ok) {
                throw new Error(`HTTP error: ${response.status}`);
            }

            const data = await response.json();

            userRole.value = data.authenticated
                ? (data.role ?? "guest")
                : "guest";
        } catch (error) {
            console.error("Session check failed:", error);
            userRole.value = "guest";
        } finally {
            isCheckingAuth.value = false;
        }
    }

    async function login(username: string, password: string) {
        try {
            loginError.value = "";

            const response = await fetch(`${config.backendBaseUrl}/login`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                credentials: "include",
                body: JSON.stringify({
                    username,
                    password,
                }),
            });

            const data = await response.json();

            if (!response.ok) {
                loginError.value = data.message ?? "Login failed.";
                return false;
            }

            userRole.value = data.role ?? "guest";
            return true;
        } catch (error) {
            console.error("Login failed:", error);
            loginError.value = "Could not connect to server.";
            return false;
        }
    }

    async function logout() {
        try {
            await fetch(`${config.backendBaseUrl}/logout`, {
                method: "POST",
                credentials: "include",
            });
        } catch (error) {
            console.error("Logout failed:", error);
        } finally {
            userRole.value = "guest";
        }
    }

    onMounted(() => {
        checkSession();
    });

    return {
        userRole,
        isCheckingAuth,
        loginError,
        login,
        logout,
    };
}
