-- FUNCTION: public.tablameses(date)

-- DROP FUNCTION public.tablameses(date);

CREATE OR REPLACE FUNCTION public.tablameses(
	f date)
RETURNS text
    LANGUAGE 'plpgsql'
    COST 100.0

AS $function$

declare
	a text[] :='{" de Enero de "," de Febrero de "," de Marzo de "," de Abril de "," de Mayo de "," de Junio de "," de Julio de "," de Agosto de "," de Septiembre de "," de Octubre de "," de Noviembre de "," de Diciembre de "}';
begin
	return (extract(day from f)||a[extract(month from f)]||extract(year from f));
end;

$function$;

ALTER FUNCTION public.tablameses(date)
    OWNER TO postgres;
