create or replace function update_tiempo_pedidows() returns trigger as $$
declare 
begin 
	if new.despachado and old.despachado = false then
		update pedido_timews set despachado = now() where pedido_id= old.id;
	elsif new.entregado and old.entregado=false then
		update pedido_timews set entregado = now() where pedido_id= old.id;
	elsif new.confirmado and old.confirmado=false then
		update pedido_timews set confirmado = now() where pedido_id= old.id;
	end if;
	return new;
end;
$$language plpgsql;

create trigger update_tiempo_pedidows after update on pedido_pedidows
	for each row execute procedure update_tiempo_pedidows()
