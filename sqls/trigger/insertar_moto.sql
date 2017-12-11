-- Function: public.insertar_moto()

-- DROP FUNCTION public.insertar_moto();

CREATE OR REPLACE FUNCTION public.insertar_moto()
  RETURNS trigger AS
$BODY$

declare
begin
	IF (TG_OP = 'INSERT') THEN
		update motorizado_moto set estado=true where id = new.id;
	end if;
	return new;
end;

$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION public.insertar_moto()
  OWNER TO postgres;

CREATE TRIGGER insertar_moto
  AFTER INSERT
  ON public.motorizado_moto
  FOR EACH ROW
  EXECUTE PROCEDURE public.insertar_moto();
