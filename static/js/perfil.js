/*---------------CAMBIAR CONTENIDO CON PESTAÑAS -------*/

document.getElementById("defaultOpen").click();

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