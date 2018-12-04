#include <iostream>
using namespace std;

const double result_var = 0.01;
const double sensor_var = 1.16;

double P = 1;
double K_gain = 0;
double result = -68.04;

double Kalman_Filter(double data)
{
	K_gain = P/( P + sensor_var);
	result = result + K_gain*(data - result);
	P = P - K_gain * P + result_var;
	return result;
}

int main()
{
	int n;
	cin>>n;
	double arr[100];
	double filter[100];
	for(int i = 1;i <= n;i++)
	{
		cin>>arr[i];
		filter[i] = Kalman_Filter(arr[i]);
	}
	cout<<"------"<<endl;
	for(int i = 1;i <= n;i++)
	{
		cout<<filter[i]<<endl;
	}
	return 0;	
} 
