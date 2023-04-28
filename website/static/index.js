function deleteNote(id) {
    fetch('/delete-note', {
        method: 'POST',
        body: JSON.stringify({noteId: id})
    }).then((_res) => {
        location.href="/";
    })
}


// verificar se a imagem é menor do q a resolucao indicada
const imageInput = document.getElementById('profile_pic');

imageInput.addEventListener('change', (event) => {
  const file = event.target.files[0];
  const image = new Image();

  image.onload = () => {
    const width = image.width;
    const height = image.height;

    if (width > 1920 || height > 1080) {
      alert('The image resolution must be less than or equal to 1920x1080.');
      imageInput.value = ''; 
    }
  };

  image.src = URL.createObjectURL(file);
});