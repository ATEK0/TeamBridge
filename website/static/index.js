function deleteNote(id) {
    fetch('/delete-note', {
        method: 'POST',
        body: JSON.stringify({noteId: id})
    }).then((_res) => {
        location.href="/";
    })
}


function startCounter() {
    const deleteBtn = document.getElementById('deleteButton');
    const countdown = document.querySelector('#deleteButton');
    let timeLeft = 5;

    const intervalId = setInterval(() => {
    timeLeft--;
    if (timeLeft <= 0) {
        clearInterval(intervalId);
        deleteBtn.disabled = false;
        countdown.innerHTML = 'Delete';
    } else {
        countdown.innerHTML = `${timeLeft}`;
    }
    }, 1000);
}
    
function deleteAccount() {
    console.log("delete account")
    window.location.href="{{ url_for('profilePage.deleteAccount', id=client.id) }}";
}
