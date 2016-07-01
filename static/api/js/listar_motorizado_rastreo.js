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
    if (!sub){
        $('.load').show();
        l.html("");
        if(window.mtajax && window.mtajax.readyState != 4){
            window.mtajax.abort();
        }
    }
    window.mtajax = $.ajax({
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
        $('.load').hide();
        var list = data.object_list;
        if(list.length > 0){
            for (var key = 0; key < list.length; key++) {
                var val = list[key];
                l.append(
                    "<li class>" +
                    "<div class='item'>" +
                    "<span class='prim'>" + val.placa + " <i>" + val.nombre + "</i></span>" +
                    "<span class='scun p'>5</span>" +
                    "<span class='scun'>" + val.apellido + "</span>" +
                    "<input type='radio' name='motorizado' datam='1''>" +
                    "</div>" +
                    "</li>"
                );
            }
        }else{
            l.html("");
            l.append('<li class="vacio"><span>No se encontraron resultados.</span></li>');
        }
        if(data.next){
            explat.cargarMotorizados(q, data.next, true);
        }
    });
};

function enviarPedido() {
    var res = {"pedido": [{
        "id": "ws_ped",
        "cliente": {
            "nombre": "mirlan",
            "apellidos": "Reyes Polo",
            "identificacion": "45454545454",
            "direccion": "dsdsdsdsddsdsdsdsdssds",
            "celular":"3103636365",
            "fijo":"6654544"
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
            "celular":"3103636365",
            "fijo":"6654544"
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
    }]};
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

function initMap() {
  // Create a map object and specify the DOM element for display.
  var map = new google.maps.Map($('.mapa').get(0), {
    center: {lat: 5.8329743, lng: -74.13289},
    // scrollwheel: false,
    zoom: 6,
    styles: [{"elementType":"geometry","stylers":[{"hue":"#ff4400"},{"saturation":-68},{"lightness":-4},{"gamma":0.72}]},{"featureType":"road","elementType":"labels.icon"},{"featureType":"landscape.man_made","elementType":"geometry","stylers":[{"hue":"#0077ff"},{"gamma":3.1}]},{"featureType":"water","stylers":[{"hue":"#00ccff"},{"gamma":0.44},{"saturation":-33}]},{"featureType":"poi.park","stylers":[{"hue":"#44ff00"},{"saturation":-23}]},{"featureType":"water","elementType":"labels.text.fill","stylers":[{"hue":"#007fff"},{"gamma":0.77},{"saturation":65},{"lightness":99}]},{"featureType":"water","elementType":"labels.text.stroke","stylers":[{"gamma":0.11},{"weight":5.6},{"saturation":99},{"hue":"#0091ff"},{"lightness":-86}]},{"featureType":"transit.line","elementType":"geometry","stylers":[{"lightness":-48},{"hue":"#ff5e00"},{"gamma":1.2},{"saturation":-23}]},{"featureType":"transit","elementType":"labels.text.stroke","stylers":[{"saturation":-64},{"hue":"#ff9100"},{"lightness":16},{"gamma":0.47},{"weight":2.7}]}]
  });
}
