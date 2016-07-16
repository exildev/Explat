$(document).on('ready',function(){
    limpiarSelect();
    mensajem = $("#men").dialog({
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
            "Ok": function() {
                $(this).dialog("close");
            }
        }
    });
    mensajea = $("#mena").dialog({
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
            "Ok": function() {
                $(this).dialog("close");
            }
        }
    });
    mensajes = $("#mens").dialog({
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
            "Ok": function() {
                $(this).dialog("close");
            }
        }
    });
    $('#id_tienda').on('change',function(event){
        limpiarSelect();
        if($(this).val().length > 0){
            $.ajax({
                url:"/motorizado/ws/list/motorizado/?q="+$(this).val()+"&page=1",
                type:'get',
                dataType:'json',
                success:function(data){
                    var r = data.object_list;
                    if (r.length > 0){
                        for (var key in r){
                            var nom = r[key].nombre,
                                ident = r[key].ident;
                            $('select[name="motorizado"]').append("<option value=\""+ident+"\">"+nom+"</option>");
                        }
                    }else{
                        mensajem.dialog('open');
                    }
                }
            });
            $.ajax({
                url:"/usuario/ws/list/supervisor/?q="+$(this).val()+"&page=1",
                type:'get',
                dataType:'json',
                success:function(data){
                    var r = data.object_list;
                    if (r.length > 0){
                        for (var key in r){
                            var nom = r[key].nombre,
                                ident = r[key].ident;
                            $('select[name="supervisor"]').append("<option value=\""+ident+"\">"+nom+"</option>");
                        }
                    }else{
                        mensajes.dialog('open');
                    }
                }
            });
            $.ajax({
                url:"/usuario/ws/list/alistador/?q="+$(this).val()+"&page=1",
                type:'get',
                dataType:'json',
                success:function(data){
                    var r = data.object_list;
                    if (r.length > 0){
                        for (var key in r){
                            var nom = r[key].nombre,
                                ident = r[key].ident;
                            $('select[name="alistador"]').append("<option value=\""+ident+"\">"+nom+"</option>");
                        }
                    }else{
                        mensajea.dialog('open');
                    }
                }
            });
        }
    });
});

function limpiarSelect(){
    $('select[name="motorizado"]').html("");
    $('select[name="motorizado"]').html("<option value>Motorizado</option>");
    $('select[name="alistador"]').html("");
    $('select[name="alistador"]').html("<option value>---------</option>");
    $('select[name="supervisor"]').html("");
    $('select[name="supervisor"]').html("<option value>---------</option>");
}
