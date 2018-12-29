#include <iostream>
using namespace std;

struct node
{
	int data;
	node *next;	
};
int n;

void insert(node *&head,int data)
{
	if(head == NULL)
	{
		head = new node();
		head->data = data;
		head->next = NULL;
	}
	else
	{
		insert(head->next,data);
	}
}

node* reverse(node *head)
{
	node *u = head;
	node *v = head->next;
	while(v->next != NULL)
	{
		node *w = v->next;
		v->next = u;
		u = v;
		v = w;
	}
	v->next = u;
	return v;
}

node* two_ptns(node *head)
{
	node *slow = head;
	node *fast = head;
	while(fast->next != NULL)
	{
		slow = slow->next;
		if(fast->next->next == NULL)
		{
			break;
		}
		else
		{
			fast = fast->next->next;
		}
	}
	return slow;
}

void PAT(node *head,node *tail,node *middle)
{
	while(head != middle && tail != middle)
	{
		cout<<head->data<<" ";
		cout<<tail->data<<" ";
		head = head->next;
		tail = tail->next;
	}
	if(n % 2 == 0)
	{
		cout<<head->data<<" ";
		cout<<middle->data;
	}
	else
	{
		cout<<middle->data;
	}
	
}

int main()
{
	cin>>n;
	node *head = NULL;
	for(int i = 1;i <= n;i++)
	{
		int temp;
		cin>>temp;
		insert(head,temp);
	}
	node *middle = two_ptns(head);
	node *tail = reverse(middle);
	PAT(head,tail,middle);
	return 0;	
} 
