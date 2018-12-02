#include <iostream>
using namespace std;

const double acc_var = 0.5;
const double gyro_var = 0.003;
const double angle_var = 0.001;
const double dt = 0.001;

double gyro_bias = 0;
double P[2][2] = {{1,0},{0,1}};
double K_angle = 0;
double K_gyro_bias = 0;
double angle = 0;

void Kalman_Filter(double acc_angle,double gyro)
{
	// Step 1
	angle = angle + (gyro - gyro_bias) * dt;
	// Step 2
	P[0][0] = angle_var + P[0][0]- P[1][0]*dt - P[0][1]*dt;
	P[0][1] = P[0][1] - P[1][1]*dt;
	P[1][0] = P[1][0] - P[1][1]*dt;
	P[1][1] = gyro_var + P[1][1];
	// Step 3
	K_angle = P[0][0]/(P[0][0] + acc_var);
	K_gyro_bias = P[1][0]/(P[0][0] + acc_var);
	// Step 4
	angle = angle + K_angle*(acc_angle - angle);
	gyro_bias = gyro_bias + K_gyro_bias*(acc_angle - angle);
	// Step 5
	P[0][0] = P[0][0] * (1 - K_angle);
	P[0][1] = P[0][1] * (1 - K_angle);
	P[1][0] = P[0][0] * (-K_gyro_bias) + P[1][0];
	P[1][1] = P[0][1] * (-K_gyro_bias) + P[1][1];
}

int main()
{
	
	return 0;	
} 

