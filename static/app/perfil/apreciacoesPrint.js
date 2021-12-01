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