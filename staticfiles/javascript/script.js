const openSettingsModal = document.getElementById('settings-button');
const settingsModal = document.getElementById('settings-pop-up');
const openNewChatModal = document.getElementById('new-chat-open');
const newChatModal = document.getElementById('new-chat-pop-up');
const closeSettingsModal = document.getElementById('close-settings');
const closeNewChatModal = document.getElementById('close-new-chat');
const openAllImagesModal = document.getElementById('nine');
const allImagesModal = document.getElementById('all-images-pop-up');
const closeAllImagesModal = document.getElementById('close-all-images');

// Pop-Up Event Listeners

openSettingsModal.addEventListener("click", openSettings);
closeSettingsModal.addEventListener("click", closeSettings);
openNewChatModal.addEventListener("click", openNewChat);
closeNewChatModal.addEventListener("click", closeNewChat);
openAllImagesModal.addEventListener("click", openAllImages);
closeAllImagesModal.addEventListener("click", closeAllImages)

// Pop-Up Functions

function openSettings() {
    settingsModal.classList.add("active");
}

function closeSettings() {
    settingsModal.classList.remove("active");
}

function openNewChat() {
    newChatModal.classList.add("active");
}

function closeNewChat() {
    newChatModal.classList.remove("active");
}

function openAllImages() {
    allImagesModal.classList.add("active");
}

function closeAllImages() {
    allImagesModal.classList.remove("active");
}


const imageLargeModal = document.getElementById('large-image-pop-up');
const closeImageLargeModal = document.getElementById('close-large-image');
const largeImg = document.getElementById('large-image-element')
const largeImgTitle = document.getElementById('large-image-title');

document.querySelectorAll('#media-image').forEach(image => {
    image.addEventListener("click", event => { 
        imageLargeModal.classList.add("active");
        largeImg.src = image.src
    });
});

document.querySelectorAll('#grid-image').forEach(image => {
    image.addEventListener("click", event => { 
        imageLargeModal.classList.add("active");
        largeImg.src = image.src
    });
});

document.querySelectorAll('#all-images-grid-item').forEach(image => {
    image.addEventListener("click", event => { 
        imageLargeModal.classList.add("active");
        largeImg.src = image.src
    });
});

closeImageLargeModal.addEventListener("click", closeImageEnlarge);

function closeImageEnlarge() {
    imageLargeModal.classList.remove("active");
    largeImg.src = ""
}

/* Search functionality */

function search() {
    let input, filter, list, li, a, i, textValue;

    input = document.getElementById("search-field");
    filter = input.value.toUpperCase();
    list = document.getElementById("chats-wrapper");
    li = document.getElementsByClassName("chat-item");

    for (i = 0; i < li.length; i++) {
        a = li[i].getElementsByTagName("a")[0];
        textValue = a.textContent || a.innerText;
        if (textValue.toUpperCase().indexOf(filter) > -1) {
          li[i].style.display = "";
        } else {
          li[i].style.display = "none";
        }
    }
}
