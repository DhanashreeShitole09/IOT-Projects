// SMART HOME AUTOMATION SYSTEM


#include <SoftwareSerial.h>     // serial header file include

#include <LiquidCrystal.h>
LiquidCrystal lcd(8, 9, 10, 11, 12, 13);//RS,EN,D4,D5,D6,D7

#include <String.h>

SoftwareSerial mySerial(6, 7);  //rx tx

#include <dht.h>
#define buzzer 3
#define fan A1 
#define bulb A0
#define light 2

dht DHT;

float humi;
int humi_temp;

//temperature
float analogtemp = A5;  // define analog I/P pin to A0
float temp = 0;         // float type vairable temp = 0;
float tempValue = 0;    // float type vairable sensor value =0;


//gas
float analoggas = A4;   // define analog I/P pin to A2
float gas = 0;          // float type vairable CO2 = 0;
float gasValue = 0;     // float type vairable sensor value =0;

//humidity
#define DHT11_PIN A3

int count;
int a=0;

  void buzz()
  {
    digitalWrite(buzzer,HIGH);
    delay(500);
    digitalWrite(buzzer,LOW);
    delay(200);
    digitalWrite(buzzer,HIGH);
    delay(500);
    digitalWrite(buzzer,LOW);
    delay(200);   
  }

void setup() 
{ 
  pinMode(fan,OUTPUT);
  pinMode(bulb,OUTPUT);
  pinMode(light,INPUT);
  
   lcd.begin(16, 2);                 // set up the LCD's number of columns and rows:
   Serial.begin(9600);                //serial communication enabling by 9600 baud rate
   mySerial.begin(115200);
   
   lcd.begin(16, 2);                 // LCD's number of columns and rows:
   lcd.setCursor(0,0);               // column 0 , row 1
   lcd.print(" IOT BASED HOME");    // lcd print Digital Art!
   lcd.setCursor(0,1);             // column 0 , row 1
   lcd.print("   AUTOMATION");     // lcd print Digital Art!
   
  buzz();
  buzz();
  buzz();
}

void loop()
{
  
//light
  if((digitalRead(light))&& a==0)
  {
    digitalWrite(bulb,HIGH);
    lcd.clear();
    lcd.setCursor(0,0);          
    lcd.print("   BULB IS ON"); 
    delay(2000); 
    a=100;  
   }
  if((!digitalRead(light))&& a==100)
  {
    digitalWrite(bulb,LOW);
    lcd.clear();
    lcd.setCursor(0,0);          
    lcd.print("  BULB  IS OFF"); 
    delay(2000); 
    a=0;  
   }

//temperature
  tempValue = analogRead(analogtemp);
  temp = (tempValue * 500.0) / 1024;
  lcd.clear();
  lcd.setCursor(0,0);          
  lcd.print("  Temp = ");  //lcd print temp =
  lcd.print(temp);          //lcd print temp float type vairable    
  delay(2000); 
      if(temp>40)
       {
       digitalWrite(fan,HIGH);
       lcd.clear();
       lcd.setCursor(0,0);          
       lcd.print("  FAN  IS ON"); 
       delay(2000);   
      }
     if(temp<=40)
       {
       digitalWrite(fan,LOW);
       lcd.clear();
       lcd.setCursor(0,0);          
       lcd.print("   FAN IS OFF"); 
       delay(2000);   
       }

//gas
  gasValue = analogRead(analoggas);
  gas = (gasValue / 850);
  lcd.clear();
  lcd.setCursor(0,0);          
  lcd.print("   GAS = ");   //lcd print temp =
  lcd.print(gas,2);        //lcd print temp float type vairable    
  delay(2000);
  

//humidity
  int chk = DHT.read11(DHT11_PIN);
  if(DHT.humidity>=1)
  {
  humi=DHT.humidity+0;   
  }
  lcd.clear();
  lcd.setCursor(0,0);          
  lcd.print("  Humi = ");            //lcd print
  lcd.print(humi);                     //lcd print vairable
  delay(2000);
  
    
    if(gas>=0.6 || humi>=40 || temp>=45.00 || a==100)
    {
      buzz();
      Connecting_wifi();
    }
  
}

void ShowSerialData()
{
  while(mySerial.available()!=0)
    Serial.write(mySerial.read());
}


void Connecting_wifi()
{
    mySerial.println("AT+CIPMUX=0");  //set single connection 
    delay(1000);
      //
      if(mySerial.available())
      {
        if(mySerial.find("OK"))       //if OK available
          {
            lcd.clear();
            lcd.setCursor(0,0);            // row 0 , colomn 0  
            lcd.print("Connecting..OK-1"); // lcd print
          }

        else
          {
            lcd.clear();
            lcd.setCursor(0,0);            // row 0 , colomn 0
            lcd.print("Connecting.error"); // lcd print
          }
      }
      //ShowSerialData();
      delay(2000);
       
    mySerial.println("AT+CIPSTART=\"TCP\",\"api.thingspeak.com\",80");//start up the connection
    delay(1000);
      //
      if(mySerial.available())
      {
        
        if(mySerial.find("OK"))       //if OK available
          {
            lcd.clear();
            lcd.setCursor(0,0);            // row 0 , colomn 0
            lcd.print("Connecting..OK-2"); // lcd print
            buzz();
          }

        else
          {
          lcd.clear();
          lcd.setCursor(0,0);            // row 0 , colomn 0
          lcd.print("Connecting.error"); // lcd print
          }
      }
    //  ShowSerialData();
      delay(2000);
        
      
   mySerial.print("AT+CIPSEND=");//send data through this TCP Connection.
    String str="GET https://api.thingspeak.com/update?api_key=FM84GLWQCAN5E6VR&field1=" + String(temp)+"&field2=" + String(gas)+"&field3=" + String(humi)+"&field4=" + String(a);
    mySerial.println(str.length()+2);//send data through this TCP Connection.
    delay(2000);
    
    mySerial.println(str);//send data through this TCP Connection.
    delay(3000);   //waitting for reply, important! the time is base on the condition of internet


    if(mySerial.available())
      {
        if(mySerial.find("SEND OK"))
          {
          lcd.clear();
          lcd.setCursor(0,0);            // row 0 , colomn 0
          lcd.print("  Sending Data  ");  // lcd print
          //delay(1000);

          lcd.setCursor(0,1);             // row 0 , colomn 1
          lcd.print("   Data- Sent   ");  // lcd print
          delay(3000);
          }

        else
          {
          lcd.clear();
          lcd.setCursor(0,0);            // row 0 , colomn 0
          lcd.print("Connecting.error");  // lcd print
          delay(2000);
          }
      }
   
    mySerial.println("AT+CIPCLOSE");//close the connection
    delay(1500);
    ShowSerialData();
}
