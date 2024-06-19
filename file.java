public class Example {
    // Неиспользуемая переменная
    private int unusedVariable;
    public void performOperations() {

        // Избыточное создание объектов
        String redundantString = new String("Redundant");
        // Неправильное использование строк и операций с ними
        String inefficientString = "";
        for (int i = 0; i < 1000; i++) {
            inefficientString += "a";
        }
        duplicateCode();
        duplicateCode();
        // Использование небезопасных API
        File file = new File("example.txt");
        FileReader fr = null;
        try {
            fr = new FileReader(file);
            BufferedReader br = new BufferedReader(fr);
            String line;
            while ((line = br.readLine()) != null) {
                System.out.println(line);
            }
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            // Утечка ресурсов: не закрыты FileReader и BufferedReader
            // Неправильное управление памятью
        }
    }
    // Несоответствие соглашениям о наименовании
    public void BADNAMINGCONVENTION() {
        System.out.println("Bad naming convention");
    }
}