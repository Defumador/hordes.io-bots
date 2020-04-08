from driver import Driver
from mage import Mage
import time

d = Driver()
d.start()
input("Press ENTER...")
Mage(d).run()
