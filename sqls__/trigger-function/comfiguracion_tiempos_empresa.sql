CREATE FUNCTION public.comfiguracion_tiempos_empresa()
    RETURNS trigger
    LANGUAGE 'plpgsql'
    COST 100.0
AS $BODY$

declare
begin
	insert into pedido_configuraciontiempo (retraso,pedido,distancia,empresa_id,primero,segundo,gps) values(3,3,1000,new.id,1,15,1);
	return new;
end;

$BODY$;

ALTER FUNCTION public.comfiguracion_tiempos_empresa()
    OWNER TO postgres;
