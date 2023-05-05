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
