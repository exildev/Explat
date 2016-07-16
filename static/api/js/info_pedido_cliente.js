$( document ).ready(function() {
  $('#id_busq').on('click',function(event){
      $.ajax({
          url:'/pedidos/ws/info/pedido/',
          type:'post',
          dataType:'json',
          data:{pedido:$('#pedido').val()},
          success:function(data){
              if(data.r){
                  $('.clear').val("");
                  $('#alistamiento').val(data.alistar);
                  $('#despacho').val(data.despacho);
                  $('#entrega').val(data.entrega);
                  $('#cliente').val(data.cliente);
              }else{
                  $('.clear, #pedido').val("");
                  alert("El pedido no se encuentra registrado.");
              }
          }
      });
  });
});
