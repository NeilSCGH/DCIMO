class tools():
  def __init__(self, args):
    self.args = args

  def argExist(self,argName): #check if the argument is provided
    return argName in self.args

  def getArgs(self): #get all the args
    return self.args

  def argValue(self,argName): #extract the value of the argument
    indx=self.args.index(argName)
    return self.args[indx+1]

  def argHasValue(self,argName):#Check if this arg has a valid value
    if not self.argExist(argName):
      return False

    indx=self.args.index(argName)
    if indx+1 == len(self.args): #if the argName is the last element
      return False #Missing value

    val=self.argValue(argName) 
    if val[0]=="-":#if the argName start with a -, it's not a value but the new arg
      return False
    return self.argExist(self.argValue(argName))