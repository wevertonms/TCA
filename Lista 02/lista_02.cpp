#include <cmath>
#include <iostream>
#include "primitivas.h"

using namespace std;

template <class V>
V pseudoAngulo(V x, V y)
{
   V angulo;
   if (x > 0)
   {
      if (y > 0) // Primeiro quadrante
         if (x > y)
            angulo = y / x;
         else
            angulo = 2 - x / y;
      else // Quarto quadrante
          if (x > -y)
            angulo = 8 + y / x;
         else
            angulo = 6 - x / y;
   }
   else {
      if (y > 0) // Segundo quadrante
         if (-x > y)
            angulo = 4 + y / x;
         else
            angulo = 2 - x / y;
      else // Terceiro quadrante
         if (x > y)
            angulo = 6 - x / y;
         else
            angulo = 4 + y / x;
   }
   return angulo;
}

template <class V>
int entre(vector<V> u, vector<V> v, vector<V> w)
{
   double anguloU = pseudoAngulo(u[0], u[1]);
   double anguloV = pseudoAngulo(v[0], v[1]);
   double anguloW = pseudoAngulo(w[0], w[1]);
   int relacao;

   if (anguloU == anguloV)
      relacao = 0;
   else if (anguloW >= anguloU && anguloW <= anguloV)
      relacao = 1;
   else if (anguloW <= anguloU && anguloW >= anguloV)
      relacao = 1;
   else
      relacao = 2;

   return relacao;
}

int main(int argc, char const *argv[])
{
   vector<int> u(2, 1);
   vector<int> v(4, 1);
   vector<int> w(3, 1);

   // vector<int> soma = somaVetorial(x, y);
   // vector<int> mult = multEscalar(20, x);
   // cout << soma[0] << " " << soma[1] << endl;
   // cout << mult[0] << " " << mult[1] << endl;
   // cout << prodEscalar(x, y) << endl;
   // cout << norma(x) << endl;
   // cout << pseudoAngulo(2, 3) << endl;
   cout << entre(u, v, w) << endl;

   system("read");
   return 0;
}
