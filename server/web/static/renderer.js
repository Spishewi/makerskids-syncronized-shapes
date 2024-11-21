// Connect to the server
const socket = io("http://127.0.0.1:8080/renderer", {
	transports: ["websocket"],
}); // will use the /renderer namespace later
console.log(socket);

// Global variable to store the shapes
let shapes = {};
let usernames = [];

// Event handler for the "connect" event
socket.on("connect", () => {
	console.log("Connected to the server.");
	socket.emit("get_shapes", (data) => {
		shapes = data;
		console.log("Shapes: ", shapes);
	});
	socket.emit("get_usernames", (data) => {
		console.log("Usernames: ", data);
		update_usernames(data);
	});
});

// Event handler for the "disconnect" event
socket.on("disconnect", () => {
	console.log("Disconnected from the server.");
});

socket.on("usernames_update", (data) => {
	update_usernames(data);
});

// Event handler for the "shapes_update" event
socket.on("shapes_update", (data) => {
	// Get the updated shapes
	new_shapes = data.new;
	updated_shapes = data.updated;
	deleted_shapes = data.deleted;

	// add new shapes to the shapes object
	if (new_shapes && new_shapes.length > 0) {
		for (let i = 0; i < new_shapes.length; i++) {
			shapes[new_shapes[i][0]] = [new_shapes[i][1], new_shapes[i][2]];
		}
	}

	// update existing shapes in the shapes object
	if (updated_shapes && updated_shapes.length > 0) {
		for (let i = 0; i < updated_shapes.length; i++) {
			shapes[updated_shapes[i][0]] = [
				updated_shapes[i][1],
				updated_shapes[i][2],
			];
		}
	}

	// delete shapes from the shapes object
	if (deleted_shapes && deleted_shapes.length > 0) {
		for (let i = 0; i < deleted_shapes.length; i++) {
			delete shapes[deleted_shapes[i]];
		}
	}
});

function update_usernames(data) {
	console.log("update_usernames: ", data);
	if (data === undefined) return;

	usernames = data;

	usernames_list = document.getElementById("usernames-list");
	usernames_list.innerHTML = "";

	for (const [uuid, username] of Object.entries(usernames)) {
		li = document.createElement("li");
		li.innerText = username;

		usernames_list.appendChild(li);
	}
}

/**
 * Draws the canvas by iterating through the shapes and calling the appropriate drawing function.
 */
function draw_canvas() {
	const canvas = document.getElementById("canvas-renderer");
	const ctx = canvas.getContext("2d");

	// Clear the canvas by drawing a white rectangle over it
	ctx.fillStyle = "white";
	ctx.fillRect(0, 0, canvas.width, canvas.height);

	// Iterate through the shapes and draw each one
	for (const [uuid, shape] of Object.entries(shapes)) {
		if (shape[0] == "Rectangle") {
			// Draw a rectangle
			draw_rect(ctx, shape[1]);
		} else if (shape[0] == "SpaceShip") {
			// Draw a rectangle
			draw_spaceship(ctx, shape[1]);
		} else if (shape[0] == "Ellipse") {
			// Draw an ellipse
			draw_ellipse(ctx, shape[1]);
		} else if (shape[0] == "Line") {
			// Draw a line
			draw_line(ctx, shape[1]);
		}
	}
}

/**
 * Draws a rectangle on the canvas.
 * @param {CanvasRenderingContext2D} ctx - The 2D rendering context for the drawing surface of the canvas.
 * @param {Object} data - The data containing rectangle properties.
 * @param {number} data.__x - The x-coordinate of the top left corner.
 * @param {number} data.__y - The y-coordinate of the top left corner.
 * @param {number} data.__width - The width of the rectangle.
 * @param {number} data.__height - The height of the rectangle.
 * @param {Array} data.__color - An array representing the RGB color of the rectangle.
 */
function draw_rect(ctx, data) {
	const { x, y, width, height, color } = {
		x: data["__x"],
		y: data["__y"],
		width: data["__width"],
		height: data["__height"],
		color: data["__color"],
	};

	// Set the fill color for the rectangle
	ctx.fillStyle = `rgb(${color[0]}, ${color[1]}, ${color[2]})`;

	// Draw the rectangle
	ctx.fillRect(x, y, width, height);
}

/**
 * Draws an ellipse on the canvas.
 * @param {CanvasRenderingContext2D} ctx - The 2D rendering context for the drawing surface of the canvas.
 * @param {Object} data - The data containing ellipse properties.
 * @param {number} data.__x - The x-coordinate of the center of the ellipse.
 * @param {number} data.__y - The y-coordinate of the center of the ellipse.
 * @param {number} data.__x_radius - The x-axis radius of the ellipse.
 * @param {number} data.__y_radius - The y-axis radius of the ellipse.
 * @param {Array} data.__color - An array representing the RGB color of the ellipse.
 */
function draw_ellipse(ctx, data) {
	const { x, y, x_radius, y_radius, color } = {
		x: data["__x"],
		y: data["__y"],
		x_radius: data["__x_radius"],
		y_radius: data["__y_radius"],
		color: data["__color"],
	};

	// Set the fill color for the ellipse
	ctx.fillStyle = `rgb(${color[0]}, ${color[1]}, ${color[2]})`;

	// Begin the path for the ellipse shape
	ctx.beginPath();

	// Draw the ellipse
	ctx.ellipse(x, y, x_radius, y_radius, 0, 0, 2 * Math.PI);

	// Fill the ellipse with the specified color
	ctx.fill();
}

function degToRad(degrees) {
	// Store the value of pi.
	var pi = Math.PI;
	// Multiply degrees by pi divided by 180 to convert to radians.
	return degrees * (pi / 180);
}

function draw_spaceship(ctx, data) {
	const { __x: x, __y: y, __rotation: rotation, __color: color } = data;

	const height = 50;
	const width = 16;
	const bottomCenter = {
		x: 0,
		y: height * 0.3,
	};
	ctx.save();
	ctx.translate(x, y);
	ctx.rotate(degToRad(rotation));

	// Set the fill color for the ellipse
	ctx.fillStyle = `rgb(${color[0]}, ${color[1]}, ${color[2]})`;

	// Begin the path for the ellipse shape
	ctx.beginPath();
	ctx.moveTo(bottomCenter.x, bottomCenter.y);
	// Half bottom line
	ctx.lineTo(bottomCenter.x + width * 0.3, bottomCenter.y);
	// Right curved line
	ctx.bezierCurveTo(
		bottomCenter.x + width,
		bottomCenter.y - height * 0.2,
		bottomCenter.x + width,
		bottomCenter.y - height * 0.8,
		bottomCenter.x,
		bottomCenter.y - height
	);
	// Left curved line
	ctx.bezierCurveTo(
		bottomCenter.x - width,
		bottomCenter.y - height * 0.8,
		bottomCenter.x - width,
		bottomCenter.y - height * 0.2,
		bottomCenter.x - width * 0.3,
		bottomCenter.y
	);
	// Other half bottom line
	ctx.lineTo(bottomCenter.x, bottomCenter.y);
	ctx.strokeStyle = "#000000";
	ctx.fillStyle = `rgb(${color[0]}, ${color[1]}, ${color[2]})`;
	ctx.fill();
	ctx.lineWidth = 0.5;
	ctx.closePath();
	ctx.stroke();
	ctx.fill();
	draw_spaceship_foot(ctx, -width, height, color);
	draw_spaceship_foot(ctx, width, height, color);
	drawWindow(ctx, height, width);
	ctx.restore();
}

function draw_spaceship_foot(ctx, offsetWidth, height, color) {
	x = y = 0;
	ctx.beginPath();
	ctx.moveTo(x + offsetWidth * 0.85, y);
	ctx.quadraticCurveTo(
		x + offsetWidth * 2,
		y + height * 0.2,
		x + offsetWidth * 0.75,
		y + height * 0.45
	);
	ctx.quadraticCurveTo(
		x + offsetWidth * 1.2,
		y + height * 0.2,
		x + offsetWidth * 0.6,
		y + height * 0.25
	);
	ctx.lineWidth = 0.5;
	ctx.fillStyle = "#000000";
	ctx.strokeStyle = `rgb(${color[0]}, ${color[1]}, ${color[2]})`;
	ctx.closePath();
	ctx.fill();
	ctx.stroke();
}

function drawWindow(ctx, width, height, color) {
	const initialX = 0;
	const windowRadius = width * 0.1;
	const windowYPosition = -height;
	ctx.beginPath();
	ctx.moveTo(windowRadius, windowYPosition);
	ctx.arc(initialX, windowYPosition, windowRadius, 0, 2 * Math.PI);
	ctx.lineWidth = 1;
	ctx.fillStyle = "#1297E0";
	ctx.strokeStyle = "#0067B0";
	ctx.closePath();
	ctx.fill();
	ctx.stroke();
}
/**
 * Draws a line on the canvas.
 * @param {CanvasRenderingContext2D} ctx - The 2D rendering context for the drawing surface of the canvas.
 * @param {Object} data - The data containing line properties.
 * @param {number} data.__x1 - The x-coordinate of the start point.
 * @param {number} data.__y1 - The y-coordinate of the start point.
 * @param {number} data.__x2 - The x-coordinate of the end point.
 * @param {number} data.__y2 - The y-coordinate of the end point.
 * @param {Array} data.__color - An array representing the RGB color of the line.
 */
function draw_line(ctx, data) {
	// Destructure the properties from the data object
	const { x1, y1, x2, y2, color } = {
		x1: data["__x1"],
		y1: data["__y1"],
		x2: data["__x2"],
		y2: data["__y2"],
		color: data["__color"],
	};

	// Set the stroke color for the line
	ctx.strokeStyle = `rgb(${color[0]}, ${color[1]}, ${color[2]})`;

	// Begin a new path for the line
	ctx.beginPath();
	ctx.moveTo(x1, y1); // Move to the start point
	ctx.lineTo(x2, y2); // Draw the line to the end point
	ctx.stroke(); // Render the line
}

// Draw the canvas 60 times per second
setInterval(() => {
	draw_canvas();
}, 1000 / 60);

// Print the shapes every 5 second
setInterval(() => {
	console.log("Shapes: ", shapes);
}, 5000);
