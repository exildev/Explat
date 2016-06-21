$(document).on('ready',function(){
	$('#search').on('keyup',function(){
		cargarMotorizados($(this).val(),1,2);
	});

});

function cargarMotorizados(bus,star,pag){
	$.ajax({
		url: '/plataforma/motorizado/listar/rastreo/',
		type: 'post',
		dataType: 'json',
		data: {busq: bus,start:star,pag:pag},
		success:function(data){
			if(data.data.length > 0){
				var l =$('.lis_emp');
				l.html("");
				for(var i=0;i<data.data.length;i++){
					var nom=data.data[i].nom ,ape=data.data[i].ape ;ide=data.data[i].ide;
					l.append(
						"<ul>"+
	                    "<li>"+nom+"</li>"
	                    +"<li>"+ape+"</li>"
	                    +"<li>"+ide+"</li>"
	                    +"<input type=\"radio\" name=\"selec\">"
	                  	+"</ul>"
	                );
				}
			}
		}
	});

}

function enviarPedido(){
	var res ={"pedido":{"id":"ws_ped","cliente":{"nombre":"mirlan","apellidos":"Reyes Polo",
		"identificacion":"45454545454","dirreccion":"dsdsdsdsddsdsdsdsdssds"},
		"tienda":{"identificador":"123456"},"descripcion":[{"nombre":"jajaja","cantidad":5,"valor":1000},
		{"nombre":"jajaja","cantidad":5,"valor":1000}],"total_pedido":50000,"tipo_pago":1},
		"pedido":{"id":"ws_ped","cliente":{"nombre":"mirlan","apellidos":"Reyes Polo","identificacion":"45454545454","dirreccion":"dsdsdsdsddsdsdsdsdssds"},
		"tienda":{"identificador":"123456"},"descripcion":[{"nombre":"jajaja","cantidad":5,"valor":1000},
		{"nombre":"jajaja","cantidad":5,"valor":1000}],"total_pedido":50000,"tipo_pago":1}};
		$.ajax({
			url: '/pedido/res/ws/pedido/',
			type: 'POST',
			dataType: 'json',
			data: JSON.stringify(res),
			success:function(data){
				console.log(data);
			}
		});
}
