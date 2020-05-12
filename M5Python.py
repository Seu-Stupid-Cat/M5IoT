from m5stack import *
from m5ui import *
from uiflow import *
import unit
import machine

#初始化M5
remoteInit()
#设置屏幕颜色
setScreenColor(0x222222)

#从Unit获取数据
env2 = unit.get(unit.ENV, unit.PORTA)
light4 = unit.get(unit.LIGHT, unit.PORTB)
pir2 = unit.get(unit.PIR, unit.PORTC)

#设置标签
Light = M5TextBox(180, 90, "Light", lcd.FONT_Default,0xFFFFFF, rotate=0)
Temperat = M5TextBox(179, 28, "Temperature", lcd.FONT_Default,0xFFFFFF, rotate=0)
label0 = M5TextBox(72, 28, "Temperature", lcd.FONT_Default,0xFFFFFF, rotate=0)
label1 = M5TextBox(74, 90, "Light", lcd.FONT_Default,0xFFFFFF, rotate=0)
label3 = M5TextBox(182, 204, "Text", lcd.FONT_Default,0xFFFFFF, rotate=0)
label2 = M5TextBox(75, 150, "PIR", lcd.FONT_Default,0xFFFFFF, rotate=0)
label4 = M5TextBox(75, 205, "Text", lcd.FONT_Default,0xFFFFFF, rotate=0)
PIR = M5TextBox(181, 148, "PIR", lcd.FONT_Default,0xFFFFFF, rotate=0)

#初始化标签
uart = None
Temperature = None
Times = None
counter_1 = None
Text = None
Text_1 = None
counter = None
Light_Value = None
PIR_Value = None

#定义计数器函数
def dosomething2():
  global uart, Temperature, Times, counter_1, Text, Text_1, counter, Light_Value, PIR_Value
  if Light_Value <= 300 and PIR_Value == 1:
    counter = counter + 10
  elif Light_Value <= 300 and PIR_Value == 0:
    if counter > 0:
      counter_1 = counter_1 + 1
    counter = 0
  return counter_1


#定义远程发送数据
def _remote_温度():
  global Temperature, Times, counter_1, Text, Text_1, counter, Light_Value, PIR_Value, env2, light4, pir2, dosomething2
  Temperature = env2.temperature
  return Temperature
def _remote_次数():
  global Temperature, Times, counter_1, Text, Text_1, counter, Light_Value, PIR_Value, env2, light4, pir2, dosomething2
  Times = dosomething2()
  return Times
def _remote_老人身体状况():
  global Temperature, Times, counter_1, Text, Text_1, counter, Light_Value, PIR_Value, env2, light4, pir2, dosomething2
  if counter_1 >= 3:
    Text = 'Warning!!!'.encode()
  else:
    Text = 'Normal'.encode()
  return Text
def _remote_温度情况():
  global Temperature, Times, counter_1, Text, Text_1, counter, Light_Value, PIR_Value, env2, light4, pir2, dosomething2
  if Temperature >= 36:
    Text_1 = "It's too hot!!!".encode()
  elif Temperature <= 16:
    Text_1 = "It's too cold!!!".encode()
  else:
    Text_1 = 'Suitable temperature'.encode()
  return Text_1

#Uart端口重映射
uart = machine.UART(2, tx=17, rx=16)
uart.init(921600, bits=8, parity=None, stop=1)

#初始化计数器
counter = 0
counter_1 = 0

#UI设计
lcd.rect(40, 30, 10, 10, color=0xffff00)
lcd.rect(40, 90, 10, 10, color=0xffff00)
lcd.rect(40, 150, 10, 10, color=0xffff00)

#自动开关灯主函数设计
while True:
  Light.setText(str(light4.analogValue))
  Temperat.setText(str(env2.temperature))
  PIR.setText(str(pir2.state))
  label3.setText(str(counter))
  label4.setText(str(counter_1))
  Light_Value = light4.analogValue
  PIR_Value = pir2.state
  if Light_Value <= 300 and PIR_Value == 1:
    rgb.setColorAll(0xffffff)
  else:
    rgb.setColorAll(0x000000)
  wait_ms(2)