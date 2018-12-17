#include <iostream>
using namespace std;

struct node
{
	int data;
	int color;
	node *left;
	node *right;
	node *parent;	
};

int n;
int data[100];

void build(node *&root,int data,node *parent = NULL)
{
	if(root == NULL)
	{
		root = new node();
		root->data = data;
		if(data > 0)
			root->color = 0;
		else
			root->color = 1;
		root->left = root->right = NULL;
		root->parent = parent;
	}
	else
	{
		if(data > root->data)
			build(root->right,data,root);
		else
			build(root->left,data,root);
	}
}

void route(node *root)
{
	while(root != NULL)
	{
		cout<<root->data<<"   ";
		root = root->parent;
	}
}

void preorder(node *root)
{
	if(root == NULL)
	{
		return;
	}
	if(root->left == NULL && root->right == NULL)
	{
		route(root);
		cout<<endl;
	}
	preorder(root->left);
	preorder(root->right);
}

int main()
{
	cin>>n;
	node *root = NULL;
	for(int i = 1;i <= n;i++)
	{
		cin>>data[i];
		build(root,data[i]);
	}
	preorder(root);
	return 0;
}
