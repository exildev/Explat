CREATE TRIGGER crear_token
    AFTER INSERT
    ON public.usuario_tienda
    FOR EACH ROW
    EXECUTE PROCEDURE crear_token();
