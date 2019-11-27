
/*---------------CAMBIAR CONTENIDO CON PESTAÑAS -------*/

document.getElementById("defaultOpen").click();
document.getElementById("defaultOpenSide").click();
/*----------------------MENUS DE LOCALES Y DEGUSTACIONES --------- */
function tab_main(evt,pageName) {

    var i, tabcontent;
    tabcontent = document.getElementsByClassName("main");
    for (i = 0; i < tabcontent.length; i++) {
      tabcontent[i].style.display = "none";
    }
    document.getElementById(pageName).style.display = "block";
    evt.currentTarget.className += " active";

  }

/*-------------MENUS DE USUARIO, ESTADISTICAS Y SOLICITUDES---------------- */
  function tab_info_menu(evt,pageName) {
    var i, tabcontent;
    tabcontent = document.getElementsByClassName("info_menu");
    for (i = 0; i < tabcontent.length; i++) {
      tabcontent[i].style.display = "none";
    }
    document.getElementById(pageName).style.display = "block";
    evt.currentTarget.className += " active";

  }

  /*------------MODAL BOX DE AYUDA---------------- */
// Get the modal
var modal = document.getElementById("helpModal");

// Get the button that opens the modal
var btn = document.getElementById("helpBtn");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// When the user clicks the button, open the modal 
btn.onclick = function() {
  modal.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
  modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}
