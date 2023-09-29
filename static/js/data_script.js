function openTab(evt, tabName) {
    var i, tabcontent, tablinks;
    
    // Hide all content
    tabcontent = document.getElementsByClassName("content");
    for (i = 0; i < tabcontent.length; i++) {
      tabcontent[i].style.display = "none";
    }
    
    // Remove "active" class from all buttons
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
      tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    
    // Show the selected content and mark the button as active
    document.getElementById(tabName).style.display = "block";
    evt.currentTarget.className += " active";
  };

function redirecttovalidation() {
    window.location.href = '/validate_' + req_tables;
}

// chat function which loads user message and gets bot response by invoking the URI
document.addEventListener("DOMContentLoaded", function () {
  const msgerForm = document.querySelector(".msger-inputarea");
  const msgerInput = document.querySelector("#textInput");
  const msgerChat = document.querySelector(".chat-container");

  msgerForm.addEventListener("submit", function (event) {
    event.preventDefault();
    const msgText = msgerInput.value;
    if (!msgText) return;

    appendMessage(msgText);
    msgerInput.value = "";
    botResponse(msgText);
  });

  function appendMessage(text) {
    const msgHTML = `
      <div class="user-message">
        <div class="user-icon"></div>
        <div class="user-message-bubble">
          ${text}
        </div>
      </div>
    `;
    msgerChat.insertAdjacentHTML("beforeend", msgHTML);
    msgerChat.scrollTop += 500;
  }

  function botResponse(rawText) {
    const selectElement = document.getElementById("table-dropdown");
    const desiredValue = document.getElementById("table-dropdown").value;
    let selected_tbl_name = '';
    for (let i = 0; i < selectElement.options.length; i++) {
      const option = selectElement.options[i];
      if (option.value === desiredValue) {
        // Found a match, get the innerHTML
        selected_tbl_name = option.innerHTML.toLowerCase();
        break; // Exit the loop since we found a match
      }
    }


    $.get("/get_llmresponse", { msg: rawText, table_selected: selected_tbl_name }).done(function (data) {
      console.log(rawText);
      console.log(data);
      const msgHTML = `
        <div class="bot-message">
          <div class="bot-icon"></div>
          <div class="bot-message-bubble">
            ${data}
          </div>
        </div>
      `;
      msgerChat.insertAdjacentHTML("beforeend", msgHTML);
      msgerChat.scrollTop += 500;
    });
  }
});
