CREATE TRIGGER crear_tiempo_pedido
    AFTER INSERT
    ON public.pedido_pedido
    FOR EACH ROW
    EXECUTE PROCEDURE crear_tiempo_pedido();
