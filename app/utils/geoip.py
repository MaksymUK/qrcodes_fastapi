import geoip2.database

reader = geoip2.database.Reader(
    "GeoLite2-City.mmdb"
)


def get_geo_data(ip_address: str):
    try:
        response = reader.city(ip_address)

        return {
            "country": response.country.name,
            "city": response.city.name
        }

    except Exception:
        return {
            "country": None,
            "city": None
        }
