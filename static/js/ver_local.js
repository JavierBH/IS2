
function degustaciones_window(img_url,name){
    //Se crea un div donde se colocan los elementos de la degustacion
    var card = document.createElement("DIV");
    card.setAttribute("class","content");

    //Se crea la imagen
    var img = document.createElement("img");
    img.src = img_url
    //Se crea el elemento de texto
    var text = document.createTextNode(name);
    var H4 = document.createElement("H4");
    H4.appendChild(text);
    card.appendChild(img);
    card.appendChild(H4);
    document.getElementById("row_id").appendChild(card);
  }

  /* Se crean 6 de prueba*/

for(var i = 0; i<15;i++){
    degustaciones_window("https://66.media.tumblr.com/21ceabba01c5c84f86331f6cb9fa98a3/tumblr_o4zjfrrpFJ1rlwpsao8_500.png","Degus" + i);
  }