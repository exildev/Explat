CREATE FUNCTION public.crear_tiempo_pedido()
    RETURNS trigger
    LANGUAGE 'plpgsql'
    COST 100.0
AS $BODY$

declare
begin
	insert into pedido_time(pedido_id,creado) values (new.id,now());
	return new;
end;

$BODY$;

ALTER FUNCTION public.crear_tiempo_pedido()
    OWNER TO postgres;
