comp = []
import src.CPU as item; comp.append(item); CPU = comp[len(comp)-1]
import src.GPU as item; comp.append(item); GPU = comp[len(comp)-1]
def init():
 print("\nInitalizing all Components...")
 for i in comp: i.reset()
#
def tick(): # may be unused...
 for i in comp: i.tick()
#

