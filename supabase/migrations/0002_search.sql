create function search_properties(
  q_embedding halfvec(1024) default null,
  p_type text default null,
  p_uf text default null,
  p_max_price numeric default null,
  p_min_bedrooms int default null,
  p_min_visual real default null,
  p_poi_cat text default null,
  p_poi_radius_m int default 2000,
  p_bbox float8[] default null
) returns table (
  property_id text, property_type text, uf text, city text, neighborhood text,
  raw_address text, sale_value numeric, appraised_value numeric, discount numeric,
  area_m2 numeric, bedrooms int, parking_spots int, image_file text,
  lat double precision, lon double precision, geocode_precision text,
  visual_score real, visual_age text, similarity real
) language sql stable as $$
  select p.property_id, p.property_type, p.uf, p.city, p.neighborhood,
         p.raw_address, p.sale_value, p.appraised_value, p.discount,
         p.area_m2, p.bedrooms, p.parking_spots, p.image_file,
         p.lat, p.lon, p.geocode_precision,
         p.visual_score, p.visual_age,
         (1 - (e.embedding <=> q_embedding))::real
  from properties p
  left join property_embeddings e on e.property_id = p.property_id
  where (p_type is null or p.property_type = p_type)
    and (p_uf is null or p.uf = p_uf)
    and (p_max_price is null or p.sale_value <= p_max_price)
    and (p_min_bedrooms is null or p.bedrooms >= p_min_bedrooms)
    and (p_min_visual is null or p.visual_score >= p_min_visual)
    and (p_bbox is null or p.geom && st_makeenvelope(p_bbox[1], p_bbox[2], p_bbox[3], p_bbox[4], 4326)::geography)
    and (p_poi_cat is null or exists (
      select 1 from property_poi pp join pois o on o.id = pp.poi_id
      where pp.property_id = p.property_id and o.category = p_poi_cat and pp.dist_m <= p_poi_radius_m
    ))
  order by e.embedding <=> q_embedding nulls last, p.discount desc nulls last
  limit 100
$$;

create function property_pois(p_id text)
returns table (category text, name text, lat double precision, lon double precision, dist_m int)
language sql stable as $$
  select o.category, o.name, o.lat, o.lon, pp.dist_m
  from property_poi pp join pois o on o.id = pp.poi_id
  where pp.property_id = p_id
  order by pp.dist_m
$$;
