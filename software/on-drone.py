import adafruit_ads1x15.ads1115 as ADS
import adafruit_ads1x15.analog_in
import adafruit_bmp3xx
import adafruit_ccs811
import adafruit_gps
import adafruit_pcf8523
import adafruit_sdcard
import adafruit_sht31d
import board
import busio
import digitalio
import gc
import json
import neopixel
import os
import storage
import time

# Cleanup anything left over
gc.collect()

# Initialize Neopixel
pixel = neopixel.NeoPixel(board.NEOPIXEL, 1, pixel_order=neopixel.RGB)
pixel.brightness = .5
pixel[0] = (255, 0, 0)

# Buses
spi_bus = busio.SPI(board.SCK, board.MOSI, board.MISO)
i2c_bus = busio.I2C(board.SCL, board.SDA)

# Initialize the onboard clock
rtc = adafruit_pcf8523.PCF8523(i2c_bus)
# Set the onboard clock if needed
# The format is (year, month, day, hour, minute, second, dayOfWeek, dayInYear, isDST)
# See https://docs.python.org/3/library/time.html#time.struct_time for more details
# Uncomment the next two lines to set the onboard clock:
# rtc.datetime = time.struct_time(
#     (2020,  6,   24,   14,  40,  0,    0,   -1,    -1))

# SD
SD_CS = board.D10
cs = digitalio.DigitalInOut(SD_CS)
sdcard = adafruit_sdcard.SDCard(spi_bus, cs)
vfs = storage.VfsFat(sdcard)
storage.mount(vfs, "/sd")

# Create metadata file
meta = {}
meta["pilot"] = "Fill this in."
t = rtc.datetime
meta["date-start"] = "%s-%s-%s" % (t.tm_mon, t.tm_mday, t.tm_year)
meta["time-start"] = "%s:%s:%s" % (t.tm_hour, t.tm_min, t.tm_sec)
meta["location"] = "Fill this in."
meta["TimeZone"] = "PST"
with open('/sd/meta.json', 'w') as outfile:
    json.dump(meta, outfile)


# Set the Neopixel to green now that we found a valid SD card
pixel[0] = (0, 255, 0)

# Initialize the GPS module
gps_uart = busio.UART(board.TX, board.RX, baudrate=9600, timeout=10)
gps = adafruit_gps.GPS(gps_uart, debug=True)
gps.send_command(b'PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')
gps.send_command(b'PMTK220,1000')
gps.update()

# Initialize the BMP388 sensor (pressure and altitude)
bmp = adafruit_bmp3xx.BMP3XX_I2C(i2c_bus)
bmp.pressure_oversampling = 8
bmp.temperature_oversampling = 2
print("Pressure: {:6.1f}  Altitude: {:5.2f}".format(
    bmp.pressure, bmp.altitude))


# Initialize the CCS sensor (eCO2 and TVOC)
ccs811 = adafruit_ccs811.CCS811(i2c_bus)
# Wait for the sensor to be ready
while not ccs811.data_ready:
    pass


# Initialize the SHT31 (temperature and humidity)
sht31 = adafruit_sht31d.SHT31D(i2c_bus)
print(sht31.temperature)
print(sht31.relative_humidity)

# Initialize the PMS5003 arduino
pms_uart = busio.UART(board.D12, board.D13, baudrate=115200, timeout=1)
pms_pin = digitalio.DigitalInOut(board.A4)
pms_pin.direction = digitalio.Direction.OUTPUT
pms_pin.value = False  # set the pin low since we don't need any data right now


# ADCs
adc1 = ADS.ADS1115(i2c_bus, address=0x48)
adc2 = ADS.ADS1115(i2c_bus, address=0x49)

# Alphasense
ox_we = adafruit_ads1x15.analog_in.AnalogIn(adc1, ADS.P0)
ox_ae = adafruit_ads1x15.analog_in.AnalogIn(adc1, ADS.P1)
co_we = adafruit_ads1x15.analog_in.AnalogIn(adc1, ADS.P2)
co_ae = adafruit_ads1x15.analog_in.AnalogIn(adc1, ADS.P3)
no_we = adafruit_ads1x15.analog_in.AnalogIn(adc2, ADS.P0)
no_ae = adafruit_ads1x15.analog_in.AnalogIn(adc2, ADS.P1)
h2s_we = adafruit_ads1x15.analog_in.AnalogIn(adc2, ADS.P2)
h2s_ae = adafruit_ads1x15.analog_in.AnalogIn(adc2, ADS.P3)

# print the header to the data file
meta_file = open('/sd/meta.json', 'w')
data_file = open('/sd/data.csv', 'a')  # We want to append in case of a restart
data_file.write(
    "month, date, year, hour, minute, second, fix, lat deg, long deg, fixq, fixq3d, sat, speed knots, pressure hPa, alt m, temp C, humidity %, eCO2 ppm, TVOC ppm, as1, as2, as3, as4, as5, as6, as7, as8, pms new, pm1.0s, pm2.5s, pm10.0s, pm1.0e, pm2.5e, pm10.0e, p0.3um, p0.5um, p1.0um, p2.5um, p10.0um\n")
data_file.flush()

# Set the Neopixel to white now that we're ready!
pixel[0] = (255, 255, 255)

while True:
    # Set the Neopixel to purpleish-blue
    pixel[0] = (100, 0, 255)

    # Get the current time and put that in the metadata file
    t = rtc.datetime
    meta["date-end"] = "%s-%s-%s" % (t.tm_mon, t.tm_mday, t.tm_year)
    meta["time-end"] = "%s:%s:%s" % (t.tm_hour, t.tm_min, t.tm_sec)
    meta_file.seek(0)
    json.dump(meta, meta_file)
    meta_file.flush()

    # And print it to the data file
    time_string = "%s,%s,%s,%s,%s,%s," % (t.tm_mon,
                                          t.tm_mday, t.tm_year, t.tm_hour, t.tm_min, t.tm_sec)
    print(time_string)
    data_file.write(time_string)
    del time_string

    # Get the current location and print it to the data file
    gps.update()
    gps_string = '%s,%s,%s,%s,%s,%s,%s,' % (
        gps.has_fix, gps.latitude, gps.longitude, gps.fix_quality, gps.fix_quality_3d, gps.satellites, gps.speed_knots)
    # gps_string = gps.readline()
    print(gps_string)
    data_file.write(gps_string)
    del gps_string

    # Get the current pressure and altitude and print them to the data file
    bmp_string = "%s,%s," % (bmp.pressure, bmp.altitude)
    print(bmp_string)
    data_file.write(bmp_string)
    del bmp_string

    # Get the current temperature and humidity and print them to the data file
    sht31_string = "%s,%s," % (sht31.temperature, sht31.relative_humidity)
    print(sht31_string)
    data_file.write(sht31_string)
    del sht31_string

    # Get the current eCO2 and TVOC readings and print them to the data file
    ccs_string = "%s,%s," % (ccs811.eco2, ccs811.tvoc)
    print(ccs_string)
    data_file.write(ccs_string)
    del ccs_string

    # Get the raw Alphasense readings and print them to the data file
    as_string = "%s,%s,%s,%s,%s,%s,%s,%s," % (
        ox_we.voltage * 1000,
        ox_ae.voltage * 1000,
        co_we.voltage * 1000,
        co_ae.voltage * 1000,
        no_we.voltage * 1000,
        no_ae.voltage * 1000,
        h2s_we.voltage * 1000,
        h2s_ae.voltage * 1000
    )
    print(as_string)
    data_file.write(as_string)
    del as_string

    # Get the data from the PMS5003 arduino and print it to the data file
    pms_pin.value = True  # Set the pin high so it sends data
    data_in = pms_uart.readline()  # Get one line
    pms_string = ',,,,,,,,,,,,\n'
    if data_in is None or len(data_in) > 24:  # data is valid, so let's set it
        pms_string = ''.join([chr(b) for b in data_in])
    pms_pin.value = False  # Set the pin low so it does not send data
    print(pms_string)
    data_file.write(pms_string)
    del data_in
    del pms_string

    # Set the Neopixel to red now that we finished collecting data
    pixel[0] = (255, 20, 20)

    data_file.flush()
    os.sync()

    print('-------------')
    print()
    print('-------------')
