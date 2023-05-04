from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

my_urls = ["https://www.newegg.com/Product/ProductList.aspx?Submit=ENE&N=-1&IsNodeId=1&Description=GTX&bop=And&Page=1&PageSize=36&order=BESTMATCH",
        "https://www.newegg.com/Hewlett-Packard-Desktop-Graphics-Cards/BrandSubCat/ID-1186-48/Page-2"]


class WebScraping:
    def __init__(self, urls):
        self.urls = my_urls

        # single data
        self.brand = ""
        self.product_name = ""
        self.shipping = ""
        self.price = ""

        # total data
        self.brands = []
        self.product_names = []
        self.shippings = []
        self.prices = []


    @staticmethod
    def file_init():
        # name the output file to write to local disk
        filename = "graphic_cards.csv"
        # header of csv file to be written
        headers = "brand,product_name,shipping \n"
        # opens file, and writes headers
        f = open(filename, "w")
        f.write("")

        return f


    def page_init(self, current_url):
        # opens the connection and downloads html page from url
        uClient = uReq(current_url)

        # parses html into a soup data structure to traverse html
        # as if it were a json data type.
        page_soup = soup(uClient.read(), "html.parser")
        uClient.close()

        # finds each product from the store page
        containers = page_soup.findAll("div", {"class":"item-cell"})

        return containers



    def get_brand_name(self, container):
        brand_container = container.findAll("div", {"class":"item-info"})[0]
        self.brand = brand_container.div.img["title"]

    def get_product_name(self, container):
        title_container = container.findAll("a", {"class": "item-title"})[0]
        self.product_name = title_container.text

    def get_shipping_price(self, container):
        commercial_info_container = container.findAll("div", {"class": "item-action"})[0]
        shipping_container = commercial_info_container.findAll("li", {"class": "price-ship"})[0]
        self.shipping = shipping_container.text

    def get_product_price(self, container):
        commercial_info_container = container.findAll("div", {"class": "item-action"})[0]
        price_container = commercial_info_container.findAll("li", {"class": "price-current"})[0]
        dollars = price_container.strong.text.replace(",", "")
        pennies = price_container.sup.text.replace(".", "")
        self.price = dollars + "." + pennies


    def error_check(self, f):
        # catches any HTML false information or structure
        if "\n" in self.brand:
            f.write("Brand not found" + "," + self.product_name + "," + self.price + "," + self.shipping + "\n")
            return True

        if "\n" in self.product_name:
            f.write(self.brand + "," + "Product not found" + "," + self.price + "," + self.shipping + "\n")
            return True

        if "\n" in self.shipping:
            f.write(self.brand + "," + self.product_name + "," + self.price + "," + "Shipping price not found" + "\n")
            return True

        return False


    def main(self):
        f = self.file_init()

        for current_url in self.urls:
            containers = self.page_init(current_url)

            for container in containers:
                self.get_brand_name(container)
                self.get_product_name(container)
                self.get_shipping_price(container)
                self.get_product_price(container)

                if self.error_check(f):
                    continue

                # prints the dataset to console
                print("brand:" + self.brand)
                print("product_name:" + self.product_name)
                print("shipping:" + self.shipping)
                print("Price:" + self.price)


                f.write(self.brand + "," + self.product_name.replace(",", "|")
                        + "," + self.price + "," + self.shipping + "\n")


        f.close()



test = WebScraping(my_urls)
test.main()

