/* Проблема
У вас есть несколько условных операторов, ведущих к одинаковому результату или действию. */
double disabilityAmount() {
  if (seniority < 2) {
    return 0;
  }
  if (monthsDisabled > 12) {
    return 0;
  }
  if (isPartTime) {
    return 0;
  }
  // И так далее
  // ...
}