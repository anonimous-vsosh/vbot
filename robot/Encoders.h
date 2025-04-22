#ifndef ENCODERS_H
#define ENCODERS_H

volatile long lt = 0, rt = 0;

void lenc() {
  if (!digitalRead(8)) lt++;
  else lt--;
}

void renc() {
  if (digitalRead(11)) rt++;
  else rt--;
}

void initEncoders() {
  pinMode(8, INPUT);
  pinMode(11, INPUT);
  attachInterrupt(0, lenc, RISING);
  attachInterrupt(1, renc, RISING);
}

#endif
