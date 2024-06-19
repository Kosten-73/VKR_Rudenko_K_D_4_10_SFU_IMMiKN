import java.time.LocalDate;
import java.util.Random;
import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;

public class Main {
    /**
     * Функция проверки высокостного года
     */
    public static boolean isLeapYear(int got){
        return (got % 4 == 0 && got % 100 != 0) || got % 400 == 0;
    }
    /**
     * Функция проверки корректноски даты для клиента
     */
    public static boolean osnova(int day, int month, int year){
        if (1 <= day && day <= 31 && 1950 <= year && year <= 2010 && 1 <= month && month <= 12) {
            if (month == 1 || month == 3 || month == 5 || month == 7 || month == 8 || month == 10 || month == 12) {
                return true;
            } else if (month == 4 || month == 6 || month == 9 || month == 11) {
                if (day <= 30) {
                    return true;
                } else {
                    return false;
                }
            } else if (month == 2) {
                if (isLeapYear(year)) {
                    if (day <= 29) {
                        return true;
                    } else {
                        return false;
                    }
                } else if (day <= 28) {
                    return true;
                } else {
                    return false;
                }
            }
        } else {
            return false;
        }
        return false;
    }
    /**
     * Функция проверки корректноски даты для выпуска карты
     */
    public static boolean osnova1(int day, int month, int year){
        if (1 <= day && day <= 31 && 2020 <= year && year <= 2024 && 1 <= month && month <= 12) {
            if (month == 1 || month == 3 || month == 5 || month == 7 || month == 8 || month == 10 || month == 12) {
                return true;
            } else if (month == 4 || month == 6 || month == 9 || month == 11) {
                if (day <= 30) {
                    return true;
                } else {
                    return false;
                }
            } else if (month == 2) {
                if (isLeapYear(year)) {
                    if (day <= 29) {
                        return true;
                    } else {
                        return false;
                    }
                } else if (day <= 28) {
                    return true;
                } else {
                    return false;
                }
            }
        } else {
            return false;
        }
        return false;
    }
    /**
     * Функция генерации строки
     */
    public static String generateRandomWord(int length) {
        StringBuilder sb = new StringBuilder();
        Random random = new Random();
        for (int j = 0; j < 3; j++) {
            for (int i = 0; i < length; i++) {
                char randomChar = (char) (random.nextInt(32) + 'а'); // Генерация случайной буквы от 'a' до 'z'
                sb.append(randomChar);
            }
            sb.append(' ');
        }
        return sb.toString();
    }
    /**
     * Функция генерации email'а
     */
    public static String generateRandomEmail() {
        StringBuilder sb = new StringBuilder();
        Random random = new Random();
        int l = 5 + (int)(Math.random() * 20);
        for (int i = 0; i < l; i++) {
            char randomChar = (char) (random.nextInt(26) + 'a'); // Генерация случайной буквы от 'a' до 'z'
            sb.append(randomChar);
        }
        sb.append(".sfedu.ru");
        return sb.toString();
    }

    public static void main(String[] args) {
        int randomNumberClient = 5 + (int)(Math.random() * 15);
        Client[] clients = new Client[randomNumberClient];
        clients[0] = new Client("Руденко Константин Дмитриевич",
                "korudenko@sfedu.ru",
                LocalDate.of(2000, 10, 1));
        for (int i = 1; i < clients.length; i++){
            int randomNumberInRange = 3 + (int)(Math.random() * 20);
            int year = 1950 + (int)(Math.random() * (2010 - 1950 + 1));
            int mount = 1 + (int)(Math.random() * 12);
            int day = 1 + (int)(Math.random() * 31);
            while (!osnova(day, mount, year)){
                day = 1 + (int)(Math.random() * 31);
            }
            clients[i] = new Client(generateRandomWord(randomNumberInRange),
                    generateRandomEmail(),
                    LocalDate.of(year, mount, day));
        }
        for (int i = 0; i < clients.length - 1; i++){
            System.out.println(clients[i].toString());
        }

        bank_card[] b_c = new bank_card[randomNumberClient];
        for (int i = 0; i < randomNumberClient - 1; i++){
            int year1 = 2020 + (int)(Math.random() * (2024 - 2020 + 1));
            int mount1 = 1 + (int)(Math.random() * 12);
            int day1 = 1 + (int)(Math.random() * 31);
            while (!osnova1(day1, mount1, year1)){
                day1 = 1 + (int)(Math.random() * 31);
            }
            b_c[i] = new bank_card(clients[i], year1, mount1, day1);
        }
        for (int i = 0; i < randomNumberClient - 1; i++){
            System.out.println(b_c[i].toString());
        }

        String fileNotification = "output.txt";
        while (true){
            for (int i = 0; i < randomNumberClient - 1; i++){
                if ((b_c[i].getExpiration_date()).getYear() < (LocalDate.now()).getYear() ||
                        (b_c[i].getExpiration_date()).getYear() == (LocalDate.now()).getYear() &&
                        (b_c[i].getExpiration_date()).getMonthValue() < (LocalDate.now()).getMonthValue() ||
                        (b_c[i].getExpiration_date()).getYear() == (LocalDate.now()).getYear() &&
                                (b_c[i].getExpiration_date()).getMonthValue() == (LocalDate.now()).getMonthValue() &&
                        (b_c[i].getExpiration_date()).getDayOfMonth() < (LocalDate.now()).getDayOfMonth()
                        ) {
                    try (BufferedWriter writer = new BufferedWriter(new FileWriter(fileNotification, true))) {
                        Mail m1 = new Mail(b_c[i].getClient_bc().getEmail());
                        m1.mes_out();
                        writer.write(b_c[i].getClient_bc().getId() + ' ' + b_c[i].getExpiration_date().toString() + '\n');
                        System.out.println("Запись в файл успешно выполнена.");
                        b_c[i].setNumber_cert(bank_card.generateUUIDBased16DigitNumber());
                        b_c[i].setData_issue(LocalDate.of((LocalDate.now()).getYear(), (LocalDate.now()).getMonthValue(), (LocalDate.now()).getDayOfMonth()));
                        b_c[i].setExpiration_date(LocalDate.of((LocalDate.now()).getYear() + 1, (LocalDate.now()).getMonthValue(), (LocalDate.now()).getDayOfMonth()));
                    } catch (IOException e) {
                        System.err.println("Ошибка при записи в файл: " + e.getMessage());
                    }
                }
            }
        }
    }
}
