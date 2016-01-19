

#include <Servo.h>
#include <Wire.h>
//#include <time.h>
#include <stdlib.h>
#include <stdio.h>
#include <iostream>
#include <unistd.h>

//#define int num_sequences = 10;
//#define int num_chromes = 10;

Servo servo1;
Servo servo2;

FILE * file;
FILE * wFile;
//FILE * r.state;

int NUM_SEQ = 1;

int NUM_CHROMO = 10;
int current_seq = 0;
int previous_seq = 0;
void setup() {
  Serial.begin(9600);
  delay(15000);
  boolean experiment = true;

                       delay(2000);
  int generation[][5][5][3] = {0};
  int result;

  while (experiment) {
    const char *state = "/media/galileo/state.txt";
    result = access(state, F_OK);
    Serial.println(result);
    while (result == -1) {

      result = access(state, F_OK);
      Serial.println("State file does not exist");
      delay(2000);
      servo1.write(90);
      servo2.write(90);
    }
    while (result != -1) {
      delay(1000);
      Serial.println("found file");
      int state_num;

      FILE* state = fopen("/media/galileo/state.txt", "r");
      fscanf(state, "%d" , &state_num);
      fclose(state);

      Serial.println(state_num);

      if (state_num == 0) {
        Serial.println("Current State: " + state_num);
        Serial.println("Move to start area");
      }
      else if ( state_num == 1) {
        Serial.print("Current State: ");
        Serial.println(state_num);
        servo1.attach(9);
        servo2.attach(11);
        servo1.write(90);
        servo2.write(90);
        fileRead(generation);

        execution(generation, current_seq);
      }

      else if ( state_num == 2) {

        Serial.print("Current State: ");
        Serial.println(state_num);
        Serial.println("Finished sequence, analyzing . . . ");
        Serial.print(current_seq);
      }





      else if (state_num == 3) {
        if (current_seq == 5) {
          Serial.println("End of Gen found");
          delay(5000);
          stateChange(4);
        } else {

          stateChange(0);
        }
      }
      else if (state_num == 4) {

        Serial.println("Waiting for python");
      }
      else if (state_num == 5) {
        current_seq = current_seq * 0;
        Serial.print("Current State: ");
        Serial.println(state_num);
        Serial.println("Finished generation, analyzing . . . ");

        servo1.detach();
        servo2.detach();
        stateChange(0);


      }
      else if (state_num == 6) {
        if (current_seq - previous_seq == 1) {

          Serial.println(current_seq);
          current_seq = current_seq - 1;
          Serial.println(current_seq);
          stateChange(0);
        } else {
          Serial.println(current_seq);
          stateChange(0);
        }

      }
      else if (state_num == 7) {
        Serial.println("Experiment has finished");
        delay(10000);
        //experiment = false
      }
    }
  }
}

void loop() {

}

void fileRead(int generation[][5][5][3]) {
  int NUM_SEQ = 100;
  int NUM_CHROMO = 100;
  int lineSize = 1300;
  Serial.println("Trying to open file . . . ");

  file = fopen("/media/galileo/generation.txt", "r");

  if (!file) {
    Serial.println("File does not exist");
    delay(3000);
  }
  if (file == NULL) {
    Serial.println("Something went wrong");
    stateChange(4);

  }
  int line;
  char buffer[3];

  for (int i = 0; i < 5; i++) {
    for (int j = 0; j < 5; j++) {
      for ( int k = 0; k < 3; k++) {
        if (fscanf(file, "%d,", &line) != 1) {
          break;
        }

        generation[0][i][j][k] = line;

      }
    }
  }
  fclose(file);
}

void stateChange(int rstate) {
  wFile = fopen("/media/galileo/state.txt", "w");
  while ( wFile == NULL) {
    Serial.println("State File is nonexistant or open already");
  }
  fprintf(wFile, "%d", rstate);
  fclose(wFile);
}

void writeTime(float time) {
  FILE* tFile = fopen("/media/galileo/tfile.txt", "w");
  fprintf(tFile, "%f", time);
  fclose(tFile);
}

int checkState() {
  int state_num;

  FILE* state = fopen("/media/galileo/state.txt", "r");
  while (state == NULL) {
    Serial.println("Waiting to check state...");
  }
  fscanf(state, "%d" , &state_num);
  fclose(state);

  return state_num;
}

int execution(int generation[0][5][5][3], int curr_seq) {
  int current[] = {90, 90};
  int startSeq = 0;

  startSeq = millis();
  for (int j = 0; j < 5; j++) {

    int start = millis();
    Serial.println("Starting ramp...");
    while (start >= millis() - 1000) {
      //Serial.println(millis());
      float t = (millis() - start) / 1000.0;
      int m1 = ((1 - t) * current[0]) + (generation[0][curr_seq][j][0] * t);
      int m2 = ((1 - t) * current[1]) + (generation[0][curr_seq][j][1] * t);

      servo1.write(m1);
      servo2.write(m2);

      //Serial.println(t);
      //Serial.println(m1);
      //Serial.println(m2);

    }
    delay(50);
    Serial.println(curr_seq);
    Serial.println("Finished ramping");
    Serial.print("Current m1 speed: ");

    Serial.print(generation[0][curr_seq][j][0]);
    Serial.print(" | Current m2 speed: ");
    Serial.println(generation[0][curr_seq][j][1]);
    servo1.write(generation[0][curr_seq][j][0]);
    servo2.write(generation[0][curr_seq][j][1]);
    current[0] = generation[0][curr_seq][j][0];
    current[1] = generation[0][curr_seq][j][1];
    delay((generation[0][curr_seq][j][2] * 1000) );

  }
  Serial.println("Finished Sequence");
  servo1.detach();
  servo2.detach();
  int tStop = millis();

  int state = checkState();

  if (state == 6) {
    Serial.println("Data loss detected, restarting sequence");
    stateChange(0);
  } else {

    writeTime((tStop - startSeq) / 1000.0);
    previous_seq = current_seq;
    current_seq = current_seq + 1;
    Serial.println("next State");

    stateChange(2);
  }


}






