-- FUNCTION: public.tabla_pedidos_cancelados(integer, text, integer, integer)

-- DROP FUNCTION public.tabla_pedidos_cancelados(integer, text, integer, integer);

CREATE OR REPLACE FUNCTION public.tabla_pedidos_cancelados(
	id_user integer,
	search_ text,
	start_ integer,
	length_ integer)
RETURNS text
    LANGUAGE 'plpgsql'
    COST 100.0

AS $function$

  declare
    l json;
    t integer :=0;
  begin
      select count(p.id) from (select * from public.usuario_empleado where usuario_ptr_id=id_user limit 1) as emp
                         inner join public.pedido_pedido as p on (activado=false and reactivacion=false and emp.tienda_id=p.tienda_id) into t;
      SELECT COALESCE(array_to_json(array_agg(row_to_json(p))), '[]') from (
              select u.first_name||' '||u.last_name as motorizado,p.num_pedido as num ,tablameses(p.fecha_pedido) as fecha,t.nombre,p.id from (select * from public.usuario_empleado where usuario_ptr_id=id_user limit 1)
                  as emp inner join public.pedido_pedido as p on (activado=false and reactivacion=false and emp.tienda_id=p.tienda_id)
                  inner join auth_user as u on (u.id=p.motorizado_id)
                  inner join public.usuario_tienda as t on (p.tienda_id=t.id) where p.num_pedido like '%'||upper(search_)||'%' or upper(t.nombre) like '%'||upper(search_)||'%'
                  limit length_ offset start_
      ) p into l;
      return '{"recordsFiltered": '|| case when t is null then 0 else t end ||', "recordsTotal": '|| json_array_length(l) ||', "data": '|| l||'}';
  end;

$function$;

ALTER FUNCTION public.tabla_pedidos_cancelados(integer, text, integer, integer)
    OWNER TO postgres;
