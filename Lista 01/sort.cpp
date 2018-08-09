#include <cstdlib>
#include <iostream>
#include <ctime>
#include <cstring>

using namespace std;

int* selectionSort(int* x, int n)
{
	for(int i = 0; i < n-1; i++)
	{
		int m = i;
		for (int j = i+1; j < n; j++)
		{
			if (x[j] < x[m])
				m = j;
		}
		double aux = x[i];
		x[i] = x[m];
		x[m] = aux;
	}
	return x;
}

void mergeSort(int* x, int n)
{
	if (n < 2)
		return;    
   
   int m = n/2;
   for (int i = 0; i < n; ++i)
      cout << x[i] << " ";
   cout << endl;

	mergeSort(x, m);
	mergeSort(x+m, n-m);

   int i = 0;
   int j = 0;
	int* l = new int[m];
	memcpy(l, x, m);
	for (int i = 0; i < m; ++i)
      cout << l[i] << " ";
   cout << endl;

	int* r = new int[n-m];
	memcpy(r, &x[m], n-m);
	for (int i = 0; i < n-m; ++i)
      cout << r[i] << " ";
   cout << endl;
    
   for (int i = 0; i < n; ++i)
      cout << x[i] << " ";
   cout << endl;
    
	for (int k = 0; k < n; ++k)
	{
		if (l[i] < r[j])
		{
			x[k] = l[i];
         i++;
         if (i = m)
         {
            i--;
            l[i] = r[n-m];
         }
      }
		else
		{
         x[k] = r[j];
			j++;
         if (j = n-m)
         {
            j--;
            r[j] = l[m];
         }
		}
	}
}

void quickSort(int* x, int r, int s)
{
	if (s <= r)
		return;
	
	int v = x[r];
	int i = r;
	int j = s+1;
	do
	{
		for (; x[i] >= v; i++);
		for (; x[j] <= v; j--);
		double aux = x[i];
		x[i] = x[j];
		x[j] = aux;
	} while (j <= i);

	double aux = x[i];
	x[i] = x[j];
	x[j] = aux;

	aux = x[i];
	x[i] = x[s];
	x[s] = aux;

	quickSort(x, r, i-1);
	quickSort(x, i+1, s);
}

int main(int argc, char const *argv[])
{
	int n;
	cin >> n;
	int* x = new int[n];
	for (int i = 0; i < n; ++i)
	{
		x[i] = rand() % n;
		cout << x[i] << " ";
	}
	cout << endl;

    clock_t begin = clock();
    //selectionSort(x, n);
    clock_t end = clock();
    double timeSelection = double(end - begin) ; // CLOCKS_PER_SEC;
    cout << "Tempo: " << timeSelection << " s" << endl;

 	
    begin = clock();	
 	mergeSort(x, n);
 	end = clock();
   	double timeMerge = double(end - begin); // CLOCKS_PER_SEC;
    for (int i = 0; i < n; ++i)
    {
        cout << x[i] << " ";
    }
	cout << endl;

    // for (int i = 0; i < n; ++i)
	// {
	// 	x[i] = rand() % n;
	// }
	// quickSort(x, 0, n);
	// end = clock();
    // double timeQucik = double(end - begin) / CLOCKS_PER_SEC;


	// cout << "Tempo: " << timeMerge << " s" << endl;
	// cout << "Tempo: " << timeQucik << " s" << endl;

	delete x;
	return 0;
}
