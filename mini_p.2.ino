//system

#include <stdio.h>
#include <string.h>
#include <stdlib.h>

// My LIB
#include "My_Arduino_GPIO_Lib_V1_6.h"

#define BZ 10 // 부저 핀7번
#define flame 11 // 불꽃감지 센서 핀8번
#define MQ A0

// 3color LED
#define LED_R  3
#define LED_G  5
#define LED_B  6
struct SENSOR
{
int ALM_1 = 0;   // 불꽃감지 알림
int ALM_2 = 0;   // 가스감지 알림 
int state = 0;   //
int mq_value = 0;
}sen;

//=========================== 불꽃감지 센서
void FIR(){
  sen.state = digitalRead(flame);     // 불꽃감지센서값 입력받음
  if(sen.state == 0){                 // 불꽃감지센서가 0일 때 
    Serial.println("ON");        // 시리얼 통신에 센서값 출력
    //delay(1000);
   }
else{                             // 불꽃감지센서가 1일 떄
  Serial.println("OFF");          // 시리얼 통신에 센서값 출력
  //delay(1000);
  }
}
//================== gas 감지센서

void GAS(){
sen.mq_value=analogRead(MQ);
Serial.println(sen.mq_value);
//delay(1000);
}
//=========================== 부저 


 void sound_func(){
 if(sen.state == 1){
  digitalWrite(7, 1); 
  }
else{
    digitalWrite(7, 0); 
  }
}
//================== RGB 3color
void set_color(int r, int g, int b)
{
  analogWrite(LED_R, r);  // PWM 출력 나가는것 값이 클수록 펄스 폭이 길어진다  
  analogWrite(LED_G, g);
  analogWrite(LED_B, b);
}
//=================== color 0일때 RED , 1일떄 GREEN
void color(){
  if(sen.mq_value > 450)
  {
    d_out(LED_R, 255);
    d_out(LED_G, 0);
    sen.ALM_2 = 1;
  }
  else
  {
    d_out(LED_R, 0);
    d_out(LED_G, 255);
    sen.ALM_2 = 0;
  }
}
//================
void setup() {
pinMode(flame, INPUT_PULLUP);            // 불꽃감지센서를 입력으로
pinMode(BZ, OUTPUT);               // 부저를 출력으로
pinMode(MQ, INPUT);
Serial.begin(9600);
}

//================
void loop() 
{
 FIR();
 sound_func();
 color();
 GAS();
}





