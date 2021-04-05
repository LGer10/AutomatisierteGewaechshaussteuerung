# automatisiertes gewächshaus | Results Class | version 0.1

# this class is used to transfer the current sensor data into threads
class Results:
  
  # contstructor of the class
  def __init__(self, result = {}):
    self._result = result
  
  # getter method
  def get_result(self):
    return self._result 
  
  # setter method
  def set_result(self,result):
    self._result = result