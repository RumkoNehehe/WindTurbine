import { io, Socket } from 'socket.io-client'
import {config} from '@/config'

let socket: Socket | null = null

export function getSocket() {
    if (!socket) {
        socket = io(config.backendBaseUrl, {
            autoConnect: false,
            withCredentials: true
        });
    }

    return socket
}