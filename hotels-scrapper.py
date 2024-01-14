from playwright.sync_api import sync_playwright
import pandas as pd


def main():
    
    with sync_playwright() as p:
        
        # IMPORTANT: change date to wathever hotels date you want to get
        checkin_date = '2024-01-21'
        checkout_date = '2024-01-22'
        
        page_url = f'https://www.qantas.com/hotels/properties/18482?adults=2&checkIn={checkin_date}&checkOut={checkout_date}&children=0&infants=0&location=London%2C%20England%2C%20United%20Kingdom&page=1&payWith=cash&searchType=list&sortBy=popularity.json'

        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(page_url, timeout=60000)
                    
        hotels = page.locator('//div[@class="css-du5wmh-Box e1m6xhuh0"]').all()
        print(f'There are: {len(hotels)} hotels.')

        hotels_list = []
        rates=[]
        for hotel in hotels:
            hotel_dict = {}
            hotel_dict['Room_name'] = hotel.locator('//h3[@class="css-19vc6se-Heading-Heading-Text e13es6xl3"]').inner_text()
            hotel_dict['Rate_name'] = hotel.locator('//h3[@class="css-10yvquw-Heading-Heading-Text e13es6xl3"]').inner_text()
            hotel_dict['Number_of_Guests'] = hotel.locator('//span[@data-testid="offer-guest-text"]').inner_text().split('•')[0].strip()
            hotel_dict['Cancellation_Policy'] = hotel.locator('//span[@data-testid="cancellation-policy-message"]').inner_text()
            hotel_dict['Price'] = hotel.locator('//div/div[3]/div[1]/div/div[2]/div/div[1]/div[2]/div[1]/div/div/span[2]').inner_text()
            hotel_dict['Currency'] = hotel.locator('//span[@class="css-17uh48g-Text e1j4w3aq0"]').inner_text().split()[0]

            hotels_list.append(hotel_dict)
            rates.append(hotel_dict)
        for rate in rates:
            print(rate)
        df = pd.DataFrame(hotels_list)
        df.to_excel('hotels_list.xlsx', index=False) 
        df.to_csv('hotels_list.csv', index=False) 
        
            
        browser.close()
            
if __name__ == '__main__':
    main()