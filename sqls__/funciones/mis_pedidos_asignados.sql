-- FUNCTION: public.mis_pedidos_asignados(integer, integer, integer)

-- DROP FUNCTION public.mis_pedidos_asignados(integer, integer, integer);

CREATE OR REPLACE FUNCTION public.mis_pedidos_asignados(
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
	emp_id integer;
begin
	select empresa_id from usuario_empleado where usuario_ptr_id=id_des limit 1 into emp_id;
	if emp_id is null then
		emp_id:=0;
	end if;
	select count(id) from pedido_pedido where empresa_id = emp_id into t;
	if t is null then
		t:=0;
	end if;
	SELECT COALESCE(array_to_json(array_agg(row_to_json(p))), '[]') from (
		 select distinct p.id,p.num_pedido as num,p.npedido_express as nom,tablameses(p.fecha_pedido) as fecha
		  from usuario_empleado as e
		  inner join pedido_pedido as p
		  on ((p.supervisor_id=e.usuario_ptr_id or p.alistador_id = e.usuario_ptr_id) and e.usuario_ptr_id=id_des and e.empresa_id=emp_id) order by p.id desc  limit length_ offset start_
	) p into l ;
	return '{"recordsFiltered": '|| t ||', "recordsTotal": '|| json_array_length(l) ||', "data": '|| l||'}';

end;

$function$;

ALTER FUNCTION public.mis_pedidos_asignados(integer, integer, integer)
    OWNER TO postgres;
