-- Function: public.crear_token()

-- DROP FUNCTION public.crear_token();

CREATE OR REPLACE FUNCTION public.crear_token()
  RETURNS trigger AS
$BODY$

declare
begin
	update usuario_tienda set token= md5(case when new.nombre is not null and length(new.nombre) > 0 then new.nombre else cast(old.id as text) end) where id=new.id;
	return new;
end;

$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION public.crear_token()
  OWNER TO postgres;


  -- Trigger: crear_token on public.usuario_tienda

  -- DROP TRIGGER crear_token ON public.usuario_tienda;

  CREATE TRIGGER crear_token
    AFTER INSERT
    ON public.usuario_tienda
    FOR EACH ROW
    EXECUTE PROCEDURE public.crear_token();
