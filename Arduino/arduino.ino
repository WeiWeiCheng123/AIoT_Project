#define wake_btn 2
#define red 9
#define green 10
#define blue 11

String str;

void setup() {
  pinMode(wake_btn, INPUT);
  pinMode(red, OUTPUT);
  pinMode(green, OUTPUT);
  pinMode(blue, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  if (digitalRead(wake_btn) == HIGH) {
    Serial.println("wake");
    delay(500);
  }
  
  if (Serial.available()) {
    // 讀取傳入的字串直到"\n"結尾
    str = Serial.readStringUntil('\n');

    if (str == "0") {           // 若字串值是 "LED_ON" 開燈
      analogWrite(red, 255);
      analogWrite(green, 255);
      analogWrite(blue, 0);
      Serial.println("皮卡丘"); // 回應訊息給電腦
    } else if (str == "1") {
      analogWrite(red, 255);
      analogWrite(green, 0);
      analogWrite(blue, 0);
      Serial.println("小火龍");
    } else if (str == "2") {
      analogWrite(red, 0);
      analogWrite(green, 255);
      analogWrite(blue, 0);
      Serial.println("妙蛙種子");
    }
  }
}
