def one_space(string):
   while string.find("  ")>=0:
      string = string.replace("  "," ")
   return string

