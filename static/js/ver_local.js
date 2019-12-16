
function degustaciones_window(img_url,name,ver,local_name){
    //Se crea un div donde se colocan los elementos de la degustacion
    var card = document.createElement("DIV");
    card.setAttribute("class","content");
    //Se crea la imagen
    var img = document.createElement("img");
    img.src = img_url
    //Se crea el elemento de texto
    var text = document.createTextNode(name);
    var H4 = document.createElement("H4");
    var hr = document.createElement("HR");

    var button = document.createElement("button");
    button.innerHTML="Ver Más";
    button.setAttribute("name","local_button");
    var value = local_name.split('"')[2] + "," + name;
    button.setAttribute("value",value);

    H4.appendChild(text);
    card.appendChild(img);
    card.appendChild(hr);
    card.appendChild(H4);
    card.appendChild(button);
    if(ver!=1){
    document.getElementById("row_id").appendChild(card);
  }
  }

  /* Se crean 6 de prueba*/

function create_boxes(arr,fotos){
  fotos_arr = split_array(fotos);
  var degustaciones = split_array(arr);
  var n_boxes = degustaciones.length;
    if(n_boxes%5 != 0){
    while(n_boxes%5 != 0){
     n_boxes++;
  } 
  }
    for(var i = 0; i<n_boxes;i++){
      if(i>degustaciones.length-1){
        degustaciones_window("https://66.media.tumblr.com/21ceabba01c5c84f86331f6cb9fa98a3/tumblr_o4zjfrrpFJ1rlwpsao8_500.png","CACA",1,"PEDO");
      } else{
        degustaciones_window("static/"+ fotos_arr[i],degustaciones[i],0,local_name)
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