#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <stdbool.h>
#include <string.h>

typedef struct{
    int dia;
    int mes;
    int anio;
} fecha_t;

typedef struct{
    char nombre[MAX_CHAR];
    char apellidos[MAX_CHAR];
    fecha_t fechas;
    int num_asiento;
    bool estado;
}reserva_t;

typedef struct nodo{
    reserva_t reserva;
    struct nodo* sig;
}nodo_t;

void registrar_venta(nodo* servicio);
bool asiento_ocupado(nodo* servicio, int num);

int main(){
    nodo* lista=NULL
    registrar_venta(&lista);
    return 0;
}

registrar_venta(nodo* servicio){
    int asiento;
    do{
        printf("Ingrese un numero de asiento del (0-99): ");
        scanf("%d", &asiento);
        if (asiento < 0 || asiento >= 100){
            printf("Asiento invalido")
        } else if (asiento_ocupado(*servicio_asiento)){
            printf("El asiento esta ocupado");
        } else {
            break;
        }
    } while(true);

    nodo_t* nuevo = malloc(sizeof(reserva_t));
    if(!nuevo){
        printf("No hay memoria usable disponible");
        return;
    }

    printf("Ingrese su nombre: ");
    scanf("%s", nuevo->reserva.nombre);
    printf("Ingrese su apellido: ");
    scanf("%s", nuevo->reserva.apellido);
    printf("Ingrese la fecha: ");
    scanf("%d %d %d", &nuevo->reserva.dia, &nuevo->reserva.mes, &nuevo->reserva.anio);

    nuevo->reserva.numero_asiento = asiento;
    nuevo->reserva.estado = true;
    nuevo->sig = servicio*;
    servicio* = nuevo;
}

bool asiento_ocupado(nodo_t* servicio, int asiento){
    while(servicio != NULL){
        if(servicio->reserva.estado && servicio->reserva.num_asiento = asiento){
            return true;
        }
        servicio = servicio->sig;
    }
    return false;
}
