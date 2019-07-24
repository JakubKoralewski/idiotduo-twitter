def assert_quote(quote):
	assert quote['autor']
	assert quote['autor'] != '' 
	assert quote['cytat'] 
	assert quote['cytat'] != ''
	assert quote['ksiega'] 
	assert quote['ksiega'] != ''
	assert quote['z'] 
	assert quote['z'] != ''

def assert_quote_slowo_na_dzis(quote):
	assert quote['autor']
	assert quote['autor'] != '' 
	assert quote['opis'] 
	assert quote['opis'] != ''
	assert quote['tytul'] 
	assert quote['tytul'] != ''
