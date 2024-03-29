// SMART STREET LIGHT SYSTEM



#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>
#include <ESP8266mDNS.h>

#ifndef STASSID
#define STASSID "Shree"
#define STAPSK  "Shree123"
#endif

const char *ssid = STASSID;
const char *password = STAPSK;

//ldr
int ldr;
int led1=16;

//ultrasonic

const int trigPin = 4; //D2
const int echoPin = 5; //D1
int led2 = 0;    //D3
//define variables
long duration;
int distance;
ESP8266WebServer server(80);

const int led = 13;

void handleRoot() {
  digitalWrite(led, 1);
  char temp[400];
  int sec = millis() / 1000;
  int min = sec / 60;
  int hr = min / 60;

  snprintf(temp, 400,

           "<html>\
  <head>\
    <meta http-equiv='refresh' content='1'/>\
    <title>ESP8266 Demo</title>\
    <style>\
      body { background-color: #cccccc; font-family: Arial, Helvetica, Sans-Serif; Color: #000088; }\
    </style>\
  </head>\
  <body>\
    <h1>distance is :%02d</h1>\
    <h2>ldr is:%02f</h2>\
  </body>\
</html>",

           distance
           
          );
  server.send(200, "text/html", temp);
  digitalWrite(led, 0);
}

void handleNotFound() {
  digitalWrite(led, 1);
  String message = "File Not Found\n\n";
  message += "URI: ";
  message += server.uri();
  message += "\nMethod: ";
  message += (server.method() == HTTP_GET) ? "GET" : "POST";
  message += "\nArguments: ";
  message += server.args();
  message += "\n";

  for (uint8_t i = 0; i < server.args(); i++) {
    message += " " + server.argName(i) + ": " + server.arg(i) + "\n";
  }

  server.send(404, "text/plain", message);
  digitalWrite(led, 0);
}

void drawGraph() {
  String out;
  out.reserve(2600);
  char temp[70];
  out += "<svg xmlns=\"http://www.w3.org/2000/svg\" version=\"1.1\" width=\"400\" height=\"150\">\n";
  out += "<rect width=\"400\" height=\"150\" fill=\"rgb(250, 230, 210)\" stroke-width=\"1\" stroke=\"rgb(0, 0, 0)\" />\n";
  out += "<g stroke=\"black\">\n";
  int y = rand() % 130;
  for (int x = 10; x < 390; x += 10) {
    int y2 = rand() % 130;
    sprintf(temp, "<line x1=\"%d\" y1=\"%d\" x2=\"%d\" y2=\"%d\" stroke-width=\"1\" />\n", x, 140 - y, x + 10, 140 - y2);
    out += temp;
    y = y2;
  }
  out += "</g>\n</svg>\n";

  server.send(200, "image/svg+xml", out);
}



void setup(void) {

  //ldr
  pinMode(led1,OUTPUT); 
 pinMode(A0,INPUT);
Serial.begin(115200);

 //ultrasonic
 pinMode (trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  pinMode(led2,OUTPUT);
 
  pinMode(led, OUTPUT);
  digitalWrite(led, 0);
  Serial.begin(115200);
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  Serial.println("");

  // Wait for connection
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.print("Connected to ");
  Serial.println(ssid);
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());

  if (MDNS.begin("esp8266")) {
    Serial.println("MDNS responder started");
  }

  server.on("/", handleRoot);
  server.on("/test.svg", drawGraph);
  server.on("/inline", []() {
    server.send(200, "text/plain", "this works as well");
  });
  server.onNotFound(handleNotFound);
  server.begin();
  Serial.println("HTTP server started");
}

void loop(void) {
  server.handleClient();
  MDNS.update();

//ultrasonic
             { digitalWrite(trigPin, LOW);
              delayMicroseconds(2);
              digitalWrite(trigPin, HIGH);
              delayMicroseconds(10);
              digitalWrite(trigPin, LOW);
            
             duration = pulseIn(echoPin, HIGH);
             distance = duration*0.034/2;
             Serial.print("distance:");
             Serial.println(distance);
             }
             //ldr
            ldr=analogRead(A0);
                  Serial.println(ldr);
                   if(ldr>=200){
                      digitalWrite(led1,LOW);
                      Serial.println("Light off");
                      
                   
                  }
                  else
                  {
                    digitalWrite(led1, HIGH);
                    Serial.println("Light ON");
                    if(distance <=10)
                       {digitalWrite(led2,HIGH);
                       }else
                       {digitalWrite(led2,LOW);
                       }
                    
                    }
                    delay(1000);
                    server.on("/",handleRoot);

}
