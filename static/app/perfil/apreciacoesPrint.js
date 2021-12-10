function sumirModal() {
    document.getElementById("modal").style.visibility = "hidden";
    document.getElementById("corpo-modal").style.visibility = "hidden";
  }

  function gerarModal() {
    document.getElementById("modal").style.visibility = "visible";
    document.getElementById("corpo-modal").style.visibility = "visible";
  }

  function SaveAs() {
    html2canvas(document.querySelector("#card")).then(function (canvas) {
      var uri = canvas.toDataURL();
      var filename = "file-name.png";

      var link = document.createElement("a");

      if (typeof link.download === "string") {
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