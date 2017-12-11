-- Function: public.crear_tiempo_pedido()

-- DROP FUNCTION public.crear_tiempo_pedido();

CREATE OR REPLACE FUNCTION public.crear_tiempo_pedido()
  RETURNS trigger AS
$BODY$

declare
begin
	insert into pedido_time(pedido_id,creado) values (new.id,now());
	return new;
end;

$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION public.crear_tiempo_pedido()
  OWNER TO postgres;

  -- Trigger: crear_tiempo_pedido on public.pedido_pedido

  -- DROP TRIGGER crear_tiempo_pedido ON public.pedido_pedido;

  CREATE TRIGGER crear_tiempo_pedido
    AFTER INSERT
    ON public.pedido_pedido
    FOR EACH ROW
    EXECUTE PROCEDURE public.crear_tiempo_pedido();
