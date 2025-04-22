
#ifndef LINESENSORS_H
#define LINESENSORS_H

int last_err;
int minL, minR, maxL, maxR, minM = 100, maxM = 900, grey = 700;

int readL() {
  return analogRead(A1);
}

int readR() {
  return analogRead(A2);
}

void calibrate() {
  minL = 0, minR = 0, maxL = 1023, maxR = 1023;
  lt = 1000;
  rt = -1000;
  while (rt != 0) {
    minL = max(minL, readL());
    minR = max(minR, readR());
    maxL = min(maxL, readL());
    maxR = min(maxR, readR());
    setMotors(constrain(lt * -30, -100, 100), constrain(rt * -30, -100, 100));
  }
  lt = -1000;
  rt = 1000;
  while (rt != 0) {
    minL = max(minL, readL());
    minR = max(minR, readR());
    maxL = min(maxL, readL());
    maxR = min(maxR, readR());
    setMotors(constrain(lt * -30, -100, 100), constrain(rt * -30, -100, 100));
  }
  setMotors(0, 0);
}

int lineL() {
  return map(readL(), minL, maxL, minM, maxM);
}

int lineR() {
  return map(readR(), minR, maxR, minM, maxM);
}

void move_line(int speed = 100, float kp = 0.1, float kd = 0.8) {
  int errP = lineL() - lineR();
  int errD = errP - last_err;
  int U = errP * kp + errD * kd;
  setMotors(speed - U, speed + U);
  last_err = errP;
}

void move_line_to_cross(int n = 1, int t = 270, int speed = 100, float kp = 0.15, float kd = 2) {
  bool f = 0;
  while (n) {
    move_line(speed, kp, kd);
    if (lineL() > grey && lineR() > grey && !f) {
      --n;
      f = 1;
    } else if (lineL() < grey && lineR() < grey && f) {
      f = 0;
    }
  }
  long finish = millis() + t;
  while (millis() < finish) {
    move_line(speed, kp, kd);
  }
  stop();
}

#endif
