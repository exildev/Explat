CREATE FUNCTION public.update_tiempo_pedido()
    RETURNS trigger
    LANGUAGE 'plpgsql'
    COST 100.0
AS $BODY$

declare
begin
	if new.confirmado and old.confirmado=false then
		update pedido_time set confirmado = now() where pedido_id= old.id;
	elsif new.entregado and old.entregado=false then
		update pedido_time set entregado = now() where pedido_id= old.id;
	elsif new.alistado and old.alistado=false then
		update pedido_time set alistado = now() where pedido_id= old.id;
	elsif new.despachado  and old.despachado=false then
		update pedido_time set despachado = now() where pedido_id= old.id;
	elsif new.notificado  and old.notificado=false then
		update pedido_time set notificado = now() where pedido_id= old.id;
	elsif new.activado=false then
		/*update pedido_pedido set entregado=false, despachado=false, notificado=false, reactivacion=false where id = old.id;*/
		new.entregado=false;
		new.despachado=false;
		new.notificado=false;
		new.reactivacion=false;
	elsif new.activado=true then
		/*update pedido_pedido set reactivacion=true where id = new.id;*/
		new.reactivacion=true;
	end if;
	return new;
end;

$BODY$;

ALTER FUNCTION public.update_tiempo_pedido()
    OWNER TO postgres;
