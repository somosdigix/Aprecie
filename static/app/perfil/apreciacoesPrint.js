var modal = document.getElementById("modal");

var btn = document.getElementById("modal-botao");

var span = document.getElementsByClassName("fechar")[0];

btn.onclick = function () {
	modal.style.display = "block";
}

span.onclick = function () {
	modal.style.display = "none";
}

window.onclick = function (event) {
	if (event.target == modal) {
		modal.style.display = "none";
	}
}

function saveAs() {

    html2canvas(document.querySelector('#print')).then(function(canvas) {

        var uri = canvas.toDataURL();
        var filename = "file-name.png"

        var link = document.createElement('a');

        if (typeof link.download === 'string') {
    
            link.href = uri;
            link.download = filename;
    
            document.body.appendChild(link);
    
            link.click();
    
            document.body.removeChild(link);
    
        } else {
    
            window.open(uri);
    
        }
    });

}


