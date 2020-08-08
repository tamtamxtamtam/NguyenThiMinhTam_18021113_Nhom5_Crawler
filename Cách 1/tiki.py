from bs4 import BeautifulSoup
import requests
import csv
import io
import re
from http.client import IncompleteRead



start_url = "https://tiki.vn"
page_url = "&_lc=&page={}"
form_url = "https://tiki.vn{}"

product_id_file = "D:/KTLab/PythonProject/untitled/tiki_product/tiki_product/data/product-id.txt"
product_data_file = "D:/KTLab/PythonProject/untitled/tiki_product/tiki_product/data/product.txt"
product_type_file = "D:/KTLab/PythonProject/untitled/tiki_product/tiki_product/data/product-type.txt"
product_file = "D:/KTLab/PythonProject/untitled/tiki_product/tiki_product/data/product.csv"
newpage = "D:/KTLab/PythonProject/untitled/tiki_product/tiki_product/data/newpage.txt"

#lấy danh sách link các loại sản phẩm
def crawl_product_type():
    i = 1;
    product_type_list = []
    response = requests.get(start_url)
    parser = BeautifulSoup(response.text, 'html.parser')
    product_type_box = parser.findAll('a', attrs={'class' : 'MenuItem__MenuLink-sc-181aa19-1 fKvTQu'})

    for product_type in product_type_box:
        product_type_list.append(product_type["href"])
        i+=1

    print(product_type_list[0])
    return product_type_list, i

def save_product_type(product_type_list=[]):
    file = io.open(product_type_file, "w+", encoding="utf-8")
    str = "\n".join(product_type_list)
    file.write(str)
    file.close()
    print("Save file: ", product_type_file)

#lấy link từng sản phẩm
def crawl_product_id(product_type_list=[]):
    print(product_type_list[0])
    print("hello")
    product_list = []

    for url in product_type_list:
        i = 1
        while (True):
            print("Crawl page: ", i)
            try:
                response = requests.get(url + page_url.format(i))
            except IncompleteRead:
                continue
            parser = BeautifulSoup(response.text, 'html.parser')
            product_box = parser.findAll('div', attrs={'class': 'product-item'})

            if (len(product_box) == 0):
                break

            for product in product_box:
                product_list.append(product.find('a')['href'])

            i += 1

    return product_list, i

def save_product_id(product_list=[]):
    file = io.open(product_id_file, "w+", encoding="utf-8")
    str = "\n".join(product_list)
    file.write(str)
    file.close()
    print("Save file: ", product_id_file)

def crawl_product(product_list=[]):
    file = io.open(product_file, "w", encoding="utf-8")
    csv_writer = csv.writer(file)

    count = 0
    if count == 0:
        csv_writer.writerow([
            'name', 'sku', 'seller_name', 'seller_link', 'img_link', 'price', 'original_price', 'brief',
            'description', 'info'
        ])
        count += 1
    for a in product_list:

        url = form_url.format(a)
        try:
            response = requests.get(url)
        except IncompleteRead:
            continue
        if (response.status_code != 200):
            continue


        print(response)
        parser = BeautifulSoup(response.text, 'html.parser')
        if (parser.title is not None):
            name = parser.title.string
        else:
            name = ""
        if (parser.find('div', {'class': 'brand'}).find_next('span') is not None):
            sku = parser.find('div', {'class': 'brand'}).find_next('span').string
        else:
            sku = ""
        if (parser.find('a', {'class': 'seller-name'}) is not None):
            seller_name = parser.find('a', {'class': 'seller-name'}).text
            seller_link = parser.find('a', {'class': 'seller-name'})['href']
        else:
            seller_name = ""
            seller_link = ""
        if (parser.find('div', {'class': 'container'}).find('img') is not None):
            img_link = parser.find('div', {'class': 'container'}).find('img')['src']
        else:
            img_link = ""
        if (parser.find('p', {'class': 'price'}) is not None):
            price = parser.find('p', {'class': 'price'}).text
        else:
            price = ""
        if (parser.find('p', {'class': 'original-price'}) is not None):
            original_price = parser.find('p', {'class': 'original-price'}).find_next().find_next().text
        else:
            original_price = ""
        if (parser.find('ul', {'class': 'list'})):
            brief = parser.find('ul', {'class': 'list'}).text
        else:
            brief = ""
        if (parser.find('div', {'class': 'content has-table'}) is not None):
            description = parser.find('div', {'class': 'content has-table'}).text
        else:
            description = ""
        info = ""
        for i in parser.findAll('h5'):
            info += i.text
        description1 = parser.find('div', attrs={'class': 'ToggleContent__View-sc-1hm81e2-0 eIzUuC'}).find_next(
            'div').find_next('p')
        while (True):
            if (description1 is None):
                break
            info += description1.text
            description1 = description1.find_next('p')

        csv_writer.writerow([
            name, sku, seller_name, seller_link, img_link, price,original_price, brief, description, info
        ])
    file.close()
    print("Save file: ", product_file)

    return


product_type_list, page1 = crawl_product_type()

save_product_type(product_type_list)
print("No. Type", len(product_type_list))

# crawl product id
product_list, page = crawl_product_id(product_type_list)

print("No. Page: ", page)
print("No. Product ID: ", len(product_list))

# save product id for backup
save_product_id(product_list)

# crawl detail for each product id

page2 = crawl_product(product_list)

# product_list = load_raw_product()
# save product to csv
#save_product_list()
