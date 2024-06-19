import java.util.Properties;
import javax.mail.*;
import javax.mail.internet.*;

public class Mail {
    /**
     * Поле отправителя
     */
    private String out_man;
    /**
     * Поле получателя
     */
    private String in_man;
    /**
     * Пароль отправителя
     */
    private String out_password;

    public Mail(String in_man) {
        this.out_man = "rudenko@stud.rksi.ru";
        this.out_password = "cuhw zhop llvl stbx";
        this.in_man = in_man;
    }

    /**
     * Метод для отправки сообщения о окончании действии карты
     */
    public void mes_out() {
        Properties properties = new Properties();
        properties.put("mail.smtp.host", "smtp.gmail.com");
        properties.put("mail.smtp.port", "587");
        properties.put("mail.smtp.auth", "true");
        properties.put("mail.smtp.starttls.enable", "true");
        Session session = Session.getDefaultInstance(properties, new Authenticator() {
            protected PasswordAuthentication getPasswordAuthentication() {
                return new PasswordAuthentication(out_man, out_password);
            }
        });

        try {
            Message message = new MimeMessage(session);
            message.setFrom(new InternetAddress(out_man));
            message.setRecipients(Message.RecipientType.TO, InternetAddress.parse(in_man));
            message.setSubject("Ваша карта уже старенькая!");
            message.setText("Спасибо что все это время пользуютесь нашими услугами, мы уже начали готовить Вам новую карту," +
                    "так как срок текущей подходит к концу");

            Transport.send(message);

            System.out.println("Письмо успешно отправлено.");
        } catch (MessagingException e) {
            e.printStackTrace();
            System.out.println("Ошибка при отправке письма: " + e.getMessage());
        }
    }
}

