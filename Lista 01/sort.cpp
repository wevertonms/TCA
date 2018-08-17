#include <cstdlib>
#include <iostream>
#include <ctime>
#include <cstring>
#include <stdio.h>
#include <cmath>

using namespace std;

void selectionSort(double *x, int n)
{
    for (int i = 0; i < n - 1; i++)
    {
        int m = i;
        for (int j = i + 1; j < n; j++)
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

void mergeSort(double *x, int n)
{
    if (n < 2)
    {
        return;
    }

    int m = n / 2;
    mergeSort(x, m);
    mergeSort(x + m, n - m);

    double *l = new double[m];
    memcpy(l, x, m * sizeof(double));

    double *r = new double[n - m];
    memcpy(r, &x[m], (n - m) * sizeof(double));

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
                l[i] = r[n - m - 1];
            }
        }
        else
        {
            x[k] = r[j];
            j++;
            if (j == n - m)
            {
                j--;
                r[j] = l[m - 1];
            }
        }
    }
}

void quickSort(double *x, int r, int s)
{
    if (s <= r)
        return;

    double pivot = x[r];
    int pivotID = r;

    for (int i = r + 1; i < s; i++)
    {
        if (x[i] < pivot)
        {
            double aux = x[pivotID + 1];
            x[pivotID + 1] = x[i];
            x[i] = aux;

            aux = x[pivotID + 1];
            x[pivotID + 1] = pivot;
            x[pivotID] = aux;

            pivotID++;
        }
    }

    quickSort(x, r, pivotID);
    quickSort(x, pivotID + 1, s);
}

void insertionSort(double *x, int n)
{
    for (int i = 1; i < n; i++)
    {
        double v = x[i];
        int j = i;
        while (x[j - 1] > v && j > 0)
        {
            x[j] = x[j - 1];
            j--;
        }
        x[j] = v;
    }
}

double testSort(int n, char ordering, char alg)
{
    clock_t begin, end;
    double time;
    double *x = new double[n];

    switch (ordering)
    {
    case 'c':
        for (int i = 0; i < n; ++i)
            x[i] = i;
        break;
    case 'd':
        for (int i = n; i > 0; --i)
            x[i] = i;
        break;
    case 'a':
        for (int i = 0; i < n; ++i)
            x[i] = rand() % n + 1;
        break;
    default:
        break;
    }

    switch (alg)
    {
    case 's':
        // memcpy(x, number, n * sizeof(double));
        begin = clock();
        selectionSort(x, n);
        end = clock();
        time = double(end - begin) / CLOCKS_PER_SEC;
        break;
    case 'm':
        // memcpy(x, number, n * sizeof(double));
        begin = clock();
        mergeSort(x, n);
        end = clock();
        time = double(end - begin) / CLOCKS_PER_SEC;
        break;
    case 'q':
        // memcpy(x, number, n * sizeof(double));
        begin = clock();
        quickSort(x, 0, n);
        end = clock();
        time = double(end - begin) / CLOCKS_PER_SEC;
        break;
    case 'i':
        // memcpy(x, number, n * sizeof(double));
        begin = clock();
        insertionSort(x, n);
        end = clock();
        time = double(end - begin) / CLOCKS_PER_SEC;
        break;
    default:
        break;
    }
    delete x;

    return time;
}

int main(int argc, char const *argv[])
{

    for (int N = 1; N < 6; N++)
    {
        cout << "Para " << pow(10, N) << " elementos em ordem ALEATÓRIA: " << endl;
        cout << "\tSelection sort: " << testSort(pow(10, N), 'a', 's') << " s" << endl;
        cout << "\tMerge sort: " << testSort(pow(10, N), 'a', 'm') << " s" << endl;
        cout << "\tQuick sort: " << testSort(pow(10, N), 'a', 'q') << " s" << endl;
        cout << "\tInsertion sort: " << testSort(pow(10, N), 'a', 'i') << " s" << endl;
    }

    for (int N = 1; N < 6; N++)
    {
        cout << "Para " << pow(10, N) << " elementos em ordem CRESCENTE: " << endl;
        cout << "\tSelection sort: " << testSort(pow(10, N), 'a', 's') << " s" << endl;
        cout << "\tMerge sort: " << testSort(pow(10, N), 'a', 'm') << " s" << endl;
        cout << "\tQuick sort: " << testSort(pow(10, N), 'a', 'q') << " s" << endl;
        cout << "\tInsertion sort: " << testSort(pow(10, N), 'a', 'i') << " s" << endl;
    }

    for (int N = 1; N < 6; N++)
    {
        cout << "Para " << pow(10, N) << " elementos em ordem DECRESCENTE: " << endl;
        cout << "\tSelection sort: " << testSort(pow(10, N), 'a', 's') << " s" << endl;
        cout << "\tMerge sort: " << testSort(pow(10, N), 'a', 'm') << " s" << endl;
        cout << "\tQuick sort: " << testSort(pow(10, N), 'a', 'q') << " s" << endl;
        cout << "\tInsertion sort: " << testSort(pow(10, N), 'a', 'i') << " s" << endl;
    }

    return 0;
}
