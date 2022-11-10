var count = 1
const event_fetch = new Event('fetch_result');
var query_username = function(username){
    fetch(`/search_users?usernames=${username}`)
}

$('#query_form').submit(function(e) {
    e.preventDefault();
    // get all the inputs into an array.
     // get all the inputs into an array.
    const username = $('#username').val()
    $('#username').val('')
    query_username(username)
    document.dispatchEvent(event_fetch);
});
var repeat = true
document.addEventListener("fetch_result", function(e) {
    
    //delay one sec to fetch reuslt
    setTimeout(() => {  
        fetch('/get_result')
        .then((response) => response.json())
        .then((data_list) => {
            for(data of data_list){
                console.log(data)
                if(data[0] == 'end' & data[1] == 'end')  repeat = false;
                $('#results').append(`<a class = 'list-group-item' href='${data[1]}' target='_blank'> ${data[0]} </li>`)
                console.log("website "+data[0])
                console.log("link" + data[1])
            }
            
        });
        if(repeat) document.dispatchEvent(event_fetch);
        }, 1000);
    
    // setInterval(function () {
    //     $('#results').append(`<li class = 'list-group-item'> ${count} </li>`)
    //     count += 1
    // }, 1000);
  });



