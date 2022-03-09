import time
from os import system
import math
from pynput.mouse import Listener as MouseListener
import pynput.keyboard as kb
import pyautogui
import platform


keys = kb.Controller()
os_name = platform.system()


# define our clear function
def clear():
    # for windows
    if os_name == 'Windows':
        _ = system('cls')

    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')


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


def calcOptimal(x_diff, y_diff):
    smallestVelocity = 100
    bestAngle = 0
    global velocity
    global angle
    for possibleAngle in range(1, 90):
        try:
            v0 = calcVelocity(x_diff, y_diff, possibleAngle)
            if v0 < smallestVelocity:
                smallestVelocity = v0
                bestAngle = possibleAngle
        except Exception as e:
            pass
    clear()
    print("∠(･`_´･ ) Sir, we are on target!")
    print("\n------ Smallest -----")
    print("Power\tAngle")
    print("{:.2f}\t {:d}".format(smallestVelocity, bestAngle))
    velocity = smallestVelocity
    angle = bestAngle


def calcHighestBelow100(x_diff, y_diff):
    global highVelocity
    global highAngle
    for possibleAngle in range(1, 90):
        v0 = calcVelocity(x_diff, y_diff, 90 - possibleAngle)
        if v0 < 100:
            break

    print("\n------ Highest ------")
    print("Power\tAngle")
    print("{:.2f}\t {:d}".format(v0, 90 - possibleAngle))
    highVelocity = v0
    highAngle = 90 - possibleAngle
    time.sleep(1)
    is_left = (int(YourX > EnemyX) - 0.5) * 2
    alpha = 10.0 / 3
    pyautogui.click(YourX - alpha * is_left * highVelocity * math.cos(math.radians(highAngle)),
                    YourY - alpha * highVelocity * math.sin(math.radians(highAngle)), button='left')
    print("\nThe highest trajectory have been automatically selected!\n(automatic selection may have some errors, please check and fine tune)")
    print("\nlocate your tank(p)/target(e)")


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
    # cleanGlobals()
    print('Click your Tank')
    mouse_listener = MouseListener(on_click=posPlayer)
    mouse_listener.start()
    mouse_listener.join()
    if 'EnemyX' in globals() and 'EnemyY' in globals():
        # all needed, calc shot
        diffx = abs(YourX - EnemyX)
        diffy = -EnemyY + YourY
        calcOptimal(diffx, diffy)
        calcHighestBelow100(diffx, diffy)


def EnemyLocation():
    # cleanGlobals()
    print('Click enemy Tank')
    mouse_listener = MouseListener(on_click=posEnemy)
    mouse_listener.start()
    mouse_listener.join()
    if 'YourX' in globals() and 'YourY' in globals():
        # all needed, calc shot
        diffx = abs(YourX - EnemyX)
        diffy = -EnemyY + YourY
        calcOptimal(diffx, diffy)
        calcHighestBelow100(diffx, diffy)


if __name__ == "__main__":
    print("locate your tank(p)/target(e)")
    with kb.GlobalHotKeys({'P': PlayerLocation, 'E': EnemyLocation, '<ctrl>+C':exit}) as h:
        h.join()
