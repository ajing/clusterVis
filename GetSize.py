"""
    Get size of population from width of node
"""
import math

def GetSize(width):
    return 100 ** (width/0.3)

def GetWidth(size):
    return math.log(size, 100) * 0.3


if __name__ == "__main__":
    print "size is:", GetSize(0.15)
    print "width is:", GetWidth(25)
