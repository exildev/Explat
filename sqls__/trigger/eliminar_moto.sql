-- Trigger: eliminar_moto

-- DROP TRIGGER eliminar_moto ON public.motorizado_moto;

CREATE TRIGGER eliminar_moto
    BEFORE DELETE
    ON public.motorizado_moto
    FOR EACH ROW
    EXECUTE PROCEDURE eliminar_moto();
