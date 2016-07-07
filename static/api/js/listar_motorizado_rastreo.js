window.mtajax = null;
window.explat = {};

$(document).on('ready', function() {
    explat.cargarMotorizados(null, 1, false);
    $('#search').on('keyup', function() {
        explat.cargarMotorizados($(this).val(), 1, false);
    });
});

window.explat.cargarMotorizados = function(q, pag, sub, rq) {
    var l = $('.lis_emp');
    if (!sub) {
        $('.load').show();
        l.html("");
        if (window.mtajax && window.mtajax.readyState != 4) {
            window.mtajax.abort();
        }
    }
    window.mtajax = $.ajax({
        url: '/motorizado/ws/list/rastreo/',
        type: 'get',
        dataType: 'json',
        data: {
            q: q ? q : '',
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
        $('.load').hide();
        var list = data.object_list;
        if (list.length > 0) {
            for (var key = 0; key < list.length; key++) {
                var val = list[key];
                var dir = '';
                var ul = $('<ul></ul>');
                for (var key2 in val.direccion) {
                    var aux = val.direccion[key2];
                    ul.append('<li><div class="item"><span class="prim">'+aux.direccion+'</span></div></li>'),
                    dir += aux.direccion + (key2 == val.direccion.length ? '' : ', ');
                }
                var aux = $(
                    "<li class=" + (val.tipo == 1 ? 'it' : 'sc') + ">" +
                    "<div class='item'>" +
                    "<span class='prim'>" + val.placa + " <i>" + val.nombre + "</i></span>" +
                    "<span class='scun p'>"+val.num_pedido+"</span>" +
                    "<span class='scun dir'>" + dir + "</span>" +
                    "<input type='radio' name='motorizado' datam='"+val.identificador+"'>" +
                    "</div>" +
                    "</li>"
                );
                var aux2 = $('<div class="ov"><div class="overlay"><div></div>')
                aux2.find('.overlay').append(ul);
                aux.find('.dir').append(aux2);
                l.append(aux);
            }
            $('.dir').click(function() {
                window.ov = $(this).find('.ov');
                ov.toggle();
            });
        } else {
            l.html("");
            l.append('<li class="vacio"><span>No se encontraron resultados.</span></li>');
        }
        if (data.next) {
            explat.cargarMotorizados(q, data.next, true);
        }
    });
};

function enviarPedido() {
    var res = {
        "pedido": [{
            "id": "ws_ped",
            "cliente": {
                "nombre": "mirlan",
                "apellidos": "Reyes Polo",
                "identificacion": "45454545454",
                "direccion": "dsdsdsdsddsdsdsdsdssds",
                "celular":"366454545",
                "fijo":"6605648"
            },
            "tienda": {
                "identificador": "3"
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
        }, {
            "id": "ws_ped",
            "cliente": {
                "nombre": "mirlan",
                "apellidos": "Reyes Polo",
                "identificacion": "45454545454",
                "direccion": "dsdsdsdsddsdsdsdsdssds",
                "celular":"366454545",
                "fijo":"6605648"
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
        }]
    };
    console.log(res);
    $.ajax({
        url: '/pedidos/emp/ws/pedido/',
        type: 'POST',
        dataType: 'json',
        data: JSON.stringify(res),
        success: function(data) {
            console.log(data);
        }
    });
}
