-- Function: public.update_tiempo_pedido()

-- DROP FUNCTION public.update_tiempo_pedido();

CREATE OR REPLACE FUNCTION public.update_tiempo_pedido()
  RETURNS trigger AS
$BODY$

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

$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION public.update_tiempo_pedido()
  OWNER TO postgres;



-- Trigger: update_tiempo_pedido on public.pedido_pedido

-- DROP TRIGGER update_tiempo_pedido ON public.pedido_pedido;

CREATE TRIGGER update_tiempo_pedido
  AFTER UPDATE
  ON public.pedido_pedido
  FOR EACH ROW
  EXECUTE PROCEDURE public.update_tiempo_pedido();
