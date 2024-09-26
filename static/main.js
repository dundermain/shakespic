const dropArea = document.getElementById('drop-area');
const preview = document.getElementById('preview');
const responseDisplay = document.getElementById('response');

['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    dropArea.addEventListener(eventName, preventDefaults, false);
});

function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
}

dropArea.addEventListener('drop', handleDrop, false);

function handleDrop(e) {
    let dt = e.dataTransfer;
    let files = dt.files;
    handleFiles(files);
}

function handleFiles(files) {
    [...files].forEach(uploadFile);
}

function uploadFile(file) {
    let url = '/upload';
    let formData = new FormData();
    formData.append('file', file);

    fetch(url, {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.description) {
            responseDisplay.innerHTML = `<p>${data.description}</p>`;
        } else {
            responseDisplay.innerHTML = `<p>${data.error}</p>`;
        }
    })
    .catch(() => {
        responseDisplay.innerHTML = `<p>Upload failed</p>`;
    });
}
