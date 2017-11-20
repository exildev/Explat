-- FUNCTION: public.eliminar_moto()

-- DROP FUNCTION public.eliminar_moto();

CREATE FUNCTION public.eliminar_moto()
    RETURNS trigger
    LANGUAGE 'plpgsql'
    COST 100.0
AS $BODY$

declare
begin
	IF (TG_OP = 'DELETE') THEN
		update motorizado_moto set estado=false where id = old.id;
	end if;
	return null;
end;

$BODY$;

ALTER FUNCTION public.eliminar_moto()
    OWNER TO postgres;
