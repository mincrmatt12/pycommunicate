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
            socket.on('element.exists', function (dat) {
                var selector_ = dat[0];
                var return_tag = dat[1];
                var result = !!document.querySelector(selector_);
                socket.emit("response", result, return_tag);
            });
            socket.on('view.swap', function (dat) {
                document.write(dat);
                document.close();
            });
            socket.on('element.property', function (dat) {
                var selector = dat[0];
                var name = dat[1];
                var return_tag = dat[2];
                
                var result = document.querySelector(selector)[name];
                socket.emit("response", result, return_tag)
            });
            socket.on('element.property.set', function (dat) {
                var selector = dat[0];
                var name = dat[1];
                document.querySelector(selector)[name] = dat[2];
            });
            socket.on('element.addevent', function (dat) {
                var selector = dat[0];
                var name = dat[1];
                var event_id = dat[2];
                
                function handler() {
                    socket.emit('event', event_id);
                }
                
                addEventListener(document.querySelector(selector), name, handler);
            });
        },

        _connect: function () {
            this._socket.emit("setup", requestID);
        },

        _teardown: function () {
            this._socket.emit("teardown", requestID);
        }
    };

    return pycommunicate;
}());

addEventListener(document, "ready", pycommunicate._ready());

addEventListener(document, "beforeunload", pycommunicate._teardown());