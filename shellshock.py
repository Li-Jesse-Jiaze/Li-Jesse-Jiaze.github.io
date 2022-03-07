import math
from pynput.mouse import Listener as MouseListener
from pynput import keyboard
import pynput.keyboard as kb
import pynput.mouse as ms
import time
import platform

keys = kb.Controller()
mouse = ms.Controller()
os = platform.system()

global set_wind
set_wind = ""


# calculate velocity
def calcVelocity(x_diff, y_diff, angle):
    # from https://steamcommunity.com/sharedfiles/filedetails/?id=1327582953
    g = -379.106
    q = 0.0518718
    try:
        v0 = -2 / (g * q) * math.sqrt((-g * x_diff * x_diff) / (
                    2 * math.cos(math.radians(angle)) * math.cos(math.radians(angle)) * (
                        math.tan(math.radians(angle)) * x_diff - y_diff)))
    except ZeroDivisionError:
        v0 = 0
    return v0


# calculate velocity with wind
def calcVelocityWithWind(x_diff, y_diff, angle, wind):
    g = 379.106
    q = 0.0518718
    # z = 0.4757
    # z = 0.513538766675914
    z = 0.5
    w = z * wind
    v_0 = (g * x_diff - w * y_diff) / (math.sqrt(
        2 * g * x_diff * math.sin(math.radians(angle)) * math.cos(math.radians(angle)) + 2 * g * y_diff * pow(
            math.cos(math.radians(angle)), 2) + 2 * w * x_diff * pow(math.sin(math.radians(angle)),
                                                                     2) + 2 * w * y_diff * math.sin(
            math.radians(angle)) * math.cos(math.radians(angle))))
    power = (2 / (g * q)) * v_0
    return power


def calcVelocityWithWind_y0(x_diff, angle, wind):
    g = 379.106
    q = 0.0518718
    z = 0.4757
    w = z * wind
    print("Inputs: " + str(x_diff) + ", " + str(angle) + ", " + str(wind))
    v_0 = (g * math.sqrt(x_diff)) / (math.sqrt(
        2 * g * math.sin(math.radians(angle)) * math.cos(math.radians(angle)) + 2 * w * pow(
            math.sin(math.radians(angle)), 2)))
    power = (2 / (g * q)) * v_0
    print(power)
    return power


def calcOptimal(x_diff, y_diff, wind):
    smallestVelocity = 100
    bestAngle = 0
    global velocity
    global angle
    for possibleAngle in range(1, 90):
        try:
            if wind == 0:
                v0 = calcVelocity(x_diff, y_diff, possibleAngle)
            else:
                v0 = calcVelocityWithWind(x_diff, y_diff, possibleAngle, wind)
            if v0 < smallestVelocity:
                smallestVelocity = v0
                bestAngle = possibleAngle
        except Exception as e:
            pass

    print("Smallest Velocity")
    print("Velocity = " + str(smallestVelocity))
    print("Angle = " + str(bestAngle))
    velocity = smallestVelocity
    angle = bestAngle


def calcHighestBelow100(x_diff, y_diff, wind):
    global highVelocity
    global highAngle
    for possibleAngle in range(1, 90):
        if wind == 0:
            v0 = calcVelocity(x_diff, y_diff, 90 - possibleAngle)
        else:
            try:
                v0 = calcVelocityWithWind(x_diff, y_diff, 90 - possibleAngle, wind)
            except Exception as e:
                v0 = 101
        if v0 < 100:
            break

    print("Highest Angle with power below 100")
    print("Velocity = " + str(v0))
    print("Angle = " + str(90 - possibleAngle))
    highVelocity = v0
    highAngle = 90 - possibleAngle


def cleanGlobals():
    try:
        del globals()['YourX']
    except Exception as e:
        pass
    try:
        del globals()['YourY']
    except Exception as e:
        pass
    try:
        del globals()['EnemyX']
    except Exception as e:
        pass
    try:
        del globals()['EnemyY']
    except Exception as e:
        pass
    try:
        del globals()['set_wind']
    except Exception as e:
        pass




def posPlayer(x, y, button, pressed):
    if pressed:
        print("Your position: " + str(x) + ", " + str(y))
        global YourX
        YourX = x
        global YourY
        YourY = y
    return False


def posEnemy(x, y, button, pressed):
    if pressed:
        print("Enemy position: " + str(x) + ", " + str(y))
        global EnemyX
        EnemyX = x
        global EnemyY
        EnemyY = y
    return False


def PlayerLocation():
    global set_wind
    if set_wind == "":
        wind = 0
    else:
        wind = int(set_wind)
    # cleanGlobals()
    print('Click your Tank')
    mouse_listener = MouseListener(on_click=posPlayer)
    mouse_listener.start()
    mouse_listener.join()
    if 'EnemyX' in globals() and 'EnemyY' in globals():
        # all needed, calc shot
        diffx = abs(YourX - EnemyX)
        diffy = -EnemyY + YourY
        calcOptimal(diffx, diffy, wind)
        calcHighestBelow100(diffx, diffy, wind)
        set_wind = ""


def EnemyLocation():
    global set_wind
    if set_wind == "":
        wind = 0
    else:
        wind = int(set_wind)
    # cleanGlobals()
    print('Click enemy Tank')
    mouse_listener = MouseListener(on_click=posEnemy)
    mouse_listener.start()
    mouse_listener.join()
    if 'YourX' in globals() and 'YourY' in globals():
        # all needed, calc shot
        diffx = abs(YourX - EnemyX)
        diffy = -EnemyY + YourY
        calcOptimal(diffx, diffy, wind)
        calcHighestBelow100(diffx, diffy, wind)
        set_wind = ""


def readWind():
    global set_wind
    print("Enter wind strength followed by <ENTER> on your numpad")
    set_wind = ""
    with keyboard.Listener(on_press=readNumber) as lst:
        lst.join()
    set_wind = int(set_wind)
    print("Keystroke: " + str(set_wind))
    time.sleep(0.1)
    keys.tap(kb.Key.enter)


def readNumber(key):
    global set_wind
    # print(key.vk)
    # print(key.char)
    if os == "Linux":
        if key == kb.Key.enter:
            print("ENTER pressed")
            return False
        if hasattr(key, 'char'):
            if key.char is None:
                number = "5"
            else:
                number = key.char
            print(number)
            set_wind = set_wind + str(number)
        if hasattr(key, 'char') and key.char == '-' and set_wind == "":
            set_wind = set_wind + "-"
            print("")
    else:
        if key == kb.Key.enter:
            print("ENTER pressed")
            return False
        if hasattr(key, 'vk') and 96 <= key.vk <= 105:
            number = key.vk - 96
            print(number)
            set_wind = set_wind + str(number)
        if hasattr(key, 'char') and key.char == '-' and set_wind == "":
            set_wind = set_wind + "-"
            print("")


if __name__ == "__main__":
    with keyboard.GlobalHotKeys(
            {'<alt>+P': PlayerLocation, '<alt>+E': EnemyLocation,
             '<alt>+W': readWind}) as h:
        h.join()
