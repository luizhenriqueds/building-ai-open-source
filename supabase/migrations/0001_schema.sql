create extension if not exists vector;
create extension if not exists postgis;

create table properties (
  property_id text primary key,
  property_type text, uf text, city text, neighborhood text, raw_address text,
  appraised_value numeric, sale_value numeric, discount numeric,
  modality text, link text, description text,
  area_m2 numeric, land_area numeric, bedrooms int, parking_spots int,
  occupancy_status text, auction_date date,
  image_file text,
  lat double precision, lon double precision,
  geom geography(Point,4326) generated always as
    (case when lat is not null then st_makepoint(lon,lat)::geography end) stored,
  geocode_precision text, geocode_confidence real,
  visual_score real, visual_age text, visual_note text, visual_details jsonb,
  embed_text text
);
create index on properties using gist (geom);

create table property_embeddings (
  property_id text primary key references properties,
  embedding halfvec(1024) not null
);
create index on property_embeddings using hnsw (embedding halfvec_cosine_ops);

create table pois (
  id bigserial primary key, osm_id text unique, category text, name text,
  lat double precision, lon double precision,
  geom geography(Point,4326) generated always as (st_makepoint(lon,lat)::geography) stored
);
create index on pois using gist (geom);

create table property_poi (
  property_id text references properties, poi_id bigint references pois,
  dist_m int, primary key (property_id, poi_id)
);
