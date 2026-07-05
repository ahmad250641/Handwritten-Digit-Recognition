const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");

// إعداد اللوحة
ctx.fillStyle = "black";
ctx.fillRect(0, 0, canvas.width, canvas.height);

ctx.strokeStyle = "white";
ctx.lineWidth = 18;
ctx.lineCap = "round";
ctx.lineJoin = "round";

let drawing = false;

/*==============================
    Mouse Events
==============================*/

canvas.addEventListener("mousedown", startDrawing);
canvas.addEventListener("mousemove", draw);
canvas.addEventListener("mouseup", stopDrawing);
canvas.addEventListener("mouseleave", stopDrawing);

/*==============================
    Touch Events (Mobile)
==============================*/

canvas.addEventListener("touchstart", touchStart, { passive: false });
canvas.addEventListener("touchmove", touchMove, { passive: false });
canvas.addEventListener("touchend", stopDrawing);

/*==============================
    Drawing Functions
==============================*/

function getPosition(event) {

    const rect = canvas.getBoundingClientRect();

    return {
        x: event.clientX - rect.left,
        y: event.clientY - rect.top
    };
}

function startDrawing(event) {

    drawing = true;

    const pos = getPosition(event);

    ctx.beginPath();
    ctx.moveTo(pos.x, pos.y);
}

function draw(event) {

    if (!drawing) return;

    const pos = getPosition(event);

    ctx.lineTo(pos.x, pos.y);
    ctx.stroke();
}

function stopDrawing() {

    drawing = false;
    ctx.beginPath();
}

/*==============================
    Touch Support
==============================*/

function touchStart(event) {

    event.preventDefault();

    startDrawing(event.touches[0]);
}

function touchMove(event) {

    event.preventDefault();

    draw(event.touches[0]);
}

/*==============================
    Clear Canvas
==============================*/

document.getElementById("clearBtn").addEventListener("click", () => {

    ctx.fillStyle = "black";
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    document.getElementById("digit").innerText = "Digit: -";
    document.getElementById("confidence").innerText = "Confidence: -";
});

/*==============================
    Predict
==============================*/

document.getElementById("predictBtn").addEventListener("click", predictDigit);

async function predictDigit() {

    const image = canvas.toDataURL("image/png");

    try {

        const response = await fetch("/predict", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                image: image
            })

        });

        const result = await response.json();

        if (result.error) {

            alert(result.error);
            return;
        }

        document.getElementById("digit").innerText =
            "Digit: " + result.digit;

        document.getElementById("confidence").innerText =
            "Confidence: " + result.confidence.toFixed(2) + "%";

    }

    catch (error) {

        alert("Server Error");
        console.error(error);

    }

}