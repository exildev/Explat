-- Function: public.eliminar_moto()

-- DROP FUNCTION public.eliminar_moto();

CREATE OR REPLACE FUNCTION public.eliminar_moto()
  RETURNS trigger AS
$BODY$

declare
begin
	IF (TG_OP = 'DELETE') THEN
		update motorizado_moto set estado=false where id = old.id;
	end if;
	return null;
end;

$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION public.eliminar_moto()
  OWNER TO postgres;

CREATE TRIGGER eliminar_moto
  BEFORE DELETE
  ON public.motorizado_moto
  FOR EACH ROW
  EXECUTE PROCEDURE public.eliminar_moto();
