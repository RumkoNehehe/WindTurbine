import { io, Socket } from 'socket.io-client'

let socket: Socket | null = null

export function getSocket() {
    if (!socket) {
        socket = io("http://192.168.0.165:5000", {
            transports: ["websocket"],
            autoConnect: false,
        });
    }

    return socket
}