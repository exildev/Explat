CREATE FUNCTION public.crear_token()
    RETURNS trigger
    LANGUAGE 'plpgsql'
    COST 100.0
AS $BODY$

declare
begin
	update usuario_tienda set token= md5(case when new.nombre is not null and length(new.nombre) > 0 then new.nombre else cast(old.id as text) end) where id=new.id;
	return new;
end;

$BODY$;

ALTER FUNCTION public.crear_token()
    OWNER TO postgres;
