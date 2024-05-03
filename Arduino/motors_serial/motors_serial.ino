#include <DHT.h>

//Constants
#define DHTPIN 10     // what pin we're connected to
#define DHTTYPE DHT22   // DHT 22  (AM2302)
DHT dht(DHTPIN, DHTTYPE); //// Initialize DHT sensor for normal 16mhz Arduino

float hum;  //Stores humidity value
float temp; //Stores temperature value


// Motor A connections
int enA = 9;
int in1 = 8;
int in2 = 7;
// Motor B connections
int enB = 3;
int in3 = 5;
int in4 = 4;



void setup() {
  // Set all the motor control pins to outputs
	pinMode(enA, OUTPUT);
	pinMode(enB, OUTPUT);
	pinMode(in1, OUTPUT);
	pinMode(in2, OUTPUT);
	pinMode(in3, OUTPUT);
	pinMode(in4, OUTPUT);
	
	// Turn off motors - Initial state
	digitalWrite(in1, LOW);
	digitalWrite(in2, LOW);
	digitalWrite(in3, LOW);
	digitalWrite(in4, LOW);

  Serial.begin(115200);
  Serial.setTimeout(10);
  dht.begin();

}



int speed = 0;
int power = 57;


void addForward() {
  if(speed < 6) {
    speed++;
  
    if(speed == 0) {
      power-=33;
      digitalWrite(in1, HIGH);
      digitalWrite(in2, LOW);
      digitalWrite(in3, HIGH);
      digitalWrite(in4, LOW);

      analogWrite(enA, 0);
      analogWrite(enB, 0);

    } else if(speed > 0) {
      digitalWrite(in1, HIGH);
      digitalWrite(in2, LOW);
      digitalWrite(in3, HIGH);
      digitalWrite(in4, LOW);

      power+=33;
      analogWrite(enA, power);
      analogWrite(enB, power);
    } else {
      power-=33;
      analogWrite(enA, power);
      analogWrite(enB, power);
    }
  }
}

void addBackward() {
  if(speed > -6) {
    speed--;
  
    if(speed == 0) {
      power-=33;
      digitalWrite(in1, HIGH);
      digitalWrite(in2, LOW);
      digitalWrite(in3, HIGH);
      digitalWrite(in4, LOW);

      analogWrite(enA, 0);
      analogWrite(enB, 0);

    } else if(speed < 0) {
      digitalWrite(in1, LOW);
      digitalWrite(in2, HIGH);
      digitalWrite(in3, LOW);
      digitalWrite(in4, HIGH);

      power+=33;
      analogWrite(enA, power);
      analogWrite(enB, power);
    } else {
      power-=33;
      analogWrite(enA, power);
      analogWrite(enB, power);
    }
  }   
}

void left() {
  digitalWrite(in1, LOW);
  digitalWrite(in2, HIGH);
  digitalWrite(in3, HIGH);
  digitalWrite(in4, LOW);
  analogWrite(enA, 250);
  analogWrite(enB, 250);
  delay(450);

  speed = 0;
  power = 57;

  digitalWrite(in1, LOW);
  digitalWrite(in2, LOW);
  digitalWrite(in3, LOW);
  digitalWrite(in4, LOW);
  analogWrite(enA, 0);
  analogWrite(enB, 0);
}

void right() {
  digitalWrite(in1, HIGH);
  digitalWrite(in2, LOW);
  digitalWrite(in3, LOW);
  digitalWrite(in4, HIGH);
  analogWrite(enA, 250);
  analogWrite(enB, 250);
  delay(450);

  speed = 0;
  power = 57;

  digitalWrite(in1, LOW);
  digitalWrite(in2, LOW);
  digitalWrite(in3, LOW);
  digitalWrite(in4, LOW);
  analogWrite(enA, 0);
  analogWrite(enB, 0);
}

void for_left() {
  digitalWrite(in1, LOW);
  digitalWrite(in2, HIGH);
  digitalWrite(in3, HIGH);
  digitalWrite(in4, LOW);
  analogWrite(enA, 250);
  analogWrite(enB, 250);
  delay(75);

  if(speed == 0) {
    stop();
  } else if(speed < 0) {
    digitalWrite(in1, LOW);
    digitalWrite(in2, HIGH);
    digitalWrite(in3, LOW);
    digitalWrite(in4, HIGH);

    analogWrite(enA, power);
    analogWrite(enB, power);
  } else {
    digitalWrite(in1, HIGH);
    digitalWrite(in2, LOW);
    digitalWrite(in3, HIGH);
    digitalWrite(in4, LOW);

    analogWrite(enA, power);
    analogWrite(enB, power);
  } 
}

void for_right() {
  digitalWrite(in1, HIGH);
  digitalWrite(in2, LOW);
  digitalWrite(in3, LOW);
  digitalWrite(in4, HIGH);
  analogWrite(enA, 250);
  analogWrite(enB, 250);
  delay(75);

  if(speed == 0) {
    stop();
  } else if(speed < 0) {
    digitalWrite(in1, LOW);
    digitalWrite(in2, HIGH);
    digitalWrite(in3, LOW);
    digitalWrite(in4, HIGH);

    analogWrite(enA, power);
    analogWrite(enB, power);
  } else {
    digitalWrite(in1, HIGH);
    digitalWrite(in2, LOW);
    digitalWrite(in3, HIGH);
    digitalWrite(in4, LOW);

    analogWrite(enA, power);
    analogWrite(enB, power);
  } 
}

void stop() {
  speed = 0;
  power = 57;

  digitalWrite(in1, LOW);
  digitalWrite(in2, LOW);
  digitalWrite(in3, LOW);
  digitalWrite(in4, LOW);
  analogWrite(enA, 0);
  analogWrite(enB, 0);
}



String msg;

void run_motors() {
  if(Serial.available() > 0) {
    msg = Serial.readString();
    msg.trim();

    if(msg=="forward")
      addForward();
    else if(msg=="backward")
      addBackward();
    else if(msg=="left")
      left();
    else if(msg=="right")
      right();
    else if(msg=="for-left")
      for_left();
    else if(msg=="for-right")
      for_right();
    else if(msg=="stop")
      stop();
  }
}

int i = 0;

void sensor() {
  if(i == 600000) {
    //Read data and store it to variables hum and temp
    hum = dht.readHumidity();
    temp= dht.readTemperature();
    //Print temp and humidity values to serial monitor
    Serial.print("Humidity: ");
    Serial.print(hum);
    Serial.print(" %, Temp: ");
    Serial.print(temp);
    Serial.println(" Celsius");
    //delay(2000); //Delay 2 sec.

    i = 0;
  }
  i++;
}



void loop() {

    sensor();

    run_motors();

}
