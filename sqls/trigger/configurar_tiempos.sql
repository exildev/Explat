-- Function: public.comfiguracion_tiempos_empresa()

-- DROP FUNCTION public.comfiguracion_tiempos_empresa();

CREATE OR REPLACE FUNCTION public.comfiguracion_tiempos_empresa()
  RETURNS trigger AS
$BODY$

declare
begin
	insert into pedido_configuraciontiempo (retraso,pedido,distancia,empresa_id,primero,segundo,gps) values(3,3,1000,new.id,1,15,1);
	return new;
end;

$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION public.comfiguracion_tiempos_empresa()
  OWNER TO postgres;

  -- Trigger: comfiguracion_tiempos_empresa on public.usuario_empresa

  -- DROP TRIGGER comfiguracion_tiempos_empresa ON public.usuario_empresa;

  CREATE TRIGGER comfiguracion_tiempos_empresa
    AFTER INSERT
    ON public.usuario_empresa
    FOR EACH ROW
    EXECUTE PROCEDURE public.comfiguracion_tiempos_empresa();
