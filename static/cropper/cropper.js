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
        
        var img = "<img id='imagem__cortada' class='imagem__cortada' src=" + imgurl + " alt='imagem cortada'/> ";
        var paragrafo = "<p> Resultado: </p>";
        var paragrafoInvisivel = "<p class='invisivel' id='url_imagem_cortada'>" + imgurl + "</p>";
        document.getElementById("cropped_result").innerHTML = paragrafoInvisivel + paragrafo + img;
        
    })
}