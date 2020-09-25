function search(event) {
    var value = document.getElementById("searchbox").value.toLowerCase()
    var navoptions = document.getElementsByClassName("navoption")
    Array.prototype.forEach.call(navoptions, function(e) {
        if (e.innerText.toLowerCase().includes(value)) {
            e.parentElement.classList.remove("hide")
        } else {
            e.parentElement.classList.add("hide")
        }
    });
    var groups = document.getElementsByClassName("nav-ul")
    Array.prototype.forEach.call(groups, function(e) {
        var subli = e.getElementsByTagName("li")
        var hasitems = [].filter.call(subli, li => ! li.classList.contains("hide")).length > 0
        if (hasitems) {
            e.classList.remove("hide")
        } else {
            e.classList.add("hide")
        }
    });
}

function navigation_unhide(event) {
    var navs = document.getElementsByClassName("nav")
    Array.prototype.forEach.call(navs, function(e) {
        if (e.classList.contains("mobile-hide")) {
            e.classList.remove("mobile-hide")
        } else {
            e.classList.add("mobile-hide")
        }
    });
}


function startup(event) {
    document.getElementById("searchbox").addEventListener('input', search)
    document.getElementById("navigation-unhide").addEventListener('click', navigation_unhide)
}


document.addEventListener("DOMContentLoaded", startup)