-- FUNCTION: public.insertar_moto()

-- DROP FUNCTION public.insertar_moto();

CREATE FUNCTION public.insertar_moto()
    RETURNS trigger
    LANGUAGE 'plpgsql'
    COST 100.0
AS $BODY$

declare
begin
	IF (TG_OP = 'INSERT') THEN
		update motorizado_moto set estado=true where id = new.id;
	end if;
	return new;
end;

$BODY$;

ALTER FUNCTION public.insertar_moto()
    OWNER TO postgres;
