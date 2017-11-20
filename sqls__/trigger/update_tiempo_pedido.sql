CREATE TRIGGER update_tiempo_pedido
    AFTER UPDATE
    ON public.pedido_pedido
    FOR EACH ROW
    EXECUTE PROCEDURE update_tiempo_pedido();
