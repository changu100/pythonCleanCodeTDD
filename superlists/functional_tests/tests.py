from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
import time
class NewVisitorTest(LiveServerTestCase):
    def setUp(self):
        # unittest 시작시 실행옵션
        self.browser =webdriver.Firefox(executable_path='E:\\books\\geckodriver-v0.30.0-win64\\geckodriver.exe')
        # 암묵적 대기 -> 나중에는 명시적대기로 변경해보라. p20
        self.browser.implicitly_wait(3)

    def tearDown(self):
        # unittest 종료시 종료 옵션
        self.browser.quit()
    
    def check_for_row_in_list_table(self, row_text):
        table= self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retriee_it_later(self):
        self.browser.get(self.live_server_url)
        self.assertIn('To-Do',self.browser.title)
        header_text= self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do',header_text)

        #그녀는 바로 작업을 추가하기로한다. 
        inputbox = self.browser.find_element_by_id('id_new_item')

        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            '작업 아이템 입력'
        )

        # "공작깃털 사기"라고 테스트 상자에 입력한다
        # (에디스의 취미는 날치 잡이용 그물을 만드는 것이다.)
        inputbox.send_keys('공작 깃털 사기')
        inputbox.send_keys(Keys.ENTER)
        
        time.sleep(1)
        
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('공작 깃털을 이용해서 그물 만들기')
        inputbox.send_keys(Keys.ENTER)

        time.sleep(1)
        # CSRF 오류 문제 확인용 코드
        # import time 
        # time.sleep(10)
        #/ CSRF 오류 문제 확인용 코드
        

        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url,'/list/.+')

        self.check_for_row_in_list_table('1: 공작 깃털 사기')
        self.check_for_row_in_list_table('2: 공작 깃털을 이용해서 그물 만들기')

        ## We use a new browser session to make sure that no information
        ## of Edith's is coming through from cookies etc
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Francis visits the home page.  There is no sign of Edith's
        # list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('공작 깃털 사기', page_text)
        self.assertNotIn('그물 만들기', page_text)

        # Francis starts a new list by entering a new item. He
        # is less interesting than Edith...
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('우유 사기')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: 우유 사기')

        # Francis gets his own unique URL
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)

        # Again, there is no trace of Edith's list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('공작 깃털 사기', page_text)
        self.assertIn('우유 사기', page_text)

