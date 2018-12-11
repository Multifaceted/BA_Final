	import delimited "C:\Users\knyag\Documents\business analytics/cleaned_data.csv", clear
	rename v1 CAMIS
    #preprocessing data
	label define alcohol2 0 "No" 1 "Beer & Wine Only" 2 "Full Bar"
	encode(alcohol), generate(alcohol2)
	label define delivery2 0 "No" 1 "Yes"
	encode(delivery), generate(delivery2)
	label define has_tv2 0 "No" 1 "Yes"
	encode(has_tv), generate(has_tv2)
	label define outdoor_seating2 0 "No" 1 "Yes"
	encode(outdoor_seating), generate(outdoor_seating2)
	label define parking2 0 "No" 1 "Yes"
	encode(parking), generate(parking2)
	label define bike_parking2 0 "No" 1 "Yes"
	encode(bike_parking), generate(bike_parking2)
	label define takeout2 0 "No" 1 "Yes"
	encode(takeout), generate(takeout2)
	label define takes_reservations2 0 "No" 1 "Yes"
	encode(takes_reservations), generate(takes_reservations2)
	label define wifi2 0 "No" 1 "Yes"
	encode(wifi), generate(wifi2)
	gen prices = price_range
	replace prices = "Under $10" if price_range == "Inexpensive"
	replace prices = "$11-30" if price_range == "Moderate"
	replace prices = "$31-60" if price_range == "Pricey"
	encode(prices), generate(prices2)
	label define noise_level2 0 "Quiet" 1 "Average" 2 "Loud" 3 "Very Loud"
	encode(noise_level), generate(noise_level2)
	label define cater2 0 "No" 1 "Yes"
	encode(cater), generate(cater2)
	drop if prices == "Above $61"

	xtset prices2
#model	
*full
xtologit overall_rating sentiment_score violation_score i.alcohol2 i.cater2 i.delivery2 i.has_tv2 i.outdoor_seating2 i.parking2 i.bike_parking2 i.takeout2 i.takes_reservations2 i.wifi2 ib1.noise_level2, vce(robust)
