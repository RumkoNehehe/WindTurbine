import { io, Socket } from 'socket.io-client'

let socket: Socket | null = null

export function getSocket() {
    if (!socket) {
        socket = io('http://192.168.0.111:5000', {
            autoConnect: false
        })
    }

    return socket
}