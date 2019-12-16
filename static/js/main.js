
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
  /*---------------- PESTAÑA DE DEGUSTACIONES PREFERIDAS ------------------- */
//La funcion recibe como parametros la url de la imagen y el nombre de la degustacion
  
function degustaciones_window(img_url,name){
  //Se crea un div donde se colocan los elementos de la degustacion
  var card = document.createElement("DIV");
  card.setAttribute("class","card");

  //Se crea el boton que lleva a la info de la degistacion
  var butt_degus = document.createElement("button");
  //Se crea la imagen
  console.log(img);
  var img = document.createElement("img");
  img.src = img_url
  //Se crea el elemento de texto
  var text = document.createTextNode(name);
  card.appendChild(img);
  card.appendChild(text);
  card.appendChild(butt_degus);
  document.getElementById("degustaciones_flex_div_id").appendChild(card);
}

function locales_window(img_url,name){
  //Se crea un div donde se colocan los elementos de la degustacion
  var card = document.createElement("DIV");
  card.setAttribute("class","card");

  //Se crea el boton que lleva a la info de la degistacion
  var butt_degus = document.createElement("button");
  //Se crea la imagen
  console.log(img);
  var img = document.createElement("img");
  img.src = img_url
  //Se crea el elemento de texto
  var text = document.createTextNode(name);
  card.appendChild(img);
  card.appendChild(text);
  card.appendChild(butt_degus);
  document.getElementById("locales_flex_div_id").appendChild(card);
}


/* Se crean 6 de prueba*/
for(var i = 0; i<6;i++){
  degustaciones_window("https://images.unsplash.com/photo-1535332371349-a5d229f49cb5?ixlib=rb-1.2.1&w=1000&q=80","Degus" + i);
  locales_window("https://images.unsplash.com/photo-1535332371349-a5d229f49cb5?ixlib=rb-1.2.1&w=1000&q=80","Local_" + i);

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
modal_box("helpModal","helpBtn",0);
/*----------------- MODAL BOX DE VER PERFIL -----------------------*/
modal_box("ver_mas_perfil_Modal","ver_mas_perfil_butt_id",1);
/*----------------- DISPLAY DE LA MODAL BOX -----------------------*/

/* La funcion modal_box, se encarga de abrir y cerrar los pop-up de la pagina
Recibe 3 argumentos: 
El primero es el  ID del div del pop up.
El segundo es el ID del boton que abre el pop up.
El 3 es el indice de del pop up (orden de aparicion), para poder cerrar el pop up
 */

function modal_box(modal_name, btn_name,close_button_index){
  // Get the modal
var modal = document.getElementById(modal_name);

// Get the button that opens the modal
var btn = document.getElementById(btn_name);

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[close_button_index];
console.log(span);
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

function activity_box(name,activity){
  //Se crea la div en la que estan las acciones
  var node = document.createElement("DIV"); //Create Div activity_box node
  node.setAttribute("id",this.id + "activity_box_id");
  node.setAttribute("class","activity_box");
  
  //Se crea el titulo del usuario
  var h2 = document.createElement("H4");
  var t = document.createTextNode(name + " acaba de hacer:");     // Create a text node
  h2.appendChild(t);

  //Se crea el parrafo con el texto
  var p = document.createElement("P");
  var t = document.createTextNode(activity); 
  p.appendChild(t);
  
  var hr = document.createElement("HR");
  //Se añaden los elementos al activity_box div
  node.appendChild(h2);
  node.appendChild(p);
  document.getElementById("recents").appendChild(node);
  document.getElementById("recents").appendChild(hr);
}

function create_activity_box(arr_name,arr_activity){
  name = split_array(arr_name);
  activity = split_array(arr_activity);
  console.log(activity);
  for ( var i = 0; i < name.length; i++) {
    activity_box(name[i],activity[i])
  }
}
/*------------- INDICADOR DEL NUMERO DE PETICIONES -------------------*/

function split_array(arr){
  var final_1 = arr.split('"');
  var res = [];
  console.log(final_1)
  for(var i = 0; i<final_1.length-1;i++){
    if(i!=0 && i%2==0){
      res.push(final_1[i]);
    }
  }
  return res;
}