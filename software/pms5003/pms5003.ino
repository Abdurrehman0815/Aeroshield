// On Leonardo / Micro or others with hardware serial, use those!
// Make sure to adjust your hardware configuration to match.
// uncomment the following line:
// #define pmsSerial Serial1

// For UNO and others without hardware serial, we must use software serial...
// pin #2 is IN from sensor (TX pin on sensor), leave pin #3 disconnected
// comment these two lines if using hardware serial
#include <SoftwareSerial.h>
SoftwareSerial pmsSerial(2, 3);

struct pms5003data {
    uint16_t framelen;
    uint16_t pm10_standard, pm25_standard, pm100_standard;
    uint16_t pm10_env, pm25_env, pm100_env;
    uint16_t particles_03um, particles_05um, particles_10um, particles_25um, particles_50um, particles_100um;
    uint16_t unused;
    uint16_t checksum;
};

struct pms5003data data;

bool new_data = false;

void setup() {
    // our output
    Serial.begin(115200);

    // sensor baud rate is 9600
    pmsSerial.begin(9600);
}

void loop() {
    readPMSdata(&pmsSerial);
    if (digitalRead(4)) {
        String ret = String(new_data) + "," + String(data.pm10_standard) + "," + String(data.pm25_standard) + "," + String(data.pm100_standard) + "," + String(data.pm10_env) + "," + String(data.pm25_env) + "," + String(data.pm100_env) + "," + String(data.particles_03um) + "," + String(data.particles_05um) + "," + String(data.particles_10um) + "," + String(data.particles_25um) + "," + String(data.particles_100um) + ",\n";
        Serial.print(ret);
        new_data = false;
        while (digitalRead(4))
            ;
    }
}

boolean readPMSdata(Stream *s) {
    if (!s->available()) {
        return false;
    }

    // Read a byte at a time until we get to the special '0x42' start-byte
    if (s->peek() != 0x42) {
        s->read();
        return false;
    }

    // Now read all 32 bytes
    if (s->available() < 32) {
        return false;
    }

    uint8_t buffer[32];
    uint16_t sum = 0;
    s->readBytes(buffer, 32);

    // get checksum ready
    for (uint8_t i = 0; i < 30; i++) {
        sum += buffer[i];
    }

    // The data comes in endian'd, this solves it so it works on all platforms
    uint16_t buffer_u16[15];
    for (uint8_t i = 0; i < 15; i++) {
        buffer_u16[i] = buffer[2 + i * 2 + 1];
        buffer_u16[i] += (buffer[2 + i * 2] << 8);
    }

    // put it into a nice struct :)
    memcpy((void *)&data, (void *)buffer_u16, 30);

    if (sum != data.checksum) {
        Serial.println("Checksum failure");
        return false;
    }

    new_data = true;
    // success!
    return true;
}
