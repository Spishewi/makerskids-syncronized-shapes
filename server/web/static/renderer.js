const socket = io("http://127.0.0.1:8080/renderer", { transports: ["websocket"] }); // will use the /renderer namespace later
console.log(socket);

socket.on("connect", () => {
    console.log("Connected to the server.");
})

function draw_canvas() {
    const canvas = document.getElementById("canvas-renderer");
    const ctx = canvas.getContext("2d");
    ctx.fillStyle = "black";
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    ctx.fillStyle = "green";
    x = 200 + Math.sin(Date.now()/1000) * 100;
    y = 200 + Math.cos(Date.now()/1000) * 100;

    ctx.fillRect(x, y, 20, 20);
}

setInterval(() => {
    draw_canvas();
}, 33/2);