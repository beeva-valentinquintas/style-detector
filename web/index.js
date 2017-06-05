
var videoInput = document.getElementById('inputVideo');
var canvasInput = document.getElementById('inputCanvas');

$( document ).ready(function() {
	htracker = new headtrackr.Tracker({
        ui: false,
        //debug: canvasInput
        debug: false
    });
    htracker.init(videoInput, canvasInput);
    htracker.start();

    setTimeout(function(){ getUserFaces(); }, 3000);

});

function getUserFaces(){

	var dataCaptured = canvasInput.toDataURL("image/png").replace("image/png", "");

    $("#imageCaptured").attr("src", dataCaptured );

    console.log( dataCaptured );

    labels = sendImage(dataCaptured);

    console.log(labels);
}

function convertToCognitiveFormat(dataURL) {
    var BASE64_MARKER = ';base64,';
    if (dataURL.indexOf(BASE64_MARKER) == -1) {
        var parts = dataURL.split(',');
        var contentType = parts[0].split(':')[1];
        var raw = decodeURIComponent(parts[1]);
        return new Blob([raw], { type: contentType });
    }
    var parts = dataURL.split(BASE64_MARKER);
    var contentType = parts[0].split(':')[1];
    var raw = window.atob(parts[1]);
    var rawLength = raw.length;

    var uInt8Array = new Uint8Array(rawLength);

    for (var i = 0; i < rawLength; ++i) {
        uInt8Array[i] = raw.charCodeAt(i);
    }

    return new Blob([uInt8Array], { type: contentType });
}


function sendImage(imageAsBytes) {
    var parts = imageAsBytes.split(',');
    url = "http://127.0.0.1:5000/labels"
    var oReq = new XMLHttpRequest();
    oReq.open("POST", url, true);
    oReq.onload = function (oEvent) {
        // do something to response
        console.log(this.responseText);
    };

    var blob = new Blob([parts[1]], {type: 'text/plain'});

    oReq.send(blob);
}

}