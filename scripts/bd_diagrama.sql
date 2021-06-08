//// -- LEVEL 1
//// -- Tables and References

// Creating tables
Table empresas {
  nome text [not null]
  razao_social text [not null]
  cnpj varchar [not null]
  id_responsavel varchar [not null]
  email text
  fone text
  cidade text
  uf varchar
  criada_em year

   Indexes {
    (cnpj, nome) [pk]
  }
}

Table pollsters {
  nome text [not null]
  cpf varchar [unique, pk]
  email text
  fone text
 }

// Creating references
// You can also define relaionship separately
// > many-to-one; < one-to-many; - one-to-one
Ref: empresas.id_responsavel > pollsters.cpf  
// Ref: empresas.nome > aprovacao.(empresa, data_fim, empresa, tipo)

//----------------------------------------------//

//// -- LEVEL 2
//// -- Adding column settings

Table aprovacao {
  data_ini date [not null]
  data_fim date [not null]
  empresa text [ref: > empresas.nome] // inline relationship (many-to-one)
  nome text [not null]
  positiva float [not null]
  regular float 
  negativa float [not null]
  nsnr float 
  erro float [not null]
  ic int [not null]
  n int [not null]
  ufs text
  cidades text
  partido text [not null]
  presidente text [not null]
  tipo text [not null]
  pergunta text
  modo text [not null]

   Indexes {
    (data_fim, empresa, tipo) [pk]
  }
}



Table intencao {
  data_ini date [not null]
  data_fim date [not null]
  empresa text [ref: > empresas.nome] // inline relationship (many-to-one)
  nome text [not null]
  cargo text [not null]
  turno int [not null]
  candidato text [not null]
  partido text [not null]
  voto float [not null]
  erro float [not null]
  ic int [not null]
  n int [not null]
  ufs text
  cidades text
  tipo text [not null]
  modo text [not null]
  pergunta text

   Indexes {
    (data_fim, empresa, cargo, turno, candidato, tipo) [pk]
  }
}



Ref: order_items.product_id > products.id

Table orders {
  id int [pk] // primary key
  user_id int [not null, unique]
  status varchar
  created_at varchar [note: 'When order created'] // add column note
}

//----------------------------------------------//

//// -- Level 3 
//// -- Enum, Indexes

// Enum for 'products' table below
Enum products_status {
  out_of_stock
  in_stock
  running_low [note: 'less than 20'] // add column note
}

// Indexes: You can define a single or multi-column index 
Table products {
  id int [pk]
  name varchar
  merchant_id int [not null]
  price int
  status products_status
  created_at datetime [default: `now()`]
  
  Indexes {
    (merchant_id, status) [name:'product_status']
    id [unique]
  }
}


Table merchants {
  id int
  country_code int
  merchant_name varchar
  
  "created at" varchar
  admin_id int [ref: > U.id]
  Indexes {
    (id, country_code) [pk]
  }
}

Table merchant_periods {
  id int [pk]
  merchant_id int
  country_code int
  start_date datetime
  end_date datetime
}

Ref: products.merchant_id > merchants.id // many-to-one
//composite foreign key
Ref: merchant_periods.(merchant_id, country_code) > merchants.(id, country_code)
