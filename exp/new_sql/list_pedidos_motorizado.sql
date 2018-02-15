create or replace function list_pedidos_motorizado(identificador text) returns json as $$
 declare
        configuracion record;
	id_tienda record;
begin
	select e.tienda_id as tienda,e.usuario_ptr_id as id from motorizado_motorizado as m
	                   inner join usuario_empleado as e
	                     on (
	                          m.identifier='861083035233844' and m.empleado_id=e.usuario_ptr_id
	                        ) limit 1 into id_tienda;
	if id_tienda is null then
		id_tienda:=0;
	end if;
	select c.gps from usuario_tienda as t inner join usuario_empresa as e on (t.empresa_id=e.id and t.id=id_tienda.tienda) inner join pedido_configuraciontiempo as c on (c.empresa_id=e.id) limit 1 into configuracion;
	return (SELECT COALESCE(array_to_json(array_agg(row_to_json(p))), '[]') from (
		select case when configuracion.gps is not null then configuracion.gps*1000 else 100 end as tiempo_gps, id, (select identifier from motorizado_motorizado where empleado_id=motorizado_id limit 1) as motorizado,10000*(select retraso from pedido_configuraciontiempo order by id desc limit 1) as retraso,
		(
			SELECT COALESCE(array_to_json(array_agg(row_to_json(emp))), '[]') from (
						select id,nit,direccion,latitud,longitud,referencia,celular,fijo from usuario_tienda where id = tienda_id limit 1
					) emp
		) as tienda,
		(
			SELECT COALESCE(array_to_json(array_agg(row_to_json(items))), '[]') from (
				select i.descripcion as nombre,pi.cantidad as cantidad,pi.valor_unitario as valor from pedido_itemspedido as pi inner join pedido_items as i on(pi.pedido_id=bus_ped.id and pi.item_id=i.id)
			) items
		) as info,
		(
			select sum(pi.cantidad*pi.valor_unitario) from pedido_itemspedido as pi inner join pedido_items as i on(pi.pedido_id=bus_ped.id and pi.item_id=i.id)
		) as total,
		(
			SELECT COALESCE(array_to_json(array_agg(row_to_json(emp_cli))), '[]') from (
						select first_name as nombre,last_name as apellidos,telefono_fijo as fijo,telefono_celular as celular,direccion from usuario_cliente where id = bus_ped.cliente_id
					) emp_cli
		) as cliente
		from pedido_pedido as bus_ped where bus_ped.motorizado_id = id_tienda.id and entregado=false and activado=true
	) p);
end;
$$language plpgsql
