-- FUNCTION: public.pedidos_a_asignar_motor(integer, integer, integer)

-- DROP FUNCTION public.pedidos_a_asignar_motor(integer, integer, integer);

CREATE OR REPLACE FUNCTION public.pedidos_a_asignar_motor(
	id_des integer,
	start_ integer,
	length_ integer)
RETURNS text
    LANGUAGE 'plpgsql'
    COST 100.0

AS $function$

declare
	l json;
	t integer;
begin
	select count(id) from pedido_pedido where empresa_id = (select empresa_id from usuario_empleado where usuario_ptr_id=id_des limit 1) into t;
	if t is null then
		t:=0;
	end if;
	SELECT COALESCE(array_to_json(array_agg(row_to_json(p))), '[]') from (
		 select p.num_pedido as num,upper(u.first_name)||' '||upper(u.last_name) as nom,tablameses(p.fecha_pedido) as fecha,p.id
			from pedido_pedido as p inner join auth_user  as u on (p.alistador_id=id_des and p.supervisor_id=u.id and p.motorizado_id is null)
	) p into l ;
	return '{"recordsFiltered": '|| t ||', "recordsTotal": '|| json_array_length(l) ||', "data": '|| l||'}';

end;

$function$;

ALTER FUNCTION public.pedidos_a_asignar_motor(integer, integer, integer)
    OWNER TO postgres;
