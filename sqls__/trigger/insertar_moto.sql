-- Trigger: insertar_moto

-- DROP TRIGGER insertar_moto ON public.motorizado_moto;

CREATE TRIGGER insertar_moto
    AFTER INSERT
    ON public.motorizado_moto
    FOR EACH ROW
    EXECUTE PROCEDURE insertar_moto();
