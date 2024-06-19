// Правильный код
void printOwing() {
  printBanner();
  // Вызов метода, который вынесли
  printDetails(getOutstanding());
}
// Выделенный участок кода в новый метод
void printDetails(double outstanding) {
  System.out.println("name: " + name);
  System.out.println("amount: " + outstanding);
}