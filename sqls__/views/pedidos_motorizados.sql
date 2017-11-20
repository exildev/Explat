CREATE OR REPLACE VIEW public.pedidos_motorizados AS
 SELECT pedido.id,
    ptime.creado,
    ptime.confirmado,
    ptime.despachado,
    ptime.entregado,
    pedido.motorizado_id
   FROM pedido_pedido pedido
     JOIN pedido_time ptime ON pedido.id = ptime.pedido_id
  WHERE pedido.motorizado_id IS NOT NULL
UNION
 SELECT pedido.id,
    ptime.creado,
    ptime.confirmado,
    ptime.despachado,
    ptime.entregado,
    pedido.motorizado_id
   FROM pedido_pedidows pedido
     JOIN pedido_timews ptime ON pedido.id = ptime.pedido_id
  WHERE pedido.motorizado_id IS NOT NULL;

ALTER TABLE public.pedidos_motorizados
    OWNER TO postgres;
