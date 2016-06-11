/*

pycommunicate.js - the main js library for pycommunicate.


<insert copyrights and blab here>

 */

var requestID = "{{ request_id }}";


var addEventListener = (function() {
    if (document.addEventListener) {
        return function (element, event, func) {
            element.addEventListener(event, func);
        }
    }
    else if (document.attachEvent) {
        return function (element, event, func) {
            element.attachEvent("on" + event, func);
        }
    }
    else {
        return function (element, event, func) {
            element["on" + event] = func
        }
    }
}());


window.pycommunicate = (function () {
    //noinspection UnnecessaryLocalVariableJS
    var pycommunicate = {

        _socket: null,

        _ready: function () {
            var socket = io.connect('http://' + document.domain + ':' + location.port);
            pycommunicate._socket = socket;
            socket.on('connect', function () {
               pycommunicate._connect(); 
            });
        },

        _connect: function () {
            this._socket.emit("setup", requestID);
        }

    };

    return pycommunicate;
}());

addEventListener(document, "ready", pycommunicate._ready());