#include <cstdlib>
#include <iostream>
#include <ctime>
#include <cstring>
#include <stdio.h>
#include <cmath>

using namespace std;

void selectionSort(int* x, int n)
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

void insertionSort(int* x, int n)
{
    for (int i = 1; i < n; i++)
    {
        int v = x[i];
        int j = i;
        while (x[j-1] > v && j > 0)
        {
            x[j] = x[j-1];
            j--;
        }
        x[j] = v;
    }
}

int main(int argc, char const *argv[])
{
    
    for(int N = 0; N < 6; N++)
    {
        int n = pow(10, N);
        cout << endl << "Para " << n << " elementos: " << endl;
        int* x = new int[n];
        int* numbers = new int[n];
        for (int i = 0; i < n; ++i)
            numbers[i] = rand() % n + 1;
        
        clock_t begin, end;
        double time;

        // SELECTION SORT //////////////////////////////////////////////////////////
        memcpy(x, numbers, n*sizeof(int));    
        begin = clock();
        selectionSort(x, n);
        end = clock();
        time = double(end - begin) / CLOCKS_PER_SEC;
        cout << "Selection sort: " << time << " s" << endl;
        
        // MERGE SORT //////////////////////////////////////////////////////////////
        memcpy(x, numbers, n*sizeof(int));
        begin = clock();	
        mergeSort(x, n);
        end = clock();
        time = double(end - begin) / CLOCKS_PER_SEC;
        cout << "Merge sort:     " << time << " s" << endl;

        // QUICK SORT //////////////////////////////////////////////////////////////
        memcpy(x, numbers, n*sizeof(int));
        begin = clock();
        quickSort(x, 0, n);
        end = clock();
        time = double(end - begin) / CLOCKS_PER_SEC;
        cout << "Quick sort:     " << time << " s" << endl;

        // INSERTION SORT ///////////////////////////////////////////////////////////
        memcpy(x, numbers, n*sizeof(int));
        begin = clock();
        insertionSort(x, n);
        end = clock();
        time = double(end - begin) / CLOCKS_PER_SEC;
        cout << "Insection sort: " << time << " s" << endl;
        
        delete x;
    }
    // system("read");
    
    return EXIT_SUCCESS;
}
