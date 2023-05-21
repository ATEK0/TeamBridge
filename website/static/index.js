function deleteNote(id) {
    fetch('/delete-note', {
        method: 'POST',
        body: JSON.stringify({noteId: id})
    }).then((_res) => {
        location.href="/";
    })
}

$(document).ready(function() {
    $('#yourCountry').change(function() {
      // Get the value of the selected option
      const selectedCountry = $(this).children('option:selected').val();
      // Set the value of the country input field to the selected country
      $('#yourCountry').val(selectedCountry);
    });
  });



//toggle sidebar

function toggleSidebar() {
  var finder = 0;
  var classList = document.getElementById('body').className.split(/\s+/);
  for (var i = 0; i < classList.length; i++) {
      if (classList[i] === 'toggle-sidebar') {
          finder++;
      }
  }

  if (finder == 0) {
    $("#body").addClass('toggle-sidebar');
    $("#main").removeClass('m-300');
  } else {
  $("#body").removeClass('toggle-sidebar');
  $("#main").addClass('m-300');
  }
}


//change register form show

function changeRegisterForm(form) {
  if (form == "company") {
    $(".register-chose-c").addClass("move-left");
    $(".register-user-c").addClass("register-apear")
  } else if (form == "reverse"){
    $(".register-chose-c").removeClass("move-left");
    $(".register-chose-c").removeClass("move-right");
    $(".register-user-c").removeClass("register-apear")
    $(".register-company-c").attr('style','left: -100%')

  } else {
    $(".register-chose-c").addClass("move-right");
    $(".register-company-c").attr('style','left: 50%')
  }
}



//check register things
function registerHandler(type) {

  const data = {
    type: "checking",
    email: $("#yourEmail").val(),
    fname: $("#firstName").val(),
    lname: $("#lastName").val(),
    password: $("#yourPassword").val()
  };
  
  fetch('/register', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
  })
    .then(response => response.json())
    .then(result => {
      // Process the response
      console.log(result);
      if (result["message"] === 'OK'){
        if ($("#yourEmail").val().length < 3) {
          showToast('danger', "Your email must be bigger than 3 characters");
        } else if ($("#firstName").val().length <= 1) {
          showToast('danger', "Your name must be bigger than 1 character");
        } else if ($("#lastName").val().length <= 1) {
          showToast('danger', "Your name must be bigger than 1 character");
        } else if ($("#yourPassword").val() != $("#yourPassword2").val()) {
          showToast('danger', "Passwords don't match!");
        } else {
          document.getElementById("register-user").submit();
        }
      } else {
        showToast('danger', result["message"]);
      }
    })
    .catch(error => {
      // Handle any errors that occur during the request
      console.error('Error:', error);
    });
  
}

function addInfosHandler(type) {
  
  var birth = document.getElementById("birth").value;
  
  const data = {
    type: "checking",
    username: $("#yourUsername").val()
  };
  
  fetch('/add-infos', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
  })
    .then(response => response.json())
    .then(result => {
      // Process the response
      console.log(result);
      if (result["message"] === 'OK'){
        if (birth === '' || birth === null) {
          const field = document.getElementById('birth');
          field.setCustomValidity('Please fill this field');
          field.reportValidity();
        } else {
          document.getElementById("add-infos-user").submit();
        }
      } else {
        showToast('danger', result["message"]);
      }
    })
    .catch(error => {
      // Handle any errors that occur during the request
      console.error('Error:', error);
    });
  
}


const showToast = (category, message) => {
  const toastContainer = document.createElement('div');
  toastContainer.setAttribute('aria-live', 'polite');
  toastContainer.setAttribute('aria-atomic', 'true');
  toastContainer.style.position = 'relative';
  toastContainer.style.zIndex = '2000';

  const toastElement = document.createElement('div');
  toastElement.classList.add('toast');
  toastElement.classList.add(`toast-${category}`);
  toastElement.classList.add('position-fixed');
  toastElement.classList.add('mt-3')

  toastElement.style.marginRight = '20px';
  toastElement.style.minWidth = '400px !important';
  toastElement.style.top = '40px';
  toastElement.style.right = '0';
  toastElement.setAttribute('data-delay', '7000');
  toastElement.setAttribute('data-bs-autohide', 'true');

  const toastHeader = document.createElement('div');
  toastHeader.classList.add('toast-header');
  toastHeader.classList.add(`toast-${category}`);

  const strongElement = document.createElement('strong');
  if (category === 'danger') {
    strongElement.classList.add('me-auto');
    strongElement.classList.add('text-danger');
    strongElement.innerHTML = '<i class="bi bi-exclamation-octagon-fill"></i> ERROR';
  } else if (category === 'success') {
    strongElement.classList.add('me-auto');
    strongElement.classList.add('text-success');
    strongElement.innerHTML = '<i class="bi bi-check-lg"></i> SUCCESS';
  } else if (category === 'warning') {
    strongElement.classList.add('me-auto');
    strongElement.classList.add('text-warning');
    strongElement.innerHTML = '<i class="bi bi-exclamation-circle-fill"></i> WARNING';
  } else if (category === 'info') {
    strongElement.classList.add('me-auto');
    strongElement.classList.add('text-info');
    strongElement.innerHTML = '<i class="bi bi-exclamation-circle-fill"></i> INFO';
  }

  const smallElement = document.createElement('small');
  smallElement.textContent = 'right now';

  const closeButton = document.createElement('button');
  closeButton.type = 'button';
  closeButton.classList.add('ml-2');
  closeButton.classList.add('mb-1');
  closeButton.classList.add('btn-close');
  closeButton.setAttribute('data-bs-dismiss', 'toast');
  closeButton.setAttribute('aria-label', 'Close');

  const toastBody = document.createElement('div');
  toastBody.classList.add('toast-body');
  toastBody.textContent = message;

  toastHeader.appendChild(strongElement);
  toastHeader.appendChild(smallElement);
  toastHeader.appendChild(closeButton);

  toastElement.appendChild(toastHeader);
  toastElement.appendChild(toastBody);

  toastContainer.appendChild(toastElement);

  document.body.appendChild(toastContainer);

  const toast = new bootstrap.Toast(toastElement);
  toast.show();
};




// this is a countdown that allows people to reread infos before deleting its account
// function startCounter() {
//     const deleteBtn = document.getElementById('deleteButton');
//     const countdown = document.querySelector('#deleteButton');
//     let timeLeft = 5;

//     const intervalId = setInterval(() => {
//     timeLeft--;
//     if (timeLeft <= 0) {
//         clearInterval(intervalId);
//         deleteBtn.disabled = false;
//         countdown.innerHTML = 'Delete';
//     } else {
//         countdown.innerHTML = `${timeLeft}`;
//     }
//     }, 1000);
// }
    
// function deleteAccount() {
//     console.log("delete account")
//     window.location.href="{{ url_for('profilePage.deleteAccount', id=client.id) }}";
// }
