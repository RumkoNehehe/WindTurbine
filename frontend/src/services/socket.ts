import { io, Socket } from 'socket.io-client'

let socket: Socket | null = null

export function getSocket() {
    if (!socket) {
        socket = io("localhost:8000", {
            autoConnect: false,
        });
    }

    return socket
}