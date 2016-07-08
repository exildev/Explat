function tablaPedidos(){
	window.table = $('#search-results').DataTable({
        "bPaginate": true,
        "bScrollCollapse": true,
        "sPaginationType": "full_numbers",
        "bRetrieve": true,
        "oLanguage": {
            "sProcessing": "Procesando...",
            "sLengthMenu": "Mostrar _MENU_ Registros",
            "sZeroRecords": "No se encontraron resultados",
            "sInfo": "Mostrando desde _START_ hasta _END_ de _TOTAL_ Registros",
            "sInfoEmpty": "Mostrando desde 0 hasta 0 de 0 Registros",
            "sInfoFiltered": "(filtrado de _MAX_ registros en total)",
            "sInfoPostFix": "",
            "sSearch": "Buscar:",
            "sUrl": "",
            "oPaginate": {
                "sFirst": "|<<",
                "sPrevious": "<<",
                "sNext": ">>",
                "sLast": ">>|"
            }
        },
        "processing": true,
        "serverSide": true,
        "ajax": {
            "url": "/pedidos/pedido/search/"

        },
        "drawCallback": function (row, data) {
           	//funciones a cargar luego de el llamado
			$('.stop').on('click',function(even){
				return false;
			});
			$('.imp').on('click',function(even){
				var win = window.open($(this).attr('href'), '_blank');
					win.focus();
			});
			$('.desactivar').on('click',function(even){
				var res_act = $(this).parent().find('input[type="hidden"]').val();
				$(this).parent().find('input[type="radio"]').prop('checked',true);
				if (res_act == "1"){
					$('#cancelar').text("Esta seguro de cancelar el pedido "+$(this).parents('tr').find('td:first').text());
					cancelar.dialog('open');
				}
			});
        },
        "columns": [
            {
                "data": "num"
            },
            {
                "data": "emp"
            },
            {
            	"data":"sup"
            },
            {
            	"data":"alis"
            },
            {
            	"data":"moto"
            },
            {
            	"data":"total"
            },
            {
            	"class":"center aligned",
                "data": "estado",
                "render": function ( data, type, full, meta ) {
                	var m="";
                	if (data == 1){
                		m="<i class=\"checkmark large green icon\"></i>";
                	}else{
                		m="<i class=\"remove large red icon\"> </i>";
                	}
					m+="<input type=\"hidden\" name=\"estado\" value=\""+data+"\">" ;
                	return m;
				}
            },
            {
            	"class":"center aligned",
                "data": "activado",
                "render": function ( data, type, full, meta ) {
                	var m="";
                	if (data == 1){
                		m="<i class=\"checkmark large green icon desactivar\"></i>";
                	}else{
                		m="<i class=\"remove large red icon activar\"> </i>";
                	}
					m+="<input type=\"hidden\" name=\"activado\" value=\""+data+"\">";
					m+="<input style=\"visibility: hidden;\" type=\"radio\" name=\"pedido\" value=\""+full.id+"\">";
                	return m;
				}
            },
            {
            	"className":"center aligned",
                "data": "id",
                "render": function ( data, type, full, meta ) {
                	var m="";
                	m+="<a href=\"/pedidos/pedido/info/"+data+"/\" class=\"ui icon green\"><i class=\"unhide large green icon\"></i></a>";
					if (full.estado == 0){
                		m+="<a href=\"/pedidos/pedido/edit/"+data+"/\" class=\"ui icon green\"><i class=\"edit large green icon\"></i></a>";
					}
                	m+="<a href=\"/pedidos/pedido/factura/"+data+"\" class=\"ui icon stop imp\"><i class=\"print large green icon\"></i></a>";
                	return m;
				}
            }
        ]
    });
}
function hides(){
	$('#search-results_filter,#dataTables_length').hide();
}
tablaPedidos();
init();
window.onload = hides;
