#include <cmath>
#include <cstdlib>
#include <cstring>
#include <ctime>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <string>

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
			double aux = x[i];
			x[i] = x[pivotID + 1];
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

void shellSort(double *x, int n)
{
	int i, j, v;
	int gap = 1;
	while (gap < n)
	{
		gap = 3 * gap + 1;
	}
	while (gap > 1)
	{
		gap /= 3;
		for (i = gap; i < n; i++)
		{
			v = x[i];
			j = i;
			while (j >= gap && v < x[j-gap])
			{
				x[j] = x[j - gap];
				j = j - gap;
			}
			x[j] = value;
		}
	}
}

double testSort(int n, char ordering, char alg)
{
	clock_t begin, end;
	double time = 0.0;
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
	case 'h':
		begin = clock();
		shellSort(x, n);
		end = clock();
		time = double(end - begin) / CLOCKS_PER_SEC;
		break;
	default:
		break;
	}

	ofstream myFile;
	string algS(1, alg);
	string orderingS(1, ordering);
	myFile.open(algS + "_" + orderingS + "_" + to_string(n) + ".txt");
	for (int i = 0; i < n; ++i)
		myFile << x[i] << endl;
	myFile.close();

	delete x;

	return time;
}

int main()
{
	cout << "Merge Sort ================================================" << endl;
	cout << "       N\tAleatório\tCrescente\tDecrescente" << endl;
	for (int N = 1; N < 6; N++)
	{
		cout << setw(8) << pow(10, N);
		cout << "\t" << setw(8) << testSort(pow(10, N), 'a', 'm');
		cout << "\t" << setw(8) << testSort(pow(10, N), 'c', 'm');
		cout << "\t" << setw(8) << testSort(pow(10, N), 'd', 'm') << endl;
	}

	cout << "Quick Sort ================================================" << endl;
	cout << "       N\tAleatório\tCrescente\tDecrescente" << endl;
	for (int N = 1; N < 6; N++)
	{
		cout << setw(8) << pow(10, N);
		cout << "\t" << setw(8) << testSort(pow(10, N), 'a', 'q');
		cout << "\t" << setw(8) << testSort(pow(10, N), 'c', 'q');
		cout << "\t" << setw(8) << testSort(pow(10, N), 'd', 'q') << endl;
	}

	cout << "Insertion Sort ============================================" << endl;
	cout << "       N\tAleatório\tCrescente\tDecrescente" << endl;
	for (int N = 1; N < 6; N++)
	{
		cout << setw(8) << pow(10, N);
		cout << "\t" << setw(8) << testSort(pow(10, N), 'a', 'i');
		cout << "\t" << setw(8) << testSort(pow(10, N), 'c', 'i');
		cout << "\t" << setw(8) << testSort(pow(10, N), 'd', 'i') << endl;
	}

	cout << "Selection Sort ============================================" << endl;
	cout << "       N\tAleatório\tCrescente\tDecrescente" << endl;
	for (int N = 1; N < 6; N++)
	{
		cout << setw(8) << pow(10, N);
		cout << "\t" << setw(8) << testSort(pow(10, N), 'a', 's');
		cout << "\t" << setw(8) << testSort(pow(10, N), 'c', 's');
		cout << "\t" << setw(8) << testSort(pow(10, N), 'd', 's') << endl;
	}

	cout << "Shell Sort ================================================" << endl;
	cout << "       N\tAleatório\tCrescente\tDecrescente" << endl;
	for (int N = 1; N < 6; N++)
	{
		cout << setw(8) << pow(10, N);
		cout << "\t" << setw(8) << testSort(pow(10, N), 'a', 'h');
		cout << "\t" << setw(8) << testSort(pow(10, N), 'c', 'h');
		cout << "\t" << setw(8) << testSort(pow(10, N), 'd', 'h') << endl;
	}

	return 0;
}
