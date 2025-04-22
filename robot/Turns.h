#ifndef TURNS_H
#define TURNS_H

void get_line(int t = 500) {
  long finish = millis() + t;
  while (millis() < finish) {
    move_line(0, 0.2, 2);
  }
  stop();
}

void turnL(int n = 1, int speed = 100) {
  while (n--) {
    while (lineL() > grey) setMotors(-speed, speed);
    while (lineL() < grey) setMotors(-speed, speed);
  }
  get_line();
}

void turnR(int n = 1, int speed = 100) {
  while (n--) {
    while (lineR() > grey) setMotors(speed, -speed);
    while (lineR() < grey) setMotors(speed, -speed);
  }
  get_line();
}

#endif
