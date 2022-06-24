#----------------------------------------------------------------------------#
#-  precious_metal_prices.py                                                -#
#-                                                                          -#
#-  A free, web-scrapey way of getting market prices of precious metals     -#
#-                                                                          -#
#-  David Mays - 6/23/22                                                    -#
#-  david@davidmays.io
#----------------------------------------------------------------------------#


from bs4 import BeautifulSoup
from urllib.request import Request, urlopen


class precious_metal_prices(object):

    def __init__(self):
        self.supported_metals = ["gold", "silver", "platinum", "palladium"]

    def get_metal_prices_usd(self, metal):

        if metal not in self.supported_metals:
            raise Exception(f"Unsupported metal type {metal}")

        site = f"https://gainesvillecoins.com/charts/{metal}-spot-price"
        hdr = {'User-Agent': 'Mozilla/5.0'}
        req = Request(site, headers=hdr)
        page=urlopen(req)
        soup = BeautifulSoup(page, features="html.parser")

        price_chart = soup.find("div", class_="chart-info__table-inner")
        weights = price_chart.findAll("span", class_="amount")
        raw_prices = price_chart.findAll("span", class_="ask")

        price_list = {}
        for i, weight in enumerate(weights):
            price_list[(weight.text).lower()] = float((raw_prices[i].text).replace('$','').replace(',',''))
        return price_list

    def get_gold_prices_usd(self):
        return self.get_metal_prices_usd("gold")

    def get_silver_prices_usd(self):
        return self.get_metal_prices_usd("silver")

    def get_platinum_prices_usd(self):
        return self.get_metal_prices_usd("platinum")

    def get_palladium_prices_usd(self):
        return self.get_metal_prices_usd("palladium")

    def get_all_prices(self):
        prices = {}
        for metal in self.supported_metals:
            prices[metal] = {}
            metal_prices = self.get_metal_prices_usd(metal)
            for weight in metal_prices:
                prices[metal][weight] = metal_prices[weight]
        return prices

    def print_all_prices(self):
        prices = self.get_all_prices()
        for metal in prices:
            print(
                f"\n{metal}:\n",
                "---------------------------\n",
                end="",
                )
            for weight in prices[metal]:
                print(f"\t{weight} - {prices[metal][weight]}")

if __name__ == "__main__":
    price = precious_metal_prices()
    print(price.print_all_prices())
