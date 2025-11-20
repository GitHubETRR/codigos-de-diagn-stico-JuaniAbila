#include <iostream>
#include <string>
#include <vector>
#include <limits>

using namespace std;

// ----------- Clases -----------
class ChalecoSensor {
public:
    int leerSensorDesdeTeclado();
};

class ArmaLaser {
public:
    void disparar();
};

class Jugador {
private:
    string nombre;
    string apellido;
    bool vivo;
    ChalecoSensor chaleco;

public:
    Jugador(const string& nombre_, const string& apellido_);
    string obtenerNombreCompleto() const;
    bool estaVivo() const;
    void resetearEstado();
    void recibirDisparo();
    void mostrarEstado() const;
};

// ----------- Prototipos de funciones -----------
void mostrarJugadores(const vector<Jugador*>& jugadores);
void agregarJugador(vector<Jugador*>& jugadores);
void iniciarPartida(vector<Jugador*>& pool);
void liberarMemoria(vector<Jugador*>& jugadores);
void esperarTecla();

// ----------- MAIN -----------
int main() {
    vector<Jugador*> jugadores;

    // Jugadores iniciales
    jugadores.push_back(new Jugador("Juan", "Pérez"));
    jugadores.push_back(new Jugador("Ana", "Martínez"));
    jugadores.push_back(new Jugador("Lucas", "Gómez"));
    jugadores.push_back(new Jugador("Sofía", "López"));

    while (true) {
        cout << "\n========= LASER TAG MENU =========\n";
        cout << "1. Iniciar nueva partida\n";
        cout << "2. Ver jugadores disponibles\n";
        cout << "3. Agregar nuevo jugador\n";
        cout << "4. Salir\n";
        cout << "Seleccione una opción: ";
        int opcion;
        cin >> opcion;

        switch (opcion) {
            case 1:
                iniciarPartida(jugadores);
                break;
            case 2:
                mostrarJugadores(jugadores);
                break;
            case 3:
                agregarJugador(jugadores);
                break;
            case 4:
                liberarMemoria(jugadores);
                cout << "¡Hasta la próxima partida!\n";
                return 0;
            default:
                cout << "Opción inválida.\n";
        }

        cin.clear();
        cin.ignore(numeric_limits<streamsize>::max(), '\n');
    }
}

// ----------- DEFINICIONES DE FUNCIONES -----------

int ChalecoSensor::leerSensorDesdeTeclado() {
    char entrada;
    cout << "[Sensor] Ingrese 'd' para disparo efectivo o 'f' para fallo: ";
    cin >> entrada;
    return (entrada == 'd' || entrada == 'D') ? 1 : 0;
}

void ArmaLaser::disparar() {
    cout << "[Arma] ¡Disparo realizado!\n";
}

Jugador::Jugador(const string& nombre_, const string& apellido_)
    : nombre(nombre_), apellido(apellido_), vivo(true) {}

string Jugador::obtenerNombreCompleto() const {
    return nombre + " " + apellido;
}

bool Jugador::estaVivo() const {
    return vivo;
}

void Jugador::resetearEstado() {
    vivo = true;
}

void Jugador::recibirDisparo() {
    if (!vivo) {
        cout << "[Chaleco] " << obtenerNombreCompleto() << " ya está muerto. Ignorando disparo.\n";
        return;
    }

    int impacto = chaleco.leerSensorDesdeTeclado();
    if (impacto == 1) {
        vivo = false;
        cout << "[Chaleco] " << obtenerNombreCompleto() << " fue alcanzado. Estado: MUERTO\n";
    } else {
        cout << "[Chaleco] " << obtenerNombreCompleto() << " esquivó el disparo.\n";
    }
}

void Jugador::mostrarEstado() const {
    cout << obtenerNombreCompleto() << " está " << (vivo ? "VIVO" : "MUERTO") << endl;
}

void mostrarJugadores(const vector<Jugador*>& jugadores) {
    cout << "\n--- Lista de jugadores ---\n";
    for (size_t i = 0; i < jugadores.size(); ++i) {
        cout << i << ": " << jugadores[i]->obtenerNombreCompleto() << endl;
    }
    esperarTecla();
}

void agregarJugador(vector<Jugador*>& jugadores) {
    string nombre, apellido;
    cout << "Ingrese nombre: ";
    cin >> nombre;
    cout << "Ingrese apellido: ";
    cin >> apellido;

    jugadores.push_back(new Jugador(nombre, apellido));
    cout << "Jugador agregado exitosamente.\n";
    esperarTecla();
}

void iniciarPartida(vector<Jugador*>& pool) {
    if (pool.size() < 2) {
        cout << "No hay suficientes jugadores para iniciar una partida.\n";
        esperarTecla();
        return;
    }

    mostrarJugadores(pool);

    int cantidad;
    cout << "\n¿Cuántos jugadores van a jugar? (mínimo 2): ";
    cin >> cantidad;

    if (cantidad < 2 || cantidad > pool.size()) {
        cout << "Cantidad inválida.\n";
        esperarTecla();
        return;
    }

    vector<Jugador*> participantes;

    for (int i = 0; i < cantidad; ++i) {
        int indice;
        cout << "Seleccioná el índice del jugador #" << (i + 1) << ": ";
        cin >> indice;

        if (indice >= 0 && indice < pool.size()) {
            participantes.push_back(pool[indice]);
        } else {
            cout << "Índice inválido. Reintentá.\n";
            --i;
        }
    }

    for (auto& jugador : participantes) {
        jugador->resetearEstado();
    }

    bool juegoActivo = true;

    while (juegoActivo) {
        cout << "\n=== Nueva Ronda ===\n";
        for (size_t i = 0; i < participantes.size(); ++i) {
            if (!participantes[i]->estaVivo()) continue;

            cout << "\nTurno de: " << participantes[i]->obtenerNombreCompleto() << endl;
            ArmaLaser arma;
            arma.disparar();

            for (size_t j = 0; j < participantes.size(); ++j) {
                if (j != i && participantes[j]->estaVivo()) {
                    cout << j << ": " << participantes[j]->obtenerNombreCompleto() << endl;
                }
            }

            int objetivo;
            cout << "Seleccioná el índice del objetivo: ";
            cin >> objetivo;

            if (objetivo >= 0 && objetivo < participantes.size() && objetivo != i) {
                participantes[objetivo]->recibirDisparo();
            } else {
                cout << "Objetivo inválido.\n";
            }
        }

        int vivos = 0;
        cout << "\n=== Estado actual ===\n";
        for (auto& jugador : participantes) {
            jugador->mostrarEstado();
            if (jugador->estaVivo()) vivos++;
        }

        if (vivos <= 1) {
            cout << "\nFin de la partida. ";
            if (vivos == 1) {
                for (auto& jugador : participantes) {
                    if (jugador->estaVivo()) {
                        cout << "Ganador: " << jugador->obtenerNombreCompleto() << endl;
                        break;
                    }
                }
            } else {
                cout << "Todos muertos, empate.\n";
            }
            juegoActivo = false;
        } else {
            char seguir;
            cout << "\n¿Continuar la partida? (s/n): ";
            cin >> seguir;
            if (seguir != 's' && seguir != 'S') {
                juegoActivo = false;
            }
        }
    }
    esperarTecla();
}

void liberarMemoria(vector<Jugador*>& jugadores) {
    for (auto jugador : jugadores) {
        delete jugador;
    }
    jugadores.clear();
}

void esperarTecla() {
    cout << "\nPresione ENTER para continuar...";
    cin.ignore(numeric_limits<streamsize>::max(), '\n'); // limpia buffer
    cin.get();
}
