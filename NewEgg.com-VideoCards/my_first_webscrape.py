from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

my_urls = [
	"https://www.newegg.com/Product/ProductList.aspx?Submit=ENE&N=-1&IsNodeId=1&Description=GTX&bop=And&Page=1&PageSize=36&order=BESTMATCH",
	"https://www.newegg.com/Hewlett-Packard-Desktop-Graphics-Cards/BrandSubCat/ID-1186-48/Page-2"]


filename = "products.csv"
f = open(filename, "w")

headers = "brand, product_name, shipping\n"

f.write("")


for current_url in my_urls:

	# opening up connection, grabbing the page
	uClient = uReq(current_url)
	page_html = uClient.read()
	uClient.close()


	#html parsing
	page_soup = soup(page_html, "html.parser")

	#grabs each product's data
	containers = page_soup.findAll("div", {"class":"item-cell"})

	
	for container in containers:

		brand_container = container.findAll("div", {"class":"item-info"})[0]
		brand = brand_container.div.img["title"]

		title_container = container.findAll("a", {"class":"item-title"})[0]
		product_name = title_container.text

		comersial_info_container = container.findAll("div", {"class":"item-action"})[0]
		shipping_container = comersial_info_container.findAll("li", {"class":"price-ship"})[0]
		shipping = shipping_container.text


		price_container = comersial_info_container.findAll("li", {"class":"price-current"})[0]
		dollars = price_container.strong.text.replace(",", "")
		pennies = price_container.sup.text.replace(".", "")

		price = dollars + "." + pennies


		if "\n" in brand:
			f.write("Brand not found" + "," + product_name + "," + price + "," + shipping + "\n")
			continue
		if "\n" in product_name:
			f.write(brand + "," + "Product not found" + "," + price + "," + shipping + "\n")
			continue
		if "\n" in shipping:
			f.write(brand + "," + product_name + "," + price + "," + "Shipping price not found" + "\n")
			continue

		print("brand:" + brand)
		print("product_name:" + product_name)
		print("shipping:" + shipping)
		print("Price:" + price)

		f.write(brand + "," + product_name.replace(",", "|") + "," + price + "," + shipping + "\n")

f.close()