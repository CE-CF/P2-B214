class RelayBoxState(object):
    
   name = "state"
   allowed = []

   def switch(self, state):
        """ Switch to new state """
        if state.name in self.allowed:
            print ('Current: '+str(self)+' => switched to new state '+state.name)
            self.__class__ = state
        else:
            print ('Current: '+str(self)+' => switching to '+state.name+' not possible.')
        if (state.name == 'on'):
            self.switch(Inactive)

   def __str__(self):
      return self.name

class Off(RelayBoxState):
   name = "off"
   allowed = ['on', 'inactive']

class On(RelayBoxState):
   """ State of being powered on and working """
   name = "on"
   allowed = ['off','inactive']

class Active(RelayBoxState):
   """ State of being in suspended mode after switched on """
   name = "active"
   allowed = ['off']

class Inactive(RelayBoxState):
   """ State of being in hibernation after powered on """
   name = "inactive"
   allowed = ['active','off']

"""
class testClass():
    #Class for testing state
    def __init__(self):
        self.state = Off()

    def change(self, state):
        #Change state
        self.state.switch(state)

relayBox = testClass()

relayBox.change(On)
#relayBox.change(Inactive)
#relayBox.change(On)
relayBox.change(Active)
relayBox.change(Off)
"""