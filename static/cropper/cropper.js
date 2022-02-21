function fecharModalCrop() {
    document.getElementById('caixa-modal').style.display = "none";
}

function readURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
            document.getElementById("imagem__selecionada__container").innerHTML = "<img id='imagem__selecionada' src=" + e.target.result + " alt='imagem selecionada'/>"
        };

        reader.readAsDataURL(input.files[0]);
        setTimeout(initCropper, 10);
        document.querySelector("#imagem__botao__cropper").style.display = "block";
    }
}

function getRoundedCanvas(sourceCanvas) {
    var canvas = document.createElement('canvas');
    var context = canvas.getContext('2d');
    var width = sourceCanvas.width;
    var height = sourceCanvas.height;

    canvas.width = width;
    canvas.height = height;
    context.imageSmoothingEnabled = true;
    context.drawImage(sourceCanvas, 0, 0, width, height);
    context.globalCompositeOperation = 'destination-in';
    context.beginPath();
    context.arc(width / 2, height / 2, Math.min(width, height) / 2, 0, 2 * Math.PI, true);
    context.fill();
    return canvas;
}

function initCropper() {
    var image = document.getElementById('imagem__selecionada');
    var cropper = new Cropper(image, {
        aspectRatio: 1 / 1,
        ready: function () {
            croppable = true;
        },
    });

    // On crop button clicked
    document.getElementById('crop_button').addEventListener('click', function () {
        var croppedCanvas = cropper.getCroppedCanvas();
        var roundedCanvas = getRoundedCanvas(croppedCanvas);
        var imgurl = roundedCanvas.toDataURL();

        document.getElementById("cropped_result").innerHTML = "<img id='imagem__cortada' class='imagem__cortada' src=" + imgurl + " alt='imagem cortada'/>"
    })
}