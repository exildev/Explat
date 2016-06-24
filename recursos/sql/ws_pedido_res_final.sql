select ws_add_pedido_service('{"pedido":{"id":"ws_ped","cliente":{"nombre":"mirlan","apellidos":"Reyes Polo","identificacion":"45454545454","dirreccion":"dsdsdsdsddsdsdsdsdssds"},"tienda":{"identificador":"3"},"descripcion":[{"nombre":"jajaja","cantidad":5,"valor":1000},{"nombre":"jajaja","cantidad":5,"valor":1000}],"total_pedido":50000,"tipo_pago":1},"pedido":{"id":"ws_ped","cliente":{"nombre":"mirlan","apellidos":"Reyes Polo","identificacion":"45454545454","dirreccion":"dsdsdsdsddsdsdsdsdssds"},"tienda":{"identificador":"123456"},"descripcion":[{"nombre":"jajaja","cantidad":5,"valor":1000},{"nombre":"jajaja","cantidad":5,"valor":1000}],"total_pedido":50000,"tipo_pago":1}}')

select ws_add_pedido_service('{"pedido":[{"id":"ws_ped","cliente":{"nombre":"mirlan","apellidos":"Reyes Polo","identificacion":"45454545454","dirreccion":"dsdsdsdsddsdsdsdsdssds"},"tienda":{"identificador":"3"},"descripcion":[{"nombre":"jajaja","cantidad":5,"valor":1000},{"nombre":"jajaja","cantidad":5,"valor":1000}],"total_pedido":50000,"tipo_pago":1},{"id":"ws_ped","cliente":{"nombre":"mirlan","apellidos":"Reyes Polo","identificacion":"45454545454","dirreccion":"dsdsdsdsddsdsdsdsdssds"},"tienda":{"identificador":"123456"},"descripcion":[{"nombre":"jajaja","cantidad":5,"valor":1000},{"nombre":"jajaja","cantidad":5,"valor":1000}],"total_pedido":50000,"tipo_pago":1}]}')


CREATE OR REPLACE FUNCTION ws_add_pedido_service(_json json)
  RETURNS text AS
$BODY$
declare
	x record;
	y record;
	tem json;
	t text;   			
	id_emp text;
	ot text;
	id_inser integer;
	error text:='';
	stop boolean :=true;
	val_item boolean;
	id_pedido integer;
	cont_pedido text:='';
	ban_pedido boolean :=true; 
	l json;
	ban_val_ind_emp boolean;
begin
		for x in select * from json_array_elements(_json::json->'pedido') loop 
			id_emp :=cast(x."value"::json->>'tienda' as json)->>'identificador'::text;
			raise notice 'este el validador de  la empresa % ',id_emp;
			select id::text from usuario_tienda where id = case when id_emp ~ '^[0-9]+$' then cast(id_emp as integer) else 0 end limit 1 into id_emp;
			if id_emp is not null then
				val_item:=true;
				<<uno>>
				for y in select nombre,case when cantidad~'^([0-9]+[.])?[0-9]+' then true else false end as cantidad,case when valor~'^([0-9]+[.])?[0-9]+' then true else false end as valor from json_populate_recordset(null::ws_descripcion,cast(x."value"::json->>'descripcion' as json)) loop
					if not y.cantidad or not y.valor then 
						val_item:=false;
						exit uno;
					end if;
				end loop;
				if val_item then
					insert into pedido_pedidows (num_pedido,npedido_express,cliente,fecha_pedido,tienda_id,tipo_pago,total,entregado,despachado,confirmado,alistado)
					values	('','',x."value"::json->>'cliente',now(),cast(id_emp as integer),case when x."value"::json->>'tipo_pago'= '1' then 'Efectivo' when x."value"::json->>'tipo_pago' = '2' then 'Tarjeta' else 'Remision' end,cast(x."value"::json->>'total_pedido' as numeric),false,false,false,false)RETURNING id into id_inser;
					insert into pedido_timews(creado,pedido_id) values (now(),id_inser);
					SELECT COALESCE(array_to_json(array_agg(row_to_json(p))), '[]') from (
						select id,nit,direccion,latitud,longitud,referencia,celular,fijo from usuario_tienda where id = cast(id_emp as integer) limit 1
					) p into l;
					
					cont_pedido:=cont_pedido||case when not ban_pedido then ',' else''end||'{"id":'||id_inser||'"empresa":'||l||',"info":'||x."value"::json||'}';
					ban_pedido:=false;
					raise notice 'este es el pedido valido % ',cont_pedido;
				else
					error:=error||case when not stop then ',' else''end||x."value"::json;
				end if;
			else
				error:=error||case when not stop then ',' else''end||x."value"::json;
				stop:=false;
			end if;
			
		end loop;
	raise notice 'El pedido valido %',cont_pedido;
	raise notice 'El pedido error %',error;
	return '{"respuesta":true,"error":['||error||'],"pedidos":['||cont_pedido||']}';

end;
$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION ws_add_pedido_service(json)
  OWNER TO postgres;

select * from pedido_pedidows

{"pedido":[{"id":"ws_ped","cliente":{"nombre":"mirlan","apellidos":"Reyes Polo","identificacion":"45454545454","dirreccion":"dsdsdsdsddsdsdsdsd
ssds"},"tienda":{"identificador":"3"},"descripcion":[{"nombre":"jajaja","cantidad":5,"valor":1000},{"nombre":"jajaja","cantidad":5,"valor":1000
}],"total_pedido":50000,"tipo_pago":1},{"id":"ws_ped","cliente":{"nombre":"mirlan","apellidos":"Reyes Polo","identificacion":"45454545454","dir
reccion":"dsdsdsdsddsdsdsdsdssds"},"tienda":{"identificador":"123456"},"descripcion":[{"nombre":"jajaja","cantidad":5,"valor":1000},{"nombre":"
jajaja","cantidad":5,"valor":1000}],"total_pedido":50000,"tipo_pago":1}]}


select * from json_array_elements('{"pedido":[{"id":"ws_ped","cliente":{"nombre":"mirlan","apellidos":"Reyes Polo","identificacion":"45454545454","dirreccion":"dsdsdsdsddsdsdsdsdssds"},"tienda":{"identificador":"3"},"descripcion":[{"nombre":"jajaja","cantidad":5,"valor":1000},{"nombre":"jajaja","cantidad":5,"valor":1000}],"total_pedido":50000,"tipo_pago":1},{"id":"ws_ped","cliente":{"nombre":"mirlan","apellidos":"Reyes Polo","identificacion":"45454545454","dirreccion":"dsdsdsdsddsdsdsdsdssds"},"tienda":{"identificador":"123456"},"descripcion":[{"nombre":"jajaja","cantidad":5,"valor":1000},{"nombre":"jajaja","cantidad":5,"valor":1000}],"total_pedido":50000,"tipo_pago":1}]}'::json->'pedido')
select * from json_each('{"pedido":[{"id":"ws_ped","cliente":{"nombre":"mirlan","apellidos":"Reyes Polo","identificacion":"45454545454","dirreccion":"dsdsdsdsddsdsdsdsdssds"},"tienda":{"identificador":"3"},"descripcion":[{"nombre":"jajaja","cantidad":5,"valor":1000},{"nombre":"jajaja","cantidad":5,"valor":1000}],"total_pedido":50000,"tipo_pago":1},{"id":"ws_ped","cliente":{"nombre":"mirlan","apellidos":"Reyes Polo","identificacion":"45454545454","dirreccion":"dsdsdsdsddsdsdsdsdssds"},"tienda":{"identificador":"123456"},"descripcion":[{"nombre":"jajaja","cantidad":5,"valor":1000},{"nombre":"jajaja","cantidad":5,"valor":1000}],"total_pedido":50000,"tipo_pago":1}]}')
