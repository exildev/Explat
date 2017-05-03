-- FUNCTION: public.cant_pedidos_motor_periodo(text)

-- DROP FUNCTION public.cant_pedidos_motor_periodo(text);

CREATE OR REPLACE FUNCTION public.cant_pedidos_motor_periodo(
	identif text)
RETURNS numeric
    LANGUAGE 'plpgsql'
    COST 100.0

AS $function$

declare
 motorizado record;
begin
	select m.empleado_id as empleado,e.empresa_id as empresa from motorizado_motorizado as m inner join usuario_empleado as e on (m.empleado_id=e.usuario_ptr_id and m.identifier=identif) limit 1 into motorizado;
	if motorizado is null then
		return 0;
	end if;
	return (select count(q.id)::numeric from (
			select p.id from public.pedido_pedido as p inner join public.pedido_configuraciontiempo as c on (p.motorizado_id=motorizado.empleado and p.empresa_id=c.empresa_id and p.activado = true and p.entregado= true)
				 where c.id = (select confi.id from public.pedido_configuraciontiempo as confi where confi.empresa_id=motorizado.empresa order by confi.id desc limit 1) and p.fecha_pedido
						between
						       case when extract(day from current_date) > c.primero and extract(day from current_date) < c.segundo then
							    cast(''||extract(year from current_date)||'-'||extract(month from current_date)||'-'||c.primero as date)
							       else
							    cast(''||extract(year from current_date)||'-'||extract(month from current_date)||'-'||c.segundo as date)
							end
						and
							case when extract(day from current_date) > c.primero and extract(day from current_date) < c.segundo then
							     cast(''||extract(year from current_date)||'-'||extract(month from current_date)||'-'||c.segundo as date)
								else
							     cast(''||extract(year from current_date)+case when extract(month from current_date) = 12 then 1 else 0 end||'-'||case when extract(month from current_date) = 12 then 1 else extract(month from current_date)+1 end||'-'||c.primero as date)
							 end
				union
				select p.id*100000 from public.pedido_pedidows as p inner join public.usuario_tienda as t on (p.motorizado_id=motorizado.empleado and p.tienda_id=t.id and p.entregado=true and p.activado=true) inner join public.pedido_configuraciontiempo as c on (t.empresa_id=c.empresa_id and p.activado = true and p.entregado= true)
				 where c.id = (select confi.id from public.pedido_configuraciontiempo as confi where confi.empresa_id=motorizado.empresa order by confi.id desc limit 1) and p.fecha_pedido
						between
						       case when extract(day from current_date) > c.primero and extract(day from current_date) < c.segundo then
							    cast(''||extract(year from current_date)||'-'||extract(month from current_date)||'-'||c.primero as date)
							       else
							    cast(''||extract(year from current_date)||'-'||extract(month from current_date)||'-'||c.segundo as date)
							end
						and
							case when extract(day from current_date) > c.primero and extract(day from current_date) < c.segundo then
							     cast(''||extract(year from current_date)||'-'||extract(month from current_date)||'-'||c.segundo as date)
								else
							     cast(''||extract(year from current_date)+case when extract(month from current_date) = 12 then 1 else 0 end||'-'||case when extract(month from current_date) = 12 then 1 else extract(month from current_date)+1 end||'-'||c.primero as date)
					        end
		      ) as q);
end;

$function$;

ALTER FUNCTION public.cant_pedidos_motor_periodo(text)
    OWNER TO postgres;
