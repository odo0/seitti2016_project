/* global $, _ */
'use strict';

$(function() {
    var gameFrame = $('#game_player_frame');

    var sendMessage = function(type, data) {
        gameFrame[0].contentWindow.postMessage(_.assign({
            messageType: type
        }, data), '*');
    };

    var sendServerError = function() {
        return sendMessage("ERROR", {
            info: "Server error"
        });
    };

    var sendClientError = function() {
        return sendMessage("ERROR", {
            info: "Invalid request"
        });
    };

    var noopCallback = function() {};
    
    var receiveMessage = function(e) {
        var data = e.originalEvent.data;
        if (data !== undefined && data.messageType !== undefined) {
            switch (data.messageType) {
                case "SAVE":
                    if (data.gameState === undefined) {
                        return sendClientError();
                    }

                    getAsyncData("DATA_SAVE", { data: JSON.stringify(data.gameState) }, noopCallback, sendServerError);
                    break;
                case "SCORE":
                    if (data.score === undefined) {
                        return sendClientError();
                    }

                    getAsyncData("SCORE_SAVE", { score: parseFloat(data.score) }, noopCallback, sendServerError);
                    break;
                case "LOAD_REQUEST":
                    getAsyncData("DATA_LOAD", {}, function(data) {
                        sendMessage("LOAD", { gameState: JSON.parse(data.data) });
                    }, function(jqxhr) {
                        if (jqxhr.status !== 404) {
                            sendServerError();
                        }
                    });
                    break;
                case "SETTING":
                    if (data.options !== undefined) {
                        if (data.options.width) {
                            gameFrame.width(parseInt(data.options.width));
                        }
                        if (data.options.height) {
                            gameFrame.height(parseInt(data.options.height));
                        }
                    }
                    break;
                default:
                    sendMessage("ERROR", {
                        info: "Invalid message type " + String(data.messageType)
                    });
            }
        } else {
            sendClientError();
        }
    };
    
    var getAsyncData = function(type, data, cbSuccess, cbFailure) {
        if (window.FOG === undefined ||
            window.FOG.SERVICE_PATHS === undefined ||
            window.FOG.SERVICE_PATHS[type] === undefined) {
            return sendMessage("ERROR", {
                info: "User interface not configured properly"
            });
        }
        
        $.ajax({
            type: "POST",
            url: window.FOG.SERVICE_PATHS[type],
            data: data,
            success: cbSuccess,
            headers: {
                "X-CSRFToken": Cookies.get("csrftoken")
            }
        }).fail(cbFailure);
    };

    $(window).on('message', receiveMessage);
});
