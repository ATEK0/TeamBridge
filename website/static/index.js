const showToast = (category, message) => {
  const toastContainer = document.createElement('div');
  toastContainer.setAttribute('aria-live', 'assertive');
  toastContainer.setAttribute('aria-atomic', 'true');
  toastContainer.style.position = 'relative';
  toastContainer.style.zIndex = '2000';
  toastContainer.classList.add("fit-content");

  const toastElement = document.createElement('div');
  toastElement.classList.add('toast');
  toastElement.classList.add(`toast-${category}`);
  toastElement.classList.add('position-fixed');
  toastElement.classList.add('ms-3')
  toastElement.classList.add('mt-3')

  toastElement.style.marginRight = '20px';
  toastElement.style.width = '400px !important';
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

    $(".register-user-c").addClass("register-apear");

    $(".register-user-c").addClass("show-reg");
    setTimeout(() => {$(".register-user-c").css("display", "block"); }, 300);


  } else if (form == "reverse"){
    $(".register-chose-c").removeClass("move-left");
    $(".register-chose-c").removeClass("move-right");

    $(".register-user-c").removeClass("show-reg");

    setTimeout(() => {$(".register-user-c").css("display", "none"); }, 1000);


    $(".register-user-c").removeClass("register-apear")

  } else {
    $(".register-chose-c").addClass("move-right");

  }
}



//check register things





fetch('/add-infos', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify(data)
})
  .then(response => response.json())
  .then(result => {

    console.log(result);

  })
  .catch(error => {

    console.error('Error:', error);
    
  });





//change background on selected file

function HandleFileSelect(fileID) {

  if ($("#" + fileID).hasClass("list-group-item-primary")) {
    $("#" + fileID).removeClass("list-group-item-primary");
    $("#btn-"+ fileID).prop("checked", false );
  } else {
    $("#" + fileID).addClass("list-group-item-primary");
    $("#btn-"+ fileID).prop("checked", true );
  }

  var checkedCount = $("#files input[type='checkbox']:checked").length;

  console.log(checkedCount);

  if (checkedCount > 0) {
    $("#download-general").css("visibility", "visible");
    $("#checkbox-general").css("visibility", "visible");
    $("#delete-general").css("visibility", "visible");
  } else {
    $("#checkbox-general").css("visibility", "hidden");
    $("#download-general").css("visibility", "hidden");
    $("#delete-general").css("visibility", "hidden");
  }

}

function DownloadMultipleFiles() {
  var fileCount = $("#files input[type='checkbox']:checked").length;
  var fileChecked = $("#files input[type='checkbox']:checked");

  for (x = 0; x < fileCount;x++){
    downloadID = fileChecked.eq(x).val();    
    // Make the POST request
    fetch("/file-explorer/download/" + downloadID, {
      method: 'POST',});
  }
}

function HandleInputClick(element) {
  if (!element.disabled) {
    event.stopPropagation();
  }
}

function changeFileName(method, fileID) {
  if (method != 'reverse') {
    $("#changeNameInput-" + fileID).removeClass("changeNameInput");
    $("#changeNameIconCancel-" + fileID).removeClass("d-none");


    $("#changeNameInput-" + fileID).removeAttr('disabled');
    $("#changeNameIcon-" + fileID).addClass("d-none");
    $("#changeNameIconConfirm-" + fileID).removeClass("d-none");

    $('#changeNameInput-' + fileID).focus();

  } else {
    resetChangeName(fileID);
  }
  

}

function resetChangeName(fileID) {
  $("#changeNameInput-" + fileID).addClass("changeNameInput");
  $("#changeNameInput-" + fileID).attr("disabled", true);
  $("#changeNameIcon-" + fileID).removeClass("d-none");

  $("#changeNameIconCancel-" + fileID).addClass("d-none");
  $("#changeNameIconConfirm-" + fileID).addClass("d-none");
}

$(document).on('click', '#changeNameOptions', function(event) {
  event.stopPropagation();
});

$('#changeNameInput').blur(function(event) {
  var fileID = $(this).data('file-id');
  console.log(fileID);
  changeFileName('reverse', fileID); 
});



function FetchFileName(fileID, option, newname) {
  const data = {
    type: option,
    id: fileID,
    nameChange: newname
  };

  fetch('/file-explorer/changeFileName', {
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

      if (option == 'close') {
        resetChangeName(fileID);
        $("#changeNameInput-" + fileID).val(result['filename']);
      } else {
        resetChangeName(fileID);
        $("#changeNameInput-" + fileID).val(result['filename']);
        showToast('success', result["message"]);
      }
      
    })
    .catch(error => {
      // Handle any errors that occur during the request
      console.error('Error:', error);
    });

  
}


// reset password

function resetPassword(userID, emaill) {
  const data = {
    id: userID,
    email: emaill
  };
  fetch('/createResetPassword', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
  })
    .then(response => response.json())
    .then(result => {
        if (result["type"] == "error") {
          showToast('danger', result["message"]);   
        } else {
          showToast('success', result["message"]);   
        }
    });
}

// fetch('/register', {
//   method: 'POST',
//   headers: {
//     'Content-Type': 'application/json'
//   },
//   body: JSON.stringify(data)
// })
//   .then(response => response.json())
//   .then(result => {
//     // Process the response
//     console.log(result);
//     var password = $("#yourPassword").val()

//     if (result["message"] === 'OK'){
//       if ($("#yourEmail").val().length < 3) {
//         showToast('danger', "Your email must be bigger than 3 characters");
//       } else if ($("#firstName").val().length <= 1) {
//         showToast('danger', "Your name must be bigger than 1 character");
//       } else if ($("#lastName").val().length <= 1) {
//         showToast('danger', "Your name must be bigger than 1 character");
//       } else if ($("#yourPassword").val() != $("#yourPassword2").val()) {
//         showToast('danger', "Passwords don't match!");
//       } else if (password.length < 7){ 
//         showToast('danger', "Password must be bigger than 7 characters!");
//       } else {
//         document.getElementById("register-user").submit();
//       }
//     } else {
//       showToast('danger', result["message"]);
//     }
//   })
//   .catch(error => {
//     // Handle any errors that occur during the request
//     console.error('Error:', error);
//   });



// this is a countdown that allows people to reread infos before deleting its account
function startCounter() {
    const deleteBtn = document.getElementById('deleteButton');
    const countdown = document.querySelector('#deleteButton');
    let timeLeft = 5;

    deleteBtn.innerHTML = "5";
    deleteBtn.disabled = true;

    const intervalId = setInterval(() => {
    timeLeft--;
    if (timeLeft <= 0) {
        clearInterval(intervalId);
        deleteBtn.disabled = false;
        countdown.innerHTML = 'Yes Delete Account';
    } else {
        countdown.innerHTML = `${timeLeft}`;
    }
    }, 1000);
}
    

function showCodeBox() {
  
}