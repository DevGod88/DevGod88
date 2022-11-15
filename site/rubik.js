let icone = document.querySelector("#menu");
let nav = document.querySelector("nav");

function menu() {
    let fichier = icone.getAttribute("src");
    if (fichier == "menu_f.png") {
        nav.style.display="block";
        icone.setAttribute("src", "fermeture.png");
    }
    else{
        icone.setAttribute("src","menu_f.png");
        nav.style.display="none"
    }
}

function corrige(){
    let largeur = document.body.clientWidth;
    if (largeur > 1485){
        nav.style.display="block"
    }
    else{
        nav.style.display="none"
    }
}

icone.addEventListener("click", menu, false);
window.addEventListener("resize", corrige, false);


//Gestion du loader :

// Définition des variables
var main_div = document.getElementById("main_div");
var loader = document.getElementById("loader");

window.scrollTo(0,0)
main_div.style.overflow="hidden"
main_div.scrollTop = 0

window.addEventListener("load", function(){

    // Définition du style du loader (animation ease-out comprise)
    loader.style.animationName="ease-out-perso";
    loader.style.animationDuration="2s";
    loader.style.animationTimingFunction="linear";
    loader.style.animationDelay="0s";
    loader.style.animationIterationCount="1";
})


loader.addEventListener("animationend",function() {
    loader.style.display="none";

    // Réactivation du scrolling
    main_div.style.overflow="auto";
})