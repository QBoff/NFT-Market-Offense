let uploadButton = document.querySelector('input[type="file"]')

uploadButton.addEventListener('change', (e) => {
    const currFiles = e.target.files
    if (currFiles.length > 0) {
        let src = URL.createObjectURL(currFiles[0])
        let imagePreview = document.getElementById('preview')
        imagePreview.src = src
        imagePreview.style.display = "block"
        imagePreview.style.width = "100%";
        imagePreview.style.height = "100%";
        imagePreview.style.borderRadius = "16px";
        // imagePreview.style.borderStyle = "dashed";
    }
})
