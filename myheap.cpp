#include <iostream>
#include <algorithm>
using namespace std;

int array[] = {0,2,6,8,11,4,3,9,-100};
// The initial of array must be 0
// Here from 1 to n makes it easily
int n = 8;

int main()
{
	// Ends at 2 because of i/2
	for(int i = n;i >= 2;i--)
	{
		if(array[i] > array[i/2])
		{
			// Upward
			int temp = i;
			swap(array[i],array[i/2]);
			// Downward
			// Here suppose the heap is 
			/*
			        temp
			       /    \
				  /      \
			  2*temp   2*temp+1
			*/
			// Boundary condition
			while(2*temp <= n)
			{ 
				// 2*temp+1 is not exist!!
				if(2*temp+1 > n)
				{
					if(array[2*temp] > array[temp])
					{
						swap(array[2*temp],array[temp]);
					}
					break;
				}
				else
				{
					// 2*temp+1 is the biggest
					if(array[2*temp+1] > array[2*temp] && array[2*temp+1] > array[temp])
					{
						swap(array[2*temp+1],array[temp]);
						temp = 2*temp+1;
					}
					// 2*temp is the biggest
					else if(array[2*temp] > array[2*temp+1] && array[2*temp] > array[temp])
					{
						swap(array[2*temp],array[temp]);
						temp = 2*temp;
					}
					else
					{
						break;	
					} 
				}
			}
		}
	}
	
	for(int i = 1;i <= n;i++)
	{
		cout<<array[i]<<" ";
	}	
	return 0;
} 
