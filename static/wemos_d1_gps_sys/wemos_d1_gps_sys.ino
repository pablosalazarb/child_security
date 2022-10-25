/*
Programa de control de hardware para el dispositivo C1 de Child Security
Utilizando placa wemos d1 mini
TinyGPS as gps information module
Desarrollado por: Grupo numero x
*/

//Declaracion de librerias utiles para el control del dispositivo
#include <TinyGPS++.h> //Libreria para controlar el modulo gps
#include <SoftwareSerial.h> //Libreria para controlar entrada y salida serial
#include <ESP8266WiFi.h> //Libreria para el control del modulo wifi de la wemos d1

//Declaracion de objetos, variables y constantes en el programa
TinyGPSPlus gps;  //Objeto de la libreria TinyGPS++
SoftwareSerial ss(4, 5); //Pines conectados para comunicacion serial del gps
const char* ssid = "Familia_Salazar2022"; //Nombre de la red wifi (ssid)
const char* password = "SALAZARBARRIOS"; //Password de la red wifi a la que nos conectaremos
float latitude , longitude; //Variables para obtener la latitud y longitud del modulo gps
int year , month , date, hour , minute , second; //Variables para obtener fecha y hora.
String date_str , time_str , lat_str , lng_str; //Strings para concatenar la informacion almacenada
int pm;
WiFiServer server(80); //Creamos un puerto en la red para ejecutar un servicio

//Funcion de configuracion inicial del arduino
void setup() {
  Serial.begin(115200); //Inicializamos el monitor serie a 115200 baudios
  ss.begin(9600); //Comunicacion serial inicializada a 9600 baudios
  Serial.println(); //Imprimimos una linea en blanco
  Serial.print("Conectando a "); //Mostramos Conectado a 
  Serial.println(ssid);
  WiFi.begin(ssid, password); //Intento de conexion a la red wifi
  while (WiFi.status() != WL_CONNECTED)//Mientras el wifi no este conectado
  {
    delay(500);
    Serial.print("."); //Imprimimos puntos para saber que esta intentando conexion "...."
  }
  Serial.println(""); //Imprimimos un espacio en blanco hacia abajo
  Serial.println("WiFi conectado"); //Mostramos un mensaje de conexion exitosa
  server.begin();
  Serial.println("Servidor inicializado...");
  Serial.println(WiFi.localIP());  //Imprimimos la direccion IP

}

void loop() {
  while (ss.available() > 0) //Mientras la recepcion de datos este disponible
    if (gps.encode(ss.read())) //Leemos el dato del sensor gps
    {
      if (gps.location.isValid()) //Si la ubicacion del gps es valida, entonces
      {
        latitude = gps.location.lat();
        lat_str = String(latitude , 6); // latitude location is stored in a string
        longitude = gps.location.lng();
        lng_str = String(longitude , 6); //longitude location is stored in a string
      }
      if (gps.date.isValid()) //check whether gps date is valid
      {
        date_str = "";
        date = gps.date.day();
        month = gps.date.month();
        year = gps.date.year();
        if (date < 10)
          date_str = '0';
        date_str += String(date);// values of date,month and year are stored in a string
        date_str += " / ";

        if (month < 10)
          date_str += '0';
        date_str += String(month); // values of date,month and year are stored in a string
        date_str += " / ";
        if (year < 10)
          date_str += '0';
        date_str += String(year); // values of date,month and year are stored in a string
      }
      if (gps.time.isValid())  //check whether gps time is valid
      {
        time_str = "";
        hour = gps.time.hour();
        minute = gps.time.minute();
        second = gps.time.second();
        minute = (minute + 30); // converting to IST
        if (minute > 59)
        {
          minute = minute - 60;
          hour = hour + 1;
        }
        hour = (hour + 5) ;
        if (hour > 23)
          hour = hour - 24;   // converting to IST
        if (hour >= 12)  // checking whether AM or PM
          pm = 1;
        else
          pm = 0;
        hour = hour % 12;
        if (hour < 10)
          time_str = '0';
        time_str += String(hour); //values of hour,minute and time are stored in a string
        time_str += " : ";
        if (minute < 10)
          time_str += '0';
        time_str += String(minute); //values of hour,minute and time are stored in a string
        time_str += " : ";
        if (second < 10)
          time_str += '0';
        time_str += String(second); //values of hour,minute and time are stored in a string
        if (pm == 1)
          time_str += " PM ";
        else
          time_str += " AM ";
      }
    }
 
 WiFiClient client = server.available(); // Check if a client has connected
  if (!client)
  {
    return;
  }
  //Mostramos los datos obtenidos en una plantilla html
  String s = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n <!DOCTYPE html> <html> <head> <title>GPS DATA</title> <style>";
  s += "a:link {background-color: YELLOW;text-decoration: none;}";
  s += "table, th, td </style> </head> <body> <h1  style=";
  s += "font-size:300%;";
  s += " ALIGN=CENTER> GPS DATA</h1>";
  s += "<p ALIGN=CENTER style=""font-size:150%;""";
  s += "> <b>Location Details</b></p> <table ALIGN=CENTER style=";
  s += "width:50%";
  s += "> <tr> <th>Latitude</th>";
  s += "<td ALIGN=CENTER >";
  s += lat_str;
  s += "</td> </tr> <tr> <th>Longitude</th> <td ALIGN=CENTER >";
  s += lng_str;
  s += "</td> </tr> <tr>  <th>Date</th> <td ALIGN=CENTER >";
  s += date_str;
  s += "</td></tr> <tr> <th>Time</th> <td ALIGN=CENTER >";
  s += time_str;
  s += "</td>  </tr> </table> ";
 
  s += "</body> </html>";

  client.print(s); // all the values are send to the webpage
  delay(100);

}
