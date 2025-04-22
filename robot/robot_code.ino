#include "Motors.h"
#include "Encoders.h"
#include "LineSensors.h"
#include "Turns.h"
#include "ColorSensor.h"

void setup() {
  Serial.begin(9600);

  // Инициализация пинов моторов и сенсоров
  pinMode(2, INPUT);
  pinMode(3, INPUT);
  pinMode(5, OUTPUT);
  pinMode(6, OUTPUT);
  pinMode(9, OUTPUT);
  pinMode(10, OUTPUT);
  pinMode(A1, INPUT);
  pinMode(A2, INPUT);

  initEncoders();
  initColorSensor();

  // Останов и сброс энкодеров
  for (int i = 0; i < 5; ++i) stop();
  lt = rt = 0;

  calibrate();

  last_err = lineL() - lineR();

  delay(2000);
}

void loop() {
  move_line_to_cross(3);
  turnR();
  move_line_to_cross(3);
  turnL();
  move_line_to_cross();

  long finish = millis() + 400;
  while (millis() < finish) {
    int err = lt - rt;
    setMotors(200 - err * 10, 200 + err * 10);
  }
  stop();

  String color = get_color();
  Serial.print("Detected color: ");
  Serial.println(color);

  while (true);
}
