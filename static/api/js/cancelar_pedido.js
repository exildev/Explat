var dialogo, pedido, cancelar;
$(document).on('ready', function() {
    //$("#modal1").show();

    cancelar = $("#cancelar").dialog({
        autoOpen: false,
        draggable: false,
        modal: true,
        show: {
            effect: "drop",
            direction: "up",
            duration: 500
        },
        hide: {
            effect: "drop",
            direction: "up",
            duration: 500
        },
        buttons: {
            "Cancelar": function() {
                $(this).dialog("close");
            },
            "Aceptar": function() {
                envio();
            }
        }
    });
});

function envio() {
    var id = $('input[name="pedido"]:checked').val();
    console.log(id);
    if (id != undefined) {
        $.ajax({
            url: '/pedidos/ws/cancelado/',
            data: {
                pedido: id
            },
            dataType: 'json',
            type: 'post',
            success: function(response) {
                window.table.column(1).search($('#search').val()).draw();
                cancelar.dialog("close");
            }
        });
    }
}

function entrega() {
    var id = $('input[name="ent"]:checked').val();
    if (id != undefined) {
        $.ajax({
            url: '/pedidos/pedido/entrega/update/',
            data: {
                id_ped: id
            },
            dataType: 'json',
            type: 'post',
            success: function(response) {
                window.table.column(1).search($('#search').val()).draw();
                pedido.dialog("close");
            }
        });
    }
}
