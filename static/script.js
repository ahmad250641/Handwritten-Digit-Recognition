const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");

// إعداد اللوحة بخلفية سوداء صلبة عند البدء
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
    const tempCanvas = document.createElement("canvas");
    tempCanvas.width = 280;
    tempCanvas.height = 280;
    const tempCtx = tempCanvas.getContext("2d");

    // ملء الخلفية بالأبيض (عكس التنسيق المعتاد للرسم)
    tempCtx.fillStyle = "white";
    tempCtx.fillRect(0, 0, 280, 280);
    
    // رسم المحتوى الأصلي
    tempCtx.drawImage(canvas, 0, 0);

    // عكس ألوان الصورة برمجياً لضمان توحيد المدخلات (الرقم يصبح أسود على خلفية بيضاء)
    const imageData = tempCtx.getImageData(0, 0, 280, 280);
    const data = imageData.data;
    for (let i = 0; i < data.length; i += 4) {
        data[i] = 255 - data[i];     // R
        data[i + 1] = 255 - data[i + 1]; // G
        data[i + 2] = 255 - data[i + 2]; // B
    }
    tempCtx.putImageData(imageData, 0, 0);

    const image = tempCanvas.toDataURL("image/png");

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
            console.error(result.error);
            return;
        }
        document.getElementById("digit").innerText = "Digit: " + result.digit;
        document.getElementById("confidence").innerText = "Confidence: " + result.confidence.toFixed(2) + "%";
    }
    catch (error) {
        console.error("Server Error", error);
    }
}