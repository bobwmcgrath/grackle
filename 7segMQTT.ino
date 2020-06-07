/*
 Based on "Basic MQTT example" 
*/
//#include <avr/wdt.h> //watch do timer
#include <SPI.h>
#include <Ethernet.h>
#include <PubSubClient.h> //MQTT

#define countdown 0
#define score 0
#define high_score 1
int top_score=0;

//GPIO declarations
//-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
byte segmentClock = 6;
byte segmentLatch = 5;
byte segmentData = 7;
int number = 0;
//-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

// Update these with values suitable for your network.
#if (countdown==1)
  #define MAC_ADDRESS 0xDE, 0xED, 0xBA, 0xFE, 0xFE, 0x01
  #define IPADDRESS 192, 168, 1, 80
  #define CLIENT "countdown"
  #endif
#if (score==1)
  #define MAC_ADDRESS 0xDE, 0xED, 0xBA, 0xFE, 0xFE, 0x02
  #define IPADDRESS 192, 168, 1, 81
  #define CLIENT "score"
  #endif
#if (high_score==1)
  #define MAC_ADDRESS 0xDE, 0xED, 0xBA, 0xFE, 0xFE, 0x03
  #define IPADDRESS 192, 168, 1, 82
  #define CLIENT "high_score"
  #endif
  
byte mac[]   = {MAC_ADDRESS};
IPAddress ip(IPADDRESS);
IPAddress server(192, 168, 1, 239);

void callback(char* topic, byte* payload, unsigned int length) {
  if ((String)topic == "start" && countdown==1)count_down();
  if ((String)topic == "score" && score==1)score_point();
  if ((String)topic == "start" && score==1){
    number=0;
    showNumber(number);
  }
  if ((String)topic == "score" && high_score==1)number++;
  if ((String)topic == "stop" && high_score==1){
    if (number>top_score)top_score=number;
    number=0;
    showNumber(top_score);
  }
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");
  for (int i=0;i<length;i++) {
    Serial.print((char)payload[i]);
  }
  Serial.println();

}

EthernetClient ethClient;
PubSubClient client(ethClient);

void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Attempt to connect
    if (client.connect(CLIENT)) {
      Serial.println("connected");
      // Once connected, publish an announcement...
      client.publish("outTopic","hello world");
      // ... and resubscribe
      client.subscribe("start");
      client.subscribe("score");
      client.subscribe("stop");
      
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}

void setup()
{
  //wdt_enable(WDTO_8S);
  Serial.begin(9600);

  client.setServer(server, 1883);
  client.setCallback(callback);

  Ethernet.begin(mac, ip);
  // Allow the hardware to sort itself out
  delay(1500);
  
  pinMode(segmentClock, OUTPUT);
  pinMode(segmentData, OUTPUT);
  pinMode(segmentLatch, OUTPUT);

  digitalWrite(segmentClock, LOW);
  digitalWrite(segmentData, LOW);
  digitalWrite(segmentLatch, LOW);

  showNumber(number);


}

int swap(int digit)
{
  
  int first_digit = digit/10;
  first_digit = floor(first_digit);
  int second_digit = digit%10;
  int swapped_number = (second_digit*10)+first_digit;

  return swapped_number;

}

void count_down()
{
  number = 31;
  showNumber(number-1); //Test pattern

  while (number!=0)
  {
    delay(980);//1 second - processing
    showNumber(number-1);
    if (number==18)showNumber(number-1);//to fix bizzar glich in displaying the number 17 as 87
    number--;
    
  Serial.println(number); //For debugging
  }
   //Reset x after 99
}

void score_point()
{
  number++;
  showNumber(number);
  delay(150);
}

void loop()
{
  if (!client.connected()) {
    reconnect();
  }
  client.loop();
  //wdt_reset();

}



void showNumber(float value)
{
  int number = abs(value); //Remove negative signs and any decimals
  number = swap(number);
  //Serial.print("number: ");
  //Serial.println(number);

  for (byte x = 0 ; x < 2 ; x++)
  {
    int remainder = number % 10;

    postNumber(remainder, false);

    number /= 10;
  }

  //Latch the current segment data
  digitalWrite(segmentLatch, LOW);
  digitalWrite(segmentLatch, HIGH); //Register moves storage register on the rising edge of RCK
}


//Given a number, or '-', shifts it out to the display
void postNumber(byte number, boolean decimal)
{
  //    -  A
  //   / / F/B
  //    -  G
  //   / / E/C
  //    -. D/DP

#define a  1<<0
#define b  1<<6
#define c  1<<5
#define d  1<<4
#define e  1<<3
#define f  1<<1
#define g  1<<2
#define dp 1<<7

  byte segments;

  switch (number)
  {
    case 1: segments = b | c; break;
    case 2: segments = a | b | d | e | g; break;
    case 3: segments = a | b | c | d | g; break;
    case 4: segments = f | g | b | c; break;
    case 5: segments = a | f | g | c | d; break;
    case 6: segments = a | f | g | e | c | d; break;
    case 7: segments = a | b | c; break;
    case 8: segments = a | b | c | d | e | f | g; break;
    case 9: segments = a | b | c | d | f | g; break;
    case 0: segments = a | b | c | d | e | f; break;
    case ' ': segments = 0; break;
    case 'c': segments = g | e | d; break;
    case '-': segments = g; break;
  }

  if (decimal) segments |= dp;

  //Clock these bits out to the drivers
  for (byte x = 0 ; x < 8 ; x++)
  {
    digitalWrite(segmentClock, LOW);
    digitalWrite(segmentData, segments & 1 << (7 - x));
    digitalWrite(segmentClock, HIGH); //Data transfers to the register on the rising edge of SRCK
  }
}