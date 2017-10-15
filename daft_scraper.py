import csv
import os
from bs4 import BeautifulSoup
from urllib.request import urlopen
import urllib.request
import bs4
import urllib
import sys


def get_short_ad_description(Beautiful_Soup_object):
    """This function extracts the short description of the advertised property. It works on a BeautifulSoup object."""
    try:
        description = Beautiful_Soup_object.find("div", {"class":"text-block"})
        description = description.p.text.strip().replace(",", "").replace("\n", "--").replace("\r", "--").replace("\t", "--")#.replace("\n", "").replace("\t", " ")
        return description
    except:
        pass


def get_property_type(Beautiful_Soup_object):
    """This function extracts the property type of the building advertised. It acts on a BeautifulSoup object."""
    try:
        property_type_html = Beautiful_Soup_object.findChild("ul", {"class":"info"})
        property_type = property_type_html.li.text.strip()[:-1]
        return property_type
    except:
        pass


def get_house_price(Beautiful_Soup_object):
    """This function extracts the price of the house from the ad. It works on a BeautifulSoup object."""
    try:
        price_html = Beautiful_Soup_object.find("strong", {"class":"price"}) # selects the strong tag
        price = price_html.text.replace(",", "") # select the actual price as a string
        return price
    except:
        pass


def get_ad_title(Beautiful_Soup_object):
    """This function extracts the title of the ad from the BeautifulSoup object provided.
    Daft.ie uses the address of the property as the ad title.
    The function accepts a BeautifulSoup object parsed as html, as a parameter."""
    try:
        a_tag_data = Beautiful_Soup_object.a.text #extracts the data in the <a><a> tag, returned as a string
        ad_title_property = a_tag_data.strip().split(",")  # select the address of the property without commas
        ad_title_property = " -- ".join(ad_title_property)
        return ad_title_property
    except:
        pass


def save_image(link, path_to_save, desired_image_name):
    """This function will save the image present at the link provided to the path provided."""
    try:
        if link[-4:] == ".jpg":
            desired_image_name = str(desired_image_name) + str(link[-4:])
        else:
             desired_image_name = str(desired_image_name) + str(link[-5:])
        #current_working_directory = os.getcwd()
        os.chdir(path_to_save)
        image = urllib.request.urlretrieve(link, desired_image_name)
        #os.chdir(current_working_directory)
    except:
        pass


def get_image_link(Beautiful_Soup_object):
    """This function extracts the link of the image from the ad. It works on a BeautifulSoup object."""
    try:
        image_html = Beautiful_Soup_object.findChild("div", {"class": "image"}) # finds the div with the image link
        link = image_html.find("img")["data-original"] #  select the src tag, containing the link
        return link
    except:
        pass


def get_number_of_beds(Beautiful_Soup_object):
    """This function extracts the number of beds from the ad. It uses a BeautifulSoup object"""
    try:
        number_of_beds_html = Beautiful_Soup_object.findChild("ul", {"class":"info"}) # gets the part of html with the beds
        number_of_beds = number_of_beds_html.li.text.strip()[:-1] # selects only the number of beds
        return number_of_beds
    except:
        pass


def get_number_of_bathrooms(Beautiful_Soup_object):
    """This function extracts the number of baths from the ad. It works on a BeautifulSoup object."""
    try:
        number_of_bathrooms_html = Beautiful_Soup_object.findChild("ul", {"class": "info"})
        number_of_bathrooms_with_extra_html = number_of_bathrooms_html.li.next_sibling.next_sibling
        number_of_baths_html = number_of_bathrooms_with_extra_html.next_sibling.next_sibling
        number_of_baths = number_of_baths_html.text.strip()
        return number_of_baths
    except:
        pass


def get_agent_name(Beautiful_Soup_object):
    """This function extracts the name of the agent that advertises the property. It works on a BeautifulSoup object."""
    try:
        agent_name_html = Beautiful_Soup_object.find("li", {"class":"agent-name-link truncate"})
        agent_name = agent_name_html.text[1:]
        return agent_name
    except:
        try:
            agent_name_html = Beautiful_Soup_object.find("ul", {"class":"links"}).li.next_sibling.next_sibling
            agent_name = agent_name_html.a.text# select the second item in the li tags and removes the "|" symbol
            return agent_name
        except:
            return ""
        pass

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


def define_output(property_title, house_price, number_of_beds, number_of_bathrooms, property_description, agent):
    """This is a helper function used to organise the output prior to writng it into a file."""
    try:
        output = property_title + "," + house_price + "," + number_of_beds + "," + number_of_bathrooms + "," + property_description + "," + agent + "\n"
        return output
    except:
        pass


def get_ad_link(Beautiful_Soup_object):
    """This function will extract the link of each ad."""
    ad_link = Beautiful_Soup_object.h2.a["href"] # select the link to the ad
    return "https://www.daft.ie" + ad_link # returns a string containing the link to the ad


def open_ad_link(ad_link):
    ad_details_html = urlopen(ad_link)
    ad_details_data = ad_details_html.read()
    ad_details_html.close()
    return ad_details_data

def save_all_ad_pictures_detail(folder_name, ad_title, ad_link):
    """This function will save all the images from an ad. It takes as a parameter a
    BeautifulSoup object, the name of the folder in which it will save the images and the title of the ad.
    The folder name should be the ad title."""
    try:
        ad_details_data = open_ad_link(ad_link)
        Beautiful_Soup_object = BeautifulSoup(ad_details_data, "html.parser")
        current_working_directory = os.getcwd()
        folder = current_working_directory + r"\\" + folder_name
        os.mkdir(folder)
        image_links = get_image_links_details(Beautiful_Soup_object)
        number = len(image_links)
        p = 0
        for link in image_links:
            save_image(link, folder, ad_title + str(p))
            p += 1
        os.chdir(current_working_directory)
    except:
        pass


def get_image_links_details(Beautiful_Soup_object):
    """This function will extract all the links to the images of the property and return them as items in a list."""
    images_html = Beautiful_Soup_object.findAll("li", {"class":"pbxl_carousel_item"})
    image_links = []
    for image in images_html:
        image_links.append(image.findChild("img")["src"])
    return image_links


def get_property_overview_detail(Beautiful_Soup_object):
    """This function will extract the detail of the property overview heading.
    The function takes as a parameter a BeautifulSoup object."""
    property_overview_detail = Beautiful_Soup_object.find("div", {"id":"overview"}).text.strip() #get the text and remove surrounding spaces
    property_overview = property_overview_detail.split("\n") #remove the newline character between the details
    return "".join(property_overview) # returns a string with the details



def get_stamp_duty(price):
    return "The stamp duty for purchasing this property is {}".format(price / 100)

def get_floor_area_detail(Beautiful_Soup_object):
    pass
    #floor_area_detail = Beautiful_Soup_object.find("div", )


def get_property_description_detail(ad_link):
    """This function extracts the detailed description of the ad. It uses the ad link as parameter."""
    html = open_ad_link(ad_link)
    Beautiful_Soup_object = BeautifulSoup(html, "html.parser")
    property_overview = get_property_overview_detail(Beautiful_Soup_object)
    description_detail = Beautiful_Soup_object.find("div", {"id":"description"}).text.replace("\n", " ").replace("\r", ";").replace(",", "-") #extract the text
    description = "".join(description_detail[:-35]).replace("\r", "")
    #print(description)
    return description[21:], property_overview[18:]


def get_property_address(ad_link):
    pass

def get_property_features_detail(Beautiful_Soup_object):
    """This function will extract the feature details of the property."""
    features = Beautiful_Soup_object.find("div", {"id":"features"}).split("\n")
    features = "--".join(features)
    return features


def web_scraper(link):
    html_file = urlopen(link)
    html_data = html_file.read()
    html_file.close()
    raw_html = BeautifulSoup(html_data, "html.parser")
    house_ads = raw_html.findAll("div", {"class":"box"}) #stored as a list
    f = open(r"C:\Users\George Burac\Desktop\p2\NSD\AlinProjects\Daft Scraper\scraped data.csv", "w+")
    f.write("Property title, Price, Beds, Bathrooms, Description, Agent\n")
    #csv_doc = csv.writer(f, dialect="excel")
    #print(link)
    i = 0
    while i < len(house_ads):
        print("i equals to: {}".format(i))
        property_title_with_address_and_type = get_ad_title(house_ads[i])
        print(property_title_with_address_and_type)
        #house_image_link = get_image_link(house_ads[i])
        #print(house_image_link)
        image_directory = r"C:\Users\George Burac\Desktop\p2\NSD\AlinProjects\Daft Scraper\Images"
        #save_image(get_image_link(house_ads[i]), image_directory, property_title_with_address_and_type)
        ad_link = get_ad_link(house_ads[i])
        save_all_ad_pictures_detail(property_title_with_address_and_type, property_title_with_address_and_type + str(i), ad_link)
        # the line above stores the image in the folder with the ads
        house_price = get_house_price(house_ads[i])
        #print(house_price)
        # optional_price_increase = str(house_ads[i].findChildren("span", {"class":"price-change-up"})).split(">")[-2][:-6]
        # above line is the optional price change, shown only in some ads, deprecated
        property_type = get_property_type(house_ads[i])
        #print(property_type)
        number_of_beds = get_number_of_beds(house_ads[i])
        #print(number_of_beds)
        number_of_bathrooms = get_number_of_bathrooms(house_ads[i])
        #print(number_of_bathrooms)
        description = get_property_description_detail(ad_link)
        #print(description)
        agent = get_agent_name(house_ads[i])

        #print(agent)
        #content = str(define_output(property_title_with_address_and_type, house_price, number_of_beds, number_of_bathrooms, short_description, agent))
        content = "Title: {}\nPrice: {}\nBeds: {}\nBathrooms: {}\nDescription: {}\nProperty overview: {}\nAgent: {}".format(property_title_with_address_and_type, house_price, number_of_beds, number_of_bathrooms, description[0], description[1], agent)
        print(content)
        print(type(content))
        output = "{},{},{},{},{},{},{}\n".format(property_title_with_address_and_type, house_price, number_of_beds, number_of_bathrooms, description[0], description[1], agent)

        f.write(output)

        i += 1



def main():
    """The for loop in this function 'glues' together the link_update function and the web_scraper function.
    The link_update function now returns a list of links."""
    link = "http://www.daft.ie/ireland/property-for-sale/?offset=0"
    pages_to_iterate = int(input("Please enter the number of pages to be iterated:"))
    links = link_update(link, pages_to_iterate)
    #print(links)

    f = open("scraped data.csv", "w")
    f.close()

    for link in links:
        web_scraper(link)


if __name__ == "__main__":
    main()
