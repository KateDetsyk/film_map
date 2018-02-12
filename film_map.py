import folium
from geopy.geocoders import Nominatim


year_input = int(input("Enter a year:"))

geolocator = Nominatim()
result = {}
with open('locations.list', mode = "r") as f:
    for line_number, line in enumerate(f.readlines()):
        if line_number > 13:
            # film name
            index_film_name_end = line.index("(")
            film_name = line[:index_film_name_end]
            film_name = film_name.strip()

            # film year
            try:
                year = line[index_film_name_end+1:index_film_name_end+5]
                year = int(year)
            except ValueError:
                print("{0} does not have a year".format(film_name))

            # skip useless year
            if year != year_input:
                continue

            # locations
            location_start = line.index(")") + 1
            film_location = line[location_start:]
            if "}" in film_location:
                 index = film_location.index("}")
                 film_location = film_location[index + 1:]
            if "(" in film_location:
                 index = film_location.index("(")
                 film_location = film_location[:index]
            film_location = film_location.strip()
            try:
                film_location = geolocator.geocode(film_location)
                film_location = [film_location.latitude, film_location.longitude]
            except AttributeError:
                print("Sorry {0} can't be converted into coordinates.".format(film_name))
            except:
                print("geopy error")

            # result
            if film_location:
                if year in result:
                    if film_name in result[year]:
                        if not film_location in result[year][film_name]:
                            result[year][film_name].append(film_location)
                    else:
                        result[year][film_name] = [film_location]
                else:
                    result[year] = {film_name: [film_location]}

# map
m = folium.Map(location=[30, 31], zoom_start = 2)
folium.TileLayer('openstreetmap').add_to(m)
folium.TileLayer('stamenterrain').add_to(m)
folium.TileLayer('stamenwatercolor').add_to(m)
folium.TileLayer('stamentoner').add_to(m)
folium.TileLayer('cartodbpositron').add_to(m)
folium.LayerControl().add_to(m)

for film_name in result[year_input]:
    for film_locations in result[year_input][film_name]:
        folium.Marker(film_locations, popup = film_name).add_to(m)

m.save('film_map.html')
print("File film_map.html generated.")
