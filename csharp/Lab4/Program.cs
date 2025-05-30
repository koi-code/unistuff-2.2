class Program
{
    static void Main()
    {
        MyString s1 = new MyString("Hello, World!");
        Pstring s2 = new Pstring();
        
        s2.Left(s1, 5).display();  // Вывод: "Hello"
        s2.Mid(s1, 7, 5).display(); // Вывод: "World"
        s2.Right(s1, 6).display();  // Вывод: "World!"
    }
}