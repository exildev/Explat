$(document).on('ready', function() {
    cargarMotorizados(null, 1, false);
    $('#search').on('keyup', function() {
        cargarMotorizados($(this).val(), 1, false);
    });
});

function cargarMotorizados(q, pag, sub) {
    $.ajax({
        url: '/motorizado/ws/list/rastreo/',
        type: 'get',
        dataType: 'json',
        data: {
            q: q? q: '',
            page: pag
        },
        statusCode: {
            400: function() {
                console.warn("list service error");
            },
            404: function() {
                console.warn("list service not found");
            }
        }
    }).done(function(data) {
        var list = data.object_list;
        var next = data.next;
        if(list.length > 0){
            console.log(list);
            var l = $('.lis_emp');
            if (!sub){
                l.html("");
            }
            for (var key = 0; key < list.length; key++) {
                var val = list[key];
                l.append(
                    "<li>" +
                    "<span>" + val.placa + "</span>" +
                    "<ul>" +
                    "<li>" + val.nombre + "</li>" +
                    "<li>" + val.apellido + "</li>" +
                    "<li>" + val.identificador + "</li>" +
                    "<input type=\"radio\" name=\"selec\">" +
                    "</ul>" +
                    "</li>"
                );
            }
        }
        if(next){
            cargarMotorizados(q, next, true);
        }
    });
}

function enviarPedido() {
    var res = {
        "pedido": {
            "id": "ws_ped",
            "cliente": {
                "nombre": "mirlan",
                "apellidos": "Reyes Polo",
                "identificacion": "45454545454",
                "dirreccion": "dsdsdsdsddsdsdsdsdssds"
            },
            "tienda": {
                "identificador": "123456"
            },
            "descripcion": [{
                "nombre": "jajaja",
                "cantidad": 5,
                "valor": 1000
            }, {
                "nombre": "jajaja",
                "cantidad": 5,
                "valor": 1000
            }],
            "total_pedido": 50000,
            "tipo_pago": 1
        },
        "pedido2": {
            "id": "ws_ped",
            "cliente": {
                "nombre": "mirlan",
                "apellidos": "Reyes Polo",
                "identificacion": "45454545454",
                "dirreccion": "dsdsdsdsddsdsdsdsdssds"
            },
            "tienda": {
                "identificador": "123456"
            },
            "descripcion": [{
                "nombre": "jajaja",
                "cantidad": 5,
                "valor": 1000
            }, {
                "nombre": "jajaja",
                "cantidad": 5,
                "valor": 1000
            }],
            "total_pedido": 50000,
            "tipo_pago": 1
        }
    };
    $.ajax({
        url: '/pedido/res/ws/pedido/',
        type: 'POST',
        dataType: 'json',
        data: JSON.stringify(res),
        success: function(data) {
            console.log(data);
        }
    });
}
