#ifndef MOTORS_H
#define MOTORS_H

void setMotors(int L, int R) {
  if (L < 0) {
    digitalWrite(9, 1);
    analogWrite(10, 255 - abs(L));
  } else {
    digitalWrite(10, 1);
    analogWrite(9, 255 - abs(L));
  }

  if (R > 0) {
    digitalWrite(5, 1);
    analogWrite(6, 255 - abs(R));
  } else {
    digitalWrite(6, 1);
    analogWrite(5, 255 - abs(R));
  }
}

void stop() {
  for (int i = 0, s = 255; i < 30; ++i, s = -s) {
    setMotors(s, s);
    delay(5);
  }
  setMotors(0, 0);
}

#endif
