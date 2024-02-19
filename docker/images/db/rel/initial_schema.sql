CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS POSTGIS;
CREATE EXTENSION IF NOT EXISTS POSTGIS_TOPOLOGY;


CREATE TABLE public.countries (
	id              uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
	name            VARCHAR(250) NOT NULL,
	geom            GEOMETRY,
	created_on      TIMESTAMP NOT NULL DEFAULT NOW(),
	updated_on      TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE public.orders (
    id              uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    invoice_no      VARCHAR(20),
    invoice_date    TIMESTAMP,
    customer_id     INT,
    country_ref     uuid NOT NULL,
    FOREIGN KEY (country_ref) REFERENCES public.Countries(id) ON DELETE CASCADE
);

CREATE TABLE public.products (
    id              uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    stock_code      VARCHAR(20),
    description     TEXT,
    unit_price      NUMERIC
);

create TABLE public.orderproducts (
	id              uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    id_order  		uuid,
    id_product 		uuid,
    FOREIGN KEY (id_order) REFERENCES public.Orders(id),
    FOREIGN KEY (id_product) REFERENCES public.Products(id),
	UNIQUE (id_order, id_product)
);

