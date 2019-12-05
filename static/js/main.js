
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
modal_box("helpModal","helpBtn");
/*----------------- MODAL BOX DE VER PERFIL -----------------------*/
modal_box("ver_mas_perfil_Modal","ver_mas_perfil_butt_id");
/*----------------- DISPLAY DE LA MODAL BOX -----------------------*/
function modal_box(modal_name, btn_name){
  // Get the modal
var modal = document.getElementById(modal_name);

// Get the button that opens the modal
var btn = document.getElementById(btn_name);

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
}
/*-----------------RECENT ACTIVITY MENU--------------------------*/ 

function create_activity_box(){
  //Se crea la div en la que estan las acciones
  var node = document.createElement("DIV"); //Create Div activity_box node
  node.setAttribute("id",this.id + "activity_box_id");
  node.setAttribute("class","activity_box");
  
  //Se crea la imagen
  var img = document.createElement("img");
  img.setAttribute("class","img_activity_box");
  img.setAttribute("src", "images/hydrangeas.jpg");

  //Se crea el titulo del usuario
  var h2 = document.createElement("H4");
  var t = document.createTextNode("Usuario 1");     // Create a text node
  h2.appendChild(t);

  //Se crea el parrafo con el texto
  var p = document.createElement("P");
  var t = document.createTextNode("JAJAJAJAJ COSAS SI COSAS JAJAJA"); 
  p.appendChild(t);
  
  var hr = document.createElement("HR");
  //Se añaden los elementos al activity_box div
  node.appendChild(img);
  node.appendChild(h2);
  node.appendChild(p);
  document.getElementById("recents").appendChild(node);
  document.getElementById("recents").appendChild(hr);
}

for ( var i = 0; i < 6; i++) {
  create_activity_box()
}

/*------------------- SOLICITUDES -------------------*/

function create_request_box(index){
  //Se crea la div en la que estan las acciones
  var node = document.createElement("DIV"); //Create Div activity_box node
  node.setAttribute("id","request_box_id" + index);
  node.setAttribute("class","request_box");
  
  //Se crea la imagen
  var img = document.createElement("img");
  img.setAttribute("class","img_request_box");
  img.setAttribute("src", "images/hydrangeas.jpg");

  //Se crea el titulo del usuario
  var h2 = document.createElement("H4");
  var t = document.createTextNode("Usuario 1");     // Create a text node
  h2.appendChild(t);

  //Se crea el botone de aceptar
  var butt_aceptar = document.createElement("button");
  butt_aceptar.setAttribute("id",this.id +"butt_aceptar_id");
  butt_aceptar.setAttribute("class","butt_aceptar");
  butt_aceptar.setAttribute("value","aceptar");
  butt_aceptar.innerHTML = "Aceptar";
  butt_aceptar.addEventListener("click", function () {
    closeButton(index);
});
  //Se crea el boton de eliminar
  var butt_eliminar = document.createElement("button");
  butt_eliminar.setAttribute("id",this.id +"butt_eliminar");
  butt_eliminar.setAttribute("class","butt_eliminar");
  butt_eliminar.setAttribute("value","eliminar");
  butt_eliminar.innerHTML = "Eliminar";
  butt_eliminar.addEventListener("click", function () {
    closeButton(index);
});

  var hr = document.createElement("HR");
  //Se añaden los elementos al activity_box div
  node.appendChild(img);
  node.appendChild(h2);
  node.appendChild(butt_aceptar);
  node.appendChild(butt_eliminar);
  node.appendChild(hr);
  document.getElementById("solicitudes").appendChild(node);

  /*Función que elimna la solictud al clicar en cualquiera de los dos botones*/ 
  function closeButton(index) {
    /*close all autocomplete lists in the document,
    except the one passed as an argument:*/
    var name = "request_box_id" + index;
    var x = document.getElementById(name);
    console.log(index);
    while (x.firstChild) {
      x.removeChild(x.firstChild);
    }
    x.parentNode.removeChild(x);
  }

}

for ( var i = 0; i < 6; i++) {
  create_request_box(i)
}

/*------------- INDICADOR DEL NUMERO DE PETICIONES -------------------*/
