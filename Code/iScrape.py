def fetch_restaurant(restaurant_name, location_name):
   
    """
    Search a restaurant by its name and location, get the fuzzy match and return its attributes and reviews.
    An index quantifying similarity and an error_code indicating potential errors are also returned.
    
    Parameters:
    -----------
    
    TEMPLATE
    (restaurant_name = str, location_name = str) -> attributes = pd.Series, reviewer = pd.DataFrame, fetched_restaurant = str, similarity_index = int, error_code = int / str
    
    INPUT
    restaurant_name: separated by space if multiple words incur
    location_name: in the order of: Building, Street, Boroughs. separated by space
    
    OUTPUT
    attributes: attributes of the restaurant, dummies with few exceptions
    review: include rating, text, date and reviewers' info
    fetched_restaurant: name of the fetched restaurant, possibly different from search name
    similarity_index: similarity between fetched name and search name, measured by fuzz.ratio function
    error_code: if empty str, nomral / if int, no data is returned / if non-empty str, incomplete data is returned
    ''  normal
    -1  fail to connect to search page
    -2  time out, fail to fetch potential restaurants list
    -3  fail to connect to restaurant page
    str errouneous reveiws indicated by str. e.g., '0/0/20/' indicates 2 errouneous reviews in the first batch of 20 reviews and 1 in the second.
    """
    
    
    from proxycrawl.proxycrawl_api import ProxyCrawlAPI
    from bs4 import BeautifulSoup
    from fuzzywuzzy import fuzz
    import pandas as pd
    import numpy as np
    import time
    import requests
    
    proxies = {'http': 'http://qitianma:1q2w3e4r@us-wa.proxymesh.com:31280',
               'https': 'http://qitianma:1q2w3e4r@us-wa.proxymesh.com:31280'}
    
    api = ProxyCrawlAPI({ 'token': 'pDH_j04XdH5SzYFv1LPJ1g' })
    
    # set error_code to be normal
    error_code = 0
    
    
    # set maximal trails to be 100
    n = 0
    
    MAXIMUM_TRAIL = 3
    while(n < MAXIMUM_TRAIL):
        time.sleep(np.random.uniform(1, 3))
        search_link = 'https://www.yelp.com/search?find_desc=' + restaurant_name + '&find_loc=' + location_name + '&ns=1'
        try:
#            search_content = BeautifulSoup(api.get(search_link)['body'])
            search_content = BeautifulSoup(requests.get(search_link).text)
        except:
            error_code = -1
            return (None, None, None, None, error_code)
        fetched_restaurants = search_content.find_all('a', {'class': "lemon--a__373c0__1_OnJ link__373c0__29943 link-color--blue-dark__373c0__1mhJo link-size--inherit__373c0__2JXk5"})
        if fetched_restaurants == []:
            fetched_restaurants = search_content.find_all('a', {'class': "biz-name js-analytics-click"})
        if fetched_restaurants != []:
            break
        n += 1
    
    if n == MAXIMUM_TRAIL:
        error_code = -2
        return (None, None, None, None, error_code)
    
    del n 
    
    
    # choose the most matching restaurant on the first seach page
    similarity = np.zeros(len(fetched_restaurants), dtype = 'int')
    for fetched_restaurant_index, fetched_restaurant in enumerate(fetched_restaurants):
        similarity[fetched_restaurant_index] = fuzz.ratio(restaurant_name.strip().lower(), fetched_restaurant.get_text().strip().lower())
    
    fetched_restaurant = fetched_restaurants[similarity.argmax()].get_text().strip()
    similarity_index = similarity.max()
    
    
    # set number of reviews to be 0
    n_reviews = 0
    
    # fetch restaurant data
    try:
        restaurant_link = 'https://www.yelp.com' + fetched_restaurants[similarity.argmax()].attrs['href'].split('?')[0] + '?start=' + str(n_reviews)
#        restaurant_content = BeautifulSoup(api.get(restaurant_link)['body'])
        restaurant_content = BeautifulSoup(requests.get(restaurant_link).text)
    except:
        error_code = -3
        return (None, None, None, None, error_code)
    
    try:
        overall_rating = restaurant_content.find('div', {'class': 'biz-rating biz-rating-very-large clearfix'}).find_next().attrs['title'].strip().split()[0].strip()
    except:
        overall_rating = np.nan
    try:
        overall_reviews = restaurant_content.find('span', {'class': 'review-count rating-qualifier'}).get_text().strip().split(' ')[0].strip()
    except:
        overall_reviews = np.nan
    try:
        price_range = restaurant_content.find('dd', {'class': 'nowrap price-description'}).get_text().strip()
    except:
        price_range = np.nan
    try:
        health_score = restaurant_content.find('dd', {'class': 'nowrap health-score-description'}).get_text().strip()
    except:
        health_score = np.nan
    head = restaurant_content.find('div', {'class':'short-def-list'})
    try:
        names = head.find_all('dt')
        values = head.find_all('dd')
    except:
        pass
    attributes = pd.Series(np.full(33, np.nan), index = ['Accepts Credit Cards',
                                                         'Accepts Bitcoin',
                                                         'Accepts Insurance',
                                                         'Alcohol',
                                                         'Appointment Only',
                                                         'Caters',
                                                         'Coat Check',
                                                         'Delivers',
                                                         'Dogs Allowed',
                                                         'Hair Types Specialized In',
                                                         'Happy Hour',
                                                         'Has TV',
                                                         'Bike Parking',
                                                         'Good for',
                                                         'Outdoor Seating',
                                                         'Parking',
                                                         'Smoking Allowed',
                                                         'Take-out',
                                                         'Takes Reservations',
                                                         'Waiter Service',
                                                         'Wheelchair Accessible',
                                                         'Wi-Fi',
                                                         'Opened 24hrs',
                                                         'Gender Neutral Restrooms',
                                                         'Ambience',
                                                         'Attire',
                                                         'Best Nights',
                                                         'Good For Dancing',
                                                         'Good For Groups',
                                                         'Good For Kids',
                                                         'Good For Meals Served',
                                                         'Music',
                                                         'Noise Level',
                                                         'Price Range'
                                                        ])
    for name, value in zip(names, values):
        if name.get_text().strip().title() in attributes:
            attributes[name.get_text().strip().title()] = value.get_text().strip()
    
    
    attributes = attributes.append(pd.Series({'price_range': price_range, 
                                              'health_score': health_score, 
                                              'overall_rating': overall_rating, 
                                              'overall_reviews': overall_reviews}))
    
    # fetch reviews data
    reviewer = pd.DataFrame({'er_name': [],
                             'er_location': [],
                             'er_freinds': [],
                             'er_reviews':[],
                             'er_photos': [],
                             'er_rating': [],
                             'er_date': [],
                             'er_text': [],
                             'er_useful': [],
                             'er_funny': [],
                             'er_cool': []
                            })
    
    error_code = ""
    
    MAXIMUM_REVIEW = 200
    while(n_reviews < MAXIMUM_REVIEW):
        try:
            reviews = restaurant_content.find_all('div', {'class':'review review--with-sidebar'})
            if reviews == []:
                break
            for review in reviews:
                text_tag = review.find('p')
                if text_tag.attrs['lang'].strip() != 'en':
                    continue
                er_text = text_tag.get_text().strip()
                er_name = review.find('a', {'class': 'user-display-name js-analytics-click'}).get_text().strip()
                er_location = review.find('li', {'class': 'user-location responsive-hidden-small'}).get_text().strip()
                try:
                    er_friends = review.find('li', {'class': 'friend-count responsive-small-display-inline-block'}).get_text().strip().split(' ')[0].strip()
                except:
                    er_friends = 0
                try:
                    er_reviews = review.find('li', {'class': 'review-count responsive-small-display-inline-block'}).get_text().strip().split(' ')[0].strip()
                except:
                    er_reviews = 0
                try:
                    er_photos = review.find('li', {'class': 'photo-count responsive-small-display-inline-block'}).get_text().strip().split(' ')[0].strip()
                except:
                    er_photos = 0
                er_rating = review.find('div', {'class': 'biz-rating biz-rating-large clearfix'}).find_next().find_next().attrs['title'].strip().split(' ')[0].strip()
                er_date = review.find('span', {'class': 'rating-qualifier'}).get_text().strip()
                statistics = review.find_all('span', {'class': 'count'})
                er_useful = statistics[0].get_text().strip()
                er_funny =  statistics[1].get_text().strip()
                er_cool = statistics[2].get_text().strip()
                reviewer = reviewer.append({'er_name': er_name,
                                            'er_location': er_location,
                                            'er_freinds': er_friends,
                                            'er_reviews': er_reviews,
                                            'er_photos': er_photos,
                                            'er_rating': er_rating,
                                            'er_date': er_date,
                                            'er_text': er_text,
                                            'er_useful': er_useful,
                                            'er_funny': er_funny,
                                            'er_cool': er_cool
                                }, ignore_index = True)
        except:
            error_code = error_code + str(n_reviews) + '/'
            continue
        print(fetched_restaurant, n_reviews)
        n_reviews += 20
        time.sleep(np.random.uniform(1, 3))
        try:
            restaurant_link = 'https://www.yelp.com' + fetched_restaurants[similarity.argmax()].attrs['href'].split('?')[0] + '?start=' + str(n_reviews)
#            restaurant_content = BeautifulSoup(api.get(restaurant_link)['body'])
            restaurant_content = BeautifulSoup(requests.get(restaurant_link).text)
        except:
            error_code = -3
            return (None, None, None, None, error_code)
    
    
    return (attributes, reviewer, fetched_restaurant, similarity_index, error_code)

def fetch_restaurants(data):
   
    """
    Fetch restaurants data from yelp and write them into three types of files:
    <CAMIS>.csv contains reviews
    attributes.csv contains restaurant attributes
    info.csv contains technical info during scraping
    
    Parameters:
    -----------
    
    TEMPLATE
    (data = pd.DataFrame) -> None
    
    INPUT
    data: DataFrame that contains columns of CAMIS, DBA, BUILDING, STREET and BORO
    """
    
    
    from datetime import datetime
    import pandas as pd
    import numpy as np
    import os
    
    directory = '../Yelp'
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    attributes_ls = []
    info = pd.DataFrame({'CAMIS':[],
                         'DBA':[],
                         'fetched_restaurant':[],
                         'similarity_index':[],
                         'error_code':[]
                        })
    for index, row in data.iterrows():
        try:
            restaurant_name = row['DBA']
            location_name = row['BUILDING'] + ' ' + row['STREET'] + ' ' + row['BORO']
            (attributes, reviewer, fetched_restaurant, similarity_index, error_code) = fetch_restaurant(restaurant_name, location_name)
            if isinstance(error_code, int): # error code is int. no data is returned.
                info = info.append({'CAMIS': row['CAMIS'],
                                'DBA': row['DBA'],
                                'fetched_restaurant': np.nan,
                                'similarity_index': np.nan,
                                'error_code': error_code,
                                'record_time': datetime.now()
                                    }, ignore_index = True)
                continue
            attributes.rename(row['CAMIS'], inplace = True)
            attributes_ls.append(attributes)
            temp_reviewer_path = '../Yelp/' + str(row['CAMIS']) + '.csv'
            if os.path.isfile(temp_reviewer_path):
                os.remove(temp_reviewer_path)
            reviewer.to_csv(temp_reviewer_path) # save review information of each restaurant to separate files, indicated by CAMIS 
            info = info.append({'CAMIS': row['CAMIS'],
                                'DBA': row['DBA'],
                                'fetched_restaurant': fetched_restaurant,
                                'similarity_index': similarity_index,
                                'error_code': error_code,
                                'record_time': datetime.now()
                               }, ignore_index = True)
        except:
            continue
    
    
    header_attr = not os.path.isfile('../Yelp/attributes.csv') 
    header_info = not os.path.isfile('../Yelp/info.csv') 
    pd.DataFrame(attributes_ls).to_csv('../Yelp/attributes.csv', mode = 'a', header = header_attr) # save restaurant attributes
    info.to_csv('../Yelp/info.csv', mode = 'a', header = header_info) # save scraping info