const editButtons = document.querySelectorAll(".edit-btn");
const saveButtons = document.querySelectorAll(".save-btn");
const backButtons = document.querySelectorAll(".back-btn");

const postLoadButton = document.querySelector("#post-load-btn")
const scrapeLoadButton = document.querySelector("#scrape-load-btn")
const sendMessageButton = document.querySelector("#send-message-btn")
const logHistoryButton = document.querySelector("#log-history-btn")

const scrapeDiv = document.querySelector("#scrape");
const sendMessageDiv = document.querySelector("#send-message");


// Home page
// With Post Load new page is opened
if (postLoadButton) {
    postLoadButton.addEventListener("click", () => {
        window.open("https://leads.landstaronline.com/AvailableLoads/NewLoadView.aspx?loadid=-500", "_blank");
    });
}

if (scrapeLoadButton) {

    scrapeLoadButton.addEventListener("click", () => {
        
        if (isHidden(scrapeDiv)) {
            scrapeLoadButton.classList.add("active")
            sendMessageButton.classList.remove("active")
            showElement(scrapeDiv);
            hideElement(sendMessageDiv);
        }

        else {
            scrapeLoadButton.classList.remove("active")
            hideElement(scrapeDiv);
        }
    });
}


if (sendMessageButton) {

    sendMessageButton.addEventListener("click", () => {
        
        if (isHidden(sendMessageDiv)) {
            sendMessageButton.classList.add("active")
            scrapeLoadButton.classList.remove("active")
            showElement(sendMessageDiv);
            hideElement(scrapeDiv);
        }

        else {
            sendMessageButton.classList.remove("active")
            hideElement(sendMessageDiv);
        }
    });
}

// Edit button in profile page
if (editButtons) {
    editButtons.forEach(btn => {

        btn.addEventListener("click", () => {
            let div = btn.parentNode.parentNode;

            let viewDiv = div.querySelector(".profile-view");
            let editDiv = div.querySelector(".profile-change");

            hideElement(viewDiv);
            showElement(editDiv);

        });
    });
}


// Edit button in profile page
if (backButtons) {
    backButtons.forEach(btn => {

        btn.addEventListener("click", () => {
            let div = btn.parentNode.parentNode.parentNode;

            let viewDiv = div.querySelector(".profile-view");
            let editDiv = div.querySelector(".profile-change");

            hideElement(editDiv);
            showElement(viewDiv);

        });
    });
}



function hideElement(element) {
    element.classList.remove("show");
    element.classList.add("hide");
}

function showElement(element) {
    element.classList.remove("hide");
    element.classList.add("show");
}

function isHidden(element) {
    return element.classList.contains("hide");
}