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
            socket.on('element.property.complex', function (dat) {
                var selector = dat[0];
                var base = dat[1];
                var other = dat[2];
                var return_tag = dat[3];

                var result = document.querySelector(selector)[base][other];
                socket.emit("response", result, return_tag);
            });
            socket.on('element.property.complex.set', function (dat) {
                var selector = dat[0];
                var base = dat[1];
                var other = dat[2];
                var value = dat[3];

                document.querySelector(selector)[base][other] = value;
            });
            socket.on('element.add.after', function (dat) {
                var selector = dat[0];
                var target_type = dat[1];
                var target_id = dat[2];
                var ack_id = dat[3];

                var ele = document.createElement(target_type);
                ele.id = target_id;
               
                var reference = document.querySelector(selector);
                reference.parentNode.insertBefore(ele, reference.nextSibling);
                
                socket.emit("response", true, ack_id);
            });
            socket.on('element.add.inside', function (dat) {
                var selector = dat[0];
                var target_type = dat[1];
                var target_id = dat[2];
                var ack_id = dat[3];
                
                var ele = document.createElement(target_type);
                ele.id = target_id;
               
                var reference = document.querySelector(selector);
                reference.appendChild(ele);
                
                socket.emit("response", true, ack_id);
            });
            socket.on('element.remove', function (dat) {
                var selector = dat[0];

                console.log(dat);

                var old = document.querySelector(selector);
                old.parentNode.removeChild(old);
            });
            socket.on('page.change', function (dat) {
                location.href = dat[0]; 
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