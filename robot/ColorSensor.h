#ifndef COLORSENSOR_H
#define COLORSENSOR_H

#include <Wire.h>
#include "Adafruit_TCS34725.h"

Adafruit_TCS34725 tcs = Adafruit_TCS34725(TCS34725_INTEGRATIONTIME_101MS, TCS34725_GAIN_1X);

void initColorSensor() {
  while (!tcs.begin()) {
    Serial.println("No TCS34725 found");
  }
  Serial.println("Found sensor");
}

String get_color() {
  uint16_t r, g, b, w, colorTemp, lux;
  tcs.getRawData(&r, &g, &b, &w);
  colorTemp = tcs.calculateColorTemperature_dn40(r, g, b, w);

  if ((colorTemp > 4000) && (colorTemp < 5500)) return "void";
  else if (colorTemp > 5500) return "blue";
  else {
    if ((float)r / g > 1.8) return "red";
    else return "yellow";
  }
}

#endif
