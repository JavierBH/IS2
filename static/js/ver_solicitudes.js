
function create_request_box(index,name,id){
    //Se crea la div en la que estan las acciones
    var node = document.createElement("DIV"); //Create Div activity_box node
    node.setAttribute("id","request_box_id" + index);
    node.setAttribute("class","request_box");
    
    //Se crea el titulo del usuario
    var h2 = document.createElement("H4");
    var t = document.createTextNode("El usuario: " + name + " le ha enviado una solicitud");     // Create a text node
    h2.appendChild(t);
  
    //Se crea el botone de aceptar
    var butt_aceptar = document.createElement("button");
    butt_aceptar.setAttribute("id","butt_aceptar_id");
    butt_aceptar.setAttribute("class","butt_aceptar");
    butt_aceptar.setAttribute("name","aceptar_solicitud");
    butt_aceptar.setAttribute("value",id);
    butt_aceptar.innerHTML = "Aceptar";
  
  //Se crea el boton de ver
    var butt_ver = document.createElement("button");
    butt_ver.setAttribute("id","butt_aceptar_id");
    butt_ver.setAttribute("class","butt_ver");
    butt_ver.setAttribute("name","ver_solicitud");
    butt_ver.setAttribute("value",id);
    butt_ver.innerHTML = "Ver";
  
    //Se crea el boton de eliminar
    var butt_eliminar = document.createElement("button");
    butt_eliminar.setAttribute("id","butt_eliminar");
    butt_eliminar.setAttribute("class","butt_eliminar");
    butt_eliminar.setAttribute("name","eliminar_solicitud");
    butt_eliminar.setAttribute("value",id);
    
    butt_eliminar.innerHTML = "Eliminar";

    var hr = document.createElement("HR");
    //Se añaden los elementos al activity_box div
    node.appendChild(h2);
    node.appendChild(butt_aceptar);
    node.appendChild(butt_ver);
    node.appendChild(butt_eliminar);
    node.appendChild(hr);
    document.getElementById("solicitudes").appendChild(node);
  
    /*Función que elimna la solictud al clicar en cualquiera de los dos botones*/ 
    function closeButton(index) {
      /*close all autocomplete lists in the document,
      except the one passed as an argument:*/
      var name = "request_box_id" + index;
      var x = document.getElementById(name);
      while (x.firstChild) {
        x.removeChild(x.firstChild);
      }
      x.parentNode.removeChild(x);
    }
  
  }
  
  function create_solicitudes_box(arr_names,arr_ids){
    var nombres_amigos = split_array(arr_names);
    var ids_amigos = split_id(arr_ids);
    console.log(nombres_amigos);
    console.log(ids_amigos);
    for ( var i = 0; i < nombres_amigos.length; i++) {
      create_request_box(i,nombres_amigos[i],ids_amigos[i])
    }
  }

  function split_id(arr){
    var final_1 = arr.split('"');
    var res = [];
    for(var i = 0; i<final_1.length-1;i++){
      if(i!=0 && i<final_1.length-1){
        res.push(final_1[i]);
      }
    }
    return res;
  }  

  
function split_array(arr){
    var final_1 = arr.split('"');
    var res = [];
    for(var i = 0; i<final_1.length-1;i++){
      if(i!=0 && i%2==0){
        res.push(final_1[i]);
      }
    }
    return res;
  }