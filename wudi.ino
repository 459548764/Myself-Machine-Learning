//////////////////////////////////////////////////////////使用说明///////////////////////////////////////////////////////////////////////////////////////////
/*安装步骤：
      1.电路板上电，红色电源指示灯亮起，表示电路板供电正常；
      2.紧接着114号橙色指示灯亮起，表示程序开始初始化传感器模块，初始化完成后橙色指示灯熄灭（橙色指示灯持续亮大概12秒钟就会熄灭，如果超时，请检查连接，断电重启）；
      3.橙色指示灯熄灭后，116号蓝色指示灯亮起，表示程序在等待清零信号的输入（等待10秒钟），这时按动一下清零按键，则蓝色指示灯熄灭表示收到清零信号（如果蓝色指示灯亮起10秒后仍然未收到按键清零信号，则需断电重启再来）；
      4.蓝色指示灯熄灭后，需在一分钟内完成安装设备盖子，一分钟后蓝色指示灯重新亮起，程序自动开始清零操作；
      5.清零完成后，设备即开始向云服务器传输数据，118号绿色指示灯亮起，数据传输完成后绿色指示灯熄灭。
（按动清零按键后大概2.5分钟，远端服务器即可查看传输来的数据；断电重新上电大概1.5分钟后，远端服务器即可查看传输来的数据）
*/
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#include <SoftwareSerial.h>
#include <Wire.h>
#include <EEPROM.h>
#include <math.h>
#include <I2Cdev.h>
#include <MPU6050.h>

//////////////////////////////////////////////////////////参数设置///////////////////////////////////////////////////////////////////////////////////////////
//*************主函数相关参数****************//
long delayTime=8000;     //延迟时间为（delayTime/1000+46）秒      
double data[5];
double tempValue = 0;
double b = 3.28 + 0.87*343 - 21.5 ;         //温度补偿常量              //@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
unsigned long starttime0;
unsigned long looptime0;
unsigned long starttime1;
unsigned long looptime1;

//*************MPU6050模块相关参数****************//
int16_t ax, ay, az, gx, gy, gz;            //MPU6050原始数据 3个加速度+3个角加速度
double Total_Acc_ini=0;
double Acc;
MPU6050 Accelgyro;                          //实例化MPU6050模块

//*************GY25模块相关参数****************//
double Y_Angle,Y_Angle_Offset=0,Z_Angle,Z_Angle_Offset=0;
unsigned char Re_buf[8],counter=0;
SoftwareSerial Soft2_Serial(4, 3);        //实例化软串口，前者为RX,后者为TX，用于连接GY25模块

//*************上位机串口相关参数****************//
SoftwareSerial Soft1_Serial(A1, A0);      //实例化软串口，前者为RX,后者为TX，用于上位机串口监视

//*************EEPROM相关参数****************//
int n=0;
const int buttonPin = 5;
int buttonState = 0;
int eeAddress = 0;

//*************GPRS模块HTTP相关参数******************************************//
//这里使用默认硬串口Serial来传输GPRS信号
const int GPRS_Enable = 2;    //GPRS模块使能引脚，高电平使能，低电平失效
#define MAXCHAR 64                                         //接收缓冲的最大值，需要修改路径arduino-1.6.5\hardware\arduino\avr\cores\arduino 下的文件HardwareSerial.h中第48行的参数#define SERIAL_RX_BUFFER_SIZE
char GPRS_data[MAXCHAR];                                    //接收GPRS模块返回的数据
char URL[]="AT+HTTPPARA=\"URL\",\"http://www.zjcetc.cn/IOTWebLink/DeviceDataToWeb?code=72196E&angley=0000.00&anglez=0000.00&acc=0000.00&temp=0000.00&rip=0000.00&iccid=00000000000000000000\"\r\n";   //设置HTTP会话参数：URL，正常返回“OK”，可执行多次 //@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

//*************加速度模块卡尔曼滤波相关参数****************//
double k_P=1;
double k_X=0;
double k_K;
double k_R=0.058;
double k_Q=0.0005;
double k_Temp1=0 , k_Temp2=0;
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////



//////////////////////////////////////////////////////////子函数//////////////////////////////////////////////////////////////////////////////////////////////
double Rip_k_P=1;
double Rip_k_X=0;
double Rip_k_K;
double Rip_k_R=0.058;
double Rip_k_Q=0.0005;
double Rip_k_Temp1=0 , Rip_k_Temp2=0;
double Rip_Value = 0, Rip_Value_Offset=0;

//*************读取内部温度**********************************************//
double getTemp(void) {
  uint16_t wADC;
  double t;
  
  ADMUX = (_BV(REFS1) | _BV(REFS0) | _BV(MUX3)); // 设置内部参考电压 1.1 和选择多路复用  ADC8 (AVR内部温度传感器)
  ADCSRA |= _BV(ADEN);                           // 使能 ADC 功能
  delay(20);                                     // 等待 AREF 电压变得稳定。
  ADCSRA |= _BV(ADSC);                           // 开启 ADC 转换
  while (bit_is_set(ADCSRA,ADSC));               // 检测ADC转换结束
  wADC = ADCW;                                   // 读寄存器值
  t = 0.87*wADC-b;                               //变换单位为摄氏度
  return t;                                      // 返回摄氏度
}

//****************************************************GPRS相关*****************************************************************************//
//*************设置URL中SIM卡识别号ICCID函数****************************************//
void set_URL_ICCID(void){
  int num6=152;
  while(1){
    digitalWrite(GPRS_Enable, LOW);      //设置GPRS模块断电
    delay(3000);
    digitalWrite(GPRS_Enable, HIGH);     //设置GPRS模块供电
    delay(6000);

    read_GPRS_Serial(GPRS_data);
    clearBuff();
    Serial.print("AT+CCID\r\n");
    delay(1000);
    read_GPRS_Serial(GPRS_data);
    if( strstr(GPRS_data,"OK")!=NULL ) break;
    Soft1_Serial.println("Set the ICCID...");
  }
  URL[num6]    = GPRS_data[10];
  URL[num6+1]  = GPRS_data[11];
  URL[num6+2]  = GPRS_data[12];
  URL[num6+3]  = GPRS_data[13];
  URL[num6+4]  = GPRS_data[14];
  URL[num6+5]  = GPRS_data[15];
  URL[num6+6]  = GPRS_data[16];
  URL[num6+7]  = GPRS_data[17];
  URL[num6+8]  = GPRS_data[18];
  URL[num6+9]  = GPRS_data[19];
  URL[num6+10] = GPRS_data[20];
  URL[num6+11] = GPRS_data[21];
  URL[num6+12] = GPRS_data[22];
  URL[num6+13] = GPRS_data[23];
  URL[num6+14] = GPRS_data[24];
  URL[num6+15] = GPRS_data[25];
  URL[num6+16] = GPRS_data[26];
  URL[num6+17] = GPRS_data[27];
  URL[num6+18] = GPRS_data[28];
  URL[num6+19] = GPRS_data[29];
  digitalWrite(GPRS_Enable, LOW);      //设置GPRS模块断电
}

//*************设置URL的数据函数****************************************//
void set_URL(double Data[5]){    //Data[0]为Y_Angle，Data[1]为Z_Angle，Data[2]为Acc，Data[3]为Temp，Data[4]为Rip_Value
  int num1=86,num2=101,num3=113,num4=126,num5=138;
  
  //设置Y_Angle
  char a[8]="0000000";
  char b[8]="0000000";
  dtostrf(Data[0],4,2,a);
  if(a[0]=='-'){
    b[0]='-';
    if(a[2]=='.')     { b[1]='0'; b[2]='0'; b[3]=a[1];b[4]='.';b[5]=a[3];b[6]=a[4];}
    else if(a[3]=='.'){ b[1]='0'; b[2]=a[1];b[3]=a[2];b[4]='.';b[5]=a[4];b[6]=a[5];}
    else if(a[4]=='.'){ b[1]=a[1];b[2]=a[2];b[3]=a[3];b[4]='.';b[5]=a[5];b[6]=a[6];}
  }else{
    if(a[1]=='.')     { b[0]='0';  b[1]='0'; b[2]='0'; b[3]=a[0];b[4]='.';b[5]=a[2];b[6]=a[3];}
    else if(a[2]=='.'){ b[0]='0';  b[1]='0'; b[2]=a[0];b[3]=a[1];b[4]='.';b[5]=a[3];b[6]=a[4];}
    else if(a[3]=='.'){ b[0]='0';  b[1]=a[0];b[2]=a[1];b[3]=a[2];b[4]='.';b[5]=a[4];b[6]=a[5];}
    else if(a[4]=='.'){ b[0]=a[0]; b[1]=a[1];b[2]=a[2];b[3]=a[3];b[4]='.';b[5]=a[5];b[6]=a[6];} 
  }
  URL[num1] = b[0];
  URL[num1+1] = b[1];
  URL[num1+2] = b[2];
  URL[num1+3] = b[3];
  URL[num1+4] = b[4];
  URL[num1+5] = b[5];
  URL[num1+6] = b[6];
  
  //设置Z_Angle
  for(int i=0;i<8;i++){
    a[i]='0';
    b[i]='0';
  }
  dtostrf(Data[1],4,2,a);
  if(a[0]=='-'){
    b[0]='-';
    if(a[2]=='.')     { b[1]='0'; b[2]='0'; b[3]=a[1];b[4]='.';b[5]=a[3];b[6]=a[4];}
    else if(a[3]=='.'){ b[1]='0'; b[2]=a[1];b[3]=a[2];b[4]='.';b[5]=a[4];b[6]=a[5];}
    else if(a[4]=='.'){ b[1]=a[1];b[2]=a[2];b[3]=a[3];b[4]='.';b[5]=a[5];b[6]=a[6];}
  }else{
    if(a[1]=='.')     { b[0]='0';  b[1]='0'; b[2]='0'; b[3]=a[0];b[4]='.';b[5]=a[2];b[6]=a[3];}
    else if(a[2]=='.'){ b[0]='0';  b[1]='0'; b[2]=a[0];b[3]=a[1];b[4]='.';b[5]=a[3];b[6]=a[4];}
    else if(a[3]=='.'){ b[0]='0';  b[1]=a[0];b[2]=a[1];b[3]=a[2];b[4]='.';b[5]=a[4];b[6]=a[5];}
    else if(a[4]=='.'){ b[0]=a[0]; b[1]=a[1];b[2]=a[2];b[3]=a[3];b[4]='.';b[5]=a[5];b[6]=a[6];} 
  }
  URL[num2] = b[0];
  URL[num2+1] = b[1];
  URL[num2+2] = b[2];
  URL[num2+3] = b[3];
  URL[num2+4] = b[4];
  URL[num2+5] = b[5];
  URL[num2+6] = b[6];

  //设置Acc
  for(int i=0;i<8;i++){
    a[i]='0';
    b[i]='0';
  }
  dtostrf(Data[2],4,2,a);
  if(a[0]=='-'){
    b[0]='-';
    if(a[2]=='.')     { b[1]='0'; b[2]='0'; b[3]=a[1];b[4]='.';b[5]=a[3];b[6]=a[4];}
    else if(a[3]=='.'){ b[1]='0'; b[2]=a[1];b[3]=a[2];b[4]='.';b[5]=a[4];b[6]=a[5];}
    else if(a[4]=='.'){ b[1]=a[1];b[2]=a[2];b[3]=a[3];b[4]='.';b[5]=a[5];b[6]=a[6];}
  }else{
    if(a[1]=='.')     { b[0]='0';  b[1]='0'; b[2]='0'; b[3]=a[0];b[4]='.';b[5]=a[2];b[6]=a[3];}
    else if(a[2]=='.'){ b[0]='0';  b[1]='0'; b[2]=a[0];b[3]=a[1];b[4]='.';b[5]=a[3];b[6]=a[4];}
    else if(a[3]=='.'){ b[0]='0';  b[1]=a[0];b[2]=a[1];b[3]=a[2];b[4]='.';b[5]=a[4];b[6]=a[5];}
    else if(a[4]=='.'){ b[0]=a[0]; b[1]=a[1];b[2]=a[2];b[3]=a[3];b[4]='.';b[5]=a[5];b[6]=a[6];} 
  }
  URL[num3] = b[0];
  URL[num3+1] = b[1];
  URL[num3+2] = b[2];
  URL[num3+3] = b[3];
  URL[num3+4] = b[4];
  URL[num3+5] = b[5];
  URL[num3+6] = b[6];
  
  //设置Temp
   for(int i=0;i<8;i++){
    a[i]='0';
    b[i]='0';
   }
  dtostrf(Data[3],2,2,a);
  if(a[0]=='-'){
    b[0]='-';
    if(a[2]=='.')     { b[1]='0'; b[2]='0'; b[3]=a[1];b[4]='.';b[5]=a[3];b[6]=a[4];}
    else if(a[3]=='.'){ b[1]='0'; b[2]=a[1];b[3]=a[2];b[4]='.';b[5]=a[4];b[6]=a[5];}
    else if(a[4]=='.'){ b[1]=a[1];b[2]=a[2];b[3]=a[3];b[4]='.';b[5]=a[5];b[6]=a[6];}
  }else{
    if(a[1]=='.')     { b[0]='0';  b[1]='0'; b[2]='0'; b[3]=a[0];b[4]='.';b[5]=a[2];b[6]=a[3];}
    else if(a[2]=='.'){ b[0]='0';  b[1]='0'; b[2]=a[0];b[3]=a[1];b[4]='.';b[5]=a[3];b[6]=a[4];}
    else if(a[3]=='.'){ b[0]='0';  b[1]=a[0];b[2]=a[1];b[3]=a[2];b[4]='.';b[5]=a[4];b[6]=a[5];}
    else if(a[4]=='.'){ b[0]=a[0]; b[1]=a[1];b[2]=a[2];b[3]=a[3];b[4]='.';b[5]=a[5];b[6]=a[6];} 
  }
  URL[num4] = b[0];
  URL[num4+1] = b[1];
  URL[num4+2] = b[2];
  URL[num4+3] = b[3];
  URL[num4+4] = b[4];
  URL[num4+5] = b[5];
  URL[num4+6] = b[6];
  for(int i=0;i<8;i++){
    a[i]='0';
    b[i]='0';
  }
  dtostrf(Data[4],4,2,a);
  if(a[0]=='-'){
    b[0]='-';
    if(a[2]=='.')     { b[1]='0'; b[2]='0'; b[3]=a[1];b[4]='.';b[5]=a[3];b[6]=a[4];}
    else if(a[3]=='.'){ b[1]='0'; b[2]=a[1];b[3]=a[2];b[4]='.';b[5]=a[4];b[6]=a[5];}
    else if(a[4]=='.'){ b[1]=a[1];b[2]=a[2];b[3]=a[3];b[4]='.';b[5]=a[5];b[6]=a[6];}
  }else{
    if(a[1]=='.')     { b[0]='0';  b[1]='0'; b[2]='0'; b[3]=a[0];b[4]='.';b[5]=a[2];b[6]=a[3];}
    else if(a[2]=='.'){ b[0]='0';  b[1]='0'; b[2]=a[0];b[3]=a[1];b[4]='.';b[5]=a[3];b[6]=a[4];}
    else if(a[3]=='.'){ b[0]='0';  b[1]=a[0];b[2]=a[1];b[3]=a[2];b[4]='.';b[5]=a[4];b[6]=a[5];}
    else if(a[4]=='.'){ b[0]=a[0]; b[1]=a[1];b[2]=a[2];b[3]=a[3];b[4]='.';b[5]=a[5];b[6]=a[6];} 
  }
  URL[num5] = b[0];
  URL[num5+1] = b[1];
  URL[num5+2] = b[2];
  URL[num5+3] = b[3];
  URL[num5+4] = b[4];
  URL[num5+5] = b[5];
  URL[num5+6] = b[6];
  
  Soft1_Serial.print(URL);
}

//*************读取软串口数据********************************************//
int read_GPRS_Serial(char result[])
{
  int i = 0;
  while (Serial.available() > 0)
  {
    char inChar = Serial.read();
    result[i] = inChar;
    i++; 
  }
  Serial.flush();
}

//*************清空从GPRS接收的数据**************************************//
void clearBuff(void)
{
  int i=0;
  for(i=0;i<MAXCHAR;i++) GPRS_data[i]=0x00;
}

/**********发送AT指令函数********************************************************************
*输入参数: b[]--- 待发送字符数组数据
*          a--- 希望接收到的应答数据指针
*          times---如果应答数据有误，循环发送AT命令的次数
*          wait_time ----发送等待时间，一般为100ms
*返    回: 正确---1  错误---0
*******************************************************************************/
int gprs_send_cmd(char b[],char *a,int times,int wait_time)         
{
  int i=0;
  clearBuff();
  while(i < times)                    
  {
    Serial.println(b);
    delay(wait_time);
    read_GPRS_Serial(GPRS_data);
    if(strstr(GPRS_data,a)!=NULL)
    {
       return 1;
    }
    i++;
  }
  return 0;
}

/***********字符串分割函数*******************************************************************
*输入参数: num--- 0:取出分割字符串（delim）前面的字符串；1;取出分割字符串（delim）后面的字符串
*          temp--- 要分割的字符串
*          delim---分割字符串    
*******************************************************************************/
char *str_delim(int num,char *temp,char *delim)
{
  int i;
  char *str[2]={0};
  char *tok=temp;
  char *restr;
  for(i=0;i<2;i++)
  {
    tok=strtok(tok,delim);
    str[i]=tok;
    tok = NULL;
  }
  restr=str[num];
  return restr;
}

/*******GPRS模块基本状态测试***********************************************************************
*返    回: 正确---1  错误---0
*说    明: GPRS上电后，先判断AT命令是否正常、能否读到卡、能否注册网络。确认无误后再进行其他操作
*******************************************************************************/
int check_status(void)
{
  digitalWrite(GPRS_Enable, LOW);      //设置GPRS模块断电
  delay(3000);
  digitalWrite(GPRS_Enable, HIGH);     //设置GPRS模块供电
  delay(10000);
  Soft1_Serial.println("Connect...");
  
  //关闭移动场景
  if(gprs_send_cmd("AT+CIPSHUT\r\n","SHUT OK",1,100))
  {
     Soft1_Serial.println("1.success");
  }
  else
  {
     Soft1_Serial.println("1.fall");
     return 0;
  }

  //同步波特率
  if(gprs_send_cmd("AT","OK",2,100)) 
  {
     Soft1_Serial.println("2.success");
  }
  else
  {
     Soft1_Serial.println("2.fall");
     return 0;
  }
  
  //查询GPRS模块能否读到SIM卡          
  if(gprs_send_cmd("AT+CPIN?","+CPIN: READY",2,100))
  {
     Soft1_Serial.println("3.success");
  }
  else
  {
     Soft1_Serial.println("3.fall");
     return 0;
  }
  
  //查询GPRS模块是否注册成功          
  if(gprs_send_cmd("AT+CREG?","+CREG:",5,100))
  {
     Soft1_Serial.println("4.success");
  }
  else
  {
     Soft1_Serial.println("4.fall");
     return 0;
  }
  
  //取消回显        
  if(gprs_send_cmd("ATE0","OK",1,100))
  {
     Soft1_Serial.println("5.success");
  }
  else
  {
     Soft1_Serial.println("5.fall");
     return 0;
  }
  return 1;
}

//********GPRS模块HTTP上传数据函数****************************************************************
int http_post(void)
{
  u8 i;
  read_GPRS_Serial(GPRS_data);
  clearBuff();
  
  delay(5000);
  //设置HTTP功能的承载类型
  if(gprs_send_cmd("AT+SAPBR=3,1,\"CONTYPE\",\"GPRS\"","OK",1,100))
  {
     Soft1_Serial.println("6.success");
  }
  else
  {
     Soft1_Serial.println("6.fall");
    return 0;
  }
  
  // 设置APN
  if(gprs_send_cmd("AT+SAPBR=3,1,\"APN\",\"CMNET\"","OK",1,100))
  {
     Soft1_Serial.println("7.success");
  }
  else
  {
     Soft1_Serial.println("7.fall");
    return 0;
  }

  //激活上下文
  if(gprs_send_cmd("AT+SAPBR=1,1","OK",1,5000))
  {
     Soft1_Serial.println("8.success");
  }
  else
  {
     Soft1_Serial.println("8.fall");
    return 0;
  }
    
  //查询承载状态
  if(gprs_send_cmd("AT+SAPBR=2,1","OK",1,1000))
  {
    Soft1_Serial.println("9.success");
  }
  else
  {
     Soft1_Serial.println("9.fall");
    return 0;
  }
  
  // 初始化HTTP协议栈
  if(gprs_send_cmd("AT+HTTPINIT","OK",1,100))
  {
     Soft1_Serial.println("10.success");
  }
  else
  {
     Soft1_Serial.println("10.fall");
    return 0;
  }
  
  // 设置HTTP会话参数：CID
  if(gprs_send_cmd("AT+HTTPPARA=\"CID\",1 ","OK",1,100))
  {
     Soft1_Serial.println("11.success");
  }
  else
  {
     Soft1_Serial.println("11.fall");
    return 0;
  }
    
  // 设置HTTP会话参数：URL
  if(gprs_send_cmd(URL,"OK",1,200)) 
  {
    Soft1_Serial.println("12.success");
  }
  else
  {
    Soft1_Serial.println("12.fall");
    return 0;
  }
  
//  // 开始写入数据
//  if(gprs_send_cmd("AT+HTTPDATA=2,100000","DOWNLOAD",1,100))
//  {
//     Soft1_Serial.println("13.开始写入数据：hello\r\n");
//     gprs_send_string("hello");
//     delay_ms(50);
//  }
//  else
//  {
//     Soft1_Serial.println("写入数据失败\r\n");
//    return 0;
//  }
  
//  //开始上传
//  read_GPRS_Serial(GPRS_data);
//  clearBuff();
//  Serial.print("AT+HTTPACTION=1\r\n");
//  for(i=0;i<5;i++)                                //60s循环判断，当数据上传成功后立马跳出循环
//  {
//    delay(1000);
//    read_GPRS_Serial(GPRS_data);
//    if( strstr(GPRS_data,"+HTTPACTION:")!=NULL )
//    {
//      Soft1_Serial.println("14.success");
//      read_GPRS_Serial(GPRS_data);
//      clearBuff();
//      break;
//    } 
//  }
//  if(i>=5)  { Soft1_Serial.println("14.fall"); return 0;}

  //开始获取返回数据
  read_GPRS_Serial(GPRS_data);
  clearBuff();
  Serial.print("AT+HTTPACTION=0\r\n");
  for(i=0;i<60;i++)                                //60s循环判断，当数据上传成功后立马跳出循环
  {
    delay(1000);
    read_GPRS_Serial(GPRS_data);
    if( strstr(GPRS_data,"+HTTPACTION: 0,200")!=NULL )
    {
      Soft1_Serial.println("15.success");
      read_GPRS_Serial(GPRS_data);
      clearBuff();
      break;
    } 
  }
  if(i>=60)  { Soft1_Serial.println("15.fall"); return 0;}
  
  //读出返回数据，并以此设置传输速率
  read_GPRS_Serial(GPRS_data);
  clearBuff();
  Serial.print("AT+HTTPREAD\r\n");
  for(i=0;i<60;i++)                                //60s循环判断，当数据上传成功后立马跳出循环
  {
    delay(1000);
    read_GPRS_Serial(GPRS_data);
    if( strstr(GPRS_data,"+HTTPREAD:")!=NULL )
    {
      Soft1_Serial.println("16.success");
      Soft1_Serial.println(GPRS_data);
      
      String a="";
      long   b=0;
      a=strstr(GPRS_data,"sendfreq");
      if(a!=NULL){
        for(int i=0;i<6;i++) b=b*10+a[i+11]-'0';
      }
      if( b!=0 ) delayTime= fabs( (b*60-46)*1000 );          //乘以60变为秒，然后减去GPRS发送数据的46秒,再变为毫秒

      //远程清空操作
      if(strstr(GPRS_data,"reset")!=NULL){
        Soft1_Serial.println("soft_clear");
        Save_EEPROM();
        Recover_EEPROM();
      }
      
      break;
    } 
  }
  if(i>=60)  { Soft1_Serial.println("16.fall"); return 0;}

  // 关闭HTTP服务
  if(gprs_send_cmd("AT+HTTPTERM","OK",1,100))
  {
     Soft1_Serial.println("17.success");
  }
  else
  {
    Soft1_Serial.println("17.fall");
    return 0;
  }

  digitalWrite(GPRS_Enable, LOW);      //设置GPRS模块断电
  
  return 1;
}
//****************************************************************************************************************************************//

//*************读取MPU6050模块原始加速度与和加速度的平方数据函数**************************************************//
int16_t Read_MPU6050_Acc_ini(void){
  int num = 20;
  double X_Acc_ini=0, X_Acc_ini_[num];
  double Y_Acc_ini=0, Y_Acc_ini_[num];
  double Z_Acc_ini=0, Z_Acc_ini_[num];

  for(int i=0;i<num;i++){
    Accelgyro.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);
    X_Acc_ini_[i] = ax;
    Y_Acc_ini_[i] = ay;
    Z_Acc_ini_[i] = az;
    delay(500);
  }

  for(int m = 0; m < (num-1); m++){
    for (int n = m+1; n < num; n++) {
      double temp ;  
      if(X_Acc_ini_[m]>X_Acc_ini_[n]){
        temp =  X_Acc_ini_[m];
        X_Acc_ini_[m] = X_Acc_ini_[n];
        X_Acc_ini_[n] = temp;
      }
    }
  }

  for(int m = 0; m < (num-1); m++){
    for (int n = m+1; n < num; n++) {
      double temp ;  
      if(Y_Acc_ini_[m]>Y_Acc_ini_[n]){
        temp =  Y_Acc_ini_[m];
        Y_Acc_ini_[m] = Y_Acc_ini_[n];
        Y_Acc_ini_[n] = temp;
      }
    }
  }

  for(int m = 0; m < (num-1); m++){
    for (int n = m+1; n < num; n++) {
      double temp ;  
      if(Z_Acc_ini_[m]>Z_Acc_ini_[n]){
        temp =  Z_Acc_ini_[m];
        Z_Acc_ini_[m] = Z_Acc_ini_[n];
        Z_Acc_ini_[n] = temp;
      }
    }
  }

  X_Acc_ini = 0;
  Y_Acc_ini = 0;
  Z_Acc_ini = 0;
  for(int m=3;m<(num-3);m++){
    X_Acc_ini += X_Acc_ini_[m];
    Y_Acc_ini += Y_Acc_ini_[m];
    Z_Acc_ini += Z_Acc_ini_[m];
  }
  X_Acc_ini = X_Acc_ini/(num-6);
  Y_Acc_ini = Y_Acc_ini/(num-6);
  Z_Acc_ini = Z_Acc_ini/(num-6);
  Total_Acc_ini = (X_Acc_ini/100.0)*(X_Acc_ini/100.0)+(Y_Acc_ini/100.0)*(Y_Acc_ini/100.0)+(Z_Acc_ini/100.0)*(Z_Acc_ini/100.0);
}

//*************读取MPU6050模块处理后真实加速度数据函数********************************************//
double Read_MPU6050_Acc_real(void){
  int num = 3;
  double X_Acc = 0, X_Acc_[num];
  double Y_Acc = 0, Y_Acc_[num];
  double Z_Acc = 0, Z_Acc_[num];
  for(int i=0;i<3;i++){
    Accelgyro.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);
    X_Acc_[i] = ax;
    Y_Acc_[i] = ay;
    Z_Acc_[i] = az;
    delay(7);
  }

  for(int m = 0; m < (num-1); m++){
    for (int n = m+1; n < num; n++) {
      double temp ;  
      if(X_Acc_[m]>X_Acc_[n]){
        temp =  X_Acc_[m];
        X_Acc_[m] = X_Acc_[n];
        X_Acc_[n] = temp;
      }
    }
  }

  for(int m = 0; m < (num-1); m++){
    for (int n = m+1; n < num; n++) {
      double temp ;  
      if(Y_Acc_[m]>Y_Acc_[n]){
        temp =  Y_Acc_[m];
        Y_Acc_[m] = Y_Acc_[n];
        Y_Acc_[n] = temp;
      }
    }
  }

  for(int m = 0; m < (num-1); m++){
    for (int n = m+1; n < num; n++) {
      double temp ;  
      if(Z_Acc_[m]>Z_Acc_[n]){
        temp =  Z_Acc_[m];
        Z_Acc_[m] = Z_Acc_[n];
        Z_Acc_[n] = temp;
      }
    }
  }

  X_Acc = 0;
  Y_Acc = 0;
  Z_Acc = 0;
  for(int m=1;m<(num-1);m++){
    X_Acc += X_Acc_[m];
    Y_Acc += Y_Acc_[m];
    Z_Acc += Z_Acc_[m];
  }
  X_Acc = X_Acc/(num-2);
  Y_Acc = Y_Acc/(num-2);
  Z_Acc = Z_Acc/(num-2);
  
  Acc = 980.0/16384.0*sqrt( abs( (X_Acc/100.0)*(X_Acc/100.0)+(Y_Acc/100.0)*(Y_Acc/100.0)+(Z_Acc/100.0)*(Z_Acc/100.0)-Total_Acc_ini ) );
//   //根据温度变化对采集的值进行补偿，tempValue为26摄氏度时，不进行补偿
//  if( tempValue < 26 ) Acc = Acc - ( -0.053571*tempValue+1.392857 );
//  else  Acc = Acc - ( 0.016667*tempValue-0.433333 );
}

//*************读取GY25模块倾角数据函数**************************************************//
double Read_GY25_Angle(void){
  int num = 11;
  double Value_Y = 0,Y_Angle_[num];
  double Value_Z = 0,Z_Angle_[num];
  
  for(int j=0;j<num;j++){
    Soft2_Serial.write(0XA5); 
    Soft2_Serial.write(0X51);   //发送数据请求指令
    delay(500);
    while (Soft2_Serial.available()) {   
      Re_buf[counter]=(unsigned char)Soft2_Serial.read();        
      if(counter==0&&Re_buf[0]!=0xAA){  // 检查帧头 
        counter=0;
        Soft2_Serial.flush();
        break;
      }      
      counter++;     
      if(counter==8) counter=0;               //接收到数据   
    }
  
    if(Re_buf[0]==0xAA && Re_buf[7]==0x55)        //检查帧头，帧尾
    {           
      Value_Y=(Re_buf[3]<<8|Re_buf[4]);
      Value_Y/=100.0; 
      Value_Z=(Re_buf[5]<<8|Re_buf[6]);
      Value_Z/=100.0;             
    }
    Y_Angle_[j] =  Value_Y;
    Z_Angle_[j] =  Value_Z;
  }
  
  for(int m = 0; m < (num-1); m++){
    for (int n = m+1; n < num; n++) {
      double temp ;  
      if(Y_Angle_[m]>Y_Angle_[n]){
        temp =  Y_Angle_[m];
        Y_Angle_[m] = Y_Angle_[n];
        Y_Angle_[n] = temp;
      }
    }
  }
  
  for(int m = 0; m < (num-1); m++){
    for (int n = m+1; n < num; n++) {
      double temp ;  
      if(Z_Angle_[m]>Z_Angle_[n]){
        temp =  Z_Angle_[m];
        Z_Angle_[m] = Z_Angle_[n];
        Z_Angle_[n] = temp;
      }
    }
  }
  
  Y_Angle = 0;
  Z_Angle = 0; 
  for(int m=3;m<(num-3);m++){
    Y_Angle+=Y_Angle_[m];
    Z_Angle+=Z_Angle_[m];
  }
  Y_Angle /= (num-6);
  Z_Angle /= (num-6);   
  
}

//*************保存倾角数据到EEPROM函数**************************************************//
void Save_EEPROM(void){
  Soft1_Serial.end();
  Soft2_Serial.listen();
  delay(500);
  tempValue = getTemp();
  
  Read_GY25_Angle();       //去除初始传输数据的不稳定干扰
  delay(500);
  Read_GY25_Angle();       //去除初始传输数据的不稳定干扰
  delay(500);
  Read_GY25_Angle();       //去除初始传输数据的不稳定干扰
  delay(500);
  Read_GY25_Angle();
  delay(500);
  Soft2_Serial.end();
  Soft1_Serial.listen();
  delay(500);
  
  eeAddress = 0;
  EEPROM.put( eeAddress, Y_Angle );
  eeAddress += sizeof(double); 
  EEPROM.put( eeAddress, Z_Angle );
  eeAddress += sizeof(double); 
  EEPROM.put( eeAddress, Rip_Value );
}

//*************从EEPROM恢复倾角数据函数**************************************************//
void Recover_EEPROM(void){
  eeAddress = 0;
  EEPROM.get( eeAddress, Y_Angle_Offset );
  eeAddress += sizeof(double); 
  EEPROM.get( eeAddress, Z_Angle_Offset );
  eeAddress += sizeof(double); 
  EEPROM.get( eeAddress, Rip_Value_Offset );
}

//*************加速度模块卡尔曼滤波函数**************************************************//
double kalman(double  k_DATA){
  k_K = k_P / ( k_P + k_R );
  k_X = k_X + k_K * ( k_DATA - k_X );
  k_P = k_P - k_K * k_P + k_Q;
  return k_X;
}
double Rip_kalman(){
  int num = 7;
  double Rip,Rip_[num];
  //求平均
  for(int j=0;j<num;j++){
    Rip_[j] = analogRead(A2);
    delay(2);
  }
  for(int m = 0; m < (num-1); m++){
    for (int n = m+1; n < num; n++) {
      double temp ;  
      if(Rip_[m]>Rip_[n]){
        temp =  Rip_[m];
        Rip_[m] = Rip_[n];
        Rip_[n] = temp;
      }
    }
  }
  Rip = 0; 
  for(int m=2;m<(num-2);m++){
    Rip+=Rip_[m];
  }
  Rip /= (num-4); 
  //卡尔曼滤波处理
  Rip_k_K = Rip_k_P / ( Rip_k_P + Rip_k_R );
  Rip_k_X = Rip_k_X + Rip_k_K * ( Rip - Rip_k_X );
  Rip_k_P = Rip_k_P - Rip_k_K * Rip_k_P + Rip_k_Q;
  return Rip_k_X;
}
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

//////////////////////////////////////////////////////////setup函数///////////////////////////////////////////////////////////////////////////////////////////
//*************setup函数**************************************************//
void setup() {
  //*************按键输入引脚************
  pinMode(5, INPUT);
  
  //*************程序运行指示灯************
  pinMode(6, OUTPUT);   //橙灯用来指示系统初始化
  pinMode(7, OUTPUT);   //蓝灯用来指示清零操作
  pinMode(8, OUTPUT);   //绿灯用来指示发送数据

  digitalWrite(6, HIGH);
  digitalWrite(7, LOW);
  digitalWrite(8, LOW);

  //*************MPU6050模块初始化************
  Wire.begin();
  Accelgyro.initialize();

  //*************GY25模块初始化************
  Soft2_Serial.begin(9600);

  //*************上位机串口通道初始化************
  Soft1_Serial.begin(9600);
  Soft1_Serial.listen();
  
  //*************GPRS模块HTTP初始化程序*********
  Serial.begin(9600);
  pinMode(GPRS_Enable,OUTPUT);  
  digitalWrite(GPRS_Enable, LOW);
  set_URL_ICCID();                                                                //@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
  for(int m=0;m<100;m++) Rip_Value = Rip_kalman();
  
  digitalWrite(6, LOW);
  
  //*************检测按键信息保存倾角偏移量程序（不保存加速度）*********
  digitalWrite(7, HIGH);
  starttime0 = millis();
  while((millis()-starttime0)<10000){      //按动按键的时间十秒钟
    buttonState = digitalRead(buttonPin);
    if (buttonState == HIGH){
      digitalWrite(7, LOW);
      delay(60000);                       //安装外壳盖子时间一分钟                   //@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
      digitalWrite(7, HIGH);
      Save_EEPROM();
      break;
    }
  }
  Recover_EEPROM();
  
  Read_MPU6050_Acc_ini();  //去除初始传输数据的不稳定干扰****非常重要
}

//////////////////////////////////////////////////////////loop函数///////////////////////////////////////////////////////////////////////////////////////////
void loop() {
  starttime0 = millis();
  Soft1_Serial.println( "start" ); 
  long v=0;
  while(1){
    starttime1 = millis();
    
    Read_MPU6050_Acc_real();
    data[2] = Acc;
    Soft1_Serial.print(data[2]);
    Soft1_Serial.print("     ");
    
    data[2] = fabs(kalman(data[2]) - 0.57);     //卡尔曼滤波
    k_Temp1 = k_Temp2;
    k_Temp2 = data[2];
    Soft1_Serial.print(data[2]);
    Soft1_Serial.print("     "); 
    Rip_Value = Rip_kalman();     
    data[4] = (Rip_Value - Rip_Value_Offset)/10;
    Soft1_Serial.print(data[4]);
    Soft1_Serial.print("     ");

    if( (k_Temp1>1.2) && (k_Temp2>1.2) )  break;        //异常跳出判断

    v++;
    if(v >= 35125){             //加速度清零时间间隔：(分钟数*60-10)/0.08，这里设置为47分钟(值为35125)，（其中10代表这里初始化操作浪费的时间）
      v = 0;
      Read_MPU6050_Acc_ini(); 
    }
    delay(8);
    
    looptime0 = millis() - starttime0;
    if( looptime0 >= delayTime){  
      Soft1_Serial.println( looptime0 );  
      break;
    }
    
    looptime1 = millis() - starttime1;
    Soft1_Serial.println( looptime1 );  
  }

  starttime0 = millis();
  tempValue = getTemp();
  Soft1_Serial.end();
  Soft2_Serial.listen();
  delay(500);
  Read_GY25_Angle();
  Soft2_Serial.end();
  Soft1_Serial.listen();
  
  data[0] = Y_Angle - Y_Angle_Offset;
  data[1] = Z_Angle - Z_Angle_Offset;
  data[3] = tempValue;
  
  set_URL(data);

  while(1){
    digitalWrite(8, HIGH);
    if(check_status())                                   
    {
      if(http_post()) {Soft1_Serial.println("*** Send Success ***"); digitalWrite(8, LOW); break;}
      else Soft1_Serial.println("*** Send Fall ***");
    }else Soft1_Serial.println("*** Init Fall ***");
  }
  
  Read_MPU6050_Acc_ini();  //去除数据的不稳定干扰****非常重要
  k_Temp1 = k_Temp2 = 0;
  k_P=1;
  k_X=0;
  Soft1_Serial.println( delayTime/1000 + 46 );
  delay(71);
  looptime0 = millis() - starttime0;
  Soft1_Serial.println( looptime0 );        //成功发送的时间为46秒
}
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////









