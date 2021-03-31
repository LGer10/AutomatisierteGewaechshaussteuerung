class Results:
  def __init__(self, result = {}):
    self._result = result
  def get_result(self):
    return self._result 
  def set_result(self,result):
    self._result = result