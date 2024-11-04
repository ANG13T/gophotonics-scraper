import requests
from bs4 import BeautifulSoup, Comment

# TODO: fix something with this method
def check_page_only_manufacturer(url):
    "Returns True if page only contains Manufacturer information"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    res = soup.select_one('#resultsBlock')
    return res == None

def get_manufacturer_details(url):
    only_man = check_page_only_manufacturer(url)
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    manufacturers = []
    if only_man:
        for item in soup.select('ul.dir-manu-list > li'):
            manufacturer = {}
            manufacturer['name'] = item.select_one('a.dir-manu-name').get_text(strip=True)
            manufacturer['url'] = item.select_one('a')['href']
            manufacturers.append(manufacturer)
    else:
        return []
        # TODO: someone please implement this
        # some suggestions:
        # 1. Invoke function to get the manufacturer details... we need to click the `#btnShowCompanies` button
        # 2. Some kind of nifty string parsing using BS4 Comments

def get_total_pages(url):
    """Returns a number denoting the total number of pages by analyzing the internal HTML."""
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find pagination element and extract all page numbers
        pagination = soup.select_one('div#pagingDiv')
        if pagination:
            page_links = pagination.select('li.page-item > a.page-link')

            # Filter valid numeric page links
            page_numbers = []
            for link in page_links:
                try:
                    page_number = int(link.get_text(strip=True))
                    page_numbers.append(page_number)
                except ValueError:
                    # Skip over "Previous" and "Next"
                    continue

            if page_numbers:
                return max(page_numbers)  # Return the highest page number found

        return 1  # Default to 1 page if no pagination found

    except requests.RequestException as e:
        print(f"Error fetching pagination data from {url}: {e}")
        return 1

def scrape_site_with_pagination(url):
    """Gets the total number of pages and then scrapes each page for items."""
    total_pages = get_total_pages(url)
    all_items = []

    if total_pages == 1:
        return {'items': [scrape_page(url)]}

    for page_number in range(1, total_pages + 1):
        page_url = f"{url}?page={page_number}"
        page_items = scrape_page(page_url)
        all_items.extend(page_items)

    return {'items': all_items}

def scrape_page(url):
    """Scrapes data from a single page and returns the items"""
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        items = []

        if check_page_only_manufacturer(url) == False:
            # Find all elements with the 'col-sm-8 col-md-7 col-lg-8 centerLeft centerLeft' class
            for item in soup.find_all(class_='col-sm-8 col-md-7 col-lg-8 centerLeft'):
                item_data = {}

                # TITLE: h3.prod-title > a (get the text inside the title link)
                title_tag = item.select_one('h3.prod-title > a')
                if title_tag:
                    item_data['title'] = title_tag.get_text(strip=True)

                    # LINK: h3.prod-title > a.href (get the href attribute of the link)
                    item_data['link'] = title_tag['href']

                # ORGANIZATION: .moreinfo > a.cur (get the organization link's text)
                org_tag = item.select_one('.moreinfo > a.cur')
                if org_tag:
                    item_data['organization'] = org_tag.get_text(strip=True)

                # SKU: .descriptiontext > TEXT (get text inside descriptiontext class)
                sku_tag = item.select_one('.descriptiontext')
                if sku_tag:
                    item_data['sku'] = sku_tag.get_text(strip=True)[4:]

                # DETAILS: .specs > .data-row > (.attribute + .value) (loop over data-row items to extract attribute-value pairs)
                details = {}
                spec_rows = item.select('.specs > .data-row')
                for row in spec_rows:
                    attribute = row.select_one('.attribute')
                    value = row.select_one('.value')
                    if attribute and value:
                        details[attribute.get_text(strip=True)] = value.get_text(strip=True)

                if details:
                    item_data['details'] = details

                items.append(item_data)
            return items
        else:
            manufacturers = get_manufacturer_details(url)
            return manufacturers

    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return []


def scrape_item(url):
    try:
        item_data = {}
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        item_title = soup.select_one('#ContentPlaceHolder1_lblProductName').get_text(strip=True)
        item_type = soup.select_one('#ContentPlaceHolder1_lblNodeSingularName').get_text(strip=True)
        item_manufacturer = soup.select_one('a#hlnkManuDisplayName').get_text(strip=True)
        item_manufacturer_url = soup.select_one('a#hlnkManuDisplayName')['href']
        item_description = soup.select_one('#ContentPlaceHolder1_lblPartCkEditor')
        if item_description:
            item_description = item_description.get_text(strip=True)
        else:
            item_description = "No description available"
        item_data['title'] = item_title
        item_data['type'] = item_type
        item_data['manufacturer'] = item_manufacturer
        item_data['manufacturer_url'] = item_manufacturer_url
        item_data['description'] = item_description
        item_data['specs'] = []
        product_specs = soup.select('.specs > #ContentPlaceHolder1_lblValues')

        for spec in product_specs:
            container = spec.select('.spec-container')
            for items in container:
                category_data = {}
                category_title = items.select_one('.spec-heading > h3').get_text(strip=True)
                specs = items.select('.spec-values > ul > li')
                category_data['title'] = category_title
                category_data['items'] = []
                if category_title != 'Technical Documents':
                    for item in specs:
                        category_field = {}
                        field = item.select_one('.field').get_text(strip=True)
                        value = item.select_one('.value').get_text(strip=True)
                        category_field['field'] = field
                        category_field['value'] = value
                        category_data['items'].append(category_field)
                    item_data['specs'].append(category_data)
        return item_data

    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return []