#define FRAMERATE 20
#define STEP 1000  //1ms

const byte sequence[FRAMERATE] = {
  B01100000,  //F1
  B01111110,  //F2
  B10011000,  //F3
  B10101110,  //F4
  B10111011,  //F5
  B11000000,  //F6
  B10111011,  //F7
  B10101110,  //F8
  B10011000,  //F9
  B01111110,  //F10
  B01100000,  //F11
  B01000010,  //F12
  B00101000,  //F13
  B00010010,  //F14
  B00000101,  //F15
  B00000000,  //F16
  B00000101,  //F17
  B00010010,  //F18
  B00101000,  //F19
  B01000010,  //F20
};

const int numSteps = sizeof(sequence) / sizeof(sequence[0]);

void setup() {
  // Configurar pines D0–D7 como salida
  DDRD = 0xFF; // Configura todo el PORTD como salida
}

void loop() {
  for (int i = 0; i < numSteps; i++) {
    PORTD = sequence[i]; // Enviar byte al puerto
    delayMicroseconds(STEP); // Esperar antes del siguiente paso
  }

  // (Opcional) esperar un poco antes de repetir la secuencia
  delayMicroseconds(STEP);
}
