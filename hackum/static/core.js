httpGET = function(url, data, cb) {
    var r = new XMLHttpRequest();
    if(!data) {
        data = "";
    } else if(typeof data != 'string')  {
        data = Object.keys(data).map(function(key) { return key + '=' + data[key]; }).join('&');
    }
    data += "&csrfmiddlewaretoken=" + window.csrfToken;
    r.open("GET", url + data, true);
    r.onreadystatechange = function () {
      if (r.readyState != 4 || r.status != 200) return;
      cb(r.responseText);
    };
    r.send();
}

httpPOST = function(url, data, cb) {
    var r = new XMLHttpRequest();
    r.open("POST", url, true);
    r.onreadystatechange = function () {
      if (r.readyState != 4 || r.status != 200) return;
      cb(r.responseText);
    };
    if(!data) {
        data = "";
    } else if(typeof data != 'string')  {
        data = Object.keys(data).map(function(key) { return key + '=' + data[key]; }).join('&');
    }
    data += "&csrfmiddlewaretoken=" + window.csrfToken;
    r.send(data);
}

b64toblob = function(base64, mime) {
    mime = mime || '';
    var sliceSize = 1024;
    var byteChars = window.atob(base64);
    var byteArrays = [];

    for (var offset = 0, len = byteChars.length; offset < len; offset += sliceSize) {
        var slice = byteChars.slice(offset, offset + sliceSize);

        var byteNumbers = new Array(slice.length);
        for (var i = 0; i < slice.length; i++) {
            byteNumbers[i] = slice.charCodeAt(i);
        }

        var byteArray = new Uint8Array(byteNumbers);

        byteArrays.push(byteArray);
    }

    return new Blob(byteArrays, {type: mime});
}