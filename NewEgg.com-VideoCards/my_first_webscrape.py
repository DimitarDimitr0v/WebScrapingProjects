from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

# URl to web scrap from.
# In this example we web scrap graphics cards from Newegg.com
my_urls = [
	"https://www.newegg.com/Product/ProductList.aspx?Submit=ENE&N=-1&IsNodeId=1&Description=GTX&bop=And&Page=1&PageSize=36&order=BESTMATCH",
	"https://www.newegg.com/Hewlett-Packard-Desktop-Graphics-Cards/BrandSubCat/ID-1186-48/Page-2"]


# loops over the urls (can be modified to do it automatically instead if using list)
for current_url in my_urls:

	# opens the connection and downloads html page from url
	uClient = uReq(current_url)

	# parses html into a soup data structure to traverse html
	# as if it were a json data type.
	page_soup = soup(uClient.read(), "html.parser")
	uClient.close()


	# finds each product from the store page
	containers = page_soup.findAll("div", {"class":"item-cell"})



	# name the output file to write to local disk
	filename = "graphics_cards.csv"
	# header of csv file to be written
	headers = "brand,product_name,shipping \n"

	# opens file, and writes headers
	f = open(filename, "w")
	f.write("")


	# loops over each product and grabs attributes about
	# each product
	for container in containers:

		brand_container = container.findAll("div", {"class":"item-info"})[0]
		brand = brand_container.div.img["title"]

		title_container = container.findAll("a", {"class":"item-title"})[0]
		product_name = title_container.text

		commercial_info_container = container.findAll("div", {"class": "item-action"})[0]
		shipping_container = commercial_info_container.findAll("li", {"class": "price-ship"})[0]
		shipping = shipping_container.text


		price_container = commercial_info_container.findAll("li", {"class": "price-current"})[0]
		dollars = price_container.strong.text.replace(",", "")
		pennies = price_container.sup.text.replace(".", "")

		price = dollars + "." + pennies

		# catches any HTML false information or structure
		if "\n" in brand:
			f.write("Brand not found" + "," + product_name + "," + price + "," + shipping + "\n")
			continue
		if "\n" in product_name:
			f.write(brand + "," + "Product not found" + "," + price + "," + shipping + "\n")
			continue
		if "\n" in shipping:
			f.write(brand + "," + product_name + "," + price + "," + "Shipping price not found" + "\n")
			continue

		# prints the dataset to console
		print("brand:" + brand)
		print("product_name:" + product_name)
		print("shipping:" + shipping)
		print("Price:" + price)

		# writes the dataset to file
		f.write(brand + "," + product_name.replace(",", "|") + "," + price + "," + shipping + "\n")

f.close()
