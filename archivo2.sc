#include <iostream>
using namespace std;

int main() {
    int n = 10, t1 = 0, t2 = 1, siguiente = 0;

    for (int i = 1; i <= n; ++i) {
        if(i == 1) {
            cout << t1 << ", ";
            continue;
        }
        if(i == 2) {
            cout << t2 << ", ";
            continue;
        }
        siguiente = t1 + t2;
        t1 = t2;
        t2 = siguiente;

        cout << siguiente << ", ";
    }
    return 0;
}

/*
  CODIGO NO FUNCIONAL EN SIMPLE C POR EL MOMENTO
  */
*/
