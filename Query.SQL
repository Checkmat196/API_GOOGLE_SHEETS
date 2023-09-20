SELECT
	A.id as 'ID_CHAMADO',
	C.name as 'TIPO_SOLICITACAO',
	A.name as 'NOME_CHAMADO',
	A.date as 'DATA_ABERTURA_CHAMADO',
	A.closedate as 'DATA_FECHAMENTO_CHAMADO'
from glpi_tickets A 
	left join glpi_entities B on A.entities_id = B.id 
	left join glpi_itilcategories C on A.itilcategories_id = C.id 
	left join glpi_users D on A.users_id_lastupdater = D.id 
	left join glpi_users F on A.users_id_recipient = F.id 
	left join glpi_solutiontypes G on A.status = G.id 
	left join glpi_groups E on F.groups_id = E.id
	left join glpi_locations H on H.id = A.locations_id
where C.completename LIKE '%KEDU FINANCEIRO > RISCO%'