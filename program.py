from machine import Pin, ADC
from neopixel import Neopixel
import time
import utime

positions = [[1, 0, 1, 0, 1, 0, 1, 0],               # 0 - clear
             [0, 1, 0, 1, 0, 1, 0, 1],               # 1 - black pawn
             [1, 0, 1, 0, 1, 0, 1, 0],				 # 2 - black quenn
             [0, 0, 0, 0, 0, 0, 0, 0],				 # 3 - white pawn
             [0, 0, 0, 0, 0, 0, 0, 0],				 # 4 - white quenn
             [0, 3, 0 ,3, 0, 3, 0 ,3],
             [3, 0 ,3, 0, 3, 0 ,3, 0],
             [0, 3, 0 ,3, 0, 3, 0 ,3]]

black_team = 12
white_team = 12

my_position = []
possible_moves = []

pos_cursor = True
player1 = True 

# Ustawienia dla taśmy LED
num_leds = 64
state_machine = 0  # ID używanego automatu stanowego PIO
pin_led = 0  # Pin, do którego podłączony jest taśma LED
mode = "GRB"  # Tryb diod LED
delay = 0.0001  
button_pin = Pin(14, Pin.IN, Pin.PULL_DOWN)
button_change = Pin(3, Pin.IN, Pin.PULL_DOWN)
# Tworzenie obiektu Neopixel
led_strip = Neopixel(num_leds, state_machine, pin_led, mode, delay)

matrix = [['b', 'w', 'b', 'w', 'b', 'w', 'b', 'w'], # matryca pola dla warcabów
          ['w', 'b', 'w', 'b', 'w', 'b', 'w', 'b'],
          ['b', 'w', 'b', 'w', 'b', 'w', 'b', 'w'],
          ['w', 'b', 'w', 'b', 'w', 'b', 'w', 'b'],
          ['b', 'w', 'b', 'w', 'b', 'w', 'b', 'w'],
          ['w', 'b', 'w', 'b', 'w', 'b', 'w', 'b'],
          ['b', 'w', 'b', 'w', 'b', 'w', 'b', 'w'],
          ['w', 'b', 'w', 'b', 'w', 'b', 'w', 'b']]

led_state = False

brightness = 100  # Wartość jasności w zakresie od 0 do 255

# RGB kolory
brown_rgb = (239, 69, 39)
white_rgb = (245, 245, 220)
green_rgb= (0, 255, 0)
blue = tuple(int(value * (brightness / 255.0)) for value in (0,0,255))
blue_rgb = (128, 0, 128)
yellow_rgb = (255,255,0)
black = (0,0,0)
red_rgb = (255, 0, 0)

# Zmniejszenie jasności dla każdego komponentu koloru
brown_rgb_dimmed = tuple(int(value * (brightness / 255.0)) for value in brown_rgb)
white_rgb_dimmed = tuple(int(value * (brightness / 255.0)) for value in white_rgb)
green_rgb_dimmed= tuple(int(value * (brightness / 255.0)) for value in green_rgb)

blue_rgb_dimmed = tuple(int(value * (brightness / 255.0)) for value in blue_rgb)
yellow_rgb_dimmed= tuple(int(value * (brightness / 255.0)) for value in yellow_rgb)


#-------------------------------------------------------------------------------------------------------------------------

def show_board():		# wyświetlenie różnych kolorów dla naszego pola z warcabami
    for i in range(8):
        for j in range(8):
            if positions[i][j] == 1:
                led_strip.set_pixel(8 * i + j, blue_rgb_dimmed)
            elif positions[i][j] == 2:
                led_strip.set_pixel(8 * i + j, blue_rgb) 
            elif positions[i][j] == 3:
                led_strip.set_pixel(8 * i + j, yellow_rgb_dimmed)
            elif positions[i][j] == 4:
                led_strip.set_pixel(8 * i + j, yellow_rgb)
            else:
                if matrix[i][j] == 'b':
                    led_strip.set_pixel(8 * i + j, brown_rgb_dimmed)  
                elif matrix[i][j] == 'w':
                    led_strip.set_pixel(8 * i + j, white_rgb_dimmed)

#-------------------------------------------------------------------------------------------------------------------------
                
x1 = y1 = 0
x2 = y2 = 7

xAxis = ADC(Pin(27)) #odczytanie ośi X z joysticka
yAxis = ADC(Pin(26)) #odczytanie ośi Y z joysticka
button = Pin(17,Pin.IN, Pin.PULL_UP)
xStatus = "middle"
yStatus = "middle"
    
def Joystick_1():
    global x1, y1,xStatus, yStatus, pos_cursor
    xValue = xAxis.read_u16()
    yValue = yAxis.read_u16()
    buttonValue = button.value()
    
    buttonStatus = "not pressed" #sprawdzenie czy joystick był naciśnienty
    
    if buttonValue == 0:
        buttonStatus = "pressed" #sprawdzenie czy joystick był naciśnienty

        
    if xValue <= 5000: #odczyt położenia joystika
        if positions[y1][x1] == 1:
                led_strip.set_pixel(8*y1+x1, blue_rgb_dimmed)
        elif positions[y1][x1]  == 2:
                led_strip.set_pixel(8*y1+x1, blue_rgb) 
        elif positions[y1][x1]  == 3:
                led_strip.set_pixel(8*y1+x1,  yellow_rgb_dimmed)
        elif positions[y1][x1]  == 4:
                led_strip.set_pixel(8*y1+x1,  yellow_rgb)
        else:
                if matrix[y1][x1]  == 'b':
                    led_strip.set_pixel(8*y1+x1,  brown_rgb_dimmed)  
                elif matrix[y1][x1] == 'w':
                    led_strip.set_pixel(8*y1+x1,  white_rgb_dimmed)
        xStatus = "left"
        if player1 == True: # odczyta jaki gracz teraz używa joystick (dla tego że powina być inwersja)
            x1+=1
        else:
            x1-=1
    # tak dalej dla innych osi
        
    if xValue >= 65000:
        if positions[y1][x1] == 1:
                led_strip.set_pixel(8*y1+x1, blue_rgb_dimmed)
        elif positions[y1][x1]  == 2:
                led_strip.set_pixel(8*y1+x1, blue_rgb) 
        elif positions[y1][x1]  == 3:
                led_strip.set_pixel(8*y1+x1,  yellow_rgb_dimmed)
        elif positions[y1][x1]  == 4:
                led_strip.set_pixel(8*y1+x1,  yellow_rgb)
        else:
                if matrix[y1][x1]  == 'b':
                    led_strip.set_pixel(8*y1+x1,  brown_rgb_dimmed) 
                elif matrix[y1][x1] == 'w':
                    led_strip.set_pixel(8*y1+x1,  white_rgb_dimmed)
        xStatus = "right"
        if player1 == True:
            x1-=1
        else:
            x1+=1
        

        
    if yValue <= 5000:
        if positions[y1][x1] == 1:
                led_strip.set_pixel(8*y1+x1, blue_rgb_dimmed)
        elif positions[y1][x1]  == 2:
                led_strip.set_pixel(8*y1+x1, blue_rgb) 
        elif positions[y1][x1]  == 3:
                led_strip.set_pixel(8*y1+x1,  yellow_rgb_dimmed)
        elif positions[y1][x1]  == 4:
                led_strip.set_pixel(8*y1+x1,  yellow_rgb)
        else:
                if matrix[y1][x1]  == 'b':
                    led_strip.set_pixel(8*y1+x1,  brown_rgb_dimmed) 
                elif matrix[y1][x1] == 'w':
                    led_strip.set_pixel(8*y1+x1,  white_rgb_dimmed)
        yStatus = "up"
        if player1 == True:
            y1+=1
        else:
            y1-=1
        

        
    if yValue >= 65000:
        if positions[y1][x1] == 1:
                led_strip.set_pixel(8*y1+x1, blue_rgb_dimmed)
        elif positions[y1][x1]  == 2:
                led_strip.set_pixel(8*y1+x1, blue_rgb) 
        elif positions[y1][x1]  == 3:
                led_strip.set_pixel(8*y1+x1,  yellow_rgb_dimmed)
        elif positions[y1][x1]  == 4:
                led_strip.set_pixel(8*y1+x1,  yellow_rgb)
        else:
                if matrix[y1][x1]  == 'b':
                    led_strip.set_pixel(8*y1+x1,  brown_rgb_dimmed)  
                elif matrix[y1][x1] == 'w':
                    led_strip.set_pixel(8*y1+x1,  white_rgb_dimmed)
        yStatus = "down"
        if player1 == True:
            y1-=1
        else:
            y1+=1
        
       
    if x1>7:
        x1-=8
        
    if y1>7:
        y1-=8
        
    if x1<0:
        x1+=8
        
    if y1<0:
        y1+=8
    
    
    
                    # choose moves #
    if buttonStatus == "pressed" and positions[y1][x1] == 1 and player1 == True: # odczyt danych jeżeli gracz numer jeden wybiera swoje piony 
        my_position.clear()
        possible_moves.clear()
        show_board()
        logic_for_bp(y1 , x1)
    
    if buttonStatus == "pressed" and positions[y1][x1] == 2 and player1 == True: # odczyt danych jeżeli gracz numer jeden wybiera swoje damki 
        my_position.clear()
        possible_moves.clear()
        show_board()
        logic_for_bq(y1 , x1)
    
    
    if buttonStatus == "pressed" and [y1, x1] in possible_moves and positions[my_position[0]][my_position[1]] == 1 and player1 == True: # odczyt danych gdzie może iść pion
    
        pawn1 = positions[my_position[0]][my_position[1]]
        positions[y1][x1] = pawn1
        positions[my_position[0]][my_position[1]] = 0
        if abs(my_position[0]-y1) == 2:
            positions[int((my_position[0]+y1)/2)][int((my_position[1]+x1)/2)] = 0
            
        if positions[y1][x1] == 1 and y1 == 7:
            positions[y1][x1] = 2
        
        my_position.clear()
        possible_moves.clear()
        show_board()


    if buttonStatus == "pressed" and [y1, x1] in possible_moves and positions[my_position[0]][my_position[1]] == 2 and player1 == True: # odczyt danych gdzie może iść damka
        queen1 = positions[my_position[0]][my_position[1]]
        positions[y1][x1] = queen1
        positions[my_position[0]][my_position[1]] = 0

        for index in range(1, abs(my_position[0] - y1)):
            position_y = my_position[0] - index if my_position[0] > y1 else my_position[0] + index
            position_x = my_position[1] - index if my_position[1] > x1 else my_position[1] + index
            positions[position_y][position_x] = 0

        my_position.clear()
        possible_moves.clear()
        show_board()
    # i tak dalej dla drugiego gracza
    
    
    if buttonStatus == "pressed" and positions[y1][x1] == 3 and player1 == False :
        my_position.clear()
        possible_moves.clear()
        show_board()
        logic_for_wp(y1 , x1)
    
    if buttonStatus == "pressed" and positions[y1][x1] == 4 and player1 == False:
        my_position.clear()
        possible_moves.clear()
        show_board()
        logic_for_wq(y1 , x1)
    
    
    if buttonStatus == "pressed" and [y1, x1] in possible_moves and positions[my_position[0]][my_position[1]] == 3 and player1 == False:
    
        pawn1 = positions[my_position[0]][my_position[1]]
        positions[y1][x1] = pawn1
        positions[my_position[0]][my_position[1]] = 0
        if abs(my_position[0]-y1) == 2:
            positions[int((my_position[0]+y1)/2)][int((my_position[1]+x1)/2)] = 0
            
        if positions[y1][x1] == 3 and y1 == 0:
            positions[y1][x1] = 4
        
        my_position.clear()
        possible_moves.clear()
        show_board()


    if buttonStatus == "pressed" and [y1, x1] in possible_moves and positions[my_position[0]][my_position[1]] == 4 and player1 == False:
        queen1 = positions[my_position[0]][my_position[1]]
        positions[y1][x1] = queen1
        positions[my_position[0]][my_position[1]] = 0

        for index in range(1, abs(my_position[0] - y1)):
            position_y = my_position[0] - index if my_position[0] > y1 else my_position[0] + index
            position_x = my_position[1] - index if my_position[1] > x1 else my_position[1] + index
            positions[position_y][position_x] = 0

        my_position.clear()
        possible_moves.clear()
        show_board()

    for vec in possible_moves: #wyświetlenie wszystkich możliwych kroków 
        led_strip.set_pixel(8 * vec[0] + vec[1], red_rgb)
        
    if player1 == True: # zmiana gracza
        if pos_cursor == False:
            show_board()
            x1 = 0
            y1 = 0
            pos_cursor = True 
        led_strip.set_pixel(8*y1+x1, green_rgb_dimmed)
    else:
        if pos_cursor == True:
            show_board()
            x1= 7
            y1= 7
            pos_cursor = False
        led_strip.set_pixel(8*y1+x1, blue)
    
    
    utime.sleep(0.25)




#------------------------------------------------------------------------------------------------------------------------- 


def logic_for_bp(y_pos, x_pos): # logika pionów
    my_position.append(y_pos) #wpisywanie danych gdzie mamy Pion
    my_position.append(x_pos)
    must_to_attack = False
    if y_pos+2 < 8 and x_pos+2 <8: # Możliwe ruchy dla pionka (trzeba atakować)
        if positions[y_pos+1][x_pos+1] == 3 or positions[y_pos+1][x_pos+1] == 4 and positions[y_pos+2][x_pos+2] == 0:
          
            must_to_attack = True
            possible_moves.append([y_pos+2, x_pos+2])#tak samo dla innej strony
        
    if y_pos+2 < 8 and x_pos-2 >= 0:    
        if positions[y_pos+1][x_pos-1] == 3 or positions[y_pos+1][x_pos-1] == 4 and positions[y_pos+2][x_pos-2] == 0:
           
            must_to_attack = True 
            possible_moves.append([y_pos+2, x_pos-2])
         
    if y_pos+1 < 8 and x_pos+1 <8 and must_to_attack == False: # Możliwe ruchy dla pionka (nie trzeba atakować)
        if positions[y_pos+1][x_pos+1] == 0:
            possible_moves.append([y_pos+1, x_pos+1])#tak samo dla innej strony
        
    if y_pos+1 < 8 and x_pos-1 >= 0 and must_to_attack == False:  
        if positions[y_pos+1][x_pos-1] == 0:
            possible_moves.append([y_pos+1, x_pos-1])
    
            
        
def logic_for_bq(y_pos, x_pos): #logika damek
    my_position.append(y_pos)
    my_position.append(x_pos)
    ur = True # bool dla odzytania gdzie możemy chodzić
    ul = True
    dr = True
    dl = True
    for i in range(1, 8, 1):
        if y_pos + i < 8 and x_pos + i < 8 and ur == True: # odczytanie możliwych wariantów dla jednej strony
            if positions[y_pos + i][x_pos + i] == 0:
                if [y_pos + i, x_pos + i] not in possible_moves:
                    possible_moves.append([y_pos + i, x_pos + i])
            else:
                if y_pos + i + 1 < 8 and x_pos + i + 1 < 8:
                    if (positions[y_pos + i][x_pos + i] == 3 or positions[y_pos + i][x_pos + i] == 4) and positions[y_pos + i + 1][x_pos + i + 1] == 0:
                        
                        possible_moves.append([y_pos + i + 1, x_pos + i + 1])
                    else:
                        ur = False
                else:
                    ur = False #tak dalej dla innych
            
        if y_pos + i < 8 and x_pos - i >= 0 and ul == True:
            if positions[y_pos + i][x_pos - i] == 0:
                if [y_pos + i, x_pos - i] not in possible_moves:
                    possible_moves.append([y_pos + i, x_pos - i])
            else:
                if y_pos + i + 1 < 8 and x_pos - i - 1 >= 0:
                    if (positions[y_pos + i][x_pos - i] == 3 or positions[y_pos + i][x_pos - i] == 4) and positions[y_pos + i + 1][x_pos - i - 1] == 0:
                      
                        possible_moves.append([y_pos + i + 1, x_pos - i - 1])
                    else:
                        ul = False
                else:
                    ul = False
        
        if y_pos - i >= 0 and x_pos + i < 8 and dr == True:
            if positions[y_pos - i][x_pos + i] == 0:
                if [y_pos - i, x_pos + i] not in possible_moves:
                    possible_moves.append([y_pos - i, x_pos + i])
            else:
                if y_pos - i - 1 >= 0 and x_pos + i + 1 < 8:
                    if (positions[y_pos - i][x_pos + i] == 3 or positions[y_pos - i][x_pos + i] == 4) and positions[y_pos - i - 1][x_pos + i + 1] == 0:
                      
                        possible_moves.append([y_pos - i - 1, x_pos + i + 1])
                    else:
                        dr = False
                else:
                    dr = False
            
        if y_pos - i >= 0 and x_pos - i >= 0 and dl == True:
            if positions[y_pos - i][x_pos - i] == 0:
                if [y_pos - i, x_pos - i] not in possible_moves:
                    possible_moves.append([y_pos - i, x_pos - i])
            else:
                if y_pos - i - 1 >= 0 and x_pos - i - 1 >= 0:
                    if (positions[y_pos - i][x_pos - i] == 3 or positions[y_pos - i][x_pos - i] == 4) and positions[y_pos - i - 1][x_pos - i - 1] == 0:
                    
                        possible_moves.append([y_pos - i - 1, x_pos - i - 1])
                    else:
                        dl = False
                else:
                    dl = False
                                
                
        

def logic_for_wp(y_pos, x_pos):
    my_position.append(y_pos)
    my_position.append(x_pos)
    must_to_attack = False
    if y_pos-2 >= 0 and x_pos+2 <8:
        if positions[y_pos-1][x_pos+1] == 1 or positions[y_pos-1][x_pos+1] == 2 and positions[y_pos-2][x_pos+2] == 0:
           
            must_to_attack = True
            possible_moves.append([y_pos-2, x_pos+2])
        
    if y_pos-2>=0 and x_pos-2 >= 0:    
        if positions[y_pos-1][x_pos-1] == 1 or positions[y_pos-1][x_pos-1] == 2 and positions[y_pos-2][x_pos-2] == 0:
           
            must_to_attack = True 
            possible_moves.append([y_pos-2, x_pos-2])
         
    if y_pos-1>=0 and x_pos+1 <8 and must_to_attack == False: 
        if positions[y_pos-1][x_pos+1] == 0:
         
            possible_moves.append([y_pos-1, x_pos+1])
        
    if y_pos-1>=0  and x_pos-1 >= 0 and must_to_attack == False:  
        if positions[y_pos-1][x_pos-1] == 0:
            possible_moves.append([y_pos-1, x_pos-1])    




def logic_for_wq(y_pos, x_pos):
    my_position.append(y_pos)
    my_position.append(x_pos)
    ur = True
    ul = True
    dr = True
    dl = True
    for i in range(1, 8, 1):
        if y_pos + i < 8 and x_pos + i < 8 and ur == True:
            if positions[y_pos + i][x_pos + i] == 0:
                if [y_pos + i, x_pos + i] not in possible_moves:
                    possible_moves.append([y_pos + i, x_pos + i])
            else:
                if y_pos + i + 1 < 8 and x_pos + i + 1 < 8:
                    if (positions[y_pos + i][x_pos + i] == 1 or positions[y_pos + i][x_pos + i] == 2) and positions[y_pos + i + 1][x_pos + i + 1] == 0:
                       
                        possible_moves.append([y_pos + i + 1, x_pos + i + 1])
                    else:
                        ur = False
                else:
                    ur = False
            
        if y_pos + i < 8 and x_pos - i >= 0 and ul == True:
            if positions[y_pos + i][x_pos - i] == 0:
                if [y_pos + i, x_pos - i] not in possible_moves:
                    possible_moves.append([y_pos + i, x_pos - i])
            else:
                if y_pos + i + 1 < 8 and x_pos - i - 1 >= 0:
                    if (positions[y_pos + i][x_pos - i] == 1 or positions[y_pos + i][x_pos - i] == 2) and positions[y_pos + i + 1][x_pos - i - 1] == 0:
                    
                        possible_moves.append([y_pos + i + 1, x_pos - i - 1])
                    else:
                        ul = False
                else:
                    ul = False
        
        if y_pos - i >= 0 and x_pos + i < 8 and dr == True:
            if positions[y_pos - i][x_pos + i] == 0:
                if [y_pos - i, x_pos + i] not in possible_moves:
                    possible_moves.append([y_pos - i, x_pos + i])
            else:
                if y_pos - i - 1 >= 0 and x_pos + i + 1 < 8:
                    if (positions[y_pos - i][x_pos + i] == 1 or positions[y_pos - i][x_pos + i] == 2) and positions[y_pos - i - 1][x_pos + i + 1] == 0:
                       
                        possible_moves.append([y_pos - i - 1, x_pos + i + 1])
                    else:
                        dr = False
                else:
                    dr = False
            
        if y_pos - i >= 0 and x_pos - i >= 0 and dl == True:
            if positions[y_pos - i][x_pos - i] == 0:
                if [y_pos - i, x_pos - i] not in possible_moves:
                    possible_moves.append([y_pos - i, x_pos - i])
            else:
                if y_pos - i - 1 >= 0 and x_pos - i - 1 >= 0:
                    if (positions[y_pos - i][x_pos - i] == 1 or positions[y_pos - i][x_pos - i] == 2) and positions[y_pos - i - 1][x_pos - i - 1] == 0:
                      
                        possible_moves.append([y_pos - i - 1, x_pos - i - 1])
                    else:
                        dl = False
                else:
                    dl = False









#------------------------------------------------------------------------------------------------------------------------- 



if __name__ == "__main__":
    while True:
        # Odczytywanie stanu przycisku
        button_state = button_pin.value()
        button_state_change = button_change.value()
        # Jeśli przycisk został naciśnięty, przełącz stan taśmy LED
        if button_state_change == 1:
            player1 = not player1
            my_position = []
            possible_moves = []
        
        if button_state == 1:
            led_state = not led_state  # Przełączamy stan
            
            # W zależności od stanu taśmy LED, włączamy lub wyłączamy ją
            if led_state:
                show_board()
            else:
                positions = [[1, 0, 1, 0, 1, 0, 1, 0],      # Odświeżenie planszy po restarcie       
                             [0, 1, 0, 1, 0, 1, 0, 1],               
                             [1, 0, 1, 0, 1, 0, 1, 0],				 
                             [0, 0, 0, 0, 0, 0, 0, 0],				 
                             [0, 0, 0, 0, 0, 0, 0, 0],				 
                             [0, 3, 0 ,3, 0, 3, 0 ,3],
                             [3, 0 ,3, 0, 3, 0 ,3, 0],
                             [0, 3, 0 ,3, 0, 3, 0 ,3]]
                my_position = []
                possible_moves = []
                led_strip.fill((0, 0, 0))  # Wyłączamy wszystkie diody LED oprócz kursora

            
        
        Joystick_1()
        
        led_strip.show()
        time.sleep(0.25)

