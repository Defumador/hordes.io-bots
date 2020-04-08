# import os.path
import time
from selenium.webdriver.common.keys import Keys
LEVEL = 1
GOOD = 2
LOW = 1
DIE = 0
HEALTH_LIMIT = 0.2 # 20%
MANA_LIMIT = 0.2   # 20%
DELAY = 0.2

class Mage:

    def __init__(self, webdriver):
        self.webdriver = webdriver
        self.driver = webdriver.driver
        self.components = []
        self.action = self.driver.find_element_by_tag_name("body")
    
    def run(self):
        """
        Main loop
        """
        # enemy_previous_health = -1

        while True:
            # try:
                self.get_components()
                print(self.components)
                
                if self.components:
                    self.player = self.components[0]
                    self.enemy = self.components[1]
                    p_health = self.check_health()
                    p_mana = self.check_mana()

                    if self.enemy[0]:
                        if p_health == DIE:
                            self.respawn()
                            continue
                        elif p_health == LOW:
                            # use health potion
                            self.action.send_keys(9)

                        if p_mana == LOW:
                            # use mana potion
                            self.action.send_keys(0)
                        
                        if self.enemy[2] != 0:
                            print("sending attack")
                            self.action.send_keys(1)
                            time.sleep(1.5)
                    else:
                        self.find_enemy()

                    time.sleep(DELAY)
                else:
                    raise Exception("Could not find necessary components")
            # except Exception as e:
            #     print(e)
            #     self.webdriver.quit()

    def check_health(self):
        """
        check player's health. LOW when <50%
        """
        max_health = self.player[0]
        current_health = self.player[1]
        
        if current_health == 0:
            return DIE

        return LOW if current_health < max_health * HEALTH_LIMIT else GOOD

    def check_mana(self):
        """
        check player's mana. LOW when < MANA_LIMIT
        """
        max_mana = self.player[2]
        current_mana = self.player[3]

        return LOW if current_mana < max_mana * MANA_LIMIT else GOOD

    def find_enemy(self):
        self.action.send_keys(Keys.TAB)

    def respawn(self):
        print("respawn..")
        pass

    def get_components(self):
        """
        Find and get all components (health bar, mana bar, info)
        """
        try:
            health = self.driver.find_element_by_xpath("//*[@id='ufplayer']/div[2]/div[1]/div[1]/span[2]").text
            print(f"get player health: {health}")
            current_health, max_health = health.split("/")

            mana = self.driver.find_element_by_xpath("//*[@id='ufplayer']/div[2]/div[2]/div[1]/span[2]").text
            print(f"get player mana: {mana}")
            if mana == "-0.0":
                time.sleep(DELAY)
                mana = self.driver.find_element_by_xpath("//*[@id='ufplayer']/div[2]/div[2]/div[1]/span[2]").text
                print(f"get player mana: {mana}")
            current_mana, max_mana = mana.split("/")

            e_is_alive = self.driver.find_elements_by_id('uftarget') != []
            e_current_health = 0
            e_max_health = 0
            if e_is_alive:
                health = self.driver.find_element_by_xpath("//*[@id='uftarget']/div[2]/div[1]/div[1]/span[2]").text
                print(f"get enemy health: {health}")
                e_current_health, e_max_health = health.split("/")

            self.components = [
                [
                    int(max_health), 
                    int(current_health),
                    int(max_mana),
                    int(current_mana)
                ],
                [
                    e_is_alive,
                    int(e_max_health), 
                    int(e_current_health)
                ]
            ]
        except AttributeError:
            print("Could not retrieve necessary components...")
