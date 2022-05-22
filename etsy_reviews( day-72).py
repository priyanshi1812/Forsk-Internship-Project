""" Day - 72 

https://www.etsy.com

https://www.etsy.com/in-en/c/jewelry-and-accessories?ref=catnav-10855

https://www.etsy.com/in-en/c/jewelry/earrings/ear-jackets-and-climbers?ref=catnav-10855

Total 16 rows with 4 columns of data on each page = 64 products
Scrap total 250 pages 
4 reviews on each page , so in total = 16x4x250x4 = 64000
https://www.etsy.com/in-en/c/jewelry/earrings/ear-jackets-and-climbers?ref=pagination&page=1

https://www.etsy.com/in-en/listing/729104205/front-back-earrings?ga_order=most_relevant&ga_search_type=all&ga_view_type=gallery&ga_search_query=&ref=sc_gallery-1-1&plkey=0c99558876e43760f83a6a354ac6be0729fc64e2%3A729104205&pro=1&col=1

Store it in a Database and also in a csv file  """


# pip install webdriver_manager
import pickle
import time
from time import sleep
import logging
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
import os

startTime = time.time()
person = []
date = []
stars = []
review = []
sentiment = []
#define export_Data function -->
def export_Data():
    if 'ScrapRev11.csv' in os.listdir(os.getcwd()):
        df1 = pd.read_csv('ScrapRev11.csv')
        '''Exporting data'''
        
        
        
        for i in range(0,len(df1["Person"])):
            if df1["Person"][i] not in person:
                person.append(df1["Person"][i])
                date.append(df1["Date"][i])
                stars.append(df1["Stars"][i])
                review.append(df1["Reviews"][i])
                sentiment.append(df1["Sentiment"][i])
        
        dataframe1 = pd.DataFrame()
        dataframe1["Person"] = person
        dataframe1["Date"] = date
        dataframe1["Stars"] = stars
        dataframe1["Reviews"] = review
        dataframe1["Sentiment"] = sentiment
        
        result = pd.concat([df1,dataframe1])
        result.to_csv('ScrapRev11.csv',index=False)
    else:
        '''Exporting data'''
        dataframe1 = pd.DataFrame()
        dataframe1["Person"] = person
        dataframe1["Date"] = date
        dataframe1["Stars"] = stars
        dataframe1["Reviews"] = review
        dataframe1["Sentiment"] = sentiment
        dataframe1.to_csv('ScrapRev11.csv',index=False)

#define check review -->
def chk_REV(Cust_Statemnt):
    '''
    Check the review is positive or negative'''
    file = open("pickle_model.pkl", 'rb')
    pickle_model = pickle.load(file)
    file = open("features.pkl", 'rb')
    vocab = pickle.load(file)
    #Cust_Statemnt has to be vectorised, that vectorizer is not saved yet
    #load the vectorize and call transform and then pass that to model preidctor
    #load it later..................................
    Transf = TfidfTransformer()
    VectLoad = CountVectorizer(decode_error="replace",vocabulary=vocab)
    vectorise_REVIEW = Transf.fit_transform(VectLoad.fit_transform([Cust_Statemnt]))
    # add code to test the sentiment of using both the model
    # 0 == negative   1 == positive
    OP = pickle_model.predict(vectorise_REVIEW)
    return OP[0]

def LOAD_SCRAPPER(nPage):
    global person,review
    print("Starting Chrome:")
    global STP1
    STP1 = pd.DataFrame()
    
    WEB = webdriver.Chrome(ChromeDriverManager().install())

    loadLn ='https://www.etsy.com/in-en/c/jewelry-and-accessories?ref=pagination&nPage={}'
    
    try:
        #Count for every nPage of website
        
            
        loadLn = loadLn.format(nPage)
        WEB.get(loadLn)
        
        print("Scraping nPage:",nPage)
        #xpath of product table
        PATH_1 = '/html/body/div[5]/div/div[1]/div/div[4]/div[2]/div[2]/div[3]/div/div/ul'
        #getting total items
        items = WEB.find_element_by_xpath(PATH_1)
        items = items.find_elements_by_tag_name('li')
        #available items in nPage
        end_product = len(items)
        #Count for every product of the nPage
        for product in range(0,end_product):
            
            print("     Scarping reviews for product",product+1)
            #clicking on product
            try:
                items[product].find_element_by_tag_name('a').click()
            except:
                print('Product link not found')
                
            
            #switch the focus of driver to new tab
            windows = WEB.window_handles
            WEB.switch_to.window(windows[1])
            
                
            
            try:
                PATH_2 = '//*[@id="same-listing-reviews-panel"]/div'
                count = WEB.find_element_by_xpath(PATH_2)
                #Number of review on any nPage
                count = count.find_elements_by_class_name('wt-grid__item-xs-12')
                for r1 in range(1,len(count)+1):
                    DAT001 = WEB.find_element_by_xpath(
                                '//*[@id="same-listing-reviews-panel"]/div/div[{}]/div[1]/div[2]/p[1]'.format(
                                    r1)).text
                    if DAT001[:DAT001.find(',')-6] not in person:
                        try:
                            person.append(DAT001[:DAT001.find(',')-6])
                            date.append(DAT001[DAT001.find(',')-6:])
                        except Exception:
                            person.append("Not Found")
                            date.append("Not Found")
                        try:
                            stars.append(WEB.find_element_by_xpath(
                                '//*[@id="same-listing-reviews-panel"]/div/div[{}]/div[2]/div/div/div[1]/span/span[1]'.format(
                                    r1)).text[0])
                        except Exception:
                            stars.append("No stars")
                        try:
                            review.append(WEB.find_element_by_xpath(
                                '//*[@id="review-preview-toggle-{}"]'.format(r1-1)).text)
                            sentiment.append(chk_REV(WEB.find_element_by_xpath(
                                '//*[@id="review-preview-toggle-{}"]'.format(r1-1)).text))
                        except Exception:
                            review.append("No Review")
                            sentiment.append(chk_REV("No Review"))
            except Exception:
                try:
                    count = WEB.find_element_by_xpath('//*[@id="reviews"]/div[2]/div[2]')
                    count = count.find_elements_by_class_name('wt-grid__item-xs-12')
                    
                    for r2 in range(1,len(count)+1):
                        DAT001 = WEB.find_element_by_xpath(
                                    '//*[@id="reviews"]/div[2]/div[2]/div[{}]/div[1]/p'.format(r2)).text
                        if DAT001[:DAT001.find(',')-6] not in person:
                            try:
                                
                                person.append(DAT001[:DAT001.find(',')-6])
                                date.append(DAT001[DAT001.find(',')-6:])
                            except Exception:
                                person.append("Not Found")
                                date.append("Not Found")
                            try:
                                stars.append(WEB.find_element_by_xpath(
                                    '//*[@id="reviews"]/div[2]/div[2]/div[{}]/div[2]/div[1]/div[1]/div[1]/span/span[1]'.format(
                                        r2)).text[0])
                            except Exception:
                                stars.append("No Stars")
                            try:
                                review.append(WEB.find_element_by_xpath(
                                    '//*[@id="review-preview-toggle-{}"]'.format(
                                        r2-1)).text)
                                sentiment.append(chk_REV(
                                    WEB.find_element_by_xpath(
                                    '//*[@id="review-preview-toggle-{}"]'.format(
                                        r2-1)).text))
                            except Exception:
                                review.append("No Review")
                                sentiment.append(chk_REV(
                                    "No Review"))                                        
                except Exception:
                    try:
                        count = WEB.find_element_by_xpath('//*[@id="reviews"]/div[2]/div[2]')
                        count = count.find_elements_by_class_name('wt-grid__item-xs-12')
                        
                        for r3 in range(1,len(count)+1):
                            DAT001 = WEB.find_element_by_xpath(
                                        '//*[@id="same-listing-reviews-panel"]/div/div[{}]/div[1]/p'.format(r3)).text
                            if DAT001[:DAT001.find(',')-6] not in person:
                                try:
                                    person.append(DAT001[:DAT001.find(',')-6])
                                    date.append(DAT001[DAT001.find(',')-6:])
                                except Exception:
                                    person.append("Not Found")
                                    date.append("Not Found")
                                try:
                                    stars.append(WEB.find_element_by_xpath(
                                        '//*[@id="same-listing-reviews-panel"]/div/div[{}]/div[2]/div[1]/div[1]/div[1]/span/span[1]'.format(r3)).text[0])
                                except Exception:
                                    stars.append("No Stars")
                                try:
                                    review.append(WEB.find_element_by_xpath(
                                        '//*[@id="review-preview-toggle-{}"]'.format(r3-1)).text)
                                    sentiment.append(chk_REV(WEB.find_element_by_xpath(
                                        '//*[@id="review-preview-toggle-{}"]'.format(r3-1)).text))
                                except Exception:
                                    review.append("No Review")
                                    sentiment.append(chk_REV("No Review"))
                    except Exception:
                        print("Error")
                        continue
                
            WEB.close()
            #swtiching focus to main tab
            WEB.switch_to.window(windows[0])
            #export data after every product
            #export_Data()
        
        
    except Exception as e_1:
        print(e_1)
        print("Program stoped:")
    export_Data()
    WEB.quit()
    
    
    
#defining the main function
def main():
    logging.basicConfig(filename='solution_etsy.log', level=logging.INFO)
    logging.info('Started')
    if 'nPage.txt' in os.listdir(os.getcwd()):
        with open('nPage.txt','r') as file1:
            nPage = int(file1.read())
        for i in range(nPage,251):
            LOAD_SCRAPPER(i)
    else:
        for i in range(1,251):
            with open('nPage.txt','w') as file:
                file.write(str(i))
            LOAD_SCRAPPER(i)
    
    export_Data()
    print("--- %s seconds ---" % (time.time() - startTime))
    logging.info('Finished')
# Calling the main function 
if __name__ == '__main__':
    main()
    
    
    
    
    
    