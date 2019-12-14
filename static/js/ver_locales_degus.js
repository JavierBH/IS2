
function degustaciones_window(img_url,name,ver){
    //Se crea un div donde se colocan los elementos de la degustacion
    var card = document.createElement("DIV");
    card.setAttribute("class","content");

    //Se crea la imagen
    var img = document.createElement("img");
    img.src = img_url;
    //Se crea el elemento de texto
    var text = document.createTextNode(name);
    var H4 = document.createElement("H4");
    var button = document.createElement("button");
    button.innerHTML="Ver Más";
    button.setAttribute("name","local_button");
    button.setAttribute("value",name);
    
    H4.appendChild(text);
    card.appendChild(img);
    card.appendChild(H4);
    card.appendChild(button);
    
    if(ver !=1){
    document.getElementById("local_box_id").appendChild(card);
  } 
  }

  /* 
  Esta funcion recibe un array con los nombres de los locales*/
function create_boxes(arr,fotos){
  fotos_arr = split_array(fotos);
var locales = split_array(arr);
var n_boxes = locales.length;
  if(n_boxes%3 != 0){
  while(n_boxes%3 != 0){
   n_boxes++;
} 
}

  for(var i = 0; i<n_boxes;i++){
    console.log(locales);
    if(i>locales.length-1){
      degustaciones_window("https://66.media.tumblr.com/21ceabba01c5c84f86331f6cb9fa98a3/tumblr_o4zjfrrpFJ1rlwpsao8_500.png","CACA",1);
    } else{
      degustaciones_window("static/"+ fotos_arr[i],locales[i],0)
    }
  }
}

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