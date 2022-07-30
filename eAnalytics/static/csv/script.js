Dropzone.autoDiscover=false;
const myDropzone= new Dropzone('#csv-file-dropzone',{
    url:'csv-upload-success/',
    maxFiles:5,
    maxFilesize:1024,
    acceptedFiles:'.csv',
})