from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest

class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        # unittest 시작시 실행옵션
        self.browser =webdriver.Firefox(executable_path='E:\\books\\geckodriver-v0.30.0-win64\\geckodriver.exe')
        # 암묵적 대기 -> 나중에는 명시적대기로 변경해보라. p20
        self.browser.implicitly_wait(3)

    def tearDown(self):
        # unittest 종료시 종료 옵션
        self.browser.quit()
        
    def test_can_start_a_list_and_retriee_it_later(self):
        self.browser.get('http://localhost:8000')
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
        inputbox.send_keys(Keys.ENTER)

        import time
        time.sleep(1)
        # CSRF 오류 문제 확인용 코드
        # import time 
        # time.sleep(10)
        #/ CSRF 오류 문제 확인용 코드
        
        table= self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertTrue(
            any(row.text == '1: 공작깃털 사기' for row in rows),
            "신규작업이 테이블에 표시되지 않는다 -- 해당 텍스트:\n%s" % (
                table.text
            )
            
        )


        self.fail('Finish the test!')

if __name__ == '__main__':
    unittest.main(warnings='ignore')