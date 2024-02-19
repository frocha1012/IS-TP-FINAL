import sys
import os
from flask import Flask, request, jsonify
from sqlalchemy import create_engine

PORT = int(sys.argv[1]) if len(sys.argv) >= 2 else 8080
PG_REL_CONN_STR = os.getenv('PG_REL_CONN_STR')

app = Flask(__name__)
app.config["DEBUG"] = True
engine = create_engine(PG_REL_CONN_STR)

@app.route('/api/tile', methods=['GET'])
def get_markers():
    args = request.args
    neLat, neLng, swLat, swLng = args.get('neLat'), args.get('neLng'), args.get('swLat'), args.get('swLng')
    query = f"""SELECT jsonb_build_object('type', 'Feature', 'id', id, 'geometry', ST_AsGeoJSON(geom)::jsonb, 'properties', to_jsonb(row) - 'id' - 'geom') FROM (SELECT * FROM countries WHERE geom @ ST_MakeEnvelope({swLng}, {swLat}, {neLng}, {neLat}, 4326)) row;"""
    with engine.connect() as conn:
        result = conn.execute(query)
        features = [row[0] for row in result]
    return jsonify(features)

@app.route('/api/entities', methods=['POST'])
def update_entity():
    content = request.json
    country_id, lat, lon = content['country_id'], content['latitude'], content['longitude']
    query = "UPDATE countries SET geom = ST_SetSRID(ST_MakePoint(%s, %s), 4326) WHERE id = %s"
    with engine.connect() as conn:
        conn.execute(query, (lon, lat, country_id))
    return jsonify({"message": "Entity updated successfully"}), 200

@app.route('/countries_without_coordinates', methods=['GET'])
def countries_without_coordinates():
    query = "SELECT id, name FROM countries WHERE geom IS NULL ORDER BY created_on ASC;"
    with engine.connect() as conn:
        result = conn.execute(query)
        countries = [dict(row) for row in result]
    return jsonify(countries)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=PORT)

