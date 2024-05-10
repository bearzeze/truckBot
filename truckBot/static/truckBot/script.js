const editButtons = document.querySelectorAll(".edit-btn");
const saveButtons = document.querySelectorAll(".save-btn");
const backButtons = document.querySelectorAll(".back-btn");

const postLoadButton = document.querySelector("#post-load-btn")
const scrapeLoadButton = document.querySelector("#scrape-load-btn")
const sendMessageButton = document.querySelector("#send-message-btn")
const logHistoryButton = document.querySelector("#log-history-btn")

const scrapeDiv = document.querySelector("#scrape");
const sendMessageDiv = document.querySelector("#send-message");

const runScrapeButton = document.querySelector("#run-scrape-btn");
const abortScrapeButton = document.querySelector("#abort-scrape-btn");
const scrapeForm = document.querySelector("#scrape form");

const sendZoomButton = document.querySelector("#send-zoom-btn");


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

// Button for opening tab where loads are visible and message can be sent
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

if (scrapeForm) {

    scrapeForm.addEventListener("submit", () => {

        runScrapeButton.disabled = true;

        runScrapeButton.innerHTML = "Running..."
        scrape_url = runScrapeButton.getAttribute("data-url");


        fetch(scrape_url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')  
            },
            body: JSON.stringify({
                is_scraping: true
            })
        });

        showElement(abortScrapeButton);
        abortScrapeButton.addEventListener("click", () => {

            hideElement(runScrapeButton);
            abortScrapeButton.disabled = true;
            abortScrapeButton.innerHTML = "Aborting..."

            abort_url = abortScrapeButton.getAttribute("data-url");
            
            fetch(abort_url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')  // Assuming you have a function to get the CSRF token
                },
                body: JSON.stringify({
                    abort_scraping: true
                })
            });
        })
    });
}

// Button which opens Zoom and send messages
if (sendZoomButton) {
    sendZoomButton.addEventListener("click", () => {
        sendZoomButton.disabled = true;

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


function getCookie(name) {
    var cookieArr = document.cookie.split(";");
    
    for(var i = 0; i < cookieArr.length; i++) {
        var cookiePair = cookieArr[i].split("=");
        
        /* Removing whitespace at the beginning of the cookie name
        and compare it with the given string */
        if(name == cookiePair[0].trim()) {
            // Decode the cookie value and return
            return decodeURIComponent(cookiePair[1]);
        }
    }
    
    // Return null if not found
    return null;
}