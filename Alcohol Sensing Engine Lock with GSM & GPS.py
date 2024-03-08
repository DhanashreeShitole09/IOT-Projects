// ALCOHOL SENSING ENGINE LOCK WITH GSM & GPS


#include<LiquidCrystal.h>
#include<SoftwareSerial.h>
#include<string.h>

LiquidCrystal lcd(8,9,10,11,12,13);
SoftwareSerial gps(6,7);

#define sensor A0
#define motor A5
#define buzzer 3

int b;
long a;
long value;

String gpString="";

int  gps_status=0;
int i;

char *test="$GNGGA";
      
float logitude;
float latitude;
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  

void lcdrst()
{
  digitalWrite(8, LOW);
  delay(200);
  digitalWrite(8, HIGH);
  delay(200);
  digitalWrite(8, LOW);
  delay(200);
}

void setup() 
{
gps.begin(9600); lcd.begin(16,2);

pinMode(motor,OUTPUT); pinMode(8, OUTPUT); pinMode(buzzer,OUTPUT);

lcd.clear();
lcd.setCursor(0,0); 
lcd.print("   WELCOME..!");
delay(2000);

lcd.clear();
lcd.setCursor(0,0); 
lcd.print("ALCOHOL IGNITION");
lcd.setCursor(0,1); 
lcd.print(" LOCKING SYSTEM ");
delay(2000);
   
   gps.println("AT");
   delay(500);
   gps.println("ATE0");
   delay(500);
   gps.println("AT+CMGF=1");
   delay(500);
   gps.println("AT&W");
   delay(500);  
 
}

void loop() 
{
   {
    gpString="";
    while(1)
    {
    
      while (gps.available()>0)                //Serial incoming data from GPS
      {
      
        char inChar = (char)gps.read();
        gpString+= inChar;                    //store incomming data from GPS to temparary string str[]
        i++;
        if (i < 7)                      
        {
          if(gpString[i-1] != test[i-1])         //check for right string
          {
            i=0;
            gpString="";
          }
        }
  
        if(inChar=='\r')
        {
             
          if(i >=65) 
          {
            gps_status=1;//
            break;
          }
        
          else
          {
          i=0;
          }
        }
      }
  
      if(gps_status)
      break;
    
    }

  }

  
  if(gps_status==1)
  {
    Degree_to_Decimal();
    delay(500);
  } 


  
a=analogRead(sensor);
value=(a/10);

if((a<=400))
{
digitalWrite(motor, HIGH);  
delay(1000);
lcdrst();

lcd.clear();
lcd.setCursor(0,0); 
lcd.print(" ALCOHOL % = ");
lcd.print(value);
lcd.setCursor(0,1); 
lcd.print("   CAR IS  ON"); 
delay(300);
b=1;
}

if((a>400)&&b==1)
{  
digitalWrite(motor, LOW);
delay(1000);
lcdrst();
lcd.clear();
lcd.setCursor(0,0); 
lcd.print(" ALCOHOL % = ");
lcd.print(value);
lcd.setCursor(0,1); 
lcd.print("   CAR IS OFF");
delay(500);
 
digitalWrite(buzzer,HIGH);
delay(100);
digitalWrite(buzzer,LOW);
delay(100);
digitalWrite(buzzer,HIGH);
delay(100);
digitalWrite(buzzer,LOW);
delay(100); 
 
  gps.print("AT+CMGS=\"+919225767509\"\r");
  delay(100);
  gps.println("Report Form ALCOHOL IGNITION LOCK");
  delay(100);
  gps.println("ALCOHOL % is HIGH");
  delay(100);
  gps.println("VEHICLE IS LOCKED AT"); 
  delay(50);
  gps.print("www.google.co.in/maps/@");
  delay(50);
  gps.print(latitude, 6);
  gps.print(",");
  gps.print(logitude, 6);
  gps.print(",299m/data=!3m1!1e3");  
  gps.print("\r\n");
  delay(500);    
  gps.write(26);
  
  
  
  lcd.clear();
  lcd.setCursor(0,0); 
  lcd.print("    SMS SENT");
  delay(2000);

lcd.clear();
lcd.setCursor(0,0); 
lcd.print("   CAR IS OFF");
delay(200);
b=0;
}

i=0;
gps_status=0;

}
void Degree_to_Decimal()
{
        //for(latitude)
        {
        String lat_degree="";
      
          for(i=18;i<20;i++)          //extract latitude from string
          {
            lat_degree+=gpString[i];
          }
          
          float degree=lat_degree.toFloat();
       
        String lat_minut="";
          for(i=20;i<27;i++)          //extract longitude from string
          {
          lat_minut+=gpString[i];
          }
          float minut= lat_minut.toFloat();
      
          minut=minut/60;
          latitude=degree+minut;
        }
  
        //for(lagitude)
        {
        String log_degree="";
      
          for(i=31;i<33;i++)          //extract latitude from string
          {
            log_degree+=gpString[i];
          }
          
          float degree=log_degree.toFloat();
       
        String log_minut="";
          for(i=33;i<39;i++)          //extract longitude from string
          {
          log_minut+=gpString[i];
          }
          float minut= log_minut.toFloat();
      
          minut=minut/60;
          logitude=degree+minut;
        }
  
}