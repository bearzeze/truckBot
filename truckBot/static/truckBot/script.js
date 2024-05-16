const editButtons = document.querySelectorAll(".edit-btn");
const saveButtons = document.querySelectorAll(".save-btn");
const backButtons = document.querySelectorAll(".back-btn");

const postLoadButton = document.querySelector("#post-load-btn")
const scrapeLoadButton = document.querySelector("#scrape-load-btn")
const sendMessageButton = document.querySelector("#send-message-btn")
const logHistoryButton = document.querySelector("#log-history-btn")
const logHistoryDiv = document.querySelector("#log-history");

const scrapeDiv = document.querySelector("#scrape");
const sendMessageDiv = document.querySelector("#send-message");

const runScrapeButton = document.querySelector("#run-scrape-btn");
const abortScrapeButton = document.querySelector("#abort-scrape-btn");
const scrapeForm = document.querySelector("#scrape form");

const sendZoomButton = document.querySelector("#send-zoom-btn");
const sendingMessagesForm = document.querySelector("#send-message form");
const checkboxes = document.querySelectorAll(".checkbox");
const zoomFootnote = document.querySelector(".zoom-footnote")

const selectAll = document.querySelector("#select-all");

const driversLinks = document.querySelectorAll(".drivers-link");
const driversInfo = document.querySelector(".drivers-info");
const driversMessages = document.querySelectorAll(".drivers-info");

const loadMessageLinks = document.querySelectorAll(".load-msg-link");
const loadMessageDivs = document.querySelectorAll(".load-msg-div");
const editLoadMessagesButtons = document.querySelectorAll(".edit-load-msg-btn")
const backLoadButtons = document.querySelectorAll(".back-msg-btn");
const saveMessageButtons = document.querySelectorAll("#send-message li .save-msg-btn");

const tableBody = document.querySelector("#log-history-table-body");


// HOME PAGE
// Pressing Post Load Button - it redirects to the new window for posting the loads
if (postLoadButton) {
    postLoadButton.addEventListener("click", () => {
        window.open("https://leads.landstaronline.com/AvailableLoads/NewLoadView.aspx?loadid=-500", "_blank");
    });
}

// Pressing Scrape Load Button opens only that div and hide all others
if (scrapeLoadButton) {

    scrapeLoadButton.addEventListener("click", () => {

        if (isHidden(scrapeDiv)) {
            activeButton(scrapeLoadButton, true);
            activeButton(sendMessageButton, false);
            activeButton(logHistoryButton, false);

            showElement(scrapeDiv);
            hideElement(sendMessageDiv);
            hideElement(logHistoryDiv);
        }

        else {
            activeButton(scrapeLoadButton, false);
            hideElement(scrapeDiv);
        }
    });
}

// Pressing Sending Message Button opens only that div and hide all others
if (sendMessageButton) {

    sendMessageButton.addEventListener("click", () => {

        if (isHidden(sendMessageDiv)) {
            activeButton(sendMessageButton, true);
            activeButton(scrapeLoadButton, false);
            activeButton(logHistoryButton, false);

            showElement(sendMessageDiv);
            hideElement(scrapeDiv);
            hideElement(logHistoryDiv);
        }

        else {
            activeButton(sendMessageButton, false);
            hideElement(sendMessageDiv);
        }
    });
}

// Pressing Sending Message Button opens only that div and hide all others
if (logHistoryButton) {

    logHistoryButton.addEventListener("click", function() {

        if (isHidden(logHistoryDiv)) {
            activeButton(logHistoryButton, true);
            activeButton(scrapeLoadButton, false);
            activeButton(sendMessageButton, false);

            showElement(logHistoryDiv);
            hideElement(sendMessageDiv);
            hideElement(scrapeDiv);

            // Fetching data calling API
            const url = logHistoryDiv.getAttribute("data-url");

            // Each time this button is clicked it needs to clear the data before fetching data
            tableBody.innerHTML = "";

            getDataAboutLogHistory(url).then(() => {
                // This code will run after the data has been fetched and the page has been updated
                window.scrollBy({top: 200, behavior: "smooth"});
            });

        }
        else {
            hideElement(logHistoryDiv);
        }
    });
}

// Submiting Scrape form and Aborting it while running
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

// Checkboxes for the loads which we want to select for sending sms
if (checkboxes) {
    checkboxes.forEach(chck => {
        chck.addEventListener("change", () => {

            // If no box is checked, Send Via Zoom Button is disabled
            let atLeastOneCheckboxIsChecked = false;
            let everyCheckBoxChecked = true;

            checkboxes.forEach(checkbox => {
                if (checkbox.checked) {
                    atLeastOneCheckboxIsChecked = true;
                }
                
                else {
                    everyCheckBoxChecked = false;
                }

            });

            if (atLeastOneCheckboxIsChecked) {
                sendZoomButton.disabled = false;
                showElement(zoomFootnote);
            }

            else {
                sendZoomButton.disabled = true;
                selectAll.checked = false;
                hideElement(zoomFootnote);
            }

            if (everyCheckBoxChecked) 
                selectAll.checked = true;
            else
                selectAll.checked = false;
        });
    })
}

// There is one select all check box for (de)selecting all checkboxes
if (selectAll) {
    selectAll.addEventListener("change", () => {

        checkboxes.forEach(element => {
            element.checked = selectAll.checked
            sendZoomButton.disabled = !selectAll.checked

            if (selectAll.checked) {
                showElement(zoomFootnote);
            }
            else {
                hideElement(zoomFootnote);
            }


        });

    });
}

// When Zoom is fired up button is disabled, and text is different
if (sendingMessagesForm) {
    sendingMessagesForm.addEventListener("submit", () => {
        sendZoomButton.disabled = true;
        sendZoomButton.innerHTML = "Press Esc to stop";
        sendZoomButton.classList.remove("btn-primary");
        sendZoomButton.classList.add("btn-danger");
        hideElement(zoomFootnote);
    });
}

// Truck Drivers Info View
if (driversLinks) {
    driversLinks.forEach(link => {

        link.addEventListener("click", () => {

            const parentLi = link.parentElement;
            const message = parentLi.querySelector(".drivers-info");

            if (message.classList.contains("hide")) {
                showElement(message);

                // All other messages for drivers will be hidden except the clicked one
                driversMessages.forEach(otherMessageDiv => {
                    if (message !== otherMessageDiv) {
                        hideElement(otherMessageDiv);
                    }
                });

                // All other load messages will be hidden
                loadMessageDivs.forEach(loadMessageDiv => {
                    hideElement(loadMessageDiv);
                });

            }
            else {
                hideElement(message);
            }


        });

    });
}

// Load message link
if (loadMessageLinks) {
    loadMessageLinks.forEach(link => {
        link.addEventListener("click", () => {

            const parentLi = link.parentElement;
            const messageDiv = parentLi.querySelector(".load-msg-div");

            if (isHidden(messageDiv)) {
                showElement(messageDiv);


                // All other load messages will be hidden except the clicked one
                loadMessageDivs.forEach(otherMessageDiv => {
                    if (messageDiv !== otherMessageDiv) {
                        hideElement(otherMessageDiv);
                    }
                });

                // All other messages for drivers will be hidden except the clicked one
                driversMessages.forEach(driverInfoDiv => {
                    hideElement(driverInfoDiv);
                });
            }

            else {
                hideElement(messageDiv);
            }
        });
    })
}

// Editing load message 
if (editLoadMessagesButtons) {

    editLoadMessagesButtons.forEach(btn => {
        btn.addEventListener("click", () => {

            const loadInfoDiv = btn.parentElement;
            const parentLi = btn.closest("li");
            const editMessageDiv = parentLi.querySelector(".edit-msg-div");

            if (!isHidden(loadInfoDiv)) {
                hideElement(loadInfoDiv);
                showElement(editMessageDiv);
            }
        })
    })
}

// Back button for the Load messages 
if (backLoadButtons) {

    backLoadButtons.forEach(btn => {

        btn.addEventListener("click", () => {

            const editMessageDiv = btn.closest("div");
            const parentLi = btn.closest("li");
            const loadInfoDiv = parentLi.querySelector(".load-info");

            if (!isHidden(editMessageDiv)) {

                hideElement(editMessageDiv);
                showElement(loadInfoDiv);
            }

        });
    });
}

// Saving edited load message 
if (saveMessageButtons) {

    saveMessageButtons.forEach(btn => {
        
        btn.addEventListener("click", function(event) {

            let message = btn.closest("div").querySelector("textarea").value;
            const load_id = btn.getAttribute("data-load_id");

            load_url = btn.getAttribute("data-url");

            saveLoadMessage(message, load_url, btn);

            event.preventDefault();
        });
    });
}


// PROFILE PAGE
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

// Back button in profile page
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


// Function for hiding and showing some html element
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

    for (var i = 0; i < cookieArr.length; i++) {
        var cookiePair = cookieArr[i].split("=");

        /* Removing whitespace at the beginning of the cookie name
        and compare it with the given string */
        if (name == cookiePair[0].trim()) {
            // Decode the cookie value and return
            return decodeURIComponent(cookiePair[1]);
        }
    }

    // Return null if not found
    return null;
}

function activeButton(button, needsToBeActive) {
    if (needsToBeActive) {
        button.classList.add("active");
    }
    else {
        button.classList.remove("active");
    }
}


// Function for getting all logs from database
function getDataAboutLogHistory(url) {

    return new Promise((resolve, reject) => {
        fetch(url, {
            method: "GET",
            headers: {
                'Content-Type': 'application/json',
            },
        })
        .then(response => response.json())
        .then(data => {

            data.forEach((log, index) => {
                const row = document.createElement("tr");

                const indexCell = document.createElement("th");
                indexCell.scope = "row";
                indexCell.textContent = index + 1;
                row.appendChild(indexCell);

                const loadIdCell = document.createElement("td");
                loadIdCell.textContent = log["load_id"];
                row.appendChild(loadIdCell);

                const driversCountCell = document.createElement("td");
                driversCountCell.textContent = log["count_drivers"];
                row.appendChild(driversCountCell);

                const dateCell = document.createElement("td");
                dateCell.textContent = log["date"];
                row.appendChild(dateCell);

                tableBody.appendChild(row);
                resolve();
            });

        })
        .catch(error => {
            console.error('Error:', error);
            reject(error);
        });
    });
}

// Function for saving the edited load message to the database
function saveLoadMessage(message, url, saveButton) {

    fetch(url, {
        method: "PUT",
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')  // Assuming you have a function to get the CSRF token
        },
        body: JSON.stringify({
            message: message
        })
    })
    .then(response => response.json())
    .then(data => {
        const editMessageDiv = saveButton.closest("div");
        const parentLi = saveButton.closest("li");
        const loadInfoDiv = parentLi.querySelector(".load-info");
        const messageParagraph = parentLi.querySelector(".message-paragraph");
            
        if (!isHidden(editMessageDiv)) {

            hideElement(editMessageDiv);
            showElement(loadInfoDiv);
            messageParagraph.textContent = message;
        }
    });

}
