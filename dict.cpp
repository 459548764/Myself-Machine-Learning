#include <iostream>
#include <string>
using namespace std;

int main()
{
	string temp;
	cin>>temp;
	char u;
	int place;
	
	string tail;
	tail = tail + temp[temp.length()-1];
	int mymin = temp[temp.length()-1] - '0';
	for(int i = temp.length()-2;i >= 0;i--)
	{
		if(temp[i] - '0' < temp[i+1] - '0')
		{
			u = temp[i];
			place = i;
			break;
		}
		else
		{
			if(temp[i] - '0' < mymin)
			{
				mymin = temp[i] - '0';
			}
			tail = tail + temp[i];
		}
	}
	
	for(int i = 0;i < tail.length();i++)
	{
		if(tail[i] - '0' == mymin)
		{
			temp[place] = tail[i];
			tail[i] = u;
			break;
		}
	}

	string result;
	for(int i = 0;i <= place;i++)
	{
		result = result + temp[i];
	}
	for(int i = 0;i < tail.length();i++)
	{
		result = result + tail[i];
	}
	cout<<result; 
	return 0;
} 
