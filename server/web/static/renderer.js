const socket = io("http://127.0.0.1:8080/client", { transports: ["websocket"] }); // will use the /renderer namespace later
console.log(socket);
socket.on("connect", () => {
    console.log("Connected to the server.");
})