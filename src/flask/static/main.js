var socket = io()
const engine = socket.io.engine;
socket.disconnect()
var input_username = null
var $loader = $('<a class="list-group-item " id="loader" href="#" target="_blank"> <div class="spinner-border"role="status"><span class="sr-only"></span></div></a>')
//submit username to query
//TODO change to post 
$('#query_form').submit(function (e) {
    repeat = true
    e.preventDefault();
    // get all the inputs into an array.
    // get all the inputs into an array.
    // fetch(`/search_users?usernames=${username}`)
    input_username = $('#username').val()
    //TODO validation
    socket.connect()
    $('#form_button').prop("disabled", true)
    $('#results').append(`<a class = 'list-group-item bg-info text-white' href='#' target='_blank'> Result for ${input_username} </a>`)
    $('#username').val('')
    socket.emit('query', {
        username: input_username
    });
});

engine.on("packet", ({ type, data }) => {
    console.log(data)
  });

// socket.on('connect', function () {
// });

socket.on('query_result', function (data) {
    data['data'].forEach(element => {
        var $new_row = $(`<a class = 'list-group-item animate__animated animate__backInLeft' href='${element[1]}' target='_blank'> ${element[0]} </a>`);
        $('#results').append($loader)
        $("#loader").before($new_row)
        $('a').last()[0].scrollIntoView
        $("#loader")[0].scrollIntoView({
            behavior: "smooth", // or "auto" or "instant"
            block: "start" // or "end"
        });

    });
    socket.emit('continous_result')
});

socket.on('query_complete', function (data) {
    socket.disconnect()
    // socket.emit('ping', { data: 'ping' });
});
socket.on('disconnect', function (data) {
    $('#results').append(`<a class = 'list-group-item bg-info text-white' href='#' target='_blank'> End of ${input_username} </a>`)
    $('#username').val('')
    $('#form_button').prop("disabled", false)
    $("#loader").remove();
    // socket.emit('ping', { data: 'ping' });
});

// window.onbeforeunload = function () {
//     socket.emit('client_disconnecting', {});
// }