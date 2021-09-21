from selenium import webdriver
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
        self.fail('Finish the test!')

if __name__ == '__main__':
    unittest.main(warnings='ignore')