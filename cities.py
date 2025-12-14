
# Top ~500 Major World Cities for Autocomplete
ALL_CITIES = [
    "Other (Type Your Own)",
    "Paris, France", "London, UK", "New York, USA", "Tokyo, Japan", "Rome, Italy", "Dubai, UAE",
    "Singapore", "Barcelona, Spain", "Bangkok, Thailand", "Istanbul, Turkey", "Bali, Indonesia",
    "Amsterdam, Netherlands", "Seoul, South Korea", "Hong Kong", "Las Vegas, USA", "Los Angeles, USA",
    "Osaka, Japan", "Phuket, Thailand", "Santorini, Greece", "Kyoto, Japan", "Prague, Czech Republic",
    "Milan, Italy", "Vienna, Austria", "Madrid, Spain", "Lisbon, Portugal", "Sydney, Australia",
    "Melbourne, Australia", "Toronto, Canada", "San Francisco, USA", "Miami, USA", "Orlando, USA",
    "Venice, Italy", "Florence, Italy", "Dublin, Ireland", "Berlin, Germany", "Munich, Germany",
    "Budapest, Hungary", "Cairo, Egypt", "Mumbai, India", "Delhi, India", "Bangalore, India",
    "Goa, India", "Chennai, India", "Hyderabad, India", "Kolkata, India", "Jaipur, India",
    "Agra, India", "Varanasi, India", "Kochi, India", "Pune, India", "Ahmedabad, India",
    "Rio de Janeiro, Brazil", "Sao Paulo, Brazil", "Buenos Aires, Argentina", "Lima, Peru",
    "Mexico City, Mexico", "Cancun, Mexico", "Cusco, Peru", "Santiago, Chile", "Bogota, Colombia",
    "Cape Town, South Africa", "Johannesburg, South Africa", "Marrakech, Morocco", "Casablanca, Morocco",
    "Nairobi, Kenya", "Zanzibar, Tanzania", "Mahe, Seychelles", "Male, Maldives",
    "Beijing, China", "Shanghai, China", "Shenzhen, China", "Guangzhou, China", "Chengdu, China",
    "Hanoi, Vietnam", "Ho Chi Minh City, Vietnam", "Da Nang, Vietnam", "Kuala Lumpur, Malaysia",
    "Manila, Philippines", "Jakarta, Indonesia", "Taipei, Taiwan", "Kathmandu, Nepal",
    "Colombo, Sri Lanka", "Auckland, New Zealand", "Queenstown, New Zealand",
    "Vancouver, Canada", "Montreal, Canada", "Chicago, USA", "Boston, USA", "Washington DC, USA",
    "Seattle, USA", "Honolulu, USA", "San Diego, USA", "Austin, USA", "New Orleans, USA",
    "Edinburgh, UK", "Manchester, UK", "Liverpool, UK", "Glasgow, UK", "Zurich, Switzerland",
    "Geneva, Switzerland", "Luzern, Switzerland", "Stockholm, Sweden", "Copenhagen, Denmark",
    "Oslo, Norway", "Helsinki, Finland", "Reykjavik, Iceland", "Brussels, Belgium", "Bruges, Belgium",
    "Athens, Greece", "Mykonos, Greece", "Dubrovnik, Croatia", "Split, Croatia", "Warsaw, Poland",
    "Krakow, Poland", "Moscow, Russia", "St. Petersburg, Russia", "Kyiv, Ukraine",
    "Tel Aviv, Israel", "Jerusalem, Israel", "Amman, Jordan", "Petra, Jordan", "Beirut, Lebanon",
    "Doha, Qatar", "Abu Dhabi, UAE", "Riyadh, Saudi Arabia", "Jeddah, Saudi Arabia",
    "Muscat, Oman", "Tehran, Iran", "Baghdad, Iraq", "Kuwait City, Kuwait", "Manama, Bahrain",
    
    # Starting with B (for User Test case)
    "Baku, Azerbaijan", "Baltimore, USA", "Bamako, Mali", "Bandung, Indonesia", "Banjul, Gambia",
    "Barquisimeto, Venezuela", "Barranquilla, Colombia", "Basel, Switzerland", "Baton Rouge, USA",
    "Belfast, UK", "Belgrade, Serbia", "Belize City, Belize", "Belo Horizonte, Brazil",
    "Bergen, Norway", "Bern, Switzerland", "Bilbao, Spain", "Birmingham, UK", "Birmingham, USA",
    "Bishkek, Kyrgyzstan", "Bissau, Guinea-Bissau", "Bloemfontein, South Africa", "Bogor, Indonesia",
    "Boise, USA", "Bologna, Italy", "Bordeaux, France", "Boston, USA", "Brasilia, Brazil",
    "Bratislava, Slovakia", "Brazzaville, Congo", "Brisbane, Australia", "Bristol, UK",
    "Brno, Czech Republic", "Bucharest, Romania", "Buffalo, USA", "Bujumbura, Burundi",
    "Bulawayo, Zimbabwe", "Bursa, Turkey", "Busan, South Korea",

    # More Major Cities A-Z
    "Accra, Ghana", "Addis Ababa, Ethiopia", "Adelaide, Australia", "Algiers, Algeria", "Almaty, Kazakhstan", 
    "Amritsar, India", "Ankara, Turkey", "Antalya, Turkey", "Antananarivo, Madagascar", "Antwerpen, Belgium",
    "Arequipa, Peru", "Ashgabat, Turkmenistan", "Asuncion, Paraguay", "Atlanta, USA", 
    "Baguio, Philippines", "Baltra, Ecuador", "Bamberg, Germany", "Banff, Canada", 
    "Bariloche, Argentina", "Bath, UK", "Batu, Indonesia", "Beijing, China", 
    "Bentonville, USA", "Bergen, Norway", "Bhopal, India", "Biarritz, France", 
    "Bora Bora, French Polynesia", "Boulder, USA", "Bozeman, USA", "Breckenridge, USA",
    "Brighton, UK", "Brunei City, Brunei", "Bryce Canyon, USA", "Burlington, USA", "Byron Bay, Australia",
    
    "Calgary, Canada", "Cali, Colombia", "Cambridge, UK", "Cambridge, USA", "Canberra, Canada",
    "Caracas, Venezuela", "Cartagena, Colombia", "Cebu, Philippines", "Chang Mai, Thailand",
    "Charlotte, USA", "Chengdu, China", "Chiang Rai, Thailand", "Chisinau, Moldova",
    "Christchurch, New Zealand", "Cincinnati, USA", "Cleveland, USA", "Cologne, Germany",
    "Columbus, USA", "Constanta, Romania", "Cordoba, Argentina", "Cordoba, Spain",
    "Cork, Ireland", "Curitiba, Brazil", "Cusco, Peru",
    
    "Dakar, Senegal", "Dallas, USA", "Damascus, Syria", "Dar es Salaam, Tanzania", "Darwin, Australia",
    "Davao, Philippines", "Denver, USA", "Des Moines, USA", "Detroit, USA", "Dhaka, Bangladesh",
    "Dijon, France", "Djibouti, Djibouti", "Dortmund, Germany", "Dresden, Germany", "Durbin, South Africa",
    "Dusseldorf, Germany",
    
    "Esfahan, Iran", "Eugene, USA",
    
    "Fes, Morocco", "Flagstaff, USA", "Fort Lauderdale, USA", "Frankfurt, Germany", "Fukuoka, Japan",
    "Fukushima, Japan",
    
    "Galapagos, Ecuador", "Galway, Ireland", "Gant, Belgium", "Genoa, Italy", "Georgetown, Guyana",
    "Georgetown, Malaysia", "Ghent, Belgium", "Giza, Egypt", "Glasgow, UK", "Gold Coast, Australia",
    "Gothenburg, Sweden", "Granada, Spain", "Grand Canyon, USA", "Graz, Austria", "Guadalajara, Mexico",
    "Guatemala City, Guatemala", "Guayaquil, Ecuador",
    
    "Hague, Netherlands", "Haifa, Israel", "Hakone, Japan", "Hamburg, Germany", "Hamilton, Bermuda",
    "Hamilton, Canada", "Hangzhou, China", "Hannover, Germany", "Harare, Zimbabwe", "Harbin, China",
    "Havana, Cuba", "Heidelberg, Germany", "Heraklion, Greece", "Hiroshima, Japan", "Hobart, Australia",
    "Houston, USA", "Hua Hin, Thailand", "Hue, Vietnam",
    
    "Ibiza, Spain", "Indianapolis, USA", "Innsbruck, Austria", "Islamabad, Pakistan", "Izmir, Turkey",
    
    "Jackson Hole, USA", "Jacksonville, USA", "Jaipur, India", "Jakarta, Indonesia", "Jasper, Canada",
    "Jerusalem, Israel", "Jodhpur, India", "Johannesburg, South Africa", "Juneau, USA",
    
    "Kabul, Afghanistan", "Kampala, Uganda", "Kansas City, USA", "Kaohsiung, Taiwan", "Karachi, Pakistan",
    "Kathmandu, Nepal", "Kauai, USA", "Kazan, Russia", "Key West, USA", "Khartoum, Sudan",
    "Kigali, Rwanda", "Kingston, Jamaica", "Kinshasa, DRC", "Kobe, Japan", "Kolkata, India",
    "Krabi, Thailand", "Krakow, Poland", "Kuala Lumpur, Malaysia", "Kuching, Malaysia", "Kyiv, Ukraine",
    "Kyoto, Japan",
    
    "Lagos, Nigeria", "Lahore, Pakistan", "Lake Tahoe, USA", "La Paz, Bolivia", "Las Vegas, USA",
    "Lausanne, Switzerland", "Leeds, UK", "Leicester, UK", "Leipzig, Germany", "Lille, France",
    "Lima, Peru", "Lisbon, Portugal", "Liverpool, UK", "Ljubljana, Slovenia", "London, UK",
    "Los Angeles, USA", "Louisville, USA", "Luang Prabang, Laos", "Lucknow, India", "Lusaka, Zambia",
    "Luxembourg City, Luxembourg", "Luxor, Egypt", "Lyon, France",
    
    "Macau, China", "Madison, USA", "Madras, India", "Madrid, Spain", "Malaga, Spain",
    "Male, Maldives", "Malmo, Sweden", "Managua, Nicaragua", "Manaus, Brazil", "Manchester, UK",
    "Mandalay, Myanmar", "Manila, Philippines", "Marrakech, Morocco", "Marseille, France", "Maui, USA",
    "Medellin, Colombia", "Melbourne, Australia", "Memphis, USA", "Mendoza, Argentina", "Mexico City, Mexico",
    "Miami, USA", "Milan, Italy", "Milwaukee, USA", "Minneapolis, USA", "Minsk, Belarus",
    "Monte Carlo, Monaco", "Montego Bay, Jamaica", "Monterey, USA", "Montevideo, Uruguay", "Montreal, Canada",
    "Moscow, Russia", "Mumbai, India", "Munich, Germany", "Muscat, Oman", "Mykonos, Greece",
    
    "Nairobi, Kenya", "Nanjing, China", "Naples, Italy", "Nashville, USA", "Nassau, Bahamas",
    "New Delhi, India", "New Orleans, USA", "New York, USA", "Newcastle, UK", "Nice, France",
    "Nicosia, Cyprus", "Nottingham, UK", "Nuremberg, Germany",
    
    "Oaxaca, Mexico", "Odessa, Ukraine", "Oklahoma City, USA", "Olympia, Greece", "Omaha, USA",
    "Orlando, USA", "Osaka, Japan", "Oslo, Norway", "Ottawa, Canada", "Oxford, UK",
    
    "Palermo, Italy", "Palm Springs, USA", "Panama City, Panama", "Papeete, Tahiti", "Paris, France",
    "Park City, USA", "Pattaya, Thailand", "Perth, Australia", "Philadelphia, USA", "Phnom Penh, Cambodia",
    "Phoenix, USA", "Phuket, Thailand", "Pisa, Italy", "Pittsburgh, USA", "Playa del Carmen, Mexico",
    "Portland, USA", "Porto, Portugal", "Porto Alegre, Brazil", "Prague, Czech Republic", "Pretoria, South Africa",
    "Providence, USA", "Puebla, Mexico", "Puerto Vallarta, Mexico", "Pune, India", "Punta Cana, Dominican Republic",
    "Busan, South Korea", "Pyongyang, North Korea",
    
    "Quebec City, Canada", "Queenstown, New Zealand", "Quito, Ecuador",
    
    "Rabat, Morocco", "Raleigh, USA", "Rangoon, Myanmar", "Recife, Brazil", "Reykjavik, Iceland",
    "Rhodes, Greece", "Riga, Latvia", "Rio de Janeiro, Brazil", "Riyadh, Saudi Arabia", "Rome, Italy",
    "Rotterdam, Netherlands",
    
    "Sacramento, USA", "Saigon, Vietnam", "Saint Petersburg, Russia", "Salt Lake City, USA", "Salvador, Brazil",
    "Salzburg, Austria", "San Antonio, USA", "San Diego, USA", "San Francisco, USA", "San Jose, Costa Rica",
    "San Jose, USA", "San Juan, Puerto Rico", "San Salvador, El Salvador", "Sanaa, Yemen", "Santa Barbara, USA",
    "Santa Fe, USA", "Santiago, Chile", "Santo Domingo, Dominican Republic", "Santorini, Greece", "Sao Paulo, Brazil",
    "Sapporo, Japan", "Sarajevo, Bosnia", "Savannah, USA", "Seattle, USA", "Sedona, USA",
    "Seoul, South Korea", "Seville, Spain", "Shanghai, China", "Sheffield, UK", "Shenzhen, China",
    "Siem Reap, Cambodia", "Singapore, Singapore", "Sofia, Bulgaria", "Sorrento, Italy", "Southampton, UK",
    "Split, Croatia", "St. Louis, USA", "St. Moritz, Switzerland", "Stockholm, Sweden", "Strasbourg, France",
    "Stuttgart, Germany", "Surat, India", "Sydney, Australia", "Syracuse, Italy",
    
    "Taipei, Taiwan", "Tallinn, Estonia", "Tampa, USA", "Tangier, Morocco", "Tbilisi, Georgia",
    "Tehran, Iran", "Tel Aviv, Israel", "Thessaloniki, Greece", "Tianjin, China", "Tijuana, Mexico",
    "Tokyo, Japan", "Toronto, Canada", "Toulouse, France", "Trieste, Italy", "Tripoli, Libya",
    "Tucson, USA", "Tulsa, USA", "Tunis, Tunisia", "Turin, Italy",
    
    "Ulaanbaatar, Mongolia", "Udaipur, India", 
    
    "Valencia, Spain", "Valletta, Malta", "Vancouver, Canada", "Varanasi, India", "Venice, Italy",
    "Verona, Italy", "Victoria, Canada", "Vienna, Austria", "Vientiane, Laos", "Vilnius, Lithuania",
    
    "Warsaw, Poland", "Washington DC, USA", "Wellington, New Zealand", "Whistler, Canada", "Windhoek, Namibia",
    "Winnipeg, Canada",
    
    "Xian, China",
    
    "Yangon, Myanmar", "Yerevan, Armenia", "Yokohama, Japan", "York, UK",
    
    "Zagreb, Croatia", "Zanzibar, Tanzania", "Zurich, Switzerland"
]
