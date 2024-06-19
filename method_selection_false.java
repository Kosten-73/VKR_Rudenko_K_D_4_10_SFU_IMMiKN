// Проблема этого фрагмента заключается в том, что фрагмент кода можно сгруппировать
void printOwing() {
  printBanner();
  // Плохое решение
  System.out.println("name: " + name);
  System.out.println("amount: " + getOutstanding());
}