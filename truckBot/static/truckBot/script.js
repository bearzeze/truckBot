// VARIABLES
// Profile
const editButtons = document.querySelectorAll(".edit-btn");
const saveButtons = document.querySelectorAll(".save-btn");
const backButtons = document.querySelectorAll(".back-btn");

// Alert Messages
const closeAllAlertMessages = document.querySelector("#close-all-alert-messages-btn");

// Big buttons on home page
const prepareLoadsBigButton = document.querySelector("#prepare-loads-btn");
const postLoadsBigButton = document.querySelector("#post-loads-btn");
const scrapeLoadBigButton = document.querySelector("#scrape-load-btn")
const sendMessageBigButton = document.querySelector("#send-message-btn")
const loadHistoryBigButton = document.querySelector("#load-history-btn")

// Prepare Loads
const prepareLoadsDiv = document.querySelector("#prepare-loads");
const txtFileLaneButtons = document.querySelectorAll(".txt-lane-info-btn");

// Post Loads
const postLoadsDiv = document.querySelector("#post-loads");
const preparedLoadLinks = document.querySelectorAll(".prepared-load-link");
const preparedLoadInfos = document.querySelectorAll(".prepared-load-info");
const checkboxesPosting = document.querySelectorAll(".checkbox-posting");
const selectAllForPosting = document.querySelector("#select-all-posting")
const postOrDeleteLoadsButton = document.querySelectorAll(".post-delete-btn");
const postingLoadsForm = document.querySelector("#post-loads form")
const abortPostingButton = document.querySelector("#abort-posting-btn");
const checkboxCounterPost = document.querySelector("#checkbox-counter-post");

// Scrape Loads
const scrapeDiv = document.querySelector("#scrape");
const sendMessageDiv = document.querySelector("#send-message");
const radiusDistanceLink = document.querySelector("#radius-distance-link");
const radiusDistance = document.querySelector("#radius-distance");
const runScrapeButton = document.querySelector("#run-scrape-btn");
const abortScrapeButton = document.querySelector("#abort-scrape-btn");
const scrapeForm = document.querySelector("#scrape form");

// Send Messages
const sendZoomButton = document.querySelector("#send-zoom-btn");
const sendingMessagesForm = document.querySelector("#send-message form");
const checkboxesSending = document.querySelectorAll(".checkbox-sending");
const zoomFootnote = document.querySelector(".zoom-footnote")
const selectAllForSendingMessages = document.querySelector("#select-all-sending");
const driversLinks = document.querySelectorAll(".drivers-link");
const driversInfo = document.querySelector(".drivers-info");
const driversMessages = document.querySelectorAll(".drivers-info");
const loadHistoryDiv = document.querySelector("#load-history");
const loadMessageLinks = document.querySelectorAll(".load-msg-link");
const loadMessageDivs = document.querySelectorAll(".load-msg-div");
const editLoadMessagesButtons = document.querySelectorAll(".edit-load-msg-btn")
const backLoadButtons = document.querySelectorAll(".back-msg-btn");
const saveMessageButtons = document.querySelectorAll("#send-message li .save-msg-btn");
const checkboxCounterSend = document.querySelector("#checkbox-counter-send");

// Log History
const tableBody = document.querySelector("#load-history-table-body");


// HOME PAGE

// 1) BIG BUTTONS
// Button which close all alert messages currently shown in index page
if (closeAllAlertMessages) {
    closeAllAlertMessages.addEventListener("click", () => {
        alertCloseBtns = document.querySelectorAll(".btn-close");

        alertCloseBtns.forEach(btn => {
            btn.click();
        });
    });
}

// Pressing Preparing Loads Button
if (prepareLoadsBigButton) {
    prepareLoadsBigButton.addEventListener("click", () => {
        // PRIJE SAMO OTVARA LANDSTAR GDJE UBACUJE POST LOAD
        // window.open("https://leads.landstaronline.com/AvailableLoads/NewLoadView.aspx?loadid=-500", "_blank");

        // Probati automatizirati ovaj proces...

        if (isHidden(prepareLoadsDiv)) {
            activeButton(prepareLoadsBigButton, true);
            activeButton(postLoadsBigButton, false);
            activeButton(scrapeLoadBigButton, false);
            activeButton(sendMessageBigButton, false);
            activeButton(loadHistoryBigButton, false);

            showElement(prepareLoadsDiv);
            hideElement(postLoadsDiv);
            hideElement(scrapeDiv);
            hideElement(sendMessageDiv);
            hideElement(loadHistoryDiv);
            hideElement(radiusDistance);
        }

        else {
            hideElement(prepareLoadsDiv);
            activeButton(prepareLoadsBigButton, false);
        }
    });
}

// Pressing Post Loads Button
if (postLoadsBigButton) {
    postLoadsBigButton.addEventListener("click", () => {
        // PRIJE SAMO OTVARA LANDSTAR GDJE UBACUJE POST LOAD
        // window.open("https://leads.landstaronline.com/AvailableLoads/NewLoadView.aspx?loadid=-500", "_blank");

        // Probati automatizirati ovaj proces...

        if (isHidden(postLoadsDiv)) {
            activeButton(postLoadsBigButton, true);
            activeButton(prepareLoadsBigButton, false);
            activeButton(scrapeLoadBigButton, false);
            activeButton(sendMessageBigButton, false);
            activeButton(loadHistoryBigButton, false);

            showElement(postLoadsDiv);
            hideElement(prepareLoadsDiv);
            hideElement(scrapeDiv);
            hideElement(sendMessageDiv);
            hideElement(loadHistoryDiv);
            hideElement(radiusDistance);
        }

        else {
            hideElement(postLoadsDiv);
            activeButton(postLoadsBigButton, false);
        }
    });
}

// Pressing Scrape Load Button opens only that div and hide all others
if (scrapeLoadBigButton) {

    scrapeLoadBigButton.addEventListener("click", () => {

        if (isHidden(scrapeDiv)) {
            activeButton(scrapeLoadBigButton, true);
            activeButton(prepareLoadsBigButton, false);
            activeButton(postLoadsBigButton, false);
            activeButton(sendMessageBigButton, false);
            activeButton(loadHistoryBigButton, false);

            showElement(scrapeDiv);
            hideElement(prepareLoadsDiv);
            hideElement(postLoadsDiv);
            hideElement(sendMessageDiv);
            hideElement(loadHistoryDiv);
            hideElement(radiusDistance);
        }

        else {
            activeButton(scrapeLoadBigButton, false);
            hideElement(scrapeDiv);
        }
    });
}

// Pressing Sending Message Button opens only that div and hide all others
if (sendMessageBigButton) {

    sendMessageBigButton.addEventListener("click", () => {

        if (isHidden(sendMessageDiv)) {
            activeButton(sendMessageBigButton, true);
            activeButton(prepareLoadsBigButton, false);
            activeButton(postLoadsBigButton, false);
            activeButton(scrapeLoadBigButton, false);
            activeButton(loadHistoryBigButton, false);

            showElement(sendMessageDiv);
            hideElement(prepareLoadsDiv);
            hideElement(postLoadsDiv);
            hideElement(scrapeDiv);
            hideElement(loadHistoryDiv);
        }

        else {
            activeButton(sendMessageBigButton, false);
            hideElement(sendMessageDiv);
        }
    });
}

// Pressing Sending Message Button opens only that div and hide all others
if (loadHistoryBigButton) {

    loadHistoryBigButton.addEventListener("click", function () {

        if (isHidden(loadHistoryDiv)) {
            activeButton(loadHistoryBigButton, true);
            activeButton(prepareLoadsBigButton, false);
            activeButton(prepareLoadsBigButton, false);
            activeButton(scrapeLoadBigButton, false);
            activeButton(sendMessageBigButton, false);

            showElement(loadHistoryDiv);
            hideElement(prepareLoadsDiv);
            hideElement(postLoadsDiv);
            hideElement(sendMessageDiv);
            hideElement(scrapeDiv);

            // Fetching data calling API
            const url = loadHistoryDiv.getAttribute("data-url");
            const userIsAdmin = loadHistoryDiv.getAttribute("data-isadmin") === "True";

            // Each time this button is clicked it needs to clear the data before fetching data
            tableBody.innerHTML = "";

            getDataAboutLoadHistory(url, userIsAdmin).then(() => {
                // This code will run after the data has been fetched and the page has been updated
                window.scrollBy({ top: 200, behavior: "smooth" });
            });

        }
        else {
            hideElement(loadHistoryDiv);
            activeButton(loadHistoryBigButton, false);
        }
    });
}


// 2.1) PREPARING LOADS
// Pressing this button will open/clear txt. file in which will Lane info be copied
if (txtFileLaneButtons) {

    txtFileLaneButtons.forEach(btn => {
        btn.addEventListener("click", () => {
            const company = btn.getAttribute("data-company");
            // opening and inserting or clearing textual content into notepad file
            const action = btn.getAttribute("data-action");

            callApiAboutTxtFileLaneInfo(action, company);

        });
    })
}

// 2.2) POSTING LOADS
// Link for each prepared load with its details
if (preparedLoadLinks) {

    preparedLoadLinks.forEach(link => {

        link.addEventListener("click", () => {

            const parentLi = link.parentElement;
            const infoDiv = parentLi.querySelector(".prepared-load-info");

            if (isHidden(infoDiv)) {
                showElement(infoDiv);

                preparedLoadInfos.forEach(otherInfoDiv => {
                    if (infoDiv !== otherInfoDiv)
                        hideElement(otherInfoDiv);
                });
            }
            else {
                hideElement(infoDiv);
            }
        });
    });

}

// Handling checkboxes for posting loads on Landstar
if (checkboxesPosting) {

    handleCheckBoxes(checkboxesPosting, selectAllForPosting, checkboxCounterPost ,postOrDeleteLoadsButton);

}

// Select every checkbox for posting load on landstar
if (selectAllForPosting) {

    selectAllForPosting.addEventListener("change", () => {
        checkboxesPosting.forEach(element => {

            element.checked = selectAllForPosting.checked;
            postOrDeleteLoadsButton.forEach(button => {
                button.disabled = !selectAllForPosting.checked;
            });

            if (selectAllForPosting.checked) {
                checkboxCounterPost.innerHTML = checkboxesPosting.length;
                showElement(checkboxCounterPost.parentElement);
            }
            else {
                hideElement(checkboxCounterPost.parentElement);
            }
        });
    });
}

// Posting or Deleting loads on landstar 
if (postOrDeleteLoadsButton) {

    postOrDeleteLoadsButton.forEach(button => {

        button.addEventListener("click", () => {
            const endpoint = button.getAttribute("data-url");

            postingLoadsForm.action = endpoint;

            // Post button needs to be disabled and delete button needs to be hidden
            changeButtonBehaviorWhenPostFormSubmit();

            postingLoadsForm.submit();

        });

    });
}



// 2.3) SCRAPING LOADS
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

        // IF user click abort button:
        abortProcess("scraping", runScrapeButton);
    });
}

if (radiusDistanceLink) {
    radiusDistanceLink.addEventListener("click", () => {

        if (isHidden(radiusDistance)) {
            showElement(radiusDistance);
        }
        else {
            hideElement(radiusDistance);
        }
    });
}

// 2.4) SENDING MESSAGES
// Checkboxes for the loads which we want to select for sending sms
if (checkboxesSending) {

    handleCheckBoxes(checkboxesSending, selectAllForSendingMessages, checkboxCounterSend, sendZoomButton);

}

// There is one select all check box for (de)selecting all checkboxes
if (selectAllForSendingMessages) {
    selectAllForSendingMessages.addEventListener("change", () => {

        checkboxesSending.forEach(element => {
            element.checked = selectAllForSendingMessages.checked
            sendZoomButton.disabled = !selectAllForSendingMessages.checked

            if (selectAllForSendingMessages.checked) {
                showElement(zoomFootnote);
                checkboxCounterSend.innerHTML = checkboxesSending.length;
                showElement(checkboxCounterSend.parentElement);
            }
            else {
                hideElement(zoomFootnote);
                hideElement(checkboxCounterSend.parentElement);
            }


        });

    });
}

// When Zoom is fired up button is disabled, and text will be different
if (sendZoomButton) {
    sendZoomButton.addEventListener("click", () => {

        sendingMessagesForm.submit();

        sendZoomButton.disabled = true;
        sendZoomButton.innerHTML = "Press Esc to Stop";
        sendZoomButton.classList.remove("btn-primary");
        sendZoomButton.classList.add("btn-danger");
        hideElement(zoomFootnote);

        checkboxesSending.forEach(chck => {
            chck.disabled = true;
        });

        selectAllForSendingMessages.disabled = true;
    });
}

// Truck Drivers Info View
if (driversLinks) {
    driversLinks.forEach(link => {

        link.addEventListener("click", () => {

            const parentLi = link.parentElement;
            const driversInfo = parentLi.querySelector(".drivers-info");

            if (driversInfo.classList.contains("hide")) {
                showElement(driversInfo);

                // All other messages for drivers will be hidden except the clicked one
                driversMessages.forEach(otherInfoDivs => {
                    if (driversInfo !== otherInfoDivs) {
                        hideElement(otherInfoDivs);
                    }
                });

                // All other load messages will be hidden
                loadMessageDivs.forEach(loadMessageDiv => {
                    hideElement(loadMessageDiv);
                });

            }
            else {
                hideElement(driversInfo);
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

        btn.addEventListener("click", function (event) {

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
    if (needsToBeActive)
        button.classList.add("active");
    else
        button.classList.remove("active");
}


// Function for getting all load history from database
function getDataAboutLoadHistory(url, userIsAdmin) {

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

                    if (userIsAdmin) {
                        const usernameCell = document.createElement("td");
                        usernameCell.textContent = log["username"];
                        usernameCell.style.color = "#6c757d";
                        row.appendChild(usernameCell);
                    }


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

// asynchronous function for opening or clearing txt file about lane loads
async function callApiAboutTxtFileLaneInfo(action, company) {

    const url = `api/${action}_txt_file/${company}`;

    try {
        const response = await fetch(url, {
            method: "GET",
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')  // Assuming you have a function to get the CSRF token
            },
        });

        if (response.ok) {
            const data = await response.json();
            // Handle the data (e.g., update UI, display alert)
            if (action === "clear") {
                alert(`Content from lane_info_${company}.txt file cleared successfully!`);
            }
        } else {
            console.error('API call failed:', response.status);
        }
    } catch (error) {
        console.error('Fetch error:', error);
    }

}

// Function for handling multiple checkboxes in the home page 
function handleCheckBoxes(checkboxes, selectAllCheckbox, checkBoxCounter, submitButton) {

    checkboxes.forEach(chck => {
        chck.addEventListener("change", () => {

            // If no box is checked, Send Via Zoom Button is disabled
            let atLeastOneCheckboxIsChecked = false;
            let everyCheckBoxChecked = true;
            let counter = 0;

            checkboxes.forEach(checkbox => {
                if (checkbox.checked) {
                    atLeastOneCheckboxIsChecked = true;
                    counter += 1;
                }

                else
                    everyCheckBoxChecked = false;

            });

            if (atLeastOneCheckboxIsChecked) {

                checkBoxCounter.innerHTML = counter;
                showElement(checkBoxCounter.parentElement)

                // If is for Sending message part
                if (submitButton === sendZoomButton) {
                    showElement(zoomFootnote);
                    submitButton.disabled = false;
                }
                // else is for Posting loads part
                else {
                    submitButton.forEach(button => {
                        button.disabled = false;
                    });
                }
            }

            else {
                selectAllCheckbox.checked = false;
                counter = 0;
                hideElement(checkBoxCounter.parentElement)

                // If is for Sending message part
                if (submitButton === sendZoomButton) {
                    showElement(zoomFootnote);
                    submitButton.disabled = true;
                }
                // else is for Posting loads part
                else {
                    submitButton.forEach(button => {
                        button.disabled = true;
                    });
                }
            }

            if (everyCheckBoxChecked)
            {
                selectAllCheckbox.checked = true;
            }
            else {
                selectAllCheckbox.checked = false;
            }
        });
    });

}

// Function which change button behavior and add abort button when posting on Landstar
function changeButtonBehaviorWhenPostFormSubmit() {
    postOrDeleteLoadsButton.forEach(btn => {
        const action = btn.getAttribute("data-action");

        if (action === "delete") {
            hideElement(btn);
        }

        else {
            btn.innerHTML = "Running..."
            btn.disabled = true;

            // Revealing Abort button
            const parentDiv = abortPostingButton.parentNode;
            showElement(parentDiv)

            // IF user click abort button:
            abortProcess("posting", btn);
        }
    });

}

// Function for aborting processes
function abortProcess(action, buttonToHide) {
    if (action === "posting")
        abortButton = abortPostingButton;

    else if (action === "scraping")
        abortButton = abortScrapeButton;

    abortButton.addEventListener("click", () => {

        if (action === "posting") {
            abortButton.classList.remove("col-5");
            abortButton.classList.add("col-6");
        }

        hideElement(buttonToHide);
        abortButton.disabled = true;
        abortButton.innerHTML = "Aborting..."

        abort_url = abortButton.getAttribute("data-url");

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
    });
}
