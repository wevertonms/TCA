#include <cstdlib>
#include <iostream>
#include <ctime>
#include <cstring>
#include <stdio.h>

using namespace std;

int* selectionSort(int* x, int n)
{
	for(int i = 0; i < n-1; i++)
	{
		int m = i;
		for (int j = i+1; j < n; j++)
		{
			if (x[j] < x[m])
            {
				m = j;
            }
		}
		double aux = x[i];
		x[i] = x[m];
		x[m] = aux;
	}
	return x;
}

void mergeSort(int* x, int n)
{
	if (n < 2) {
        return;    
    }
   
    int m = n/2;
	mergeSort(x, m);
	mergeSort(x+m, n-m);

	int* l = new int[m];
	memcpy(l, x, m*sizeof(int));

	int* r = new int[n-m];
	memcpy(r, &x[m], (n-m)*sizeof(int));
    
   	int i = 0;
   	int j = 0;
    for (int k = 0; k < n; ++k)
    {
        if (l[i] < r[j])
        {
            x[k] = l[i];
            i++;
            if (i == m)
            {
                i--;
                l[i] = r[n-m-1];
            }
        }
        else
        {
            x[k] = r[j];
            j++;
            if (j == n-m)
            {
                j--;
                r[j] = l[m-1];
            }
        }
    }
}

void quickSort(int* x, int r, int s)
{
	if (s <= r)
		return;
	
	int pivot = x[r];
	int pivotID = r;
	
	for(int i = r+1; i < s; i++)
	{
		if (x[i] < pivot)
		{
			int aux = x[pivotID+1];
			x[pivotID+1] = x[i];
			x[i] = aux;

			aux = x[pivotID+1];
			x[pivotID+1] = pivot;
			x[pivotID] = aux;
			
			pivotID++;
		}
	}

	quickSort(x, r, pivotID);
	quickSort(x, pivotID+1, s);
}

int main(int argc, char const *argv[])
{
	int n = 100000;
	int* x = new int[n];
	// for (int i = 0; i < n; ++i)
	// {
	// 	x[i] = rand() % n;
	// 	// cout << x[i] << " ";
	// }
	// cout << endl;

    clock_t begin, end;

    ////////////////////////////////////////////////////////////////////////////
    // SELECTION SORT
    ////////////////////////////////////////////////////////////////////////////
    for (int i = 0; i < n; ++i)
	    x[i] = rand() % n;
    begin = clock();
    selectionSort(x, n);
    end = clock();
    double timeSelection = double(end - begin) / CLOCKS_PER_SEC;
    cout << "Tempo: " << timeSelection << " s" << endl;
    
    ////////////////////////////////////////////////////////////////////////////
    // MERGE SORT
    ////////////////////////////////////////////////////////////////////////////
 	for (int i = 0; i < n; ++i)
	    x[i] = rand() % n;
    begin = clock();	
 	mergeSort(x, n);
 	end = clock();
   	double timeMerge = double(end - begin) / CLOCKS_PER_SEC;
    cout << "Tempo: " << timeMerge << " s" << endl;

    ////////////////////////////////////////////////////////////////////////////
    // QUICK SORT
    ////////////////////////////////////////////////////////////////////////////
    for (int i = 0; i < n; ++i)
	    x[i] = rand() % n;

	begin = clock();
	quickSort(x, 0, n);
	end = clock();
    double timeQucik = double(end - begin) / CLOCKS_PER_SEC;
	cout << "Tempo: " << timeQucik << " s" << endl;

    // for (int i = 0; i < n; ++i)
    //     cout << x[i] << " ";
	// cout << endl;
    // system("read");
	delete x;
	return 0;

}
