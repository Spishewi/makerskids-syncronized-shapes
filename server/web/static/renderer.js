const socket = io("http://127.0.0.1:8080/renderer", { transports: ["websocket"] }); // will use the /renderer namespace later
console.log(socket);

let shapes = {};

socket.on("connect", () => {
    console.log("Connected to the server.");
    socket.emit("get_shapes", (data) => {
        shapes = data;
    });
})

socket.on("disconnect", () => {
    console.log("Disconnected from the server.");
})

socket.on("shapes_update", (data) => {

    new_shapes = data.new;
    updated_shapes = data.updated;
    deleted_shapes = data.deleted;

    for (let i = 0; i < new_shapes.length; i++) {
        shapes[updated_shapes[i][0]] = (updated_shapes[i][1], updated_shapes[i][2])
    }

    for (let i = 0; i < updated_shapes.length; i++) {
        shapes[updated_shapes[i][0]] = (updated_shapes[i][1], updated_shapes[i][2]);
    }

    for (let i = 0; i < deleted_shapes.length; i++) {
        delete shapes[deleted_shapes[i][0]];
    }
})

function draw_canvas() {
    const canvas = document.getElementById("canvas-renderer");
    const ctx = canvas.getContext("2d");
    ctx.fillStyle = "white";
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // TODO
    ctx.fillStyle = "green";
    x = 200 + Math.sin(Date.now()/1000) * 100;
    y = 200 + Math.cos(Date.now()/1000) * 100;

    ctx.fillRect(x, y, 20, 20);
}

setInterval(() => {
    draw_canvas();
}, 33/2);

setInterval(() => {
    console.log(shapes);
}, 1000)