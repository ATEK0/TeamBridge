function deleteNote(id) {
    fetch('/delete-note', {
        method: 'POST',
        body: JSON.stringify({noteId: id})
    }).then((_res) => {
        location.href="/";
    })
}

function uploadFile(filename) {
    fetch('/file-explorer/upload', {
        method: 'POST',
        body: JSON.stringify({file: filename})
    }).then((_res) => {
        location.href="/file-explorer";
    })
}