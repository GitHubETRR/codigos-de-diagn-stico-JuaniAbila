const int addrPins[4] = {2, 3, 4, 5};   // A0–A3 Blanverde
const int dataInPins[4] = {6, 7, 8, 10}; // D1-D4 Azul
const int WE_PIN = 11;                  // WE negado
const int dataOutPins[4] = {A0, A1, A2, A3}; // O0–O3 (salidas BCD) Naranja

void setup() {
  Serial.begin(9600);

  for (int i = 0; i < 4; i++) {
    pinMode(addrPins[i], OUTPUT);
    pinMode(dataInPins[i], OUTPUT);
    pinMode(dataOutPins[i], INPUT);
  }

  pinMode(WE_PIN, OUTPUT);
  digitalWrite(WE_PIN, HIGH); // Modo lectura por defecto

  Serial.println("Memoria 74LS189 lista.");
  Serial.println("Formato: W <direccion> <dato (0–9)>  o  R <direccion>");
}

void setAddress(byte addr) {
  for (int i = 0; i < 4; i++) {
    digitalWrite(addrPins[i], (addr >> i) & 1);
  }
}

void writeData(byte addr, byte data) {
  setAddress(addr);

  for (int i = 0; i < 4; i++) {
    digitalWrite(dataInPins[i], (data >> i) & 1);
  }

  digitalWrite(WE_PIN, LOW); // Activar escritura
  delayMicroseconds(1);
  digitalWrite(WE_PIN, HIGH); // Volver a lectura
}

byte readData(byte addr) {
  byte value = 0;
  setAddress(addr);

  delayMicroseconds(1); // Pequeña espera por estabilidad

  for (int i = 0; i < 4; i++) {
    if (digitalRead(dataOutPins[i])) {
      value |= (1 << i);
    }
  }
  //value!=value;| //Verificar
  return value;
}

void loop() {
  if (Serial.available()) {
    String input = Serial.readStringUntil('\n');
    input.trim();

    if (input.length() < 3) {
      Serial.println("Comando inválido.");
      return;
    }

    char modo = toupper(input.charAt(0));
    int espacio1 = input.indexOf(' ');
    int espacio2 = input.indexOf(' ', espacio1 + 1);

    int direccion = input.substring(espacio1 + 1, espacio2).toInt();

    if (direccion < 0 || direccion > 15) {
      Serial.println("Dirección inválida (0–15).");
      return;
    }

    if (modo == 'W') {
      if (espacio2 == -1) {
        Serial.println("Falta dato para escritura.");
        return;
      }

      int valor = input.substring(espacio2 + 1).toInt();

      if (valor < 0 || valor > 9) {
        Serial.println("Solo se aceptan valores BCD (0–9).");
        return;
      }

      writeData(direccion, valor);
      Serial.print("Escrito ");
      Serial.print(valor);
      Serial.print(" (BCD) en dirección ");
      Serial.println(direccion);
    }
    else if (modo == 'R') {
      byte dato = readData(direccion);
      Serial.print("Leído de dirección ");
      Serial.print(direccion);
      Serial.print(": ");
      Serial.print(dato);
      Serial.print(" (BCD = ");
      Serial.print(dato, BIN);
      Serial.println(")");
    }
    else {
      Serial.println("Modo inválido. Use 'R' o 'W'.");
    }
  }
}
