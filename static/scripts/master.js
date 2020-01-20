function search(event) {
    var value = document.getElementById("searchbox").value.toLowerCase()
    var navoptions = document.getElementsByClassName("navoption")
    Array.prototype.forEach.call(navoptions, function(e) {
        if (e.innerText.toLowerCase().includes(value)) {
            e.classList.remove("navoption-hide")
        } else {
            e.classList.add("navoption-hide")
        }
    });
}


function startup(event) {
    document.getElementById("searchbox").addEventListener('input', search)
}


document.addEventListener("DOMContentLoaded", startup)