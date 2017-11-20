CREATE TRIGGER comfiguracion_tiempos_empresa
    AFTER INSERT
    ON public.usuario_empresa
    FOR EACH ROW
    EXECUTE PROCEDURE comfiguracion_tiempos_empresa();
