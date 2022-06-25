// Función de inicio del programa
int main() {
    int numero1 = 10;
    int numero2 = 20;

    double numero_decimal1 = 10.90;
    double numero_decimal2 = 20.00075;

    boolean bool1 = true;
    boolean bool2 = false;

    string cadena1 = "Hola";
    string cadena2 = "Mundo";

    char caracter1 = 'a';
    char caracter2 = 'd';


    /*
    CODIGO DEPRECADO
    cout << "Suma " << numero1 + numero2 << endl;
    ...
    */


    imprimir("Operaciones aritmeticas");
    imprimir("=======================");

    imprimir("Suma " + to_string(numero1 + numero2));
    imprimir("Resta " + to_string(numero1 - numero2));
    imprimir("Multiplicacion " + to_string(numero1 * numero2));
    imprimir("Division " + to_string(numero1 / numero2));
    imprimir("Modulo " + to_string(numero1 % numero2));

    numero2 = 10;

    imprimir("Operaciones relacionales");
    imprimir("=======================");
    imprimir("Igualdad " + to_string(numero1 == numero2));
    imprimir("Desigualdad " + to_string(numero1 != numero2));
    imprimir("Mayor que " + to_string(numero1 > numero2));
    imprimir("Menor que " + to_string(numero1 < numero2));
    imprimir("Mayor o igual que " + to_string(numero1 >= numero2));
    imprimir("Menor o igual que " + to_string(numero1 <= numero2));

    imprimir("Operaciones logicas");
    imprimir("===================");
    imprimir("AND " + to_string(bool1 && bool2));
    imprimir("OR " + to_string(bool1 || bool2));
    imprimir("NOT " + to_string(!bool1));


    imprimir("Estructuras condicionales")
    imprimir("=========================");

    if(bool1==true){
        imprimir("Bool1 es verdadero");
    } else {
        imprimir("Bool1 es falso");
    }

    imprimir("Estructuras iterativas");
    imprimir("======================");

    while(numero1 < numero2){
        imprimir("Numero1 " + to_string(numero1));
        numero1++;
    }

    numero1 = 10;

    do{
        imprimir("Numero1 " + to_string(numero1));
        numero1++;
    } while(numero1 < numero2);

    return 0;
}

// Función que imprime un mensaje en pantalla
void imprimir(string dato) {
    printf(dato + "\n");
}

void otra_funcion(int dato1, char dato2) {
    imprimir("Esto es una funcion");
}
