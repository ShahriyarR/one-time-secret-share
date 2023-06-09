window.onload=function (){
    const element = document.getElementById("copy-url-button")
    if (element) {
        document.getElementById("copy-url-button").addEventListener("click", CopyText);
    }
}

function CopyText() {
    const element = document.querySelector('#secret-url');
    const storage = document.createElement('textarea');
    storage.value = element.innerHTML;
    element.appendChild(storage);
    storage.select();
    storage.setSelectionRange(0, 99999);
    document.execCommand('copy');
    element.removeChild(storage);
    const button = document.getElementById("copy-url-button");
    button.value = "Copied";
    button.innerHTML = "Copied";
}