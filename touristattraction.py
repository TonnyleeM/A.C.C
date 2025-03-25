import json

# List of tourist locations for various African countries
locations = [
    # Algeria
    {"name": "Tassili n'Ajjer National Park", "city": "Algeria"},
    {"name": "Algiers Kasbah", "city": "Algeria"},
    {"name": "Sahara Desert", "city": "Algeria"},
    {"name": "Hoggar Mountains", "city": "Algeria"},
    {"name": "Ruins of Timgad", "city": "Algeria"},
    
    # Angola
    {"name": "Luanda Bay", "city": "Angola"},
    {"name": "Kissama National Park", "city": "Angola"},
    {"name": "Tundavala Fissure", "city": "Angola"},
    {"name": "Mussulo Island", "city": "Angola"},
    {"name": "Kalandula Falls", "city": "Angola"},
    
    # Benin
    {"name": "Ouidah Museum of History", "city": "Benin"},
    {"name": "Pendjari National Park", "city": "Benin"},
    {"name": "Royal Palace of Abomey", "city": "Benin"},
    {"name": "Grand Popo Beach", "city": "Benin"},
    {"name": "Ganvie Village", "city": "Benin"},
    
    # Botswana
    {"name": "Okavango Delta", "city": "Botswana"},
    {"name": "Chobe National Park", "city": "Botswana"},
    {"name": "Makgadikgadi Pan", "city": "Botswana"},
    {"name": "Moremi Game Reserve", "city": "Botswana"},
    {"name": "Tsodilo Hills", "city": "Botswana"},
    
    # Burkina Faso
    {"name": "Ouagadougou", "city": "Burkina Faso"},
    {"name": "Bobo-Dioulasso", "city": "Burkina Faso"},
    {"name": "Nazinga Game Ranch", "city": "Burkina Faso"},
    {"name": "Ruins of Loropéni", "city": "Burkina Faso"},
    {"name": "Lake Tengrela", "city": "Burkina Faso"},
    
    # Burundi
    {"name": "Lake Tanganyika", "city": "Burundi"},
    {"name": "Gitega National Museum", "city": "Burundi"},
    {"name": "Kibira National Park", "city": "Burundi"},
    {"name": "Saga Beach", "city": "Burundi"},
    {"name": "Source of the Nile", "city": "Burundi"},
    
    # Cape Verde
    {"name": "Sal Island", "city": "Cape Verde"},
    {"name": "Fogo Volcano", "city": "Cape Verde"},
    {"name": "Mindelo", "city": "Cape Verde"},
    {"name": "São Vicente", "city": "Cape Verde"},
    {"name": "Praia", "city": "Cape Verde"},
    
    # Cameroon
    {"name": "Mount Cameroon", "city": "Cameroon"},
    {"name": "Waza National Park", "city": "Cameroon"},
    {"name": "Dja Faunal Reserve", "city": "Cameroon"},
    {"name": "Limbe Botanic Gardens", "city": "Cameroon"},
    {"name": "Yaoundé", "city": "Cameroon"},
    
    # Central African Republic
    {"name": "Dzanga-Sangha National Park", "city": "Central African Republic"},
    {"name": "Sangha River", "city": "Central African Republic"},
    {"name": "Manova-Gounda St. Floris National Park", "city": "Central African Republic"},
    {"name": "Boali Waterfalls", "city": "Central African Republic"},
    {"name": "Berberati", "city": "Central African Republic"},
    
    # Chad
    {"name": "Zakouma National Park", "city": "Chad"},
    {"name": "Tibesti Mountains", "city": "Chad"},
    {"name": "Lake Chad", "city": "Chad"},
    {"name": "Aoûdaï National Park", "city": "Chad"},
    {"name": "N'Djamena", "city": "Chad"},
    
    # Comoros
    {"name": "Mount Karthala", "city": "Comoros"},
    {"name": "Moheli Marine Park", "city": "Comoros"},
    {"name": "Anjouan Island", "city": "Comoros"},
    {"name": "Moroni", "city": "Comoros"},
    {"name": "Ngazidja", "city": "Comoros"},
    
    # Democratic Republic of the Congo
    {"name": "Virunga National Park", "city": "DR Congo"},
    {"name": "Kahuzi-Biega National Park", "city": "DR Congo"},
    {"name": "Lake Tanganyika", "city": "DR Congo"},
    {"name": "Lola ya Bonobo", "city": "DR Congo"},
    {"name": "Kinshasa", "city": "DR Congo"},
    
    # Republic of the Congo
    {"name": "Odzala-Kokoua National Park", "city": "Republic of the Congo"},
    {"name": "Brazzaville", "city": "Republic of the Congo"},
    {"name": "Loufoulakari Falls", "city": "Republic of the Congo"},
    {"name": "Lesio-Louna Wildlife Reserve", "city": "Republic of the Congo"},
    {"name": "Tchimpounga Chimpanzee Rehabilitation Center", "city": "Republic of the Congo"},
    
    # Djibouti
    {"name": "Lake Assal", "city": "Djibouti"},
    {"name": "Djibouti City", "city": "Djibouti"},
    {"name": "Day Forest National Park", "city": "Djibouti"},
    {"name": "Gulf of Tadjoura", "city": "Djibouti"},
    {"name": "Arta Beach", "city": "Djibouti"},
    
    # Egypt
    {"name": "Pyramids of Giza", "city": "Egypt"},
    {"name": "Luxor", "city": "Egypt"},
    {"name": "Valley of the Kings", "city": "Egypt"},
    {"name": "Abu Simbel", "city": "Egypt"},
    {"name": "Egyptian Museum", "city": "Cairo"},
    
    # Equatorial Guinea
    {"name": "Malabo", "city": "Equatorial Guinea"},
    {"name": "Monte Alén National Park", "city": "Equatorial Guinea"},
    {"name": "Rio Muni", "city": "Equatorial Guinea"},
    {"name": "Bioko Island", "city": "Equatorial Guinea"},
    {"name": "Punta Europa", "city": "Equatorial Guinea"},
    
    # Eritrea
    {"name": "Asmara", "city": "Eritrea"},
    {"name": "Massawa", "city": "Eritrea"},
    {"name": "Dahlak Archipelago", "city": "Eritrea"},
    {"name": "Senafe", "city": "Eritrea"},
    {"name": "Keren", "city": "Eritrea"},
    
    # Eswatini (Swaziland)
    {"name": "Hlane Royal National Park", "city": "Eswatini"},
    {"name": "Mlilwane Wildlife Sanctuary", "city": "Eswatini"},
    {"name": "Mantenga Cultural Village", "city": "Eswatini"},
    {"name": "Sibebe Rock", "city": "Eswatini"},
    {"name": "Royal Swazi Spa", "city": "Eswatini"},
    
    # Ethiopia
    {"name": "Lalibela", "city": "Ethiopia"},
    {"name": "Simien Mountains National Park", "city": "Ethiopia"},
    {"name": "Axum", "city": "Ethiopia"},
    {"name": "Gondar", "city": "Ethiopia"},
    {"name": "Addis Ababa", "city": "Ethiopia"},
    
    # Gabon
    {"name": "Loango National Park", "city": "Gabon"},
    {"name": "Akanda National Park", "city": "Gabon"},
    {"name": "Libreville", "city": "Gabon"},
    {"name": "Ivindo National Park", "city": "Gabon"},
    {"name": "Mikongo Lodge", "city": "Gabon"},
    
    # Gambia
    {"name": "Banjul", "city": "Gambia"},
    {"name": "Kachikally Crocodile Pool", "city": "Gambia"},
    {"name": "Abuko Nature Reserve", "city": "Gambia"},
    {"name": "Tanji Village Museum", "city": "Gambia"},
    {"name": "River Gambia National Park", "city": "Gambia"},
    
    # Ghana
    {"name": "Cape Coast Castle", "city": "Ghana"},
    {"name": "Kakum National Park", "city": "Ghana"},
    {"name": "Accra", "city": "Ghana"},
    {"name": "Mole National Park", "city": "Ghana"},
    {"name": "Wli Waterfalls", "city": "Ghana"},
    
    # Guinea
    {"name": "Conakry", "city": "Guinea"},
    {"name": "Fouta Djallon", "city": "Guinea"},
    {"name": "Mount Nimba", "city": "Guinea"},
    {"name": "Boke", "city": "Guinea"},
    {"name": "Kankan", "city": "Guinea"},
    
    # Guinea-Bissau
    {"name": "Bissau", "city": "Guinea-Bissau"},
    {"name": "Orango Islands National Park", "city": "Guinea-Bissau"},
    {"name": "Joao Vieira and Poilao Marine National Park", "city": "Guinea-Bissau"},
    {"name": "Cacheu River", "city": "Guinea-Bissau"},
    {"name": "Bijagos Archipelago", "city": "Guinea-Bissau"},
    
    # Ivory Coast (Côte d'Ivoire)
    {"name": "Abidjan", "city": "Ivory Coast"},
    {"name": "Yamoussoukro", "city": "Ivory Coast"},
    {"name": "Taï National Park", "city": "Ivory Coast"},
    {"name": "Comoé National Park", "city": "Ivory Coast"},
    {"name": "Assinie-Mafia", "city": "Ivory Coast"},
    
    # Kenya
    {"name": "Maasai Mara National Reserve", "city": "Kenya"},
    {"name": "Amboseli National Park", "city": "Kenya"},
    {"name": "Lake Nakuru", "city": "Kenya"},
    {"name": "Tsavo National Park", "city": "Kenya"},
    {"name": "Nairobi National Park", "city": "Kenya"},
    
    # Lesotho
    {"name": "Sani Pass", "city": "Lesotho"},
    {"name": "Maloti Mountains", "city": "Lesotho"},
    {"name": "Sehlabathebe National Park", "city": "Lesotho"},
    {"name": "Thaba Bosiu", "city": "Lesotho"},
    {"name": "Katse Dam", "city": "Lesotho"},
    
    # Liberia
    {"name": "Monrovia", "city": "Liberia"},
    {"name": "Sapo National Park", "city": "Liberia"},
    {"name": "Robertsport", "city": "Liberia"},
    {"name": "Lake Piso", "city": "Liberia"},
    {"name": "Kpatawee Waterfall", "city": "Liberia"},
    
    # Libya
    {"name": "Leptis Magna", "city": "Libya"},
    {"name": "Cyrene", "city": "Libya"},
    {"name": "Tripoli", "city": "Libya"},
    {"name": "Ghadames", "city": "Libya"},
    {"name": "Sahara Desert", "city": "Libya"},
    
    # Madagascar
    {"name": "Avenue of the Baobabs", "city": "Madagascar"},
    {"name": "Andasibe-Mantadia National Park", "city": "Madagascar"},
    {"name": "Tsingy de Bemaraha", "city": "Madagascar"},
    {"name": "Nosy Be", "city": "Madagascar"},
    {"name": "Ranomafana National Park", "city": "Madagascar"},
    
    # Malawi
    {"name": "Lake Malawi National Park", "city": "Malawi"},
    {"name": "Liwonde National Park", "city": "Malawi"},
    {"name": "Nyika National Park", "city": "Malawi"},
    {"name": "Blantyre", "city": "Malawi"},
    {"name": "Zomba Plateau", "city": "Malawi"},
    
    # Mali
    {"name": "Timbuktu", "city": "Mali"},
    {"name": "Djenné", "city": "Mali"},
    {"name": "Bandiagara Escarpment", "city": "Mali"},
    {"name": "Mopti", "city": "Mali"},
    {"name": "Tomb of Askia", "city": "Mali"},
    
    # Mauritania
    {"name": "Banc d'Arguin National Park", "city": "Mauritania"},
    {"name": "Chinguetti", "city": "Mauritania"},
    {"name": "Ouadane", "city": "Mauritania"},
    {"name": "Atar", "city": "Mauritania"},
    {"name": "Nouakchott", "city": "Mauritania"},
    
    # Mauritius
    {"name": "Le Morne Brabant", "city": "Mauritius"},
    {"name": "Black River Gorges National Park", "city": "Mauritius"},
    {"name": "Île aux Cerfs", "city": "Mauritius"},
    {"name": "Port Louis", "city": "Mauritius"},
    {"name": "Chamarel", "city": "Mauritius"},
    
    # Morocco
    {"name": "Marrakech", "city": "Morocco"},
    {"name": "Fes", "city": "Morocco"},
    {"name": "Chefchaouen", "city": "Morocco"},
    {"name": "Sahara Desert", "city": "Morocco"},
    {"name": "Atlas Mountains", "city": "Morocco"},
    
    # Mozambique
    {"name": "Bazaruto Archipelago", "city": "Mozambique"},
    {"name": "Gorongosa National Park", "city": "Mozambique"},
    {"name": "Maputo", "city": "Mozambique"},
    {"name": "Inhaca Island", "city": "Mozambique"},
    {"name": "Ilha de Mozambique", "city": "Mozambique"},
    
    # Namibia
    {"name": "Etosha National Park", "city": "Namibia"},
    {"name": "Sossusvlei", "city": "Namibia"},
    {"name": "Swakopmund", "city": "Namibia"},
    {"name": "Fish River Canyon", "city": "Namibia"},
    {"name": "Skeleton Coast", "city": "Namibia"},
    
    # Niger
    {"name": "Air and Ténéré Natural Reserves", "city": "Niger"},
    {"name": "Agadez", "city": "Niger"},
    {"name": "Niamey", "city": "Niger"},
    {"name": "W National Park", "city": "Niger"},
    {"name": "Kouré", "city": "Niger"},
    
    # Nigeria
    {"name": "Olumo Rock", "city": "Nigeria"},
    {"name": "Aso Rock", "city": "Nigeria"},
    {"name": "Zuma Rock", "city": "Nigeria"},
    {"name": "Niger River", "city": "Nigeria"},
    {"name": "Lekki Conservation Centre", "city": "Nigeria"},
    
    # Rwanda
    {"name": "Volcanoes National Park", "city": "Rwanda"},
    {"name": "Lake Kivu", "city": "Rwanda"},
    {"name": "Akagera National Park", "city": "Rwanda"},
    {"name": "Nyungwe Forest National Park", "city": "Rwanda"},
    {"name": "Kigali Genocide Memorial", "city": "Rwanda"},
    
    # São Tomé and Príncipe
    {"name": "Obo National Park", "city": "São Tomé and Príncipe"},
    {"name": "Ilhéu das Rolas", "city": "São Tomé and Príncipe"},
    {"name": "São Tomé City", "city": "São Tomé and Príncipe"},
    {"name": "Praia das Conchas", "city": "São Tomé and Príncipe"},
    {"name": "Bom Bom Island", "city": "São Tomé and Príncipe"},
    
    # Senegal
    {"name": "Dakar", "city": "Senegal"},
    {"name": "Goree Island", "city": "Senegal"},
    {"name": "Niokolo-Koba National Park", "city": "Senegal"},
    {"name": "Pink Lake (Lac Rose)", "city": "Senegal"},
    {"name": "Saloum Delta National Park", "city": "Senegal"},
    
    # Seychelles
    {"name": "Anse Source d'Argent", "city": "Seychelles"},
    {"name": "Vallée de Mai Nature Reserve", "city": "Seychelles"},
    {"name": "Mahé Island", "city": "Seychelles"},
    {"name": "La Digue Island", "city": "Seychelles"},
    {"name": "Aldabra Atoll", "city": "Seychelles"},

  # Sierra Leone
    {"name": "Freetown", "city": "Sierra Leone"},
    {"name": "Tiwai Island Wildlife Sanctuary", "city": "Sierra Leone"},
    {"name": "Banana Islands", "city": "Sierra Leone"},
    {"name": "Bureh Beach", "city": "Sierra Leone"},
    {"name": "Loma Mountains", "city": "Sierra Leone"},
    
    # Somalia
    {"name": "Mogadishu", "city": "Somalia"},
    {"name": "Laas Geel", "city": "Somalia"},
    {"name": "Kismayo", "city": "Somalia"},
    {"name": "Hargeisa", "city": "Somalia"},
    {"name": "Berbera", "city": "Somalia"},
    
    # South Africa
    {"name": "Table Mountain", "city": "South Africa"},
    {"name": "Kruger National Park", "city": "South Africa"},
    {"name": "Cape Town", "city": "South Africa"},
    {"name": "Robben Island", "city": "South Africa"},
    {"name": "Garden Route", "city": "South Africa"},
    
    # South Sudan
    {"name": "Juba", "city": "South Sudan"},
    {"name": "Boma National Park", "city": "South Sudan"},
    {"name": "Sudd Wetlands", "city": "South Sudan"},
    {"name": "Nimule National Park", "city": "South Sudan"},
    {"name": "Bor", "city": "South Sudan"},
    
    # Sudan
    {"name": "Pyramids of Meroë", "city": "Sudan"},
    {"name": "Khartoum", "city": "Sudan"},
    {"name": "Jebel Barkal", "city": "Sudan"},
    {"name": "Nubian Desert", "city": "Sudan"},
    {"name": "Red Sea Coast", "city": "Sudan"},
    
    # Tanzania
    {"name": "Serengeti National Park", "city": "Tanzania"},
    {"name": "Mount Kilimanjaro", "city": "Tanzania"},
    {"name": "Ngorongoro Crater", "city": "Tanzania"},
    {"name": "Zanzibar", "city": "Tanzania"},
    {"name": "Tarangire National Park", "city": "Tanzania"},
    
    # Togo
    {"name": "Lomé", "city": "Togo"},
    {"name": "Koutammakou", "city": "Togo"},
    {"name": "Fazao-Malfakassa National Park", "city": "Togo"},
    {"name": "Togoville", "city": "Togo"},
    {"name": "Aneho", "city": "Togo"},
    
    # Tunisia
    {"name": "Carthage", "city": "Tunisia"},
    {"name": "Medina of Tunis", "city": "Tunisia"},
    {"name": "Sahara Desert", "city": "Tunisia"},
    {"name": "Bardo National Museum", "city": "Tunisia"},
    {"name": "El Jem", "city": "Tunisia"},
    
    # Uganda
    {"name": "Bwindi Impenetrable National Park", "city": "Uganda"},
    {"name": "Queen Elizabeth National Park", "city": "Uganda"},
    {"name": "Murchison Falls National Park", "city": "Uganda"},
    {"name": "Lake Victoria", "city": "Uganda"},
    {"name": "Kampala", "city": "Uganda"},
    
    # Zambia
    {"name": "Victoria Falls", "city": "Zambia"},
    {"name": "South Luangwa National Park", "city": "Zambia"},
    {"name": "Lower Zambezi National Park", "city": "Zambia"},
    {"name": "Kafue National Park", "city": "Zambia"},
    {"name": "Livingstone", "city": "Zambia"},
    
    # Zimbabwe
    {"name": "Victoria Falls", "city": "Zimbabwe"},
    {"name": "Hwange National Park", "city": "Zimbabwe"},
    {"name": "Mana Pools National Park", "city": "Zimbabwe"},
    {"name": "Great Zimbabwe", "city": "Zimbabwe"},
    {"name": "Matobo National Park", "city": "Zimbabwe"},
]

# Google Maps API key
api_key = "AIzaSyC2SbTlOY4ClJP2-eQ2wvaG5JX9NNiUr3A"  # Replace with your actual Google Maps API key

# Generate Google Maps iframe links and add them to the locations
for location in locations:
    name = location["name"].replace(" ", "+")
    city = location["city"].replace(" ", "+")
    iframe_link = f"https://www.google.com/maps/embed/v1/place?key={api_key}&q={name},{city}"
    location["iframe_link"] = iframe_link  # Add iframe link to the location

# Save the data with iframe links to a JSON file
with open('africa_attractions_data.json', 'w') as json_file:
    json.dump(locations, json_file, indent=4)

print("Data saved to africa_attractions_data.json")

# Print iframe HTML for each location
for location in locations:
    print(f"""
<iframe
  width="600"
  height="450"
  style="border:0"
  loading="lazy"
  allowfullscreen
  referrerpolicy="no-referrer-when-downgrade"
  src="{location['iframe_link']}">
</iframe>
""")