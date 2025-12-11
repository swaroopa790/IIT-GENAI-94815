import arithmetic
import geometry
from geometry import calc_rect_peri

num1=int(input("enter num1:"))
num2=int(input("enter num2:"))

arithmetic.add(num1,num2)
arithmetic.subtract(num1,num2)

len=int(input("enter length:"))
br=int(input("enter breadth:"))

geometry.calc_rect_area(len, br)
geometry.calc_rect_peri(len, br)

