#include <iostream>
#include <cmath>
#include <queue>
using namespace std;

struct node
{
	/*
	When data is negative -- color:red
	When data is positive -- color:black
	*/
	int data;
	node *left;
	node *right;
	node *parent;	
};
int n;

node* insert(node *&root,int data,node *p = NULL)
{
	if(root == NULL)
	{
		root = new node();
		root->data = data;
		root->left = NULL;
		root->right = NULL;
		root->parent = p;
		return root;
	}
	else
	{
		if(abs(data) > abs(root->data))
		{
			insert(root->right,data,root);
		}
		else
		{
			insert(root->left,data,root);
		}
	}
}

void redblack(node *&tail,node *&root)
{
	while(tail->parent != NULL && tail->parent->parent != NULL)
	{
		int flag = 0;
		node *z = tail;
		node *y = tail->parent;
		node *x = tail->parent->parent;
		if(z->data < 0 && y->data < 0)
		{
			// Decide the left or right
			if(abs(z->data) > abs(y->data))
			{
				// On the right side
				if(abs(y->data) > abs(x->data))
				{
					// [RIGHT---RIGHT]
					// On the right side
					node *B = y->left;
					if(x == root)
					{
						// Here is on the root 
						root = y;
						y->parent = NULL;
						y->left = x;
						y->left->right = B;
						x->parent = y;
						// Change color
						x->data = abs(x->data);
						z->data = abs(z->data); 
						break;
					}
					else
					{
						flag = 1;
						// Here is not the root
						if(abs(y->data) > abs(x->parent->data))
							x->parent->right = y;
						else
							x->parent->left = y;
						y->parent = x->parent;
						y->left = x;
						y->left->right = B;
						x->parent = y;
						// Change color
						x->data = abs(x->data);
						z->data = abs(z->data);
						tail = y; 
					}
				}
				else
				{
					// [LEFT---RIGHT]
					// On the left side
					node *B = z->left;
					node *C = z->right;
					if(x == root)
					{
						root = z;
						z->parent = NULL;
						z->left = y;
						z->right = x;
						z->left->right = B;
						z->right->left = C;
						y->parent = z;
						x->parent = z;
						x->data = abs(x->data);
						y->data = abs(y->data);
						break;
					}
					else
					{
						flag = 2;
						if(abs(z->data) > abs(x->parent->data))
							x->parent->right = z;
						else
							x->parent->left = z;
						z->parent = x->parent;
						z->left = y;
						z->right = x;
						z->left->right = B;
						z->right->left = C;
						x->parent = z;
						y->parent = z;
						x->data = abs(x->data);
						y->data = abs(y->data);
						tail = z;
					}
				}
			}
			
			else
			{
				// On the left side
				if(abs(y->data) > abs(x->data))
				{
					// [RIGHT---LEFT]
					// On the right side
					node *B = z->left;
					node *C = z->right;
					if(x == root)
					{
						root = z;
						z->parent = NULL;
						z->left = x;
						z->right = y;
						z->left->right = B;
						z->right->left = C;
						x->parent = z;
						y->parent = z;
						x->data = abs(x->data);
						y->data = abs(y->data); 
						break;
					}
					else
					{
						flag = 3;
						if(abs(z->data) > abs(x->parent->data))
							x->parent->right = z;
						else
							x->parent->left = z;
						z->parent = x->parent;
						z->left = x;
						z->right = y;
						z->left->right = B;
						z->right->left = C;
						x->parent = z;
						y->parent = z;
						x->data = abs(x->data);
						y->data = abs(y->data); 
						tail = z;
					}	
				}
				else
				{
					// [LEFT---LEFT]
					// On the left side	
					node *C = y->right;
					if(x == root)
					{
						root = y;
						y->parent = NULL;
						y->right = x;
						y->right->left = C;
						x->parent = y;
						x->data = abs(x->data);
						z->data = abs(z->data); 
						break;
					}
					else
					{
						flag = 4;
						if(abs(y->data) > abs(x->parent->data))
							x->parent->right = y;
						else
							x->parent->left = y;
						y->parent = x->parent;
						y->right = x;
						y->right->left = C;
						x->parent = y;
						x->data = abs(x->data);
						z->data = abs(z->data); 
						tail = y;
					}	
				}
			}
		}
		if(flag == 0)
		{
			tail = tail->parent;
		}	
	}
}

queue<node *> tree;
void layerOrder(node *root)
{
	tree.push(root);
	while(!tree.empty())
	{
		node *temp = tree.front();
		tree.pop();
		cout<<temp->data<<" ";
		if(temp->left != NULL)
			tree.push(temp->left);
		if(temp->right != NULL)
			tree.push(temp->right);
	}
	cout<<endl;
}

int main()
{
	cin>>n;
	node *root = NULL;
	node *leaf;
	for(int i = 1;i <= n;i++)
	{
		int temp;
		cin>>temp;
		leaf = insert(root,temp);
		redblack(leaf,root);
		if(root->data < 0)
			root->data = abs(root->data);
	}
	layerOrder(root);
	return 0;
}

/*
9
-11 -2 -14 -1 -7 -5 -8 -4 -15
8
-1 -2 -3 -4 -5 -6 -7 -8

7
-1 -2 -3 -4 -5 -6 -7

6
-1 -2 -3 -4 -5 -6
*/
