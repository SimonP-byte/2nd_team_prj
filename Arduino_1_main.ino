
#include <SoftwareSerial.h>
//system

#include <stdio.h>
#include <string.h>
#include <stdlib.h>

// My LIB
#include "My_Arduino_GPIO_Lib_V1_6.h"

#define BZ A5 // 부저 핀7번
#define flame 12 // 불꽃감지 센서 핀8번
#define MQ A0

// 3color LED
#define LED_R 3
#define LED_G  4
#define LED_B  5

#define Tx_pin 8
#define Rx_pin 7
#define RS485_EN 2

// Software 시리얼 객체선언 
SoftwareSerial RS485(Rx_pin, Tx_pin);

// 변수선언
struct FLAG{
  char rx_flag;
  char tx_flag;
  char com_flag;
  char com_chk_flag;
}flag = {0, 0, 0, 0};
struct FLAG *f_p = &flag;

struct BUFF{
  char rx_buf[20] = {0, };
  char tx_buf_1[20] = "S00100\n";
  char tx_buf_2[20] = "S00101\n";
}buf;
struct BUFF *b_p = &buf;

int lop = 0;
int ALM_1 = 0;   // 불꽃 감지 알림
int ALM_2 = 0;   // 가스 감지 알림
int ALM_3 = 0;   // 통신(라즈베리파이) 알람 신호 수신
int state = 0;   // 불꽃감지 센서
int mq_value = 0; // 가스검출 센서

// ################################################
// ################### function ###################


//=========================== 불꽃감지 센서
void FIR(){
  state = digitalRead(flame);     // 불꽃감지센서값 입력받음
  //Serial.println(state);  
   if(state == 0){   // 0 이상있음                // 불꽃감지센서가 0일 때 
         ALM_1= 1;  
             
   }
   //else{                             // 불꽃감지센서가 1일 떄
    //ALM_1 = 0;         
    //}
}
//================== gas 감지센서

void GAS(){
mq_value=analogRead(MQ);        // 가스검출 센서 입력
if(mq_value > 450){           
  ALM_2= 1;
}
//else{
  //ALM_2= 0;
//}
//delay(1000);
}
//=========================== 알림(출력) 


void ALM(){
    // Serial.print("ALM_1 : ");
    // Serial.print(ALM_1);
    // Serial.print("\tALM_2 : ");
    // Serial.print(ALM_2);
    // Serial.print("\tALM_3 : ");
    // Serial.println(ALM_3);
  if(ALM_1 == 1 || ALM_2 == 1 || ALM_3){
    digitalWrite(A5, 0);
    d_out(LED_R,255);
    d_out(LED_G,0);
    //Serial.println("fire");
  }
  else{
    digitalWrite(A5, 1); 
    d_out(LED_R,0);
    d_out(LED_G,255);
  }
  
}
//###########################sensor func end######################



void receive_data(){
  // 수신 - 프로토콜 종료 == '\n'
  int i = 0; // 인덱스

  // S/W 시리얼에 정보가 있는가 && 정보송신 flag가 0인가 (송/수신 상호방해금지)
  while(RS485.available() && flag.rx_flag == 0){
    // '\n' 문자를 받기 전까지 rx_buf 배열에 시리얼 값을 저장
    buf.rx_buf[i] = RS485.read();
    // 수신 완료시, 수신완료 flag on 수신금지
    // 커맨드 체크 플래그 on
    if(buf.rx_buf[i] == '\n') {
      flag.rx_flag = 1;
      flag.com_chk_flag = 1;
      i = 0;
      break;
    }
    i++;
  }
}

void send_data(){

  digitalWrite(RS485_EN, 1);
  
  if(flag.com_flag == 1){
    RS485.write(buf.tx_buf_1);
    digitalWrite(RS485_EN, 0);
  }
  else if(flag.com_flag == 2){
    RS485.write(buf.tx_buf_2);
    digitalWrite(RS485_EN, 0);
  }
  delay(500);
  flag.rx_flag = 0;
  flag.tx_flag = 0;
  flag.com_flag = 0;
}

void com_chk(){
  // 임시변수
  char buf_tp[20];

  // 구조체변수는 공용 자원이기 때문에 com_chk 함수 중간에 변경될 수 있음
  // 따라서 buf_tp (temperate 변수)에 값을 복사
  memcpy(buf_tp, buf.rx_buf, sizeof(buf.rx_buf));
  
  // 송신 - rx_buf[1 ~ 3] == 아두이노 일련번호 (해당 기기의 경우 001)
  //        rx_buf[4 ~ 5] == 수행동작 명령
  //        if(rx_buf[4, 5] == 00) -> 센서값을 Rpi측으로 전송
  //        if(rx_buf[4, 5] == 01) -> ex)모터 작동
  // Serial.print("Received data: ");
  // Serial.println(buf_tp);
  // 아두이노 001에 내려진 명령인가 판별
  if(buf_tp[1] == '0' && buf_tp[2] == '0' && buf_tp[3] == '1'){
    // Rpi에서 받아온 (아두이노002번에 대한)정보가 00인가 판별
    // Serial.print("ALM_1 : ");
    // Serial.print(ALM_1);
    // Serial.print("\tALM_2 : ");
    // Serial.println(ALM_2);
    if(buf_tp[4] == '0' && buf_tp[5] == '0'){
      if(ALM_1 == 1 || ALM_2 == 1){ // 스위치가 눌렸다면 (센서로 교체)
        flag.tx_flag = 1;   // 송신 flag ON
        flag.com_flag = 2;  // 명령 플래그 1 == 이상없음
        Serial.println("Emergency code sent");
      }
      else { // 스위치가 눌리지 않았다면 (센서로 교체)
        flag.tx_flag = 1;   // 송신 flag ON
        flag.com_flag = 1;  // 명령 플래그 2 == 이상있음 (다른기기에)
        Serial.println("Normal code sent");
      }
      ALM_1 = 0;
      ALM_2 = 0;
      ALM_3 = 0;
    }
    else if(buf_tp[4] == '0' && buf_tp[5] == '1'){
      Serial.println("Emergency code received");
      flag.rx_flag = 0;
      ALM_3 = 1;
    }
  }
  else flag.rx_flag = 0;  // 데이터가 깨져서 들어왔을경우
  flag.com_chk_flag = 0;  // 커맨드체크 완료 flag
}


// ################### func end ###################
// ################################################

void setup() {
  // 송-수신, 485 Enable 핀 초기화 
  pinMode(Rx_pin, INPUT);
  pinMode(Tx_pin, OUTPUT);
  pinMode(RS485_EN, OUTPUT);
  digitalWrite(RS485_EN, 0); // 485 기본상태 = 수신

  // 소프트웨어, 하드웨어 Serial 통신 시작
  RS485.begin(9600);  // Software UART
  Serial.begin(115200); // Hardware UART

  // 테스트용 pin 선언
  pinMode(13, OUTPUT);
  pinMode(A1, INPUT_PULLUP);
  pinMode(BZ, OUTPUT);
  digitalWrite(A5, 1); 
  pinMode(flame, INPUT);
}

void loop() {
  
  FIR();
  GAS();
  ALM();

  lop++;

  if(lop > 5000){
    receive_data(); // 읽으면 rx_data == 1
    lop = 0;
  }

  if(flag.com_chk_flag == 1) {
    com_chk();
     if(flag.tx_flag == 1){
      send_data();
    }
  }
}
