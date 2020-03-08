from selenium import webdriver
#导入鼠标动作链
from selenium.webdriver.common.action_chains import ActionChains
import time

def get_tracks(distance):
    #初速度
    v = 0
    #单位时间为0.3秒来统计轨迹，轨迹即0.3秒内的位移
    t = 0.3
    #位移（轨迹）列表，列表内的一个元素代表0.2s的位移
    teacks= []
    #当前位移
    current = 0
    #到达mid值开始减速
    mid = distance*4/5
    while current < distance:
        if current < mid:
            a = 2
        else:
            #加速度越小，单位时间的位移越小，模拟的轨迹就越多越详细
            a = -3

        v0 = v

        s = v0*t + 0.5*a*(t**2)

        current += s
        #添加到轨迹列表
        teacks.append(round(s))

        v = v0 + a*t
    return teacks

driver = webdriver.Chrome()

driver.get('https://www.douban.com/')
#转化到新的iframe,传入参数0代表第一个iframe
driver.switch_to.frame(0)
#由于有iframe,点击不到密码登陆，需要转化到iframe
driver.find_element_by_xpath('/html/body/div[1]/div[1]/ul[1]/li[2]').click()

driver.find_element_by_xpath('//*[@id="username"]').send_keys('你的账号')
driver.find_element_by_xpath('//*[@id="password"]').send_keys('你的密码')
driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div[5]/a').click()

time.sleep(3)

driver.switch_to.frame(0)
#每次验证码滑动距离都一样，总和为为205
element = driver.find_element_by_xpath('//*[@id="tcaptcha_drag_thumb"]')
#perform()鼠标漂浮
ActionChains(driver).click_and_hold(on_element=element).perform()
ActionChains(driver).move_to_element_with_offset(to_element=element,xoffset=160,yoffset=0).perform()
# ActionChains(driver).release().perform()

tracks = get_tracks(50)
# ActionChains(driver).click_and_hold(on_element=element).perform()
for track in tracks:
    ActionChains(driver).move_by_offset(xoffset=track, yoffset=0).perform()
time.sleep(1)
ActionChains(driver).release().perform()


