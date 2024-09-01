import requests
from bs4 import BeautifulSoup

# Set a base URL for concatenating with relative links extracted later
base_url = "https://forums.redflagdeals.com/"

def userMenu():
    """
    Displays the main menu options to the user.
    """
    print("***** Web Scraping Adventure *****")
    print("1. Display Latest Deals")
    print("2. Analyze Deals by Category")
    print("3. Find Top Stores")
    print("4. Log Deal Information")
    print("5. Exit")

def getListings():
    """
    Fetches the listings from the Hot Deals section of the website.

    Returns:
        listings (bs4.element.ResultSet): A list of BeautifulSoup elements containing deal listings.
    """
    response = requests.get("https://forums.redflagdeals.com/hot-deals-f9/")
    response.raise_for_status()  # Ensure the request was successful
    soup = BeautifulSoup(response.content, "html.parser")
    listings = soup.find_all("li", class_="row topic")  # Extract deal listings
    return listings

def extractInfo(listing, selector):
    """
    Extracts information from a single listing based on the provided CSS selector.

    Parameters:
        listing (bs4.element.Tag): The listing from which to extract information.
        selector (str): The CSS selector used to find the desired element within the listing.

    Returns:
        str: The extracted text content or "N/A" if the element is not found.
    """
    element = listing.select_one(selector)
    return element.text.strip() if element else "N/A"

def option1(listings):

    """
    This function allows us to display the latest deals to the user.
    For each component of the deals, we go and extract the information from the listing, by calling the extractInfo() method, and then we print it in the end.

    It takes in a parameter:
    - listing (BeautifulSoup): The BeautifulSoup object represents a deal listing.

    """

    counter = len(listings)
    print("\n")
    print("Total deals found: ", counter)
    print("\n")

    # Extracts the info by category.
    deals = []
    for listing in listings:
        store = extractInfo(listing, '.topictitle_retailer')
        item = extractInfo(listing, '.topic_title_link')
        votes = extractInfo(listing, '.total_count_selector')
        username = extractInfo(listing, '.thread_meta_author')
        timeStamp = extractInfo(listing, '.first-post-time')
        category = extractInfo(listing, '.thread_category a')
        replies = extractInfo(listing, '.posts')
        views = extractInfo(listing, '.views')
        url_element = listing.select_one('.topic_title_link')['href']
        url = base_url + url_element if url_element else "N/A"

        # Store each deal as a dictionary for easy sorting
        deal = {
            'store': store,
            'item': item,
            'votes': votes,
            'username': username,
            'timeStamp': timeStamp,
            'category': category,
            'replies': replies,
            'views': views,
            'url': url
        }
        deals.append(deal)

    # Sort deals based on user input
    sort_by = input("Sort by (votes/replies/views): ").lower()
    if sort_by in ['votes', 'replies', 'views']:
        deals.sort(key=lambda x: int(x[sort_by]), reverse=True)

    # Print sorted deals
    for deal in deals:
        print("Store: ", deal['store'])
        print("Item: ", deal['item'])
        print("Votes: ", deal['votes'])
        print("Username: ", deal['username'])
        print("Timestamp: ", deal['timeStamp'])
        print("Category: ", deal['category'])
        print("Replies: ", deal['replies'])
        print("Views: ", deal['views'])
        print("URL: ", deal['url'])
        print("---------------------------------")
        print("\n")

def option2(listings):
    """
    Analyzes and displays the number of deals by category.

    Parameters:
        listings (bs4.element.ResultSet): The listings to be analyzed.
    """
    catcount = {}

    # Count the number of listings in each category
    for listing in listings:
        category = extractInfo(listing, '.thread_category a')
        if category != "N/A":
            catcount[category] = catcount.get(category, 0) + 1

    # Display the deal counts by category
    longest_category = max(len(category) for category in catcount)
    longest_count = max(len(str(counter)) for counter in catcount.values())

    print("\n")
    print("Deals by Category:")
    print("\n")

    for category, counter in sorted(catcount.items()):
        count_str = f"{counter} deals".rjust(longest_count + 6)
        print(f"{category.rjust(longest_category)}: {count_str}")

    print("*" * (longest_category + longest_count + 9)) 
    print("\n")

def option3():
    """
    Prompts the user to enter a number and displays that many of the top stores by deal count.
    """
    storeNum = int(input("Enter the number of top stores to display: "))
    listings = getListings()

    # Count the number of deals for each store
    storeCount = {}
    for listing in listings:
        store = extractInfo(listing, '.topictitle_retailer')
        if store != "N/A":
            storeCount[store] = storeCount.get(store, 0) + 1

    # Display the top stores
    storesSort = sorted(storeCount.items(), key=lambda x: x[1], reverse=True)
    longest_store = max(len(store) for store, _ in storesSort[:storeNum])
    longest_count = max(len(str(count)) for _, count in storesSort[:storeNum])

    print("\nTop Stores")
    for store, counter in storesSort[:storeNum]:
        count_str = f"{counter} deals".rjust(longest_count + 6)
        print(f"{store.rjust(longest_store)} : {count_str}")

    print("*" * (longest_store + longest_count + 9))
    print("\n")

def option4():
    """
    Allows the user to select a category and logs the deal URLs for that category to a file.
    """
    listings = getListings()

    # Collect all unique categories
    cats = set()
    for listing in listings:
        category = extractInfo(listing, '.thread_category a')
        if category != "N/A":
            cats.add(category)

    # Display the categories
    print("\n")
    print("List of Categories:")
    print("\n")
    for i, category in enumerate(cats, start=1):
        print(f"{i}. {category}")

    # Log deal URLs for the selected category
    catchoice = int(input("Enter the number corresponding to the category: "))
    chosencat = list(cats)[catchoice - 1]

    catdeals = []
    for listing in listings:
        category = extractInfo(listing, '.thread_category a')
        if category == chosencat:
            url_element = listing.select_one('.topic_title_link')['href']
            url = base_url + url_element if url_element else "N/A"
            catdeals.append(url)

    with open('log.txt', "w") as f:
        for deal_link in catdeals:
            f.write(deal_link + '\n')
    
    print("All the links have been logged successfully.")
    print("\n")

def switch(choice):
    """
    Calls the appropriate function based on the user's menu choice.

    Parameters:
        choice (int): The user's menu choice.
    """
    if choice == 1:
        listings = getListings()
        option1(listings)
    elif choice == 2:
        listings = getListings()
        option2(listings)
    elif choice == 3:
        option3()
    elif choice == 4:
        option4()
    elif choice == 5:
        print("Exiting the program. Goodbye!")
        exit()
    else:
        print("Error, something went wrong.")

def main():
    """
    The main function that drives the program. It repeatedly displays the menu and processes the user's choice.
    """
    while True:
        userMenu()
        choice = int(input("Enter your choice (1-5): "))
        switch(choice)

        if choice == 5:
            break

if __name__ == "__main__":
    main()
