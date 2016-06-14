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

        _used_internal_ids: [],

        _alphanumeric_string: function (length) {
            var choices = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_?!., ';

            var temp = "";
            for (var i = 0; i < length; i ++) {
                temp += choices[Math.floor(Math.random() * choices.length)];
            }

            return temp;
        },

        _selector: function (dat) {

            var element = document.querySelector(dat[0]);
            var return_tag = dat[1];

            var part1 = "[data-pycommunicate-id=\"";
            var part2 = "\"]";

            if (element.dataset.hasOwnProperty("pycommunicateId")) {
                this._socket.emit("response", part1 + element.dataset.pycommunicateId + part2, return_tag);
            }
            else {
                var identifier = pycommunicate._alphanumeric_string(15);
                while (!(pycommunicate._used_internal_ids.indexOf(identifier) === -1)) {
                    identifier = pycommunicate._alphanumeric_string(15);
                }
                
                element.dataset.pycommunicateId = identifier;
                this._socket.emit("response", part1 + element.dataset.pycommunicateId + part2, return_tag);
            }

        },
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
            socket.on('element.selector', function (dat) {
                 pycommunicate._selector(dat);
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
                var ack_id = dat[2];

                var element = document.createElement(target_type);

                var identifier = pycommunicate._alphanumeric_string(15);
                while (!(pycommunicate._used_internal_ids.indexOf(identifier) === -1)) {
                    identifier = pycommunicate._alphanumeric_string(15);
                }

                var part1 = "[data-pycommunicate-id=\"";
                var part2 = "\"]";

                element.dataset.pycommunicateId = identifier;

                var reference = document.querySelector(selector);
                reference.parentNode.insertBefore(element, reference.nextSibling);

                socket.emit("response", part1 + identifier + part2, ack_id);
            });
            socket.on('element.add.inside', function (dat) {
                var selector = dat[0];
                var target_type = dat[1];
                var ack_id = dat[2];
                
                var element = document.createElement(target_type);

                var identifier = pycommunicate._alphanumeric_string(15);
                while (!(pycommunicate._used_internal_ids.indexOf(identifier) === -1)) {
                    identifier = pycommunicate._alphanumeric_string(15);
                }

                var part1 = "[data-pycommunicate-id=\"";
                var part2 = "\"]";

                element.dataset.pycommunicateId = identifier;

                var reference = document.querySelector(selector);
                reference.appendChild(element);
                
                socket.emit("response", part1 + identifier + part2, ack_id);
            });
            socket.on('element.add.before', function (dat) {
                var selector = dat[0];
                var target_type = dat[1];
                var ack_id = dat[2];
                
                var element = document.createElement(target_type);

                var identifier = pycommunicate._alphanumeric_string(15);
                while (!(pycommunicate._used_internal_ids.indexOf(identifier) === -1)) {
                    identifier = pycommunicate._alphanumeric_string(15);
                }

                var part1 = "[data-pycommunicate-id=\"";
                var part2 = "\"]";

                element.dataset.pycommunicateId = identifier;

                var reference = document.querySelector(selector);
                reference.parentNode.insertBefore(element, reference);
                
                socket.emit("response", part1 + identifier + part2, ack_id);
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