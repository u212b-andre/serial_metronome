import serial

# Acquisisco i dati dalla Arduino

lettura_dati = True
Numeratore = 0
TempoBPM = 0

Arduino = serial.Serial('COM3', 9600)

while lettura_dati == True:
    dati = Arduino.readline()
    dati = (dati.decode('ascii')).split(sep=",")
    dati[0] = float(dati[0].strip())
    dati[1] = float(dati[1].strip()) 
    
    if (dati[0] + dati[1] > 8):
        
        NumRes = float(dati[0]) / 10
        VelRes = float(dati[1]) / 10

        # Genero i valori di numeratore
        
        for i in range(9):
            if NumRes >= i * 100 and NumRes < (i+1) * 100:
                Numeratore = 2 + i
        
        if NumRes >= 900 and NumRes < 1100:
            Numeratore = 10 #\12\ Per qualche motivo con 11 e 12 come valori il buzzer si
            # impalla, quindi tengo 10 come valore limite

        # Genero i valori di tempo (in BPM)

        if VelRes >= 0 and VelRes < 100:
            TempoBPM = 44
        elif VelRes >= 100 and VelRes < 200:
            TempoBPM = 60
        elif VelRes >= 200 and VelRes < 300:
            TempoBPM = 72
        elif VelRes >= 300 and VelRes < 400:
            TempoBPM = 81
        elif VelRes >= 400 and VelRes < 500:
            TempoBPM = 92
        elif VelRes >= 500 and VelRes < 600:
            TempoBPM = 108
        elif VelRes >= 600 and VelRes < 700:
            TempoBPM = 121 # Va più come un 120
        elif VelRes >= 700 and VelRes < 800:
            TempoBPM = 132 # Va più come un 130
        elif VelRes >= 800 and VelRes < 900:
            TempoBPM = 144 # Va più come un 141
        elif VelRes >= 900 and VelRes < 1100:
            TempoBPM = 144 #\162\ # (162) Va più come un 158, inoltre tra una battuta e l'altra c'è qualche
            # istante di troppo, quindi tengo come valore limite 144
    
        # Passo dai valori di tempo in BPM ai valori di tempo in millisecondi, in modo che
        # all'Arduino passo direttamente il valore di tempo in millisecondi tra un suono e l'altro

        msTempo = round(((600 / (23 * TempoBPM)) * 1000), 2)
        # Devo tuttavia considerare la possibilità che arrotondando, il numero risultante NON sia
        # di 5 cifre ma di 4 (ad esempio 376.90125 si arrotonda a 376.9), nel caso devo aggiustare

        if (msTempo * 10 - round(msTempo * 10) == 0.0):
            msTempo = msTempo + 0.01 
            # Aumento il valore di un centesimo di millisecondo in modo che questo abbia 5 cifre
            # se e solo se il valore di msTempo non è già a 5 cifre

        # Sistemo i valori da passare in una formula particolare che me li renda
        # facili da separare in seguito

        toArduino = str((msTempo * 100 + Numeratore / 100)).encode()


        print(toArduino.decode())


        Arduino.write(toArduino)

    else:
        scelta = input("Vuoi continuare? (Digita \"SI\" per continuare, qualunque altra cosa per terminare il programma) ")

        if scelta == "SI":
            Arduino.write(str(32206.09).encode())
        else:
            lettura_dati = False