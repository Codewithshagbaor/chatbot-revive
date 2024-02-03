const settingsbtn = document.getElementById('settingsbtn');
const settings = document.getElementById('settings');
const form = document.getElementById('form');
const textarea = document.getElementById('user-message');
const container = document.getElementById('container');

// adjusts the textarea's container
textarea.addEventListener('input', function () {
  this.style.height = 'auto';
  this.style.height = (this.scrollHeight) + 'px';
});

container.addEventListener('input', function () {
  checkOverflow();
});

function checkOverflow() {
  const isOverflowing = container.scrollHeight > container.clientHeight;

  if (isOverflowing) {
    container.style.height = 'auto';
    container.style.height = (this.scrollHeight) + 'px';
    console.log('is working')
  }
}

// toggling the display of the form
settingsbtn.addEventListener('click', function () {
  form.classList.toggle('hidden');
});

settings.addEventListener('click', function () {
  form.classList.toggle('hidden');
  settings.classList.toggle('rotate-90');
});
var storedName = localStorage.getItem('user_name');
var storedEmail = localStorage.getItem('user_email');
function submitUserDetails() {
  var userName = $('#user-name').val();
  var userEmail = $('#user-email').val();

  // Store details in localStorage
  localStorage.setItem('user_name', userName);
  localStorage.setItem('user_email', userEmail);

  // Hide the form and show the chat container
  $('#user-details-container').hide();
  $('#settingsbtn').show();
  $('#container').show();
}
function UpdateUserDetails() {
  var userName = $('#user-name-1').val();
  var userEmail = $('#user-email-1').val();
  $('#alert-show').show();
  // Store details in localStorage
  localStorage.setItem('user_name', userName);
  localStorage.setItem('user_email', userEmail);
}

if (!storedName || !storedEmail) {
  // If details are not stored, show the form to input details
  $('#user-details-container').show();
  $('#container').hide();
} else {
  // User details are available, show the chat container
  $('#user-details-container').hide();
  $('#settingsbtn').show();
  $('#container').show();

  // Set user details in the form
  $('#user-name').val(storedName);
  $('#user-email').val(storedEmail);
  $('#user-name-1').val(storedName);
  $('#user-email-1').val(storedEmail);

  // Load and display chat history
  var chatHistory = JSON.parse(localStorage.getItem('chat_history')) || [];
  displayChatHistory(chatHistory);
}
function displayChatHistory(chatHistory) {
  // Display chat history in the message container
  chatHistory.forEach(function (message) {
      var messageClass = message.type === 'user' ? 'flex flex-col self-end blue1 max-w-52 sm:max-w-60 md:max-w-80 text-white text-pretty p-2 rounded-t-xl rounded-bl-xl mb-8' : 'flex flex-col blue1 max-w-52 sm:max-w-60 md:max-w-80 text-white text-pretty p-2 rounded-t-xl rounded-br-xl mb-3';

      // Check if the time property exists in the message
      var timeElement = message.time ? '<p class="text-sm self-end">' + message.time + '</p>' : '';

      $('#message-container').append('<div class="' + messageClass + '">' +
          '<p class="text-wrap mr-14">' + message.message + '</p>' +
          timeElement +
          '</div>');
  });
}


// Save chat messages in localStorage

function sendMessage(option) {
  var userMessage = option || $('#user-message').val();
  var currentTime = new Date();
        
        // Format time as HH:mm
  var formattedTime = currentTime.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  $('#message-container').append('<div class="flex flex-col self-end blue1 max-w-52 sm:max-w-60 md:max-w-80 text-white text-pretty p-2 rounded-t-xl rounded-bl-xl mb-8">' + '<p class="text-wrap mr-14">' + userMessage + '</p>' + '<p class="text-sm self-end">' + formattedTime + '</p>' + '</div>');
  saveChatMessage('user', userMessage, formattedTime);

  $.ajax({
    url: '/',
    type: 'POST',
    data: { 'user_message': userMessage, 'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val() },
    dataType: 'json',
    beforeSend: function () {
      // Add typing animation before sending the request
      $('#message-container').append('<div class="chatbot-message typing-indicator">Typing...</div>');
    },
    success: function (data) {
      // Remove typing indicator before appending the actual response
      $('.typing-indicator').remove();
      

        // Create and append time element
      

      // Simulate typing animation for the response
      var responseContainer = $('<div  class="flex flex-col blue1 max-w-52 sm:max-w-60 md:max-w-80 text-white text-pretty p-2 rounded-t-xl rounded-br-xl mb-3"></div>');
      $('#message-container').append(responseContainer);
      saveChatMessage('chatbot', data.response, formattedTime);
      var bar = $('<p class="text-wrap mr-14"></p>');
      var timeElement = $('<p class="text-sm self-end"></p>').text(formattedTime);
      var responseText =data.response;
      var index = 0;

      function appendNextCharacter() {
        if (index < responseText.length) {
          bar.append(responseText.charAt(index));
          index++;
          setTimeout(appendNextCharacter, 50); // Adjust the delay between characters if needed
        } else {
          // Display menu options if available
          if (data.faq_options && data.faq_options.length > 0) {
            var optionsContainer = $('<div>');
        
            // Use Math.min to ensure we iterate up to the first five elements or the length of the array if it's less than five
            data.faq_options.slice(0, Math.min(5, data.faq_options.length)).forEach(function (option) {
                var button = $('<button class="border-2 rounded text-pretty cursor-pointer text-sm border-blue-600  md:max-w-34 p-2">').text(option);
                button.click(function () {
                    sendMessage(option);
                    $('#button-container').hide(); // Hide the button container after clicking an option
                });
                optionsContainer.append(button);
            });
        
            $('#button-container').html(optionsContainer).show(); // Update and show the button container
        }
        
          // Call displayChatHistory after the chatbot response is fully displayed
        }
      }
      responseContainer.append(bar);
responseContainer.append(timeElement);
      appendNextCharacter();
    }

  });


  if (!option) {
    $('#user-message').val('');
  }
}
function saveChatMessage(type, message, time) {
  var chatHistory = JSON.parse(localStorage.getItem('chat_history')) || [];
  chatHistory.push({ type: type, message: message, time: time });
  localStorage.setItem('chat_history', JSON.stringify(chatHistory));
}
// When ending the chat session, clear stored data
function endChat() {
  localStorage.removeItem('user_name');
  localStorage.removeItem('user_email');
  localStorage.removeItem('chat_history');
  $('#user-details-container').show();
  $('#message-container').hide();
  $('#settingsbtn').hide();
  $('#container').hide();
  $('#form').hide();
}
