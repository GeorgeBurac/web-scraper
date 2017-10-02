import os
from bs4 import BeautifulSoup
from urllib.request import urlopen
import urllib.request
import bs4
import urllib
import sys

def get_ad_title(Beautiful_Soup_object):
    """This function extracts the title of the ad from the BeautifulSoup object provided.
    Daft.ie uses the address of the property as the ad title.
    The function accepts a BeautifulSoup object parsed as html, as a parameter."""
    ad_box = Beautiful_Soup_object.findChild("div", {"class":"box"})
    a_tag_data = ad_box.a #extracts the data in the <a><a> tag.
    ad_title_property = "".join(a_tag_data.text.strip().split(",")) # select the address of the property without commas
    return ad_title_property


def save_image(link, path_to_save, desired_image_name):
    """This function will save the image present at the link provided to the path provided."""
    current_working_directory = os.getcwd()
    os.chdir(path_to_save)
    image = urllib.request.urlretrieve(link, desired_image_name)
    os.chdir(current_working_directory)

def get_image_link(Beautiful_Soup_object):
    image_html = Beautiful_Soup_object.findChild("div", {"class": "image"}) # finds the div with the image link
    image = str(image) # transform the html into a string to extract the link to the image
    link_to_image = image.split('src="')[1] # get rid of html "fluff"
    link = link_to_image.split()[0][:-1] # select only the link
    return link

def get_number_of_beds(Beautiful_Soup_object):
    number_of_beds_html = Beautiful_Soup_object.findChild("ul", {"class":"info"}) # gets the part of html with the beds
    number_of_beds = number_of_beds_html.li.text.strip()[:-1] # selects only the number of beds
    return number_of_beds


def get_number_of_bathrooms(Beautiful_Soup_object):
    number_of_bathrooms_html = Beautiful_Soup_object.findChild("ul", {"class": "info"})
    number_of_bathrooms_with_extra_html = number_of_bathrooms_html.li.next_sibling.next_sibling
    number_of_baths_html = number_of_bathrooms_with_extra_html.next_sibling.next_sibling
    number_of_baths = number_of_baths_html.text.strip()
    return number_of_baths

link = "http://www.daft.ie/ireland/property-for-sale/?offset=0"
def link_update(link, pages_to_iterate):
    links = []
    pages_to_iterate *= 20
    """This function will update the link such that the web scraper will scrape the next page.
    The first argument taken is the link of the website, the second argument taken is the number of pages to iterate through.
    Daft.ie uses an offset of 20, therefore the number of pages to be iterated needs to be multiplied by 20.
    The multiplication is done by the function"""
    i = 0
    while i < pages_to_iterate:
        link = link.split("=") # daft.ie uses an = at the end of the link to specify the page,
        link = link[0] + "="  #it actually specifies the number of ads. There are 20 ads per page. Therefore, offset=20 is page 1
        link += "%d" % i
        links.append(link)
#        print(link)
        i += 20
    return links

def web_scraper(link):
    html_file = urlopen(link)
    html_data = html_file.read()
    html_file.close()
    raw_html = BeautifulSoup(html_data, "html.parser")
    house_ads = raw_html.findAll("div", {"class":"box"}) #stored as a list
    print(house_ads)
    with open("scraped data.csv") as f:
        i = 0
        while i < len(house_ads):
            property_title_with_address_and_type = " ".join(house_ads[i].a.text.strip().split(","))
            house_image_link = str(house_ads[i].findChild("div", {"class":"image"})).split()[-9][5:-1]
            urllib.request.urlretrieve(house_image_link, property_title_with_address_and_type)
            # the line above stores the image in the folder with the ads
            house_price = str(house_ads[i].findChildren("div", {"class":"info-box"})).split()[4][:-9]
            # optional_price_increase = str(house_ads[i].findChildren("span", {"class":"price-change-up"})).split(">")[-2][:-6]
            # above line is the optional price change, shown only in some ads, deprecated
            property_type = str(house_ads[i].findChildren("ul", {"class":"info"})).split("\n")[2].strip().split("<")[0]
            number_of_beds = str(house_ads[i].findChildren("ul", {"class":"info"})).split("\n")[4].strip().split("<")[0]
            to_be_written = str(property_title_with_address_and_type) + "," + str(house_image_link) + "," + str(house_price) + "," + str(property_type) + "," +  str(number_of_beds + "\n")
            f.write(to_be_written)
            print("Number: {}\nProperty title with address and type of property: {}\nLink to the image of the house: {}\nPrice of the property: {}\n\nProperty type: {}\nNumber of beds: {}".format(i, property_title_with_address_and_type, house_image_link, house_price, property_type, number_of_beds))
            i += 1




# print(len(house_ads))
# address_of_property = code.body.table.h2.text.strip()
# link_to_house_image =
# image_of_house = urllib.urlretrieve(link_to_house_image)
def main():
    """The for loop in this function 'glues' together the link_update function and the web_scraper function.
    The link_update function now returns a list of links."""
    link = "http://www.daft.ie/ireland/property-for-sale/?offset=0"
    pages_to_iterate = int(input("Please enter the number of pages to be iterated:"))
    links = link_update(link, pages_to_iterate)
    print(links)
    for link in links:
        web_scraper(link)

if __name__ == "__main__":
    main()
