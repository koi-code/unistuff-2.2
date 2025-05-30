using System;

public class MyString
{
    protected readonly int SZ = 80;
    public char[] str;
    public MyString()
    {
        str = new char[SZ];
        str[0] = '\x0';
    }

    public MyString(string s)
    {
        str = new char[SZ];
        int len = s.Length;
        for (int i = 0; i < len; i++)
        {
            str[i] = s[i];
        }
        str[len] = '\x0';
    }

    public void display()
    {
        string s = "";
        for (int i = 0; str[i] != '\x0'; i++)
        {
            s += str[i];
        }
        Console.Write(" " + s);
    }
}
