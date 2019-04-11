# Unit testing all the pages

from  flaskweb import app
import unittest


class My_unit_testing(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True 

    def test_home_page1(self):
        tester = app.test_client(self)
        response = tester.get('http://127.0.0.1:5000/', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_home_page2(self):
        self.app = app.test_client()
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)
    
    def test_home_page3(self):
        self.app = app.test_client()
        response = self.app.get("/reference_product_selection")
        self.assertEqual(response.status_code, 200)
    
    def test_home_page4(self):
        result = self.app.get('/') 
        self.assertTrue('like to find some new features for' in str(result.data))
        self.assertTrue('Mobile' in str(result.data))
        self.assertTrue('Home' in str(result.data))
        # testing if all the external file like bootstrap, google fonts are loaded
        self.assertTrue('href="https://fonts.googleapis.com/css?family=Source+Sans+Pro:400,300,900,700,600,200"' in str(result.data))
        self.assertTrue('https://maxcdn.bootstrapcdn.com/font-awesome/4.6.2/css/font-awesome.min.css' in str(result.data))
        self.assertTrue('https://fonts.googleapis.com/css?family=Source+Sans+Pro:400,300,900,700,600,200' in str(result.data))
        self.assertTrue('https://maxcdn.bootstrapcdn.com/font-awesome/4.6.2/css/font-awesome.min.css' in str(result.data))
        self.assertTrue('https://www.google-analytics.com/analytics.js' in str(result.data))
        self.assertEqual(result.status_code, 200) 


    def test_feedback(self):
        # sends HTTP GET request to the application on the specified path
        result = self.app.get('/feedback') 
        # assert the status code of the response
        self.assertEqual(result.status_code, 200) 

    def test_faq(self):
        result = self.app.get('/faq') 
        self.assertEqual(result.status_code, 200) 
    
    def test_faq2(self):
        result = self.app.post('/faq') 
        self.assertEqual(result.status_code, 405) # It don't have post method
    
    def test_faq3(self):
        result = self.app.get('/faq') 
        self.assertTrue(b'Frequently Asked Questions' in result.data)
        self.assertTrue(b'What is Idea Studio?' in result.data)
        self.assertTrue(b'What do you offer?' in result.data)
        self.assertTrue(b'Will be there be login in the future?' in result.data)
        self.assertEqual(result.status_code, 200)

    def test_privacypolicy1(self):
        result = self.app.get('/privacypolicy') 
        self.assertEqual(result.status_code, 200) 
    
    def test_privacypolicy2(self):
        result = self.app.post('/privacypolicy') 
        self.assertEqual(result.status_code, 405) # It don't have post method
    
    def test_privacypolicy3(self):
        result = self.app.get('/privacypolicy') 
        self.assertTrue(b'Privacy Policy' in result.data)
        self.assertTrue(b'Third-Party disclosure' in result.data)
        self.assertTrue(b'behavioral tracking?' in result.data)
        self.assertTrue(b'Is this webpage and idea patented?' in result.data)
        self.assertEqual(result.status_code, 200)

    def test_sitemap1(self):
        result = self.app.get('/sitemap') 
        self.assertEqual(result.status_code, 200) 
    
    def test_sitemap2(self):
        result = self.app.post('/sitemap') 
        self.assertEqual(result.status_code, 405) # It don't have post method
    
    def test_sitemap3(self):
        result = self.app.get('/sitemap') 
        self.assertTrue(b'Site Map' in result.data)
        self.assertTrue(b'Reference Product Selection' in result.data)
        self.assertTrue(b'Revolution List G2' in result.data)
        self.assertTrue(b'Privacy Policy' in result.data)
        self.assertEqual(result.status_code, 200)

    def test_aboutus1(self):
        result = self.app.get('/aboutus') 
        self.assertEqual(result.status_code, 200) 
    
    def test_aboutus2(self):
        result = self.app.post('/aboutus') 
        self.assertEqual(result.status_code, 405) # It don't have post method
    
    def test_aboutus3(self):
        result = self.app.get('/aboutus') 
        self.assertTrue(b'About Us' in result.data)
        self.assertTrue(b'Jiyad Aglodiya' in result.data)
        self.assertTrue(b'Lava Shrestha' in result.data)
        self.assertTrue(b'Jack' in result.data)
        self.assertTrue(b'Emily Wang' in result.data)
        self.assertTrue(b'Andy' in result.data)
        self.assertEqual(result.status_code, 200)
    
    def test_contactus1(self):
        result = self.app.get('/contactus') 
        self.assertEqual(result.status_code, 200)
    
    def test_contactus2(self):
        result = self.app.post('/contactus') 
        self.assertEqual(result.status_code, 405) # It don't have post method
    
    def test_contactus3(self):
        result = self.app.get('/contactus') 
        self.assertTrue(b'Contacting Idea Studio' in result.data)
        self.assertTrue(b'Name:' in result.data)
        self.assertTrue(b'Email Address:' in result.data)
        self.assertTrue(b'Subject:' in result.data)
        self.assertTrue(b'Message:' in result.data)
        self.assertTrue(b'jagl9690@uni.sydney.edu.au' in result.data)
        self.assertEqual(result.status_code, 200)
    
    def test_feedback1(self):
        result = self.app.get('/feedback') 
        self.assertEqual(result.status_code, 200)
    
    def test_feedback2(self):
        result = self.app.post('/feedback') 
        self.assertEqual(result.status_code, 405) # It don't have post method
    
    def test_feedback3(self):
        result = self.app.get('/feedback') 
        self.assertTrue(b'Feedback' in result.data)
        self.assertTrue(b'Name:' in result.data)
        self.assertTrue(b'Email Address:' in result.data)
        self.assertTrue(b'Subject:' in result.data)
        self.assertTrue(b'provide us with comments regarding our website.' in result.data)
        self.assertTrue(b'Submit Feedback' in result.data)
        self.assertEqual(result.status_code, 200)

    def test_display_products2(self):
        result = self.app.get('/display_products2')        
        self.assertEqual(result.status_code, 200)

    def test_select_categories(self):
        result = self.app.get('/select_categories')        
        self.assertEqual(result.status_code, 200)
    
    def test_errorpage1(self):
        result = self.app.get('/data')
        self.assertEqual(result.status_code, 404) # Don't have this page.
    
    def test_errorpage2(self):
        result = self.app.get('/display_random')
        self.assertEqual(result.status_code, 404) # Don't have this page
    
    def test_server_error1(self):
        result = self.app.get('/revolution_list_g2')       
        # We dont do anything for get request for this page.
        # It returns None for get request which results in status code of 500 
        self.assertEqual(result.status_code, 500) 
    
    def test_server_error2(self):
        result = self.app.get('/revolution_list_g1')  
        # We dont do anything for get request for this page.
        # It returns None for get request which results in status code of 500      
        self.assertEqual(result.status_code, 500) 

    def test_server_error3(self):
        result = self.app.get('/display_similar_products') 
        # We dont do anything for get request for this page.
        # It returns None for get request which results in status code of 500       
        self.assertEqual(result.status_code, 500)
    
    def test_server_error4(self):
        result = self.app.get('/threshold')        
        # We dont do anything for get request for this page.
        # It returns None for get request which results in status code of 500
        self.assertEqual(result.status_code, 500)
    
    def test_server_error5(self):
        result = self.app.get('/matrix_display')   
        # We dont do anything for get request for this page.
        # It returns None for get request which results in status code of 500     
        self.assertEqual(result.status_code, 500)

    def test_server_error6(self):
        result = self.app.get('/feature_display')        
        # We dont do anything for get request for this page.
        # It returns None for get request which results in status code of 500
        self.assertEqual(result.status_code, 500)
    
    def test_server_error7(self):
        result = self.app.get('/display_products') 
        # We dont do anything for get request for this page.
        # It returns None for get request which results in status code of 500
        self.assertEqual(result.status_code, 500)
    
    def test_server_error8(self):
        result = self.app.get('/select_category_1')
        # We dont do anything for get request for this page.
        # It returns None for get request which results in status code of 500 
        self.assertEqual(result.status_code, 500)
    
    def test_identify_category1(self):
        result = self.app.post('/identify_category/Mobile%20Phones')
        self.assertEqual(result.status_code, 200)
    
    def test_identify_category2(self):
        result = self.app.post('/identify_category/Mobile')
        self.assertEqual(result.status_code, 500)
    
    def test_identify_category3(self):
        result = self.app.get('/identify_category')
        self.assertEqual(result.status_code, 404)
    
    def test_identify_category4(self):
        result = self.app.post('/identify_category/Mobile%20Phones')
        self.assertTrue(b'he product you selected belongs to' in result.data)
        self.assertTrue(b'Electronics' in result.data)
        self.assertEqual(result.status_code, 200)
    
    def test_display_products2_1(self):
        result = self.app.post('/display_products2')
        self.assertEqual(result.status_code, 200)
    
    def test_display_products2_2(self):
        result = self.app.post('/display_products2', data={'display_products': ['Samsung NX3000' , 'Nikon D800']})
        self.assertTrue('Samsung NX3000' in str(result.data))
        self.assertTrue('Nikon D800' in str(result.data))
        self.assertFalse('Playstation 4' in str(result.data))
        self.assertEqual(result.status_code, 200)
    
    def test_display_products2_3(self):
        result = self.app.get('/display_products2')
        self.assertTrue(b'Samsung Galaxy S III' in result.data)
        self.assertEqual(result.status_code, 200)

    def test_feature_display1(self):
        result = self.app.post('/feature_display' , data={'original': 'Samsung Galaxy S III'})
        self.assertEqual(result.status_code, 200)

    def test_feature_display2(self):
        result = self.app.post('/feature_display' , data={'original': 'Nikon D800'})
        self.assertEqual(result.status_code, 200)

    def test_feature_display3(self):
        result = self.app.post('/feature_display' , data={'original': ['Samsung NX3000' , 'Nikon D800']})
        self.assertTrue('Samsung NX3000' in str(result.data)) 
        self.assertTrue('Nikon D800' in str(result.data)) 
        self.assertTrue('select non-feature words to delete' in str(result.data))
        self.assertTrue('image' in str(result.data))
        self.assertTrue('key' in str(result.data))
        self.assertTrue('camera' in str(result.data))
        self.assertTrue('press' in str(result.data))
        self.assertTrue('Next' in str(result.data))
        self.assertTrue('Prev' in str(result.data))
        self.assertEqual(result.status_code, 200) 
    
    
    def test_matrix_display1(self):
        result = self.app.post('/matrix_display' , data={'original': 'Samsung Galaxy S III'})
        self.assertEqual(result.status_code, 200)

    def test_matrix_display2(self):
        result = self.app.post('/matrix_display' , data={'original': ['Samsung Galaxy S III' , 'Nikon D800']})
        self.assertEqual(result.status_code, 200)
    
    def test_matrix_display3(self):
        result = self.app.post('/matrix_display' , data={'original': ['Samsung Galaxy S III' , 'Nikon D800']})
        self.assertTrue('Matrix Display' in str(result.data)) 
        self.assertTrue('Cosine Similarity' in str(result.data))  
        self.assertTrue('0.548' in str(result.data))
    
    def test_matrix_display4(self):
        result = self.app.post('/matrix_display' , data={'original':''})
        self.assertEqual(result.status_code, 500)
    
    def test_matrix_display5(self):
        result = self.app.post('/matrix_display' , data={'original':'item_not_in_database'})
        self.assertEqual(result.status_code, 500)
    
    def test_matrix_display6(self):
        result = self.app.post('/matrix_display' , data={'original':'Nikon D800'})
        self.assertEqual(result.status_code, 500)
    
    def test_threshold1(self):
        result = self.app.post('/threshold' , data={'original': 'Samsung Galaxy S III'})
        self.assertEqual(result.status_code, 200)
    
    def test_threshold2(self):
        result = self.app.post('/threshold' , data={'original': ['Samsung Galaxy S III' , 'Nikon D800']})
        self.assertEqual(result.status_code, 200)
    
    def test_threshold3(self):
        result = self.app.post('/threshold')
        self.assertTrue('Lower limit' in str(result.data))
        self.assertTrue('Upper limit' in str(result.data))
        self.assertEqual(result.status_code, 200)
    
    def test_threshold4(self):
        result = self.app.post('/threshold' , data={'original':''})
        self.assertEqual(result.status_code, 200)

    def test_threshold5(self):
        result = self.app.post('/threshold' , data={'original':'item_not_in_database'})
        self.assertEqual(result.status_code, 200) #don't really care about what it has in its inputs
    
    def test_display_similar_products1(self):
        result = self.app.post('/display_similar_products', data={'original':'Samsung Galaxy S III', 'lowerlimit':'0.1', 'upperlimit':'0.9'})
        self.assertEqual(result.status_code, 200)
    
    def test_display_similar_products2(self):
        result = self.app.post('/display_similar_products', data={'original':'Samsung Galaxy S III' })
        self.assertEqual(result.status_code, 400)
    
    def test_display_similar_products3(self):
        result = self.app.post('/display_similar_products', data={'original': ['Samsung Galaxy S III' , 'Nikon D800'] , 'lowerlimit':'0.1', 'upperlimit':'0.9'})
        self.assertEqual(result.status_code, 200)
    
    def test_display_similar_products4(self):
        result = self.app.post('/display_similar_products')
        self.assertEqual(result.status_code, 400)
    
    def test_display_similar_products5(self):
        result = self.app.post('/display_similar_products', data={'original':'Nikon D800' , 'lowerlimit':'0.1', 'upperlimit':'0.9'})
        self.assertTrue('Nikon D800' in str(result.data))
        self.assertFalse('Samsung NX3000' in str(result.data))
        self.assertEqual(result.status_code, 200)
    
    def test_display_similar_products6(self):
        result = self.app.post('/display_similar_products' , data={'original':''})
        self.assertEqual(result.status_code, 400)
    
    def test_display_similar_products7(self):
        result = self.app.post('/display_similar_products' , data={'original':'item_not_in_database'})
        self.assertEqual(result.status_code, 400)
    
    def test_evolution_list1(self):
        result = self.app.post('/evolution_list', data={'original': ['Samsung NX3000' , 'Nikon D800']})
        self.assertEqual(result.status_code, 200)
    
    def test_evolution_list2(self):
        result = self.app.post('/evolution_list', data={'original': ['Samsung NX3000' , 'Nikon D800']})
        self.assertTrue('Evolution List for Samsung Galaxy S III' in str(result.data))
        self.assertTrue('Evolution List for Nikon D800' in str(result.data))
        self.assertTrue('Evolution List for Samsung NX3000' in str(result.data))
        self.assertEqual(result.status_code, 200)
    
    def test_evolution_list3(self):
        result = self.app.post('/evolution_list')
        self.assertEqual(result.status_code, 200)
    
    def test_evolution_list4(self):
        result = self.app.post('/evolution_list', data={'original': ''})
        self.assertEqual(result.status_code, 500)
    
    def test_evolution_list5(self):
        result = self.app.post('/evolution_list', data={'original': 'item_not_in_database'})
        self.assertEqual(result.status_code, 500)
    
    def test_revolution_list_g1_1(self):
        result = self.app.post('/revolution_list_g1', data={'original': ['Samsung NX3000' , 'Nikon D800']})
        self.assertEqual(result.status_code, 200)
    
    def test_revolution_list_g1_2(self):
        result = self.app.post('/revolution_list_g1', data={'original': ['Samsung NX3000' , 'Nikon D800']})
        self.assertFalse('G1 Revolution List for Samsung Galaxy S III' in str(result.data))
        self.assertTrue('G1 Revolution List for Nikon D800' in str(result.data))
        self.assertTrue('G1 Revolution List for Samsung NX3000' in str(result.data))
        self.assertEqual(result.status_code, 200)
    
    def test_revolution_list_g1_3(self):
        result = self.app.post('/revolution_list_g1')
        self.assertEqual(result.status_code, 200)
    
    def test_revolution_list_g1_4(self):
        result = self.app.post('/revolution_list_g1', data={'original': ''})
        self.assertEqual(result.status_code, 500)
    
    def test_revolution_list_g1_5(self):
        result = self.app.post('/revolution_list_g1', data={'original': 'item_not_in_database'})
        self.assertEqual(result.status_code, 500)
    
    def test_revolution_list_g2_1(self):
        result = self.app.post('/revolution_list_g2', data={'original': ['Samsung NX3000' , 'Nikon D800']})
        self.assertEqual(result.status_code, 200)
    
    def test_revolution_list_g2_2(self):
        result = self.app.post('/revolution_list_g2', data={'original': ['Samsung NX3000' , 'Nikon D800']})
        self.assertFalse('G2 Revolution List for Samsung Galaxy S III' in str(result.data))
        self.assertTrue('G2 Revolution List for Nikon D800' in str(result.data))
        self.assertTrue('G2 Revolution List for Samsung NX3000' in str(result.data))
        self.assertEqual(result.status_code, 200)
    
    def test_revolution_list_g2_3(self):
        result = self.app.post('/revolution_list_g2')
        self.assertEqual(result.status_code, 200)
    
    def test_revolution_list_g2_4(self):
        result = self.app.post('/revolution_list_g2', data={'original': ''})
        self.assertEqual(result.status_code, 500)
    
    def test_revolution_list_g2_5(self):
        result = self.app.post('/revolution_list_g2', data={'original': 'item_not_in_database'})
        self.assertEqual(result.status_code, 500)
    
    def test_select_categories1(self):
        result = self.app.post('/select_categories')
        self.assertEqual(result.status_code, 200)
    
    def test_select_categories2(self):
        result = self.app.get('/select_categories')
        self.assertEqual(result.status_code, 200)
    
    def test_select_categories3(self):
        result = self.app.post('/select_categories', data={'original': ['Electronics', 'Cameras & Optics' ]})
        self.assertTrue('Please select more category' in str(result.data))
        self.assertTrue('Electronics' in str(result.data))
        self.assertTrue('Cameras &amp; Optics' in str(result.data))
        self.assertEqual(result.status_code, 200)
    
    def test_select_categories4(self):
        result = self.app.post('/select_categories', data={'original': ['Electronics', 'Cameras & Optics' ],'check1': ['Cameras', 'Communications']})
        self.assertTrue('Video Conferencing' in str(result.data))
        self.assertTrue('Intercom Accessories' in str(result.data))
        self.assertTrue('Webcams' in str(result.data))
        self.assertTrue('Surveillance Cameras' in str(result.data))
        self.assertEqual(result.status_code, 200)
    
    def test_select_categories5(self):
        result = self.app.post('/select_categories', data={'original': ['Electronics', 'Cameras & Optics' ],'check1': ['Cameras', 'Communications'], 'check2': ['Digital Cameras','Telephony']})
        self.assertTrue('Telephony' in str(result.data))
        self.assertTrue('Film Cameras' in str(result.data))
        self.assertTrue('Borescopes' in str(result.data))
        self.assertTrue('Caller IDs' in str(result.data))
        self.assertEqual(result.status_code, 200)
    
    def test_select_categories6(self):
        result = self.app.post('/select_categories', data={'original': ['Electronics', 'Cameras & Optics' ],'check1': ['Cameras', 'Communications'], 'check2': ['Digital Cameras','Telephony'],'check3': ['Mobile Phones', 'Conference Phones']})
        self.assertTrue('Communication Radios' in str(result.data))
        self.assertTrue('Video Conferencing' in str(result.data))
        self.assertTrue('Video Cameras' in str(result.data))
        self.assertTrue('Webcams' in str(result.data))
        self.assertTrue('Pagers' in str(result.data))
        self.assertEqual(result.status_code, 200)
    
    # Check if all the categories from the databases are loaded or not for category selection
    def test_select_categories7(self):
        result = self.app.post('/select_categories')
        self.assertTrue('Animals &amp; Pet Supplies' in str(result.data))
        self.assertTrue('Apparel &amp; Accessories' in str(result.data))
        self.assertTrue('Arts &amp; Entertainment' in str(result.data))
        self.assertTrue('Baby &amp; Toddler' in str(result.data))
        self.assertTrue('Electronics' in str(result.data))
        self.assertTrue('Food, Beverages &amp; Tobacco' in str(result.data))
        self.assertTrue('Hardware' in str(result.data))
        self.assertTrue('Furniture' in str(result.data))
        self.assertTrue('Health &amp; Beauty' in str(result.data))
        self.assertTrue('Home &amp; Garden' in str(result.data))
        self.assertTrue('Luggage &amp; Bags' in str(result.data))
        self.assertTrue('Mature' in str(result.data))
        self.assertTrue('Media' in str(result.data))
        self.assertTrue('Office Supplies' in str(result.data))
        self.assertTrue('Software' in str(result.data))
        self.assertTrue('Sporting Goods' in str(result.data))
        self.assertTrue('Toys &amp; Games' in str(result.data))
        self.assertTrue('Vehicles &amp; Parts' in str(result.data))
        self.assertTrue('Religious &amp; Ceremonial' in str(result.data))
        self.assertEqual(result.status_code, 200)

if __name__ == '__main__':
    unittest.main()

    