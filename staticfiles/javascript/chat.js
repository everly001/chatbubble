const id = JSON.parse(document.getElementById('json-username').textContent);
const message_username = JSON.parse(document.getElementById('json-message-username').textContent)

const socket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/'
    + id
    + '/'
);

socket.onopen = function(e){
    console.log('CONNECTION ESTABLISHED');
};

socket.onclose = function(e){
    console.log('CONNECTION LOST');
};

socket.onerror = function(e){
    console.log(e);
};

socket.onmessage = function(e){
    location.reload();
    /* const data = JSON.parse(e.data);
    
    if(data.username == message_username){
        document.querySelector('#messages').innerHTML += 
        `<div id="sent-message">
            <div id="chat-bubble-wrapper">
                <h5>${data.username}</h5>
                <div id="chat-bubble">
                    <p>${data.message}</p>
                    <img src="${data.media}" alt="">
                </div>
            </div>
            <div id="profile-picture-group">
                <div class="profile-picture"><img src="${data.profile_pic}" alt=""></div>
            </div>
        </div>`
    }else{
        document.querySelector('#messages').innerHTML +=
        `<div id="received-message">
            <div id="profile-picture-group">
                <div class="profile-picture"><img src="${data.profile_pic}" alt=""></div>
            </div>
            <div id="chat-bubble-wrapper">
                <h5>${data.username}</h5>
                <div id="chat-bubble">
                    <p>${data.message}</p>
                    <img src="${data.media}" alt="">
                </div>
            </div>
        </div>`
    } */
};

function getBase64(media_input, message) {
    const promise = new Promise((resolve) => {
        const reader = new FileReader();
        reader.onload = function () {
            resolve(reader.result)
        }
        reader.readAsDataURL(media_input)
    });

    promise.then(media_input => {
        console.log(media_input)
        socket.send(JSON.stringify({
            'message': message,
            'media': media_input,
            'username': message_username,
            'message_type': 'media'
        }));
    });
};

document.querySelector('#send-button').onclick = function(e){
    const message_input = document.querySelector('#text-input');
    const message = message_input.value;
    const media_input = document.querySelector('#media-upload').files[0];

    if (media_input) {
        getBase64(media_input, message)
    } else {
        socket.send(JSON.stringify({
            'message': message,
            'username': message_username,
            'message_type': 'text'
        }));
    }
    message_input.value = '';
};