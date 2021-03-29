def get_soil_humidity():
    
    # load libraries
    from machine import Pin, ADC
    from time import sleep
    import statistics

    # define pin
    pot = ADC(Pin(36))
    pot.atten(ADC.ATTN_11DB)       #Full range: 3.3v

    i = 0

    while i < 10:
        
        moisture = pot.read()
        list = []
        list.append(moisture)

        i += 1
        sleep(0.5)
        
        # measure soil_humidity

    # voll nass = 1449.0
    # voll trocken = 4095


    # Example to find average of list
    number_list = list
    avg = sum(number_list)/len(number_list)
    wert = (round(avg,2))

    print(wert)

    if wert > 4000:
        print(0)
    else:
        percent = ((4095 - wert) / 2646 ) * 100

        print(percent)
