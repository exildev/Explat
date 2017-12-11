-- View: public.pedidos_motorizados

-- DROP VIEW public.pedidos_motorizados;

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
/********************************************************************/
-- View: public.pedidos_tiempos

-- DROP VIEW public.pedidos_tiempos;

CREATE OR REPLACE VIEW public.pedidos_tiempos AS
 SELECT pf.nump,
    pf.cliente,
    pf.supervisor,
    pf.alistador,
    pf.motori,
    pf.direccion,
    pf.total,
    pf.cliente_id,
    pf.supervisor_id,
    pf.alistador_id,
    pf.motorizado_id,
    pf.empresa_id,
    pf.fecha,
    pf.alistar,
    pf.despacho,
    pf.entrega
   FROM ( SELECT p.nump,
            p.cliente,
            p.supervisor,
            p.alistador,
            p.motori,
            p.direccion,
            p.total,
            p.cliente_id,
            p.supervisor_id,
            p.alistador_id,
            p.motorizado_id,
            p.empresa_id,
            p.fecha,
                CASE
                    WHEN p.alistamiento IS NOT NULL THEN round(p.alistamiento::numeric, 2)::text
                    ELSE 'No asignado'::text
                END AS alistar,
                CASE
                    WHEN p.despacho IS NOT NULL THEN round(p.despacho::numeric, 2)::text
                    ELSE 'No asignado'::text
                END AS despacho,
                CASE
                    WHEN p.entrega IS NOT NULL THEN round(p.entrega::numeric, 2)::text
                    ELSE 'No asignado'::text
                END AS entrega
           FROM ( SELECT p_1.id,
                    p_1.num_pedido AS nump,
                    (c.first_name::text || ' '::text) || c.last_name::text AS cliente,
                    (s.first_name::text || ' '::text) || s.last_name::text AS supervisor,
                    c.direccion,
                    p_1.cliente_id,
                    p_1.alistador_id,
                    p_1.motorizado_id,
                    p_1.supervisor_id,
                    (a.first_name::text || ' '::text) || a.last_name::text AS alistador,
                    (m.first_name::text || ' '::text) || m.last_name::text AS motori,
                    p_1.empresa_id,
                    p_1.fecha_pedido AS fecha,
                        CASE
                            WHEN p_1.total IS NOT NULL THEN p_1.total
                            ELSE 0::numeric
                        END::text AS total,
                    (date_part('epoch'::text, t.confirmado) - date_part('epoch'::text, t.creado)) / 60::double precision AS alistamiento,
                    (date_part('epoch'::text, t.despachado) - date_part('epoch'::text, t.confirmado)) / 60::double precision AS despacho,
                    (date_part('epoch'::text, t.entregado) - date_part('epoch'::text, t.despachado)) / 60::double precision AS entrega
                   FROM pedido_pedido p_1
                     JOIN auth_user m ON p_1.motorizado_id = m.id
                     JOIN auth_user a ON p_1.alistador_id = a.id
                     JOIN auth_user s ON p_1.supervisor_id = s.id
                     JOIN usuario_cliente c ON p_1.cliente_id = c.id
                     JOIN pedido_time t ON p_1.id = t.pedido_id
                     JOIN pedido_time ti ON ti.pedido_id = p_1.id
                  ORDER BY p_1.fecha_pedido DESC) p) pf;

ALTER TABLE public.pedidos_tiempos
  OWNER TO postgres;
/********************************************************************/
-- View: public.pedidos_tiempos_actualizada

-- DROP VIEW public.pedidos_tiempos_actualizada;

CREATE OR REPLACE VIEW public.pedidos_tiempos_actualizada AS
 SELECT pf.nump,
    pf.cliente,
    pf.supervisor,
    pf.alistador,
    pf.motori,
    pf.direccion,
    pf.total,
    pf.cliente_id,
    pf.supervisor_id,
    pf.alistador_id,
    pf.motorizado_id,
    pf.empresa_id,
    pf.fecha,
    pf.alistar,
    pf.despacho,
    pf.entrega,
    pf.estado,
    pf.tienda,
    pf.ciudad
   FROM ( SELECT p.nump,
            p.cliente,
            p.supervisor,
            p.alistador,
            p.motori,
            p.direccion,
            p.total,
            p.cliente_id,
            p.supervisor_id,
            p.alistador_id,
            p.motorizado_id,
            p.empresa_id,
            p.fecha,
                CASE
                    WHEN p.alistamiento IS NOT NULL THEN round(p.alistamiento::numeric, 2)::text
                    ELSE 'No asignado'::text
                END AS alistar,
                CASE
                    WHEN p.despacho IS NOT NULL THEN round(p.despacho::numeric, 2)::text
                    ELSE 'No asignado'::text
                END AS despacho,
                CASE
                    WHEN p.entrega IS NOT NULL THEN round(p.entrega::numeric, 2)::text
                    ELSE 'No asignado'::text
                END AS entrega,
            p.empresa_id AS empresa,
            p.ciudad,
            p.tienda,
            p.estado
           FROM ( SELECT p_1.id,
                    p_1.num_pedido AS nump,
                    (c.first_name::text || ' '::text) || c.last_name::text AS cliente,
                    (s.first_name::text || ' '::text) || s.last_name::text AS supervisor,
                    c.direccion,
                    p_1.cliente_id,
                    p_1.alistador_id,
                    p_1.motorizado_id,
                    p_1.supervisor_id,
                    (a.first_name::text || ' '::text) || a.last_name::text AS alistador,
                    (m.first_name::text || ' '::text) || m.last_name::text AS motori,
                    p_1.empresa_id,
                    p_1.fecha_pedido AS fecha,
                        CASE
                            WHEN p_1.total IS NOT NULL THEN p_1.total
                            ELSE 0::numeric
                        END::text AS total,
                    (date_part('epoch'::text, t.confirmado) - date_part('epoch'::text, t.creado)) / 60::double precision AS alistamiento,
                    (date_part('epoch'::text, t.despachado) - date_part('epoch'::text, t.confirmado)) / 60::double precision AS despacho,
                    (date_part('epoch'::text, t.entregado) - date_part('epoch'::text, t.despachado)) / 60::double precision AS entrega,
                    p_1.tienda_id AS tienda,
                    tiend.ciudad_id AS ciudad,
                    p_1.entregado AS estado
                   FROM pedido_pedido p_1
                     JOIN auth_user m ON p_1.motorizado_id = m.id
                     JOIN auth_user a ON p_1.alistador_id = a.id
                     JOIN auth_user s ON p_1.supervisor_id = s.id
                     JOIN usuario_cliente c ON p_1.cliente_id = c.id
                     JOIN pedido_time t ON p_1.id = t.pedido_id
                     JOIN pedido_time ti ON ti.pedido_id = p_1.id
                     JOIN usuario_tienda tiend ON tiend.id = p_1.tienda_id
                UNION
                 SELECT pws.id,
                        CASE
                            WHEN pws.num_pedido IS NULL OR length(pws.num_pedido::text) = 0 THEN 'PdWs'::character varying
                            ELSE pws.num_pedido
                        END AS nump,
                    ((pws.cliente::json ->> 'nombre'::text) || ' '::text) || (pws.cliente::json ->> 'apellidos'::text) AS cliente,
                    'Super_Ws'::text AS supervisor,
                    pws.cliente::json ->> 'direccion'::text,
                    0 AS cliente_id,
                    0 AS alistador_id,
                        CASE
                            WHEN pws.motorizado_id IS NOT NULL THEN pws.motorizado_id
                            ELSE 0
                        END AS motorizado_id,
                    0 AS supervisor_id,
                    'Alistador Pws'::text AS alistador,
                    (m.first_name::text || ' '::text) || m.last_name::text AS motori,
                    tiend.empresa_id,
                    pws.fecha_pedido AS fecha,
                        CASE
                            WHEN pws.total IS NOT NULL THEN pws.total
                            ELSE 0::numeric
                        END::text AS total,
                    (date_part('epoch'::text, t.confirmado) - date_part('epoch'::text, t.creado)) / 60::double precision AS alistamiento,
                    (date_part('epoch'::text, t.despachado) - date_part('epoch'::text, t.confirmado)) / 60::double precision AS despacho,
                    (date_part('epoch'::text, t.entregado) - date_part('epoch'::text, t.despachado)) / 60::double precision AS entrega,
                    pws.tienda_id AS tienda,
                    tiend.ciudad_id AS ciudad,
                    pws.entregado AS estado
                   FROM pedido_pedidows pws
                     JOIN auth_user m ON pws.motorizado_id = m.id
                     JOIN usuario_tienda tiend ON tiend.id = pws.tienda_id
                     JOIN pedido_timews t ON pws.id = t.pedido_id) p) pf
  ORDER BY pf.fecha;

ALTER TABLE public.pedidos_tiempos_actualizada
  OWNER TO postgres;
/********************************************************************/
-- Function: public.eliminar_moto()

-- DROP FUNCTION public.eliminar_moto();

CREATE OR REPLACE FUNCTION public.eliminar_moto()
  RETURNS trigger AS
$BODY$

declare
begin
	IF (TG_OP = 'DELETE') THEN
		update motorizado_moto set estado=false where id = old.id;
	end if;
	return null;
end;

$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION public.eliminar_moto()
  OWNER TO postgres;

CREATE TRIGGER eliminar_moto
  BEFORE DELETE
  ON public.motorizado_moto
  FOR EACH ROW
  EXECUTE PROCEDURE public.eliminar_moto();
/********************************************************************/
-- Function: public.insertar_moto()

-- DROP FUNCTION public.insertar_moto();

CREATE OR REPLACE FUNCTION public.insertar_moto()
  RETURNS trigger AS
$BODY$

declare
begin
	IF (TG_OP = 'INSERT') THEN
		update motorizado_moto set estado=true where id = new.id;
	end if;
	return new;
end;

$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION public.insertar_moto()
  OWNER TO postgres;

CREATE TRIGGER insertar_moto
  AFTER INSERT
  ON public.motorizado_moto
  FOR EACH ROW
  EXECUTE PROCEDURE public.insertar_moto();
/********************************************************************/
-- Function: public.comfiguracion_tiempos_empresa()

-- DROP FUNCTION public.comfiguracion_tiempos_empresa();

CREATE OR REPLACE FUNCTION public.comfiguracion_tiempos_empresa()
  RETURNS trigger AS
$BODY$

declare
begin
	insert into pedido_configuraciontiempo (retraso,pedido,distancia,empresa_id,primero,segundo,gps) values(3,3,1000,new.id,1,15,1);
	return new;
end;

$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION public.comfiguracion_tiempos_empresa()
  OWNER TO postgres;

  -- Trigger: comfiguracion_tiempos_empresa on public.usuario_empresa

  -- DROP TRIGGER comfiguracion_tiempos_empresa ON public.usuario_empresa;

  CREATE TRIGGER comfiguracion_tiempos_empresa
    AFTER INSERT
    ON public.usuario_empresa
    FOR EACH ROW
    EXECUTE PROCEDURE public.comfiguracion_tiempos_empresa();
/********************************************************************/
-- Function: public.crear_tiempo_pedido()

-- DROP FUNCTION public.crear_tiempo_pedido();

CREATE OR REPLACE FUNCTION public.crear_tiempo_pedido()
  RETURNS trigger AS
$BODY$

declare
begin
	insert into pedido_time(pedido_id,creado) values (new.id,now());
	return new;
end;

$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION public.crear_tiempo_pedido()
  OWNER TO postgres;

  -- Trigger: crear_tiempo_pedido on public.pedido_pedido

-- DROP TRIGGER crear_tiempo_pedido ON public.pedido_pedido;

CREATE TRIGGER crear_tiempo_pedido
  AFTER INSERT
  ON public.pedido_pedido
  FOR EACH ROW
  EXECUTE PROCEDURE public.crear_tiempo_pedido();


/********************************************************************/

-- Function: public.update_tiempo_pedido()

-- DROP FUNCTION public.update_tiempo_pedido();

CREATE OR REPLACE FUNCTION public.update_tiempo_pedido()
  RETURNS trigger AS
$BODY$

declare
begin
	if new.confirmado and old.confirmado=false then
		update pedido_time set confirmado = now() where pedido_id= old.id;
	elsif new.entregado and old.entregado=false then
		update pedido_time set entregado = now() where pedido_id= old.id;
	elsif new.alistado and old.alistado=false then
		update pedido_time set alistado = now() where pedido_id= old.id;
	elsif new.despachado  and old.despachado=false then
		update pedido_time set despachado = now() where pedido_id= old.id;
	elsif new.notificado  and old.notificado=false then
		update pedido_time set notificado = now() where pedido_id= old.id;
	elsif new.activado=false then
		/*update pedido_pedido set entregado=false, despachado=false, notificado=false, reactivacion=false where id = old.id;*/
		new.entregado=false;
		new.despachado=false;
		new.notificado=false;
		new.reactivacion=false;
	elsif new.activado=true then
		/*update pedido_pedido set reactivacion=true where id = new.id;*/
		new.reactivacion=true;
	end if;
	return new;
end;

$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION public.update_tiempo_pedido()
  OWNER TO postgres;

  -- Trigger: update_tiempo_pedido on public.pedido_pedido

  -- DROP TRIGGER update_tiempo_pedido ON public.pedido_pedido;

  CREATE TRIGGER update_tiempo_pedido
    AFTER UPDATE
    ON public.pedido_pedido
    FOR EACH ROW
    EXECUTE PROCEDURE public.update_tiempo_pedido();
/********************************************************************/
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
/********************************************************************/
-- Function: public.mis_pedidos_asignados(integer, integer, integer)

-- DROP FUNCTION public.mis_pedidos_asignados(integer, integer, integer);

CREATE OR REPLACE FUNCTION public.mis_pedidos_asignados(
    id_des integer,
    start_ integer,
    length_ integer)
  RETURNS text AS
$BODY$

declare
	l json;
	t integer;
	emp_id integer;
begin
	select empresa_id from usuario_empleado where usuario_ptr_id=id_des limit 1 into emp_id;
	if emp_id is null then
		emp_id:=0;
	end if;
	select count(id) from pedido_pedido where empresa_id = emp_id into t;
	if t is null then
		t:=0;
	end if;
	SELECT COALESCE(array_to_json(array_agg(row_to_json(p))), '[]') from (
		 select distinct p.id,p.num_pedido as num,p.npedido_express as nom,tablameses(p.fecha_pedido) as fecha
		  from usuario_empleado as e
		  inner join pedido_pedido as p
		  on ((p.supervisor_id=e.usuario_ptr_id or p.alistador_id = e.usuario_ptr_id) and e.usuario_ptr_id=id_des and e.empresa_id=emp_id) order by p.id desc  limit length_ offset start_
	) p into l ;
	return '{"recordsFiltered": '|| t ||', "recordsTotal": '|| json_array_length(l) ||', "data": '|| l||'}';

end;

$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION public.mis_pedidos_asignados(integer, integer, integer)
  OWNER TO postgres;

/********************************************************************/
-- Function: public.pedidos_a_asignar_motor(integer, integer, integer)

-- DROP FUNCTION public.pedidos_a_asignar_motor(integer, integer, integer);

CREATE OR REPLACE FUNCTION public.pedidos_a_asignar_motor(
    id_des integer,
    start_ integer,
    length_ integer)
  RETURNS text AS
$BODY$

declare
	l json;
	t integer;
begin
	select count(id) from pedido_pedido where empresa_id = (select empresa_id from usuario_empleado where usuario_ptr_id=id_des limit 1) into t;
	if t is null then
		t:=0;
	end if;
	SELECT COALESCE(array_to_json(array_agg(row_to_json(p))), '[]') from (
		 select p.num_pedido as num,upper(u.first_name)||' '||upper(u.last_name) as nom,tablameses(p.fecha_pedido) as fecha,p.id
			from pedido_pedido as p inner join auth_user  as u on (p.alistador_id=id_des and p.supervisor_id=u.id and p.motorizado_id is null)
	) p into l ;
	return '{"recordsFiltered": '|| t ||', "recordsTotal": '|| json_array_length(l) ||', "data": '|| l||'}';

end;

$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION public.pedidos_a_asignar_motor(integer, integer, integer)
  OWNER TO postgres;

/********************************************************************/
-- Function: public.reactivar_pedido(integer)

-- DROP FUNCTION public.reactivar_pedido(integer);

CREATE OR REPLACE FUNCTION public.reactivar_pedido(id_ped integer)
  RETURNS json AS
$BODY$

declare
	pedido record;
	id_pedido integer;
	nom_pedido text;
	v_nom text[];
	motorizado_identifier text;
begin
	select * from pedido_pedido where id = id_ped limit 1 into pedido;
	select num_pedido from pedido_pedido as p  order by p.id desc limit 1 into nom_pedido;
	if pedido.id is not null then
		update pedido_pedido set reactivacion=true where id = id_ped;
		select identifier from motorizado_motorizado where empleado_id = pedido.motorizado_id limit 1 into motorizado_identifier;
		if motorizado_identifier is not null then
			select string_to_array(nom_pedido, '_') into v_nom;
			nom_pedido:=v_nom[1]||'_'||cast(v_nom[2] as numeric)+1;
			insert into pedido_pedido
			   (num_pedido,npedido_express,fecha_pedido,tipo_pago,total,entregado,despachado,confirmado,alistado,alistador_id,cliente_id,empresa_id,motorizado_id,supervisor_id,tienda_id,notificado,activado,reactivacion)
			   values
			   (nom_pedido,nom_pedido,now(),pedido.tipo_pago,pedido.total,false,false,false,false,pedido.alistador_id,pedido.cliente_id,pedido.empresa_id,pedido.motorizado_id,pedido.supervisor_id,pedido.tienda_id,false,true,false) returning id into id_pedido;
			   insert into pedido_itemspedido (cantidad,valor_unitario,valor_total,item_id,pedido_id) select cantidad,valor_unitario,valor_total,item_id,id_pedido from pedido_itemspedido where pedido_id=id_ped;

			   return (array_to_json(array_agg(row_to_json(row(id_pedido,motorizado_identifier,get_add_pedido_admin(id_pedido))))));
		end if;
	end if;
	return get_add_pedido_admin(id_pedido);

end;

$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION public.reactivar_pedido(integer)
  OWNER TO postgres;

/********************************************************************/
-- Function: public.reporte_pedidos(integer, text, text, integer, integer)

-- DROP FUNCTION public.reporte_pedidos(integer, text, text, integer, integer);

CREATE OR REPLACE FUNCTION public.reporte_pedidos(
    id_des integer,
    search_ text,
    order_ text,
    start_ integer,
    length_ integer)
  RETURNS text AS
$BODY$

declare
	l json;
	t integer :=0;
	id_emp integer;
begin
	select empresa_id from usuario_empleado where usuario_ptr_id = id_des limit 1 into id_emp;
	if id_emp is null then
		id_emp:=0;
	end if;
	select count(empresa_id) from pedido_pedido where empresa_id = id_emp  into t;
	SELECT COALESCE(array_to_json(array_agg(row_to_json(p))), '[]') from (

		select * from (
				select nump,express,cliente,supervisor,alistador,motori,total,
				case when alistamiento is not null then round(alistamiento::numeric,2)::text else 'No asignado' end::text as alistar,
				case when despacho is not null then round(despacho::numeric,2)::text else 'No asignado' end::text as despacho ,
				case when entrega is not null then round(entrega::numeric,2)::text else 'No asignado' end::text as entrega
				from (
					select p.id,p.num_pedido as nump,p.npedido_express as express,c.first_name||' '||c.last_name as cliente,s.first_name||' '||s.last_name as supervisor,
					       a.first_name||' '||a.last_name as alistador,m.first_name||' '||m.last_name as motori,
					       case when p.total is not null then p.total else 0 end::text as total,
					       (EXTRACT(EPOCH from t.confirmado)-EXTRACT(EPOCH from t.creado)) /60 as alistamiento,
					       (EXTRACT(EPOCH from t.despachado)-EXTRACT(EPOCH from t.confirmado)) /60 as despacho,
					       (EXTRACT(EPOCH from t.entregado)-EXTRACT(EPOCH from t.despachado)) /60 as entrega
							from pedido_pedido as p inner join auth_user as m on(p.motorizado_id=m.id)
							inner join auth_user as a on (p.alistador_id=a.id) inner join auth_user as s on (p.supervisor_id=s.id)
							inner join usuario_cliente as c on (p.cliente_id=c.id) inner join pedido_time as t on (p.id=t.pedido_id)
							inner join pedido_time as ti on(ti.pedido_id=p.id) where p.empresa_id=id_emp order by p.fecha_pedido desc) as p
				    ) as pf where pf.nump like '%'||search_||'%' or pf.cliente like '%'||search_||'%' or pf.supervisor like '%'||search_||'%' or pf.alistador like '%'||search_||'%'  or pf.motori like '%'||search_||'%' limit length_ offset start_
	) p into l;
	return '{"recordsFiltered": '|| t ||', "recordsTotal": '|| json_array_length(l) ||', "data": '|| l||'}';
end;

$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION public.reporte_pedidos(integer, text, text, integer, integer)
  OWNER TO postgres;

/********************************************************************/
-- Function: public.reporte_tiempos_empleados(integer, text, text, integer, integer, integer)

-- DROP FUNCTION public.reporte_tiempos_empleados(integer, text, text, integer, integer, integer);

CREATE OR REPLACE FUNCTION public.reporte_tiempos_empleados(
    id_des integer,
    search_ text,
    order_ text,
    start_ integer,
    length_ integer,
    id_user_sec integer)
  RETURNS text AS
$BODY$

declare
	l json;
	t integer :=0;
	id_emp integer;
	typo integer ;
begin
	select empresa_id from usuario_empleado where usuario_ptr_id = id_des limit 1 into id_emp;
	if id_emp is null then
		id_emp:=0;
	end if;
	select case when cargo='ADMINISTRADOR' then 1 when cargo='SUPERVISOR' then 2 when cargo='ALISTADOR' then 3 else 4 end as peso
	from usuario_empleado where usuario_ptr_id=id_des limit 1 into typo;
	if typo is null then
		typo=0;
		id_des:=0;
	end if;

	if typo=1 then
		SELECT COALESCE(array_to_json(array_agg(row_to_json(p))), '[]') from (
			select nump,cliente,supervisor,alistador,motori,alistar,despacho,entrega from pedidos_tiempos where empresa_id=id_emp order by fecha desc
			limit length_ offset start_
		) p into l;
	elsif typo=2 then
		SELECT COALESCE(array_to_json(array_agg(row_to_json(p))), '[]') from (
			select nump,cliente,supervisor,alistador,motori,alistar,despacho,entrega from pedidos_tiempos where supervisor_id=id_des and  empresa_id=id_emp  order by fecha desc
			limit length_ offset start_
		) p into l;
	elsif typo=3 then
		SELECT COALESCE(array_to_json(array_agg(row_to_json(p))), '[]') from (
			select nump,cliente,supervisor,alistador,motori,alistar,despacho,entrega from pedidos_tiempos where alistador_id=id_des and  empresa_id=id_emp   order by fecha desc
			limit length_ offset start_
		) p into l;
	else
		SELECT COALESCE(array_to_json(array_agg(row_to_json(p))), '[]') from (
			select nump,cliente,supervisor,alistador,motori,alistar,despacho,entrega from pedidos_tiempos where motorizado_id=id_des and  empresa_id=id_emp   order by fecha desc
			limit length_ offset start_
		) p into l;
	end if;
	select count(empresa_id) from pedido_pedido where empresa_id = id_emp  into t;
	return '{"recordsFiltered": '|| t ||', "recordsTotal": '|| json_array_length(l) ||', "data": '|| l||'}';
end;

$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION public.reporte_tiempos_empleados(integer, text, text, integer, integer, integer)
  OWNER TO postgres;

/********************************************************************/
-- Function: public.tabla_cliente(integer, text, integer, integer, integer)

-- DROP FUNCTION public.tabla_cliente(integer, text, integer, integer, integer);

CREATE OR REPLACE FUNCTION public.tabla_cliente(
    id_des integer,
    search_ text,
    order_ integer,
    start_ integer,
    length_ integer)
  RETURNS text AS
$BODY$

declare
	l json;
	t integer;
	id_emp integer;
begin
	select empresa_id from usuario_empleado where usuario_ptr_id=id_des limit 1 into id_emp;
	raise notice ' % ',id_emp;
	if id_emp is null then
		id_emp:=0;
	end if;
	select count(id) from usuario_cliente where empresa_id=id_emp into t;
	raise notice ' % ',id_emp;
	SELECT COALESCE(array_to_json(array_agg(row_to_json(p))), '[]') from (
		 select first_name as nom,last_name as ape,identificacion as id,id as id2 from usuario_cliente where empresa_id=id_emp and
		 (first_name like '%'||search_||'%' or last_name like '%'||search_||'%' or identificacion like '%'||search_||'%') limit length_ offset start_
	) p into l;
	return '{"recordsFiltered": '|| t ||', "recordsTotal": '|| json_array_length(l) ||', "data": '|| l||'}';
end;

$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION public.tabla_cliente(integer, text, integer, integer, integer)
  OWNER TO postgres;

/********************************************************************/
-- Function: public.tabla_empleado(integer, text, text, integer, integer)

-- DROP FUNCTION public.tabla_empleado(integer, text, text, integer, integer);

CREATE OR REPLACE FUNCTION public.tabla_empleado(
    id_des integer,
    search_ text,
    order_ text,
    start_ integer,
    length_ integer)
  RETURNS text AS
$BODY$

declare
	l json;
	t integer :=0;
	id_emp integer;
begin
	select empresa_id from usuario_empleado where usuario_ptr_id = id_des limit 1 into id_emp;
	if id_emp is null then
		id_emp:=0;
	end if;
	select count(usuario_ptr_id) from usuario_empleado where empresa_id=id_emp into t;
	SELECT COALESCE(array_to_json(array_agg(row_to_json(p))), '[]') from (
		  select user_.first_name as nom,user_.last_name as ape,u.identificacion as ced,e.cargo,emp.first_name,
		  case when user_.is_active then 'Activo' else 'Desactivado'end as estado,e.usuario_ptr_id  from usuario_empleado as e
		  inner join usuario_usuario as u on (e.usuario_ptr_id=u.user_ptr_id and e.empresa_id=id_emp)
		  inner join auth_user as user_ on(u.user_ptr_id=user_.id) inner join usuario_empresa as emp on (e.empresa_id=emp.id and emp.id=empresa_id) where
		  user_.first_name like '%'||search_||'%' or user_.last_name  like '%'||search_||'%' or u.identificacion like '%'||search_||'%' or e.cargo like '%'||search_||'%' or emp.first_name like '%'||search_||'%' limit length_ offset start_
	) p into l;
	return '{"recordsFiltered": '|| t ||', "recordsTotal": '|| json_array_length(l) ||', "data": '|| l||'}';
end;

$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION public.tabla_empleado(integer, text, text, integer, integer)
  OWNER TO postgres;

/********************************************************************/
-- Function: public.tabla_empleado(integer, text, text, integer, integer)

-- DROP FUNCTION public.tabla_empleado(integer, text, text, integer, integer);

CREATE OR REPLACE FUNCTION public.tabla_empleado(
    id_des integer,
    search_ text,
    order_ text,
    start_ integer,
    length_ integer)
  RETURNS text AS
$BODY$

declare
	l json;
	t integer :=0;
	id_emp integer;
begin
	select empresa_id from usuario_empleado where usuario_ptr_id = id_des limit 1 into id_emp;
	if id_emp is null then
		id_emp:=0;
	end if;
	select count(usuario_ptr_id) from usuario_empleado where empresa_id=id_emp into t;
	SELECT COALESCE(array_to_json(array_agg(row_to_json(p))), '[]') from (
		  select user_.first_name as nom,user_.last_name as ape,u.identificacion as ced,e.cargo,emp.first_name,
		  case when user_.is_active then 'Activo' else 'Desactivado'end as estado,e.usuario_ptr_id  from usuario_empleado as e
		  inner join usuario_usuario as u on (e.usuario_ptr_id=u.user_ptr_id and e.empresa_id=id_emp)
		  inner join auth_user as user_ on(u.user_ptr_id=user_.id) inner join usuario_empresa as emp on (e.empresa_id=emp.id and emp.id=empresa_id) where
		  user_.first_name like '%'||search_||'%' or user_.last_name  like '%'||search_||'%' or u.identificacion like '%'||search_||'%' or e.cargo like '%'||search_||'%' or emp.first_name like '%'||search_||'%' limit length_ offset start_
	) p into l;
	return '{"recordsFiltered": '|| t ||', "recordsTotal": '|| json_array_length(l) ||', "data": '|| l||'}';
end;

$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION public.tabla_empleado(integer, text, text, integer, integer)
  OWNER TO postgres;

/********************************************************************/
-- Function: public.tabla_info_empleado(integer, text, text, integer, integer, text, text)

-- DROP FUNCTION public.tabla_info_empleado(integer, text, text, integer, integer, text, text);

CREATE OR REPLACE FUNCTION public.tabla_info_empleado(
    id_des integer,
    search_ text,
    order_ text,
    start_ integer,
    length_ integer,
    id_ciudad text,
    tipo_empleado text)
  RETURNS text AS
$BODY$

declare
	l json;
	t integer;
	id_emp integer :=0;
	tipo_emp text[] :='{"ADMINISTRADOR","SUPERVISOR","ALISTADOR","MOTORIZADO"}';
begin
	select empresa_id from usuario_empleado where usuario_ptr_id = id_des limit 1 into id_emp;
	if id_emp is null then
		id_emp=0;
	end if;
	if length(tipo_empleado) > 0 then
	     tipo_emp:='{"'||tipo_empleado||'"}';
	end if;
	select count(usuario_ptr_id) from usuario_empleado where empresa_id=id_emp into t;
	if length(id_ciudad) > 0 then
		SELECT COALESCE(array_to_json(array_agg(row_to_json(p))), '[]') from (
			select e.cargo,u.first_name||' '||u.last_name as nom, e.usuario_ptr_id as id
			from usuario_empleado as e
			inner join auth_user as u on (e.usuario_ptr_id=u.id and u.is_active and e.empresa_id=id_emp and e.ciudad=id_ciudad )
				  where e.cargo = any(tipo_emp::text[])  limit length_ offset start_
		) p into l;
	else
		SELECT COALESCE(array_to_json(array_agg(row_to_json(p))), '[]') from (
			select e.cargo,u.first_name||' '||u.last_name as nom, e.usuario_ptr_id as id
			from usuario_empleado as e
			inner join auth_user as u on (e.usuario_ptr_id=u.id and u.is_active and e.empresa_id=id_emp)
				  where e.cargo = any(tipo_emp::text[]) limit length_ offset start_
		) p into l;
	end if;
	return '{"recordsFiltered": '|| t ||', "recordsTotal": '|| json_array_length(l) ||', "data": '|| l||'}';
end;

$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION public.tabla_info_empleado(integer, text, text, integer, integer, text, text)
  OWNER TO postgres;

/********************************************************************/
-- Function: public.tabla_info_empleado_actualizado(integer, text, text, integer, integer, text, text, integer)

-- DROP FUNCTION public.tabla_info_empleado_actualizado(integer, text, text, integer, integer, text, text, integer);

CREATE OR REPLACE FUNCTION public.tabla_info_empleado_actualizado(
    id_des integer,
    search_ text,
    order_ text,
    start_ integer,
    length_ integer,
    id_ciudad text,
    tipo_empleado text,
    id_tienda integer)
  RETURNS text AS
$BODY$

declare
	l json;
	t integer;
	id_emp integer :=0;
	tipo_emp text[] :='{"ADMINISTRADOR","SUPERVISOR","ALISTADOR","MOTORIZADO"}';
begin
	select empresa_id from usuario_empleado where usuario_ptr_id = id_des limit 1 into id_emp;
	if id_emp is null then
		id_emp=0;
	end if;
	if length(tipo_empleado) > 0 then
	     tipo_emp:='{"'||tipo_empleado||'"}';
	end if;
	select count(usuario_ptr_id) from usuario_empleado where empresa_id=id_emp into t;
	if length(id_ciudad) > 0 then
		SELECT COALESCE(array_to_json(array_agg(row_to_json(p))), '[]') from (
			select e.cargo,u.first_name||' '||u.last_name as nom, e.usuario_ptr_id as id
			from usuario_empleado as e
			inner join auth_user as u on (e.usuario_ptr_id=u.id and u.is_active and e.empresa_id=id_emp and e.ciudad_id=cast(id_ciudad as integer)
				and (e.tienda_id in (select id from usuario_tienda as tien where tien.empresa_id=case when id_tienda = 0 then id_emp else id_tienda end) or e.tienda_id=case when id_tienda!=0 then id_tienda else 0 end ))
				  where e.cargo = any(tipo_emp::text[])  limit length_ offset start_
		) p into l;
	else
		SELECT COALESCE(array_to_json(array_agg(row_to_json(p))), '[]') from (
			select e.cargo,u.first_name||' '||u.last_name as nom, e.usuario_ptr_id as id
			from usuario_empleado as e
			inner join auth_user as u on (e.usuario_ptr_id=u.id and u.is_active and e.empresa_id=id_emp
				and (e.tienda_id in (select id from usuario_tienda as tien where tien.empresa_id=case when id_tienda = 0 then id_emp else id_tienda end) or e.tienda_id=case when id_tienda!=0 then id_tienda else 0 end ) )
				  where e.cargo = any(tipo_emp::text[]) limit length_ offset start_
		) p into l;
	end if;
	return '{"recordsFiltered": '|| t ||', "recordsTotal": '|| json_array_length(l) ||', "data": '|| l||'}';
end;

$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION public.tabla_info_empleado_actualizado(integer, text, text, integer, integer, text, text, integer)
  OWNER TO postgres;
/********************************************************************/
-- Function: public.tabla_items(integer, text, text, integer, integer)

-- DROP FUNCTION public.tabla_items(integer, text, text, integer, integer);

CREATE OR REPLACE FUNCTION public.tabla_items(
    id_des integer,
    search_ text,
    order_ text,
    start_ integer,
    length_ integer)
  RETURNS text AS
$BODY$

declare
	l json;
	t integer;
	id_emp integer :=0;
begin
	select empresa_id from usuario_empleado where usuario_ptr_id = id_des limit 1 into id_emp;
	if id_emp is null then
		id_emp=0;
	end if;
	select count(id) from pedido_items where "empresaI_id"=id_emp and status=true into t;
	SELECT COALESCE(array_to_json(array_agg(row_to_json(p))), '[]') from (
		 select codigo,initcap(descripcion) as descripcion,initcap(presentacion) as presentacion,id from pedido_items where "empresaI_id"=id_emp and status=true  and
		 (codigo like '%'||search_||'%' or descripcion like '%'||search_||'%' or presentacion like '%'||search_||'%') limit length_ offset start_
	) p into l;
	return '{"recordsFiltered": '|| t ||', "recordsTotal": '|| t ||', "data": '|| l||'}';
end;

$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION public.tabla_items(integer, text, text, integer, integer)
  OWNER TO postgres;

/********************************************************************/
-- Function: public.tabla_moto(integer, text, text, integer, integer)

-- DROP FUNCTION public.tabla_moto(integer, text, text, integer, integer);

CREATE OR REPLACE FUNCTION public.tabla_moto(
    id_des integer,
    search_ text,
    order_ text,
    start_ integer,
    length_ integer)
  RETURNS text AS
$BODY$

declare
	l json;
	t integer;
	id_emp integer;
begin
	select count(id) from motorizado_moto where estado=true into t;
	select empresa_id from usuario_empleado where usuario_ptr_id = id_des limit 1 into id_emp;
	if id_emp is null then
		id_emp:=0;
	end if;
	SELECT COALESCE(array_to_json(array_agg(row_to_json(p))), '[]') from (
		  select m.placa,m.tipo,m.marca,m.t_propiedad,s."numeroS",t."numeroT",m.id from motorizado_moto as m inner join motorizado_soat as s on (m.soat_id=s.id and m.estado=true and m."empresaM_id"=id_emp) inner join motorizado_tecno as t on(t.id=m.tecno_id) where
		  m.placa like '%'||search_||'%' or m.tipo like '%'||search_||'%' or m.marca like '%'||search_||'%' or m.t_propiedad like '%'||search_||'%' or t."numeroT" like '%'||search_||'%' or s."numeroS" like '%'||search_||'%' limit length_ offset start_
	) p into l;
	return '{"recordsFiltered": '|| t ||', "recordsTotal": '|| json_array_length(l) ||', "data": '|| l||'}';
end;

$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION public.tabla_moto(integer, text, text, integer, integer)
  OWNER TO postgres;

/********************************************************************/
-- Function: public.tabla_motorizado(integer, text, text, integer, integer)

-- DROP FUNCTION public.tabla_motorizado(integer, text, text, integer, integer);

CREATE OR REPLACE FUNCTION public.tabla_motorizado(
    id_des integer,
    search_ text,
    order_ text,
    start_ integer,
    length_ integer)
  RETURNS text AS
$BODY$

declare
	l json;
	t integer :=0;
	id_emp integer;
begin
	select empresa_id from usuario_empleado where usuario_ptr_id = id_des limit 1 into id_emp;
	if id_emp is null then
		id_emp:=0;
	end if;
	select count(usuario_ptr_id) from usuario_empleado where empresa_id=id_emp into t;
	if length(search_) = 0 then
		SELECT COALESCE(array_to_json(array_agg(row_to_json(p))), '[]') from (
			select u.tipo_id||'-'||u.identificacion as ident,a.first_name as nom,a.last_name as ape,m.placa,mz.identifier as gps,m.id as id_mot,mz.id as id_emp from motorizado_motorizado as mz
			inner join usuario_empleado as e on(mz.empleado_id=e.usuario_ptr_id and e.empresa_id=id_emp)
			inner join motorizado_moto as m on (mz.moto_id=m.id and m.estado=true)
			inner join auth_user as a on (a.id=e.usuario_ptr_id)
			inner join usuario_usuario as u on (u.user_ptr_id = e.usuario_ptr_id)
		) p into l;
	else
		SELECT COALESCE(array_to_json(array_agg(row_to_json(p))), '[]') from (
			select u.tipo_id||'-'||u.identificacion as ident,a.first_name as nom,a.last_name as ape,m.placa,mz.identifier as gps,m.id as id_mot,mz.id as id_emp from motorizado_motorizado as mz
			inner join usuario_empleado as e on(mz.empleado_id=e.usuario_ptr_id and e.empresa_id=id_emp)
			inner join motorizado_moto as m on (mz.moto_id=m.id)
			inner join auth_user as a on (a.id=e.usuario_ptr_id)
			inner join usuario_usuario as u on (u.user_ptr_id = e.usuario_ptr_id) where
			u.identificacion like '%'||search_||'%' or a.first_name like '%'||search_||'%' or a.last_name like '%'||search_||'%' or m.placa like '%'||search_||'%' or mz.identifier like '%'||search_||'%' limit length_ offset start_
		) p into l;
	end if;
	return '{"recordsFiltered": '|| t ||', "recordsTotal": '|| json_array_length(l) ||', "data": '|| l||'}';
end;

$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION public.tabla_motorizado(integer, text, text, integer, integer)
  OWNER TO postgres;
/********************************************************************/
-- Function: public.tabla_pedidos(integer, text, text, integer, integer)

-- DROP FUNCTION public.tabla_pedidos(integer, text, text, integer, integer);

CREATE OR REPLACE FUNCTION public.tabla_pedidos(
    id_des integer,
    search_ text,
    order_ text,
    start_ integer,
    length_ integer)
  RETURNS text AS
$BODY$

declare
	l json;
	t integer :=0;
	id_emp integer;
begin
	select empresa_id from usuario_empleado where usuario_ptr_id = id_des limit 1 into id_emp;
	if id_emp is null then
		id_emp:=0;
	end if;
	select count(empresa_id) from pedido_pedido where empresa_id = id_emp  into t;
	SELECT COALESCE(array_to_json(array_agg(row_to_json(p))), '[]') from (
		select * from (select case when p.activado then 1 else 0 end as activado,p.num_pedido as num,emp.first_name as emp,a3.first_name||' '||a3.last_name as sup,u1.first_name||' '||u1.last_name as alis,
		u2.first_name||' '||u2.last_name as moto,case when p.total is not null then to_char(p.total,'LFM9999999999,999D9999999999999') else to_char(0,'LFM9999999999,999D9999999999999') end as total,
		case when p.entregado then 1 else 0 end as estado,p.id,case when p.reactivacion then 1 else 0 end as activacion from pedido_pedido as p
		inner join usuario_empleado as e1 on (p.alistador_id=e1.usuario_ptr_id and p.empresa_id=id_emp)
		inner join usuario_empleado as e2 on (p.motorizado_id=e2.usuario_ptr_id) inner join auth_user as u1 on (e1.usuario_ptr_id=u1.id)
		inner join auth_user as u2 on (e2.usuario_ptr_id=u2.id)
		inner join usuario_empresa as emp on (p.empresa_id=emp.id) inner join auth_user as a3 on (p.supervisor_id=a3.id) where
		p.num_pedido like '%'||search_||'%' or emp.first_name like '%'||search_||'%' or a3.first_name like '%'||search_||'%' or a3.last_name like '%'||search_||'%' or u1.first_name like '%'||search_||'%'
		or u1.last_name like '%'||search_||'%' or u2.first_name like '%'||search_||'%' or u2.last_name like '%'||search_||'%'  order by p.fecha_pedido desc limit length_ offset start_) as qwr order by qwr.id desc
	) p into l;
	return '{"recordsFiltered": '|| t ||', "recordsTotal": '|| json_array_length(l) ||', "data": '|| l||'}';
end;

$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION public.tabla_pedidos(integer, text, text, integer, integer)
  OWNER TO postgres;

/********************************************************************/
-- Function: public.tabla_pedidos_cancelados(integer, text, integer, integer)

-- DROP FUNCTION public.tabla_pedidos_cancelados(integer, text, integer, integer);

CREATE OR REPLACE FUNCTION public.tabla_pedidos_cancelados(
    id_user integer,
    search_ text,
    start_ integer,
    length_ integer)
  RETURNS text AS
$BODY$

  declare
    l json;
    t integer :=0;
  begin
      select count(p.id) from (select * from public.usuario_empleado where usuario_ptr_id=id_user limit 1) as emp
                         inner join public.pedido_pedido as p on (activado=false and reactivacion=false and emp.tienda_id=p.tienda_id) into t;
      SELECT COALESCE(array_to_json(array_agg(row_to_json(p))), '[]') from (
              select u.first_name||' '||u.last_name as motorizado,p.num_pedido as num ,tablameses(p.fecha_pedido) as fecha,t.nombre,p.id from (select * from public.usuario_empleado where usuario_ptr_id=id_user limit 1)
                  as emp inner join public.pedido_pedido as p on (activado=false and reactivacion=false and emp.tienda_id=p.tienda_id)
                  inner join auth_user as u on (u.id=p.motorizado_id)
                  inner join public.usuario_tienda as t on (p.tienda_id=t.id) where p.num_pedido like '%'||upper(search_)||'%' or upper(t.nombre) like '%'||upper(search_)||'%'
                  limit length_ offset start_
      ) p into l;
      return '{"recordsFiltered": '|| case when t is null then 0 else t end ||', "recordsTotal": '|| json_array_length(l) ||', "data": '|| l||'}';
  end;

$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION public.tabla_pedidos_cancelados(integer, text, integer, integer)
  OWNER TO postgres;

/********************************************************************/
-- Function: public.tabla_pedidos_despacho(integer, text, text, integer, integer)

-- DROP FUNCTION public.tabla_pedidos_despacho(integer, text, text, integer, integer);

CREATE OR REPLACE FUNCTION public.tabla_pedidos_despacho(
    id_des integer,
    search_ text,
    order_ text,
    start_ integer,
    length_ integer)
  RETURNS text AS
$BODY$

declare
	l json;
	t integer :=0;
	id_emp integer;
begin
	select empresa_id from usuario_empleado where usuario_ptr_id = id_des limit 1 into id_emp;
	if id_emp is null then
		id_emp:=0;
	end if;
	select count(empresa_id) from pedido_pedido where empresa_id = id_emp  into t;
	SELECT COALESCE(array_to_json(array_agg(row_to_json(p))), '[]') from (
		select p.num_pedido as num,emp.first_name as emp,a3.first_name||' '||a3.last_name as sup,u1.first_name||' '||u1.last_name as alis,
		u2.first_name||' '||u2.last_name as moto,case when p.total is not null then to_char(p.total,'$999,999,999.9') else to_char(0,'$999,999,999.9') end as total,
		case when p.despachado then 1 else 0 end as estado,case when p.entregado then 1 else 0 end as entregado,p.id from pedido_pedido as p
		inner join usuario_empleado as e1 on (p.alistador_id=e1.usuario_ptr_id and p.empresa_id=id_emp)
		inner join usuario_empleado as e2 on (p.motorizado_id=e2.usuario_ptr_id) inner join auth_user as u1 on (e1.usuario_ptr_id=u1.id)
		inner join auth_user as u2 on (e2.usuario_ptr_id=u2.id)
		inner join usuario_empresa as emp on (p.empresa_id=emp.id) inner join auth_user as a3 on (p.supervisor_id=a3.id) where
		emp.first_name like '%'||search_||'%' or a3.first_name like '%'||search_||'%' or a3.last_name like '%'||search_||'%' or u1.first_name like '%'||search_||'%'
		or u1.last_name like '%'||search_||'%' or u2.first_name like '%'||search_||'%' or u2.last_name like '%'||search_||'%'  limit length_ offset start_
	) p into l;
	return '{"recordsFiltered": '|| t ||', "recordsTotal": '|| json_array_length(l) ||', "data": '|| l||'}';
end;

$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION public.tabla_pedidos_despacho(integer, text, text, integer, integer)
  OWNER TO postgres;
/********************************************************************/
-- Function: public.tabla_pedidos_motorizado(integer, text, text, integer, integer)

-- DROP FUNCTION public.tabla_pedidos_motorizado(integer, text, text, integer, integer);

CREATE OR REPLACE FUNCTION public.tabla_pedidos_motorizado(
    id_des integer,
    search_ text,
    order_ text,
    start_ integer,
    length_ integer)
  RETURNS text AS
$BODY$

declare
l json;
t integer :=0;
id_emp integer;
begin
select empresa_id from usuario_empleado where usuario_ptr_id = id_des limit 1 into id_emp;
if id_emp is null then
  id_emp:=0;
end if;
select count(empresa_id) from pedido_pedido where motorizado_id = id_des  into t;
SELECT COALESCE(array_to_json(array_agg(row_to_json(p))), '[]') from (
  select num_pedido as num,npedido_express as exp,tablameses(fecha_pedido) as fecha, id,case when entregado then 1 else 0 end as foto,case when entregado then 1 else 0 end as entra
  from pedido_pedido where motorizado_id=id_des and (num_pedido like '%'||search_||'%' or npedido_express like '%'||search_||'%') order by fecha_pedido desc,entregado limit length_ offset start_
) p into l;
return '{"recordsFiltered": '|| t ||', "recordsTotal": '|| json_array_length(l) ||', "data": '|| l||'}';
end;

$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION public.tabla_pedidos_motorizado(integer, text, text, integer, integer)
  OWNER TO postgres;

/********************************************************************/
-- Function: public.tabla_tienda(integer, text, integer, integer)

-- DROP FUNCTION public.tabla_tienda(integer, text, integer, integer);

CREATE OR REPLACE FUNCTION public.tabla_tienda(
    id_user integer,
    search_ text,
    start_ integer,
    length_ integer)
  RETURNS text AS
$BODY$

declare
	l json;
	t integer;
	id_emp integer;
begin
	select empresa_id from usuario_empleado where usuario_ptr_id = id_user limit 1 into id_emp;
	if id_emp is null then
		id_emp:=0;
	end if;
	select count(id) from usuario_tienda where status=true and empresa_id = id_emp into t;
	SELECT COALESCE(array_to_json(array_agg(row_to_json(p))), '[]') from (
		  select t.nit,c.nombre as ciudad,t.nombre,t.direccion,case when t.fijo is not null and length(t.fijo) <> 0 then t.fijo else 'No Registrado' end as fijo,case when t.celular is not null and length(t.celular) <> 0 then t.celular else 'No Registrado' end as celular,t.id
			from usuario_tienda as t inner join usuario_ciudad as c on(t.ciudad_id = c.id and c.status=true and t.status =true and t.empresa_id=id_emp)where
		  t.nit like '%'||search_||'%' or c.nombre like '%'||search_||'%' or t.nombre like '%'||search_||'%' or t.direccion like '%'||search_||'%' or t.fijo like '%'||search_||'%' or t.celular like '%'||search_||'%' limit length_ offset start_
	) p into l;
	return '{"recordsFiltered": '|| t ||', "recordsTotal": '|| json_array_length(l) ||', "data": '|| l||'}';
end;

$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION public.tabla_tienda(integer, text, integer, integer)
  OWNER TO postgres;

/********************************************************************/
-- Function: public.tablameses(date)

-- DROP FUNCTION public.tablameses(date);

CREATE OR REPLACE FUNCTION public.tablameses(f date)
  RETURNS text AS
$BODY$

declare
	a text[] :='{" de Enero de "," de Febrero de "," de Marzo de "," de Abril de "," de Mayo de "," de Junio de "," de Julio de "," de Agosto de "," de Septiembre de "," de Octubre de "," de Noviembre de "," de Diciembre de "}';
begin
	return (extract(day from f)||a[extract(month from f)]||extract(year from f));
end;

$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION public.tablameses(date)
  OWNER TO postgres;
/********************************************************************/
-- Function: public.ws_add_pedido_service(json)

-- DROP FUNCTION public.ws_add_pedido_service(json);

CREATE OR REPLACE FUNCTION public.ws_add_pedido_service(_json json)
  RETURNS text AS
$BODY$

declare
	x record;
	y record;
	tem json;
	t text;
	id_emp text;
	ot text;
	id_inser integer;
	error text:='';
	stop boolean :=true;
	val_item boolean;
	id_pedido integer;
	cont_pedido text:='';
	ban_pedido boolean :=true;
	l json;
	ban_val_ind_emp boolean;
	tiempo_pedido numeric;
	tienda record;
	configuracion record;
	gen_nom_ped text;
	gen_nom_emp text;
	get_nom_arra text[];
begin
		for x in select * from json_array_elements(_json::json->'pedido') loop
			id_emp :=cast(x."value"::json->>'tienda' as json)->>'identificador'::text;
			select id::text,ciudad_id from usuario_tienda where id = case when id_emp ~ '^[0-9]+$' then cast(id_emp as integer) else 0 end limit 1 into tienda;
			if tienda is not null then
				val_item:=true;
				<<uno>>
				for y in select nombre,case when cantidad~'^([0-9]+[.])?[0-9]+' then true else false end as cantidad,case when valor~'^([0-9]+[.])?[0-9]+' then true else false end as valor from json_populate_recordset(null::ws_descripcion,cast(x."value"::json->>'descripcion' as json)) loop
					if not y.cantidad or not y.valor then
						val_item:=false;
						exit uno;
					end if;
				end loop;
				if val_item then
					/*+++ Generar el nombre del pedido ws */
					select num_pedido from pedido_pedidows where tienda_id= cast(tienda.id as integer) order by id desc limit 1 into gen_nom_ped;
					gen_nom_ped:= case when gen_nom_ped is null then null when length(gen_nom_ped)=0 then null else gen_nom_ped end;
					if gen_nom_ped is not null then
						select num_pedido from pedido_pedidows order by id desc limit 1 into gen_nom_ped;
						get_nom_arra:=string_to_array(gen_nom_ped,'_');
						gen_nom_emp:=get_nom_arra[1]||'_'||(cast(get_nom_arra[2] as integer) +1);
					else
						select e.first_name from usuario_tienda as t inner join usuario_empresa as e on (t.empresa_id=e.id and t.id=cast(tienda.id as integer)) limit 1 into gen_nom_emp;
						gen_nom_emp :=  left(upper(gen_nom_emp), 2)||'WS_1';
					end if;
					/*+++++++++++++++++*/
					select c.gps from usuario_tienda as t inner join usuario_empresa as e on (t.empresa_id=e.id and t.id=2) inner join pedido_configuraciontiempo as c on (c.empresa_id=e.id) limit 1 into configuracion;
					insert into pedido_pedidows (activado,detalle,num_pedido,npedido_express,cliente,fecha_pedido,tienda_id,tipo_pago,total,entregado,despachado,confirmado,alistado)
					values	(True,x."value",gen_nom_emp,gen_nom_emp,x."value"::json->>'cliente',now(),cast(tienda.id as integer),case when x."value"::json->>'tipo_pago'= '1' then 'Efectivo' when x."value"::json->>'tipo_pago' = '2' then 'Tarjeta' else 'Remision' end,cast(x."value"::json->>'total_pedido' as numeric),false,false,false,false)RETURNING id into id_inser;
					insert into pedido_timews(creado,pedido_id) values (now(),id_inser);
					SELECT COALESCE(array_to_json(array_agg(row_to_json(p))), '[]') from (
						select id,nit,direccion,latitud,longitud,referencia,celular,fijo from usuario_tienda where id = cast(tienda.id as integer) limit 1
					) p into l;
					cont_pedido:=cont_pedido||case when not ban_pedido then ',' else''end||'{"tiempo_gps":'||case when configuracion.gps is not null then configuracion.gps*1000 else 100 end||',"id":'||id_inser||',"ciudad":'||tienda.ciudad_id||',"tienda":'||l||',"info":'||x."value"::json||'}';
					ban_pedido:=false;
				else
					error:=error||case when not stop then ',' else''end||x."value"::json;
				end if;
			else
				error:=error||case when not stop then ',' else''end||x."value"::json;
				stop:=false;
			end if;

		end loop;
		select last(pedido)*10000 from pedido_configuraciontiempo into tiempo_pedido;
		return '{"respuesta":true,"error":['||error||'],"pedidos":['||cont_pedido||'],"retardo":'||tiempo_pedido||'}';
EXCEPTION WHEN others THEN
		return '{"respuesta":false,"mensage":"Error en la estructura del json"}';
end;

$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION public.ws_add_pedido_service(json)
  OWNER TO postgres;

/********************************************************************/
-- Function: public.ws_notif_pedidos(integer)

-- DROP FUNCTION public.ws_notif_pedidos(integer);

CREATE OR REPLACE FUNCTION public.ws_notif_pedidos(id_user integer)
  RETURNS json AS
$BODY$

 declare
	id_nit_tien integer;
 begin
	/*select nit from domicilios_empresa where id = (select empresa_id from domicilios_empleado where usuario_ptr_id=id_user limit 1) limit 1 into id_nit_tien;*/
	select empresa_id from domicilios_empleado where usuario_ptr_id=id_user limit 1 into id_nit_tien;
	if id_nit_tien is null then
		id_nit_tien:=0;
	end if;
	return (
		SELECT COALESCE(array_to_json(array_agg(row_to_json(p))), '[]') from (
			select id,cast(cliente as json)->>'nombre'::text as nom,
			       cast(cliente as json)->>'apellidos'::text as apellido,
			       cast(cliente as json)->>'dirreccion'::text as dir,
			       (
					select t.nombre from domicilios_tienda as t where t.nit = tienda limit 1
			       ) as emp,
			       (
					select t.direccion from domicilios_tienda as t where t.nit = tienda limit 1
			       ) as emp_dir
			       from domicilios_pedidows where empresa_id=id_nit_tien
		) p
	);
 end;

$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION public.ws_notif_pedidos(integer)
  OWNER TO postgres;
/********************************************************************/
-- Function: public.auto_asignar(integer, json)

-- DROP FUNCTION public.auto_asignar(integer, json);

CREATE OR REPLACE FUNCTION public.auto_asignar(
    tienda_id integer,
    motorizado_json json)
  RETURNS text AS
$BODY$
declare
	d numeric;
	result text;
begin
	d := (select last(distancia) from public.pedido_configuraciontiempo);
	result := (select
		motorizado.identifier
	from public.motorizado_motorizado as motorizado
	left join public.pedidos_motorizados as pedido on motorizado.empleado_id = pedido.motorizado_id
	join (select nombre, (latitud ||','|| longitud), (lat ||','|| lng), (degrees(ST_Distance(ST_GeomFromText('POINT('|| ti.latitud ||' '|| ti.longitud ||')'), ST_GeomFromText('POINT('|| n.lat ||' '|| n.lng ||')'))) * 2000), identificador from usuario_tienda as ti
		join (select * from json_populate_recordset(null::t, motorizado_json)) as n
			on (degrees(ST_Distance(ST_GeomFromText('POINT('|| ti.latitud ||' '|| ti.longitud ||')'), ST_GeomFromText('POINT('|| n.lat ||' '|| n.lng ||')'))) * 2000) < d
		where id=tienda_id) as distance on distance.identificador = motorizado.identifier
	group by motorizado.id
	order by last(pedido.creado) desc nulls first limit 1)::text;
	if result is null then
		return (select
			motorizado.identifier
		from public.motorizado_motorizado as motorizado
		join public.usuario_empleado as empleado on motorizado.empleado_id = empleado.usuario_ptr_id
		join public.usuario_tienda as tienda on tienda.empresa_id = empleado.empresa_id and tienda.id = tienda_id and empleado.ciudad_id = tienda.ciudad_id
		join (select * from json_populate_recordset(null::t, motorizado_json)) as n
			on motorizado.identifier = n.identificador
		order by (degrees(ST_Distance(ST_GeomFromText('POINT('|| tienda.latitud ||' '|| tienda.longitud ||')'), ST_GeomFromText('POINT('|| n.lat ||' '|| n.lng ||')'))) * 2000) asc
		limit 1)::text;
	end if;
	return result;
end;
$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION public.auto_asignar(integer, json)
  OWNER TO postgres;
/********************************************************************/
-- Function: public.get_add_pedido_admin(integer)

-- DROP FUNCTION public.get_add_pedido_admin(integer);

CREATE OR REPLACE FUNCTION public.get_add_pedido_admin(id_pedido integer)
  RETURNS json AS
$BODY$

declare
	configuracion record;
	id_tienda integer;
begin
	select tienda_id from pedido_pedido where id = id_pedido limit 1 into id_tienda;
	if id_tienda is null then
		id_tienda:=0;
	end if;
	select c.gps from usuario_tienda as t inner join usuario_empresa as e on (t.empresa_id=e.id and t.id=id_tienda) inner join pedido_configuraciontiempo as c on (c.empresa_id=e.id) limit 1 into configuracion;
	return (SELECT COALESCE(array_to_json(array_agg(row_to_json(p))), '[]') from (
		select case when configuracion.gps is not null then configuracion.gps*1000 else 100 end as tiempo_gps, id, (select identifier from motorizado_motorizado where empleado_id=motorizado_id limit 1) as motorizado,10000*(select retraso from pedido_configuraciontiempo order by id desc limit 1) as retraso,
		(
			SELECT COALESCE(array_to_json(array_agg(row_to_json(emp))), '[]') from (
						select id,nit,direccion,latitud,longitud,referencia,celular,fijo from usuario_tienda where id = tienda_id limit 1
					) emp
		) as tienda,
		(
			SELECT COALESCE(array_to_json(array_agg(row_to_json(items))), '[]') from (
				select i.descripcion as nombre,pi.cantidad as cantidad,pi.valor_unitario as valor from pedido_itemspedido as pi inner join pedido_items as i on(pi.pedido_id=id_pedido and pi.item_id=i.id)
			) items
		) as info,
		(
			select sum(pi.cantidad*pi.valor_unitario) from pedido_itemspedido as pi inner join pedido_items as i on(pi.pedido_id=id_pedido and pi.item_id=i.id)
		) as total,
		(
			SELECT COALESCE(array_to_json(array_agg(row_to_json(emp_cli))), '[]') from (
						select first_name as nombre,last_name as apellidos,telefono_fijo as fijo,telefono_celular as celular,direccion from usuario_cliente where id = cliente_id
					) emp_cli
		) as cliente
		from pedido_pedido where id = id_pedido limit 1
	) p);
end;

$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION public.get_add_pedido_admin(integer)
  OWNER TO postgres;
/********************************************************************/
-- Function: public.get_info_empleados_report_act(integer, text, text, boolean)

-- DROP FUNCTION public.get_info_empleados_report_act(integer, text, text, boolean);

CREATE OR REPLACE FUNCTION public.get_info_empleados_report_act(
    id_emp integer,
    fecha1 text,
    fecha2 text,
    state boolean)
  RETURNS json AS
$BODY$

declare
	emp json;
	dat json;
begin
	SELECT COALESCE(array_to_json(array_agg(row_to_json(p))), '[]') from (
		select u.identificacion as iden,a.first_name||' '||a.last_name as nom,e.direccion as dir,
			'Tel : '||u.telefono_fijo||'-'||u.telefono_celular as tel,a.email as correo
			from usuario_empleado as e
			inner join usuario_usuario as u on (e.usuario_ptr_id=u.user_ptr_id)
			inner join auth_user as a on(a.id=u.user_ptr_id and a.id=id_emp) limit 1
	) p into emp;
	SELECT COALESCE(array_to_json(array_agg(row_to_json(p))), '[]') from (
		select cliente,total,direccion,motori,alistar,despacho,entrega
			from pedidos_tiempos_actualizada where fecha BETWEEN fecha1::date AND fecha2::date and estado = state
				and (supervisor_id=id_emp or alistador_id=id_emp or motorizado_id=id_emp)
	) p into dat;
	return (array_to_json(array_agg(row_to_json(row(emp,dat)))));
end;

$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION public.get_info_empleados_report_act(integer, text, text, boolean)
  OWNER TO postgres;
/********************************************************************/
-- Function: public.get_info_pedido_cliente(text)

-- DROP FUNCTION public.get_info_pedido_cliente(text);

CREATE OR REPLACE FUNCTION public.get_info_pedido_cliente(nom_pedido text)
  RETURNS text AS
$BODY$

declare
 info json;
 res boolean;
begin
    select 'OL_4'~'([a-z]*[A-Z]*){0,2}_([0-9])+' into res;
    if res then
    	SELECT COALESCE(array_to_json(array_agg(row_to_json(p2))), '[]') from (
            select c.first_name||' '||c.last_name as cliente,
                    case when t.creado is not null then to_char(t.creado, 'DD/MM/YYYY - HH12:MI:SS')::text else 'No Asignado' end as creado
                    ,case when t.despachado is not null then to_char(t.despachado, 'DD/MM/YYYY - HH12:MI:SS')::text else 'No Asignado' end as alistamiento
                    ,case when t.entregado is not null then to_char(t.entregado, 'DD/MM/YYYY - HH12:MI:SS')::text else 'No Asignado' end as entregado
                        from pedido_pedido as p
                        inner join pedido_time as t on (t.pedido_id=p.id and p.num_pedido like ''||upper(nom_pedido)||'') inner join usuario_cliente as c on (c.id=p.cliente_id)  limit 1
    	) p2 into info;
        raise notice 'el valo res %',json_array_length(info);
        if json_array_length(info) = 0 then
            SELECT COALESCE(array_to_json(array_agg(row_to_json(p2))), '[]') from (
                select replace(cast(cast(p.cliente as json)::json->'nombre' as text)||' '||cast(cast(p.cliente as json)::json->'apellidos' as text),'"','') as cliente,
                        case when t.creado is not null then to_char(t.creado, 'DD/MM/YYYY - HH12:MI:SS')::text else 'No Asignado' end as creado
                        ,case when t.despachado is not null then to_char(t.despachado, 'DD/MM/YYYY - HH12:MI:SS')::text else 'No Asignado' end as alistamiento
                        ,case when t.entregado is not null then to_char(t.entregado, 'DD/MM/YYYY - HH12:MI:SS')::text else 'No Asignado' end as entregado
                            from pedido_pedidows as p
                            inner join pedido_timews as t on (p.id=t.pedido_id and p.num_pedido like ''||upper(nom_pedido)||'')  limit 1
            ) p2 into info;
            raise notice 'el valo res %',json_array_length(info);
            if json_array_length(info) > 0 then
                return '{"r":true,"lista":'||info||'}';
            end if;
            return '{"r":false}';
        end if;
        return '{"r":true,"lista":'||info||'}';
    end if;
    return '{"r":false}';
end;

$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION public.get_info_pedido_cliente(text)
  OWNER TO postgres;
/********************************************************************/
/********************************************************************/
/********************************************************************/
/********************************************************************/
/********************************************************************/
/********************************************************************/
/********************************************************************/
/********************************************************************/
/********************************************************************/
/********************************************************************/
/********************************************************************/
/********************************************************************/
/********************************************************************/
/********************************************************************/
