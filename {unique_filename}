import java.time.LocalDate;
import java.time.Period;
import java.util.UUID;

public class Client {
    /**
     * Поле id клиента
     */
    private String id;
    /**
     * Поле Фамилии Имени Отчества
     */
    private String fio;
    /**
     * Поле возраста
     */
    private int age;
    /**
     * Поле email'а для отправки смс
     */
    private String email;
    /**
     * Поле даты рождения
     */
    private LocalDate data_birth;

    /**
     * Конструктор
     */
    public Client(String fio, String email, LocalDate data_birth) {
        this.id = UUID.randomUUID().toString();
        this.fio = fio;
        this.email = email;
        this.data_birth = data_birth;
        this.age = Period.between(data_birth, LocalDate.now()).getYears();
    }

    public String getFio() {
        return fio;
    }
    public String getId() {
        return id;
    }

    public void setFio(String fio) {
        this.fio = fio;
    }

    public void setAge(int age) {
        this.age = age;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public LocalDate getData_birth() {
        return data_birth;
    }

    public void setData_birth(LocalDate data_birth) {
        this.data_birth = data_birth;
    }

    @Override
    public String toString() {
        return "клиент{" +
                "ФИО='" + fio + '\'' +
                ", возраст=" + age +
                ", почта='" + email + '\'' +
                ", дата рожения=" + data_birth +
                ", id = " + id +
                '}';
    }
}
